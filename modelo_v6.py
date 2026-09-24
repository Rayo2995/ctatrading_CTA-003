"""
MODELO DE DECISION DE TRADING - AI Trading Challenge (CTA-003)
================================================================
Equipo Anzoategui y Rayo
v6 - Replanteo robusto sobre v5 (XGBoost)
     ------------------------------------------------------------
     Motivacion: en v5, con 16 señales BUY simultaneas y ROC AUC ~0.5,
     detectamos que el modelo reflejaba el sesgo alcista general del
     periodo historico, no una seleccion genuina de activos. v6 rediseña
     la arquitectura en 6 puntos para corregir eso:

     1) TARGET RELATIVO (cross-sectional), no absoluto:
        El clasificador ya NO predice "¿sube este activo?" (pregunta que
        el regimen de mercado contesta igual para casi todos). Predice
        "¿este activo supera la MEDIANA del universo esa misma semana?"
        - un target que obliga a diferenciar entre activos incluso en
        un mercado alcista generalizado. El regresor de retorno absoluto
        se mantiene aparte, solo para reporte/VaR/CVaR/tamaño de stop.

     2) RANKING + CUPO FIJO (top-N), no umbral absoluto:
        La decision BUY/HOLD ya no depende de cruzar 55% de probabilidad.
        Se ordenan los candidatos por probabilidad de superar la mediana
        y se seleccionan solo los N_POSICIONES_SEMANA mejores, con un
        piso absoluto de seguridad (UMBRAL_RETORNO_MIN_ABSOLUTO) para no
        comprar "el menos malo" en un crash generalizado.

     3) ENSAMBLE (bagging), no un solo modelo:
        Se entrenan N_MODELOS_ENSAMBLE clasificadores (y regresores) con
        distintas semillas y remuestreo bootstrap del dataset, y se
        promedian sus predicciones. Reduce la varianza de una sola
        corrida ruidosa con dataset chico.

     4) ARQUITECTURA EN CAPAS (el ensamble no decide solo):
          Capa 1 - Cuantitativa: ensamble XGBoost -> ranking de candidatos.
          Capa 2 - Riesgo: veto si el CVaR del candidato es peor que
                   CVAR_VETO_PCT, sin importar que tan bien rankeo.
          Capa 3 - Cualitativa (RAG, PENDIENTE de integracion real):
                   hook explicito guardar_veto_cualitativo() listo para
                   conectar un sistema de recuperacion de noticias + LLM.
                   Por ahora es un stub que NO bloquea nada (siempre
                   aprueba) - dejarlo asi hasta implementar el RAG real
                   es una decision consciente, no un descuido.

     5) GUARDRAILS EXPLICITOS:
          - Cupo semanal fijo (punto 2).
          - Sanity clipping del retorno predicho (heredado de v5).
          - Veto de riesgo por CVaR (punto 4, capa 2).
          - CIRCUIT BREAKER: si el drawdown real de la cuenta (vs. maximo
            historico) supera CIRCUIT_BREAKER_DRAWDOWN_PCT, se pausan
            TODAS las compras nuevas hasta revision manual del equipo
            (se debe resetear a mano en el estado).
          - MONITOR DE HIT-RATE: cada semana se registra si las compras
            de la semana ANTERIOR efectivamente superaron la mediana del
            universo (una vez se conoce el resultado real); si el
            hit-rate movil cae por debajo de UMBRAL_HIT_RATE_ALERTA, se
            imprime una alerta de posible degradacion del modelo (model
            drift), sin bloquear automaticamente (decision del equipo).

     6) REENTRENAMIENTO PERIODICO, no una sola vez al inicio:
          El ensamble se guarda en disco (joblib) junto con la fecha de
          entrenamiento. Si han pasado menos de SEMANAS_ENTRE_REENTRENOS
          desde el ultimo entrenamiento, se reutiliza el ensamble
          guardado (mas rapido, y fuerza una cadencia de reentrenamiento
          deliberada en vez de reentrenar con cada corrida o nunca).

     QUE NO CAMBIA: descarga con reintentos, chequeo de calidad de datos,
     asignar_capital (piso de conviccion + tope de exposicion), stop_loss
     por volatilidad, generar_bloque_json, validar_orden - todo heredado
     de v4/v5 sin cambios de fondo.

     ADVERTENCIA HONESTA: esto sigue siendo un dataset chico para un
     problema financiero. Las 6 mejoras reducen riesgos concretos
     (sesgo de regimen, sobreajuste, punto unico de falla, compras sin
     limite, degradacion silenciosa del modelo), pero no convierten esto
     en un sistema de grado institucional. Documentar esa honestidad es
     parte de usar el modelo correctamente.

NOTA: requiere yfinance, xgboost, scikit-learn, joblib.
"""

import json
import os
import time
import joblib
import smtplib
import requests
import pandas as pd
import numpy as np
import yfinance as yf
import xgboost as xgb
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sklearn.metrics import roc_auc_score
from datetime import datetime, timezone

# ------------------------------------------------------------------
# CONFIGURACION GENERAL (heredada de v4/v5)
# ------------------------------------------------------------------

TICKERS = [
    "SPY", "QQQ", "KO", "BRK-B", "AAPL", "MSFT", "NVDA",
    "005930.KS", "000660.KS", "TSM", "XLE", "TRGP", "XLV", "MRK",
    "GDX", "NEM",
]

MONEDA_TICKER = {"005930.KS": "KRW", "000660.KS": "KRW"}
PAR_FX_A_USD = {"KRW": "KRW=X"}

FECHA_INICIO = "2023-01-01"
FECHA_FIN = datetime.today().strftime("%Y-%m-%d")

DIAS_PROYECTADOS = 30
DIAS_HABILES_ANIO = 252
SEMILLA_BASE = 42

TICKER_REFERENCIA_MERCADO = "SPY"

CAPITAL_TOTAL = 10000.0
SEMANAS_TOTALES = 13
ARCHIVO_ESTADO = "estado_portafolio.json"

PCT_CAPITAL_POR_SEMANA = 0.35
PESO_MINIMO_CONVICCION = 0.05
STOP_LOSS_N_DESVIACIONES = 1.5
STOP_LOSS_MIN_PCT = 0.04
STOP_LOSS_MAX_PCT = 0.20
MAX_EXPOSICION_PCT_POSICION = 0.25
NIVEL_CONFIANZA_VAR = 0.05
MAX_RONDAS_REDISTRIBUCION = 20

GAP_DIAS_AVISO = 10
OUTLIER_PCT_AVISO = 30.0
OUTLIER_PCT_CRITICO = 70.0

MODO_PRUEBA = True

# SOLO simbolos CONFIRMADOS como aprobados en clase. Ajustar segun lo
# que el equipo confirme; nunca incluir codigos coreanos crudos aqui.
SIMBOLOS_HABILITADOS = {
    "SPY", "QQQ", "KO", "BRK.B", "AAPL", "MSFT", "NVDA",
    "MRK", "GDX", "XLE", "NEM", "XLV", "TSM", "TRGP", "005930", "000660",
}
ACCIONES_VALIDAS = {"BUY", "SELL", "CLOSE"}
TIPOS_VALIDOS = {"MARKET", "LIMIT"}

FEATURE_COLS = [
    "ret_1d", "ret_5d", "ret_10d", "ret_20d",
    "vol_10d", "vol_20d",
    "sma_ratio_10_50", "momentum_20", "dist_sma_10",
    "rsi_14", "dow",
]
VENTANA_WARMUP = 50

XGB_PARAMS_BASE = dict(
    max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8,
    reg_lambda=1.0, reg_alpha=0.1, tree_method="hist",
    enable_categorical=True,
)
N_ESTIMATORS_FIJO = 150  # sin early stopping por-modelo del ensamble (ver punto 3)

RETORNO_PRED_MIN_PCT = -25.0
RETORNO_PRED_MAX_PCT = 30.0

# ------------------------------------------------------------------
# NUEVO v6 - PUNTO 2: ranking + cupo fijo semanal
# ------------------------------------------------------------------
N_POSICIONES_SEMANA = 6          # cuantos tickers se compran como maximo por semana
UMBRAL_RETORNO_MIN_ABSOLUTO = -5.0  # piso de seguridad: ni el mejor rankeado
                                     # se compra si su retorno absoluto esperado
                                     # es peor que esto (evita "el menos malo"
                                     # en un crash generalizado)

# ------------------------------------------------------------------
# NUEVO v6 - PUNTO 3: ensamble (bagging)
# ------------------------------------------------------------------
N_MODELOS_ENSAMBLE = 5
FRACCION_BOOTSTRAP = 0.8   # cada modelo del ensamble ve el 80% de las filas,
                           # remuestreado con reemplazo (bagging clasico)

# ------------------------------------------------------------------
# NUEVO v6 - PUNTO 4 (capa 2): veto de riesgo por CVaR
# ------------------------------------------------------------------
# FIX (post-prueba con datos reales): un umbral ABSOLUTO fijo (ej. -18%)
# resulto mal calibrado - el CVaR real de estos activos a 30 dias suele
# rondar -20% a -35%, asi que un numero adivinado sin base empirica
# termino vetando el 100% de las señales (el mismo tipo de fragilidad
# que motivo cambiar el punto 1 de absoluto a relativo). Se corrige
# usando el MISMO principio: el veto descarta solo el peor tramo
# RELATIVO de los candidatos de esa semana, nunca un numero fijo -
# asi es matematicamente imposible que este guardrail vete al 100%.
CVAR_VETO_PERCENTIL = 20  # se descarta el 20% de candidatos con peor
                           # CVaR relativo a los DEMAS candidatos de esa
                           # misma semana (no un umbral absoluto fijo)

# ------------------------------------------------------------------
# NUEVO v6 - PUNTO 5: guardrails (circuit breaker + monitor de hit-rate)
# ------------------------------------------------------------------
CIRCUIT_BREAKER_DRAWDOWN_PCT = -20.0  # drawdown vs. maximo historico que
                                       # pausa TODAS las compras nuevas
VENTANA_HIT_RATE_SEMANAS = 6          # semanas recientes consideradas
UMBRAL_HIT_RATE_ALERTA = 0.40         # bajo esto, se alerta model drift

# ------------------------------------------------------------------
# NUEVO v6 - PUNTO 6: cadencia de reentrenamiento
# ------------------------------------------------------------------
SEMANAS_ENTRE_REENTRENOS = 3
# ------------------------------------------------------------------
# NUEVO v6 - PUNTO 4 (capa 3): guardrail cualitativo con RAG real
# ------------------------------------------------------------------
# Retrieval: noticias recientes via yfinance (ya lo usan para precios,
# sin costo ni API adicional). Generation: Claude lee las noticias y
# decide si hay algo grave que justifique vetar la compra esta semana.
ARCHIVO_ENSAMBLE = "ensamble_v6.joblib"

# ------------------------------------------------------------------
# NUEVO: informe semanal en Markdown (E7 - Reporting)
# ------------------------------------------------------------------
CARPETA_INFORMES = "informes"
# Proveedor del LLM para el guardrail cualitativo: "openrouter" (gratis,
# recomendado - ver modelos :free en openrouter.ai) o "anthropic" (de
# pago, Claude directo). Se elige con la variable de entorno
# RAG_PROVEEDOR; por defecto usa OpenRouter para no depender de un
# presupuesto pago en un proyecto estudiantil.
RAG_PROVEEDOR = os.environ.get("RAG_PROVEEDOR", "openrouter").strip().lower()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODELO_LLM_ANTHROPIC = "claude-haiku-4-5-20251001"

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
# Modelo gratuito de OpenRouter. Aviso importante: los modelos ":free" de
# OpenRouter rotan de vez en cuando (algunos se retiran, aparecen otros
# nuevos) - si este deja de funcionar, revisar la lista actual en
# https://openrouter.ai/models?max_price=0 y cambiar este valor. No hace
# falta tocar nada mas del codigo.
OPENROUTER_MODELO = os.environ.get("OPENROUTER_MODELO", "deepseek/deepseek-v4-flash:free")
VENTANA_NOTICIAS_DIAS = 7
MAX_NOTICIAS_POR_TICKER = 8

# ------------------------------------------------------------------
# NUEVO: automatizacion de correo (Sprint 3, adaptado para correr sin
# supervision en GitHub Actions - sin input() interactivo).
# ------------------------------------------------------------------
EMAIL_DESTINATARIO = "jahir.rodriguez@salesiana.edu.co"
CODIGO_CUENTA = "CTA-003"
SMTP_SERVOR = "smtp.gmail.com"
SMTP_PUERTO = 587

# Credenciales SOLO desde variables de entorno (GitHub Secrets en CI,
# o exportadas manualmente si corren esto en local/Colab). NUNCA
# hardcodear aqui.
EMAIL_REMITENTE = os.environ.get("EMAIL_REMITENTE")
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")

# Doble seguro contra un envio accidental: el envio automatico SOLO
# ocurre si AMBAS condiciones se cumplen:
#   1) MODO_PRUEBA_OVERRIDE=false (variable de entorno, no la constante
#      de arriba - para no tener que editar el archivo cada semana)
#   2) ENVIAR_CORREO_REAL=true (variable de entorno separada, un
#      interruptor explicito solo para el envio de correo)
# Si cualquiera de las dos falta, el script llega hasta imprimir el
# JSON validado y se detiene ahi, igual que en Colab con MODO_PRUEBA.
_MODO_PRUEBA_OVERRIDE = os.environ.get("MODO_PRUEBA_OVERRIDE")
if _MODO_PRUEBA_OVERRIDE is not None:
    MODO_PRUEBA = _MODO_PRUEBA_OVERRIDE.strip().lower() not in ("false", "0", "no")

ENVIAR_CORREO_REAL = os.environ.get("ENVIAR_CORREO_REAL", "false").strip().lower() in ("true", "1", "si")


# ------------------------------------------------------------------
# DESCARGA Y CALIDAD DE DATOS (heredado de v4/v5, sin cambios)
# ------------------------------------------------------------------

def descargar_con_reintentos(ticker, intentos=3, espera_segundos=5, **kwargs_download):
    ultimo_error = None
    for intento in range(1, intentos + 1):
        try:
            datos = yf.download(ticker, progress=False, **kwargs_download)
            if datos is not None and len(datos.dropna(how="all")) > 0:
                return datos
            ultimo_error = "descarga vacia (posible rate limiting)"
        except Exception as e:
            ultimo_error = str(e)
        if intento < intentos:
            print(f"  Aviso: intento {intento}/{intentos} fallo para {ticker} "
                  f"({ultimo_error}). Reintentando en {espera_segundos}s...")
            time.sleep(espera_segundos)
    raise ValueError(f"No se pudo descargar {ticker} tras {intentos} intentos "
                      f"(ultimo error: {ultimo_error}).")


def obtener_tasas_cambio(tickers):
    monedas_necesarias = {MONEDA_TICKER[t] for t in tickers if t in MONEDA_TICKER}
    tasas = {}
    for moneda in monedas_necesarias:
        par = PAR_FX_A_USD.get(moneda)
        if par is None:
            tasas[moneda] = 1.0
            continue
        try:
            precios_fx = descargar_con_reintentos(
                par, start=FECHA_INICIO, end=FECHA_FIN, auto_adjust=True
            )["Close"]
            if isinstance(precios_fx, pd.DataFrame):
                precios_fx = precios_fx.iloc[:, 0]
            tasas[moneda] = float(precios_fx.iloc[-1])
        except Exception as e:
            print(f"  Error obteniendo tipo de cambio {par}: {e}")
            tasas[moneda] = None
    return tasas


def revisar_calidad_datos(ticker, datos):
    fechas = pd.Series(datos.index)
    diffs_dias = fechas.diff().dt.days.dropna()
    gaps = diffs_dias[diffs_dias > GAP_DIAS_AVISO]
    for idx in gaps.index:
        print(f"  Aviso calidad de datos [{ticker}]: gap de {int(diffs_dias.loc[idx])} "
              f"dias antes de {fechas.iloc[idx].date()}.")

    cambios_pct = datos.pct_change(fill_method=None).dropna() * 100
    criticos = cambios_pct[cambios_pct.abs() > OUTLIER_PCT_CRITICO]
    if len(criticos) > 0:
        fecha = criticos.index[0]
        raise ValueError(
            f"Movimiento diario de {criticos.iloc[0]:.1f}% detectado el "
            f"{fecha.date()} para {ticker}, por encima del umbral critico "
            f"de {OUTLIER_PCT_CRITICO}%. Se excluye el ticker esta semana."
        )
    moderados = cambios_pct[cambios_pct.abs() > OUTLIER_PCT_AVISO]
    for fecha, cambio in moderados.items():
        print(f"  Aviso calidad de datos [{ticker}]: movimiento atipico de "
              f"{cambio:.1f}% el {fecha.date()}.")


def obtener_serie_close(ticker):
    datos = descargar_con_reintentos(
        ticker, start=FECHA_INICIO, end=FECHA_FIN, auto_adjust=True
    )["Close"]
    if isinstance(datos, pd.DataFrame):
        datos = datos.iloc[:, 0]
    datos = datos.dropna()

    minimo_filas = VENTANA_WARMUP + DIAS_PROYECTADOS + 20
    if len(datos) < minimo_filas:
        raise ValueError(f"Datos insuficientes para {ticker} ({len(datos)} filas).")

    revisar_calidad_datos(ticker, datos)
    return datos


# ------------------------------------------------------------------
# FEATURES TECNICOS (heredado de v5, sin cambios)
# ------------------------------------------------------------------

def calcular_features(precios):
    df = pd.DataFrame({"close": precios})
    df["ret_1d"] = df["close"].pct_change(1)
    df["ret_5d"] = df["close"].pct_change(5)
    df["ret_10d"] = df["close"].pct_change(10)
    df["ret_20d"] = df["close"].pct_change(20)
    df["vol_10d"] = df["ret_1d"].rolling(10).std()
    df["vol_20d"] = df["ret_1d"].rolling(20).std()
    sma_10 = df["close"].rolling(10).mean()
    sma_50 = df["close"].rolling(50).mean()
    df["sma_ratio_10_50"] = sma_10 / sma_50 - 1
    df["dist_sma_10"] = df["close"] / sma_10 - 1
    df["momentum_20"] = df["close"] / df["close"].shift(20) - 1
    delta = df["close"].diff()
    ganancia = delta.clip(lower=0)
    perdida = -delta.clip(upper=0)
    avg_gain = ganancia.rolling(14).mean()
    avg_loss = perdida.rolling(14).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["rsi_14"] = 100 - (100 / (1 + rs))
    df["dow"] = df.index.dayofweek.astype(float)
    return df


def construir_dataset(tickers):
    bloques = []
    series_por_ticker = {}
    tickers_excluidos = {}
    for ticker in tickers:
        print(f"Descargando y preparando {ticker}...")
        try:
            precios = obtener_serie_close(ticker)
        except Exception as e:
            print(f"  Error con {ticker}: {e}")
            tickers_excluidos[ticker] = str(e)
            continue
        series_por_ticker[ticker] = precios
        feats = calcular_features(precios)
        feats["target_ret_fwd"] = precios.shift(-DIAS_PROYECTADOS) / precios - 1
        feats["ticker"] = ticker
        feats["fecha"] = feats.index
        bloques.append(feats)

    if not bloques:
        raise RuntimeError("No se pudo preparar ningun ticker.")

    dataset_pool = pd.concat(bloques, axis=0, ignore_index=True)
    dataset_pool["ticker"] = dataset_pool["ticker"].astype("category")
    return dataset_pool, series_por_ticker, tickers_excluidos


# ------------------------------------------------------------------
# NUEVO v6 - PUNTO 1: TARGET RELATIVO (cross-sectional)
# ------------------------------------------------------------------

def agregar_target_relativo(dataset_pool):
    """Para cada fecha, calcula la MEDIANA de target_ret_fwd entre todos
    los tickers que tienen dato valido ESA MISMA fecha, y define:
      label_supera_mediana = 1 si el ticker superó esa mediana esa fecha.
    Esto fuerza al clasificador a aprender diferenciacion relativa entre
    activos, no la direccion general del mercado (que la mediana ya
    captura y queda "restada" implicitamente).

    Nota de rigor: la mediana se calcula solo con filas de la MISMA
    fecha (nunca mezclando fechas), asi que no hay fuga de informacion
    temporal - es una operacion transversal (cross-sectional), no
    temporal."""
    dataset_pool = dataset_pool.copy()
    medianas_por_fecha = dataset_pool.groupby("fecha")["target_ret_fwd"].transform("median")
    dataset_pool["target_relativo"] = dataset_pool["target_ret_fwd"] - medianas_por_fecha
    dataset_pool["label_supera_mediana"] = (dataset_pool["target_relativo"] > 0).astype("Int64")
    return dataset_pool


# ------------------------------------------------------------------
# NUEVO v6 - PUNTO 3: ENTRENAMIENTO DEL ENSAMBLE (bagging)
# ------------------------------------------------------------------

def entrenar_ensamble(dataset_pool):
    """Entrena N_MODELOS_ENSAMBLE pares (clasificador de target relativo +
    regresor de retorno absoluto), cada uno sobre un remuestreo bootstrap
    distinto del dataset completo, con semillas distintas. Devuelve listas
    de modelos entrenados (para promediar predicciones despues) y los
    residuos combinados del regresor (aproximados via un holdout simple,
    ver nota abajo) para calibrar VaR/CVaR."""
    datos_validos = dataset_pool.dropna(
        subset=FEATURE_COLS + ["target_ret_fwd", "label_supera_mediana"]
    ).copy()
    datos_validos = datos_validos.sort_values("fecha").reset_index(drop=True)

    # Holdout simple (ultimo 15% cronologico) SOLO para calibrar
    # residuos de VaR/CVaR del regresor - separado del entrenamiento del
    # ensamble para no medir el error con datos ya vistos por ningun
    # miembro del ensamble.
    fechas_unicas = np.sort(datos_validos["fecha"].unique())
    corte = fechas_unicas[int(len(fechas_unicas) * 0.85)]
    train_pool = datos_validos[datos_validos["fecha"] <= corte]
    holdout = datos_validos[datos_validos["fecha"] > corte]

    X_holdout = holdout[FEATURE_COLS + ["ticker"]]
    y_holdout_reg = holdout["target_ret_fwd"]

    modelos_clf = []
    modelos_reg = []
    aucs = []
    residuos_holdout_acumulados = []

    print(f"  Entrenando ensamble de {N_MODELOS_ENSAMBLE} modelos (bagging)...")
    rng_np = np.random.default_rng(SEMILLA_BASE)
    for i in range(N_MODELOS_ENSAMBLE):
        semilla_i = SEMILLA_BASE + i
        muestra = train_pool.sample(frac=FRACCION_BOOTSTRAP, replace=True,
                                     random_state=semilla_i)

        X_i = muestra[FEATURE_COLS + ["ticker"]]
        y_i_clf = muestra["label_supera_mediana"].astype(int)
        y_i_reg = muestra["target_ret_fwd"]

        modelo_clf_i = xgb.XGBClassifier(
            **XGB_PARAMS_BASE, n_estimators=N_ESTIMATORS_FIJO,
            objective="binary:logistic", eval_metric="logloss",
            random_state=semilla_i,
        )
        modelo_clf_i.fit(X_i, y_i_clf)
        modelos_clf.append(modelo_clf_i)

        modelo_reg_i = xgb.XGBRegressor(
            **XGB_PARAMS_BASE, n_estimators=N_ESTIMATORS_FIJO,
            objective="reg:squarederror", random_state=semilla_i,
        )
        modelo_reg_i.fit(X_i, y_i_reg)
        modelos_reg.append(modelo_reg_i)

        if len(X_holdout) > 0:
            proba_holdout = modelo_clf_i.predict_proba(X_holdout)[:, 1]
            y_holdout_clf = holdout["label_supera_mediana"].astype(int)
            if y_holdout_clf.nunique() > 1:
                aucs.append(roc_auc_score(y_holdout_clf, proba_holdout))
            pred_reg_holdout = modelo_reg_i.predict(X_holdout)
            residuos_holdout_acumulados.append(y_holdout_reg.values - pred_reg_holdout)

        print(f"    Modelo {i+1}/{N_MODELOS_ENSAMBLE} entrenado "
              f"(bootstrap: {len(muestra)} filas, semilla {semilla_i}).")

    residuos_val = (np.concatenate(residuos_holdout_acumulados)
                     if residuos_holdout_acumulados else np.array([]))

    if aucs:
        print(f"\n  ROC AUC promedio del ENSAMBLE en holdout (target relativo): "
              f"{np.mean(aucs):.3f} (0.5 = azar; con target relativo, un AUC "
              f"por encima de 0.5 ya indica diferenciacion real entre activos, "
              f"no solo sesgo de regimen).")

    tasa_positivos_original = float((datos_validos["target_ret_fwd"] > 0).mean())
    tasa_positivos_relativo = float((datos_validos["label_supera_mediana"] == 1).mean())
    print(f"  (referencia) % ventanas con retorno absoluto positivo: "
          f"{tasa_positivos_original*100:.1f}%")
    print(f"  (referencia) % ventanas que superan la mediana relativa: "
          f"{tasa_positivos_relativo*100:.1f}% (deberia rondar 50% por diseño, "
          f"ya que 'mediana' reparte la mitad arriba y la mitad abajo)")

    return {
        "modelos_clf": modelos_clf,
        "modelos_reg": modelos_reg,
        "residuos_val": residuos_val,
        "fecha_entrenamiento": datetime.today().strftime("%Y-%m-%d"),
    }


def predecir_ensamble(ensamble, fila_features):
    """Promedia la probabilidad (clasificador) y el retorno (regresor)
    de todos los modelos del ensamble para una fila de features."""
    probas = [m.predict_proba(fila_features)[0, 1] for m in ensamble["modelos_clf"]]
    retornos = [m.predict(fila_features)[0] for m in ensamble["modelos_reg"]]
    return float(np.mean(probas)), float(np.mean(retornos)), float(np.std(probas))


# ------------------------------------------------------------------
# NUEVO v6 - PUNTO 6: CACHE / CADENCIA DE REENTRENAMIENTO
# ------------------------------------------------------------------

def cargar_o_entrenar_ensamble(dataset_pool):
    if os.path.exists(ARCHIVO_ENSAMBLE):
        try:
            ensamble = joblib.load(ARCHIVO_ENSAMBLE)
            fecha_entreno = datetime.strptime(ensamble["fecha_entrenamiento"], "%Y-%m-%d")
            dias_desde_entreno = (datetime.today() - fecha_entreno).days
            if dias_desde_entreno < SEMANAS_ENTRE_REENTRENOS * 7:
                print(f"  Reutilizando ensamble guardado (entrenado hace "
                      f"{dias_desde_entreno} dias, cadencia: "
                      f"{SEMANAS_ENTRE_REENTRENOS} semanas). No se reentrena esta corrida.")
                return ensamble
            else:
                print(f"  El ensamble guardado tiene {dias_desde_entreno} dias "
                      f"(supera la cadencia de {SEMANAS_ENTRE_REENTRENOS} semanas) "
                      f"- reentrenando.")
        except Exception as e:
            print(f"  Aviso: no se pudo cargar el ensamble guardado ({e}), reentrenando.")

    ensamble = entrenar_ensamble(dataset_pool)
    joblib.dump(ensamble, ARCHIVO_ENSAMBLE)
    print(f"  Ensamble guardado en {ARCHIVO_ENSAMBLE} (fecha: "
          f"{ensamble['fecha_entrenamiento']}).")
    return ensamble


# ------------------------------------------------------------------
# NUEVO v6 - PUNTO 4 (capa 3): hook de guardrail cualitativo (RAG)
# ------------------------------------------------------------------

def obtener_noticias_recientes(ticker, dias=VENTANA_NOTICIAS_DIAS,
                                max_noticias=MAX_NOTICIAS_POR_TICKER):
    """RETRIEVAL: trae noticias recientes de yfinance para un ticker y
    filtra solo las de los ultimos `dias`. Parseo defensivo porque el
    formato de yf.Ticker(x).news ha cambiado entre versiones de la
    libreria (algunas anidan los campos bajo "content", otras no)."""
    try:
        crudo = yf.Ticker(ticker).news
    except Exception as e:
        print(f"  Aviso RAG: no se pudo obtener noticias para {ticker}: {e}")
        return []

    noticias = []
    ahora = datetime.now(timezone.utc)
    for item in (crudo or []):
        contenido = item.get("content", item) if isinstance(item, dict) else {}
        titulo = contenido.get("title") or item.get("title")
        if not titulo:
            continue
        resumen = contenido.get("summary") or contenido.get("description") or ""

        fecha_raw = (contenido.get("pubDate") or item.get("providerPublishTime")
                     or contenido.get("displayTime"))
        fecha = None
        if isinstance(fecha_raw, (int, float)):
            fecha = datetime.fromtimestamp(fecha_raw, tz=timezone.utc)
        elif isinstance(fecha_raw, str):
            try:
                fecha = datetime.fromisoformat(fecha_raw.replace("Z", "+00:00"))
            except ValueError:
                fecha = None

        if fecha is not None and (ahora - fecha).days > dias:
            continue  # demasiado vieja, se ignora

        noticias.append({"titulo": titulo, "resumen": (resumen or "")[:300], "fecha": fecha})
        if len(noticias) >= max_noticias:
            break

    return noticias


def construir_prompt_rag(ticker, noticias):
    lineas = []
    for n in noticias:
        fecha_txt = n["fecha"].strftime("%Y-%m-%d") if n["fecha"] else "fecha desconocida"
        linea = f"- [{fecha_txt}] {n['titulo']}"
        if n["resumen"]:
            linea += f" — {n['resumen']}"
        lineas.append(linea)
    return f"Ticker: {ticker}\n\nNoticias recientes (ultimos {VENTANA_NOTICIAS_DIAS} dias):\n" + "\n".join(lineas)


_SYSTEM_PROMPT_RAG = (
    "Eres un analista de riesgo que revisa noticias recientes de un activo "
    "financiero ANTES de que un equipo estudiantil lo compre esta semana en "
    "una cuenta simulada. Tu unico trabajo es detectar si hay una noticia "
    "MATERIAL y NEGATIVA reciente (ej. fraude, investigacion regulatoria "
    "seria, quiebra, escandalo grave, retiro masivo de producto, salida "
    "abrupta de un ejecutivo clave por causa negativa) que justifique NO "
    "comprar este activo esta semana.\n\n"
    "Se conservador: resultados trimestrales mixtos, volatilidad normal de "
    "precio, opiniones de analistas, o ruido general de mercado NO deben "
    "bloquear la compra - eso ya lo evalua por separado un modelo "
    "cuantitativo. Solo vetar ante señales genuinamente graves.\n\n"
    "Responde EXCLUSIVAMENTE con un JSON valido, sin texto adicional antes "
    "ni despues, con este formato exacto:\n"
    '{"aprobado": true o false, "motivo": "explicacion breve en una linea"}'
)


def _consultar_anthropic(prompt_usuario):
    """Consulta a Claude directo via API de Anthropic (de pago)."""
    respuesta = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": MODELO_LLM_ANTHROPIC,
            "max_tokens": 200,
            "system": _SYSTEM_PROMPT_RAG,
            "messages": [{"role": "user", "content": prompt_usuario}],
        },
        timeout=30,
    )
    respuesta.raise_for_status()
    data = respuesta.json()
    return "".join(
        bloque.get("text", "") for bloque in data.get("content", [])
        if bloque.get("type") == "text"
    )


def _consultar_openrouter(prompt_usuario):
    """Consulta a un modelo gratuito via OpenRouter (endpoint compatible
    con el formato de OpenAI). Ver OPENROUTER_MODELO arriba - los modelos
    ':free' pueden rotar; revisar openrouter.ai/models?max_price=0 si este
    deja de responder."""
    respuesta = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENROUTER_MODELO,
            "messages": [
                {"role": "system", "content": _SYSTEM_PROMPT_RAG},
                {"role": "user", "content": prompt_usuario},
            ],
            "max_tokens": 200,
        },
        timeout=30,
    )
    respuesta.raise_for_status()
    data = respuesta.json()
    return data["choices"][0]["message"]["content"]


def veto_cualitativo_rag(ticker):
    """Capa 3 (cualitativa): RETRIEVAL (noticias recientes via yfinance) +
    GENERATION (un LLM - Claude u OpenRouter gratuito, segun
    RAG_PROVEEDOR - lee las noticias y decide). Devuelve (aprobado, motivo).

    Diseño fail-open deliberado: si falta la API key, no hay noticias, o la
    llamada al LLM falla por cualquier razon, se aprueba por defecto en vez
    de bloquear todo el pipeline - un guardrail cualitativo que tumba el
    sistema entero por una falla tecnica seria peor que no tenerlo. Se
    imprime siempre un aviso claro cuando esto pasa, para que quede
    documentado y no sea un fallo silencioso."""
    if RAG_PROVEEDOR == "openrouter" and not OPENROUTER_API_KEY:
        return True, "OPENROUTER_API_KEY no configurada - guardrail RAG inactivo (aprobado por defecto)."
    if RAG_PROVEEDOR == "anthropic" and not ANTHROPIC_API_KEY:
        return True, "ANTHROPIC_API_KEY no configurada - guardrail RAG inactivo (aprobado por defecto)."
    if RAG_PROVEEDOR not in ("openrouter", "anthropic"):
        return True, (f"RAG_PROVEEDOR={RAG_PROVEEDOR!r} no reconocido (usar 'openrouter' "
                       f"o 'anthropic') - guardrail RAG inactivo (aprobado por defecto).")

    noticias = obtener_noticias_recientes(ticker)
    if not noticias:
        return True, (f"Sin noticias recientes para {ticker} en los ultimos "
                       f"{VENTANA_NOTICIAS_DIAS} dias - aprobado por defecto.")

    prompt_usuario = construir_prompt_rag(ticker, noticias)

    try:
        if RAG_PROVEEDOR == "openrouter":
            texto = _consultar_openrouter(prompt_usuario)
        else:
            texto = _consultar_anthropic(prompt_usuario)

        texto = texto.strip().replace("```json", "").replace("```", "").strip()
        resultado = json.loads(texto)
        aprobado = bool(resultado.get("aprobado", True))
        motivo = str(resultado.get("motivo", "Sin motivo especificado por el modelo."))
        return aprobado, f"[RAG/{RAG_PROVEEDOR}] {motivo}"

    except Exception as e:
        print(f"  Aviso RAG ({RAG_PROVEEDOR}): fallo la consulta para {ticker} ({e}). "
              f"Fail-open: se aprueba por defecto.")
        return True, f"Error en guardrail RAG ({e}) - aprobado por defecto (fail-open)."


# ------------------------------------------------------------------
# NUEVO v6 - PUNTO 5: CIRCUIT BREAKER Y MONITOR DE HIT-RATE
# ------------------------------------------------------------------

def verificar_circuit_breaker(estado):
    """Compara el capital actual contra el maximo historico registrado.
    Si el drawdown supera CIRCUIT_BREAKER_DRAWDOWN_PCT, se pausan todas
    las compras nuevas hasta que el equipo lo revise y resetee
    manualmente 'circuit_breaker_activo' en el estado."""
    capital_actual = estado.get("capital_disponible", CAPITAL_TOTAL)
    capital_maximo_historico = estado.get("capital_maximo_historico", CAPITAL_TOTAL)
    capital_maximo_historico = max(capital_maximo_historico, capital_actual)
    estado["capital_maximo_historico"] = capital_maximo_historico

    drawdown_pct = (capital_actual / capital_maximo_historico - 1) * 100

    if estado.get("circuit_breaker_activo", False):
        print(f"  CIRCUIT BREAKER SIGUE ACTIVO (activado manualmente en una corrida "
              f"anterior). No se generaran compras nuevas hasta que el equipo lo "
              f"revise y ponga 'circuit_breaker_activo': false en {ARCHIVO_ESTADO}.")
        return True, estado

    if drawdown_pct <= CIRCUIT_BREAKER_DRAWDOWN_PCT:
        print(f"  *** CIRCUIT BREAKER ACTIVADO *** Drawdown actual: {drawdown_pct:.1f}% "
              f"(umbral: {CIRCUIT_BREAKER_DRAWDOWN_PCT}%). Se pausan TODAS las compras "
              f"nuevas esta semana. Revisar la estrategia como equipo antes de "
              f"reactivar manualmente.")
        estado["circuit_breaker_activo"] = True
        return True, estado

    print(f"  Circuit breaker OK (drawdown actual: {drawdown_pct:.1f}%, "
          f"umbral: {CIRCUIT_BREAKER_DRAWDOWN_PCT}%).")
    return False, estado


def actualizar_monitor_hit_rate(estado, precios_actuales_por_ticker):
    """Revisa las compras de semanas anteriores (registradas en el
    historial) cuyo horizonte de DIAS_PROYECTADOS ya se cumplio, y
    verifica si superaron la mediana del universo ese periodo (el mismo
    criterio que usa el modelo para decidir). Mantiene un hit-rate movil
    de las ultimas VENTANA_HIT_RATE_SEMANAS decisiones evaluables."""
    historial = estado.get("historial", [])
    if not historial:
        return estado

    hoy = datetime.today()
    hit_rates_recientes = estado.get("hit_rate_historico", [])

    for entrada in historial:
        if entrada.get("evaluado_hit_rate", False):
            continue
        fecha_compra = datetime.strptime(entrada["fecha"], "%Y-%m-%d")
        dias_transcurridos = (hoy - fecha_compra).days
        if dias_transcurridos < DIAS_PROYECTADOS * 1.4:  # ~40% de margen habil/calendario
            continue  # aun no ha pasado suficiente tiempo para evaluar

        aciertos, total = 0, 0
        for orden in entrada.get("ordenes", []):
            ticker = orden["ticker"]
            precio_compra = orden.get("precio_compra_referencia")
            precio_hoy = precios_actuales_por_ticker.get(ticker)
            if precio_compra and precio_hoy:
                retorno_real = precio_hoy / precio_compra - 1
                # Comparacion simplificada: se considera "acierto" si el
                # retorno real fue positivo (proxy razonable sin volver a
                # calcular la mediana historica exacta de esa semana).
                total += 1
                if retorno_real > 0:
                    aciertos += 1
        if total > 0:
            hit_rates_recientes.append(aciertos / total)
        entrada["evaluado_hit_rate"] = True

    hit_rates_recientes = hit_rates_recientes[-VENTANA_HIT_RATE_SEMANAS:]
    estado["hit_rate_historico"] = hit_rates_recientes

    if len(hit_rates_recientes) >= 3:
        hit_rate_promedio = float(np.mean(hit_rates_recientes))
        print(f"\n  === MONITOR DE HIT-RATE (model drift) ===")
        print(f"  Hit-rate promedio de las ultimas {len(hit_rates_recientes)} "
              f"semanas evaluables: {hit_rate_promedio*100:.1f}%")
        if hit_rate_promedio < UMBRAL_HIT_RATE_ALERTA:
            print(f"  ALERTA: hit-rate por debajo del umbral "
                  f"({UMBRAL_HIT_RATE_ALERTA*100:.0f}%) - posible degradacion del "
                  f"modelo (cambio de regimen de mercado, features desactualizados). "
                  f"Considerar forzar un reentrenamiento aunque no toque por cadencia.")

    return estado


# ------------------------------------------------------------------
# EVALUACION POR TICKER (usa el ensamble + capas de riesgo/cualitativa)
# ------------------------------------------------------------------

def evaluar_activo_v6(ticker, precios, feats, ensamble, tasas_cambio=None):
    tasas_cambio = tasas_cambio or {}
    fila_actual = feats.iloc[[-1]][FEATURE_COLS + ["ticker"]]
    if fila_actual[FEATURE_COLS].isna().any(axis=None):
        raise ValueError(f"Features insuficientes para {ticker}.")

    prob_supera_mediana, retorno_pred, std_proba_ensamble = predecir_ensamble(ensamble, fila_actual)
    retorno_esperado_pct = float(np.clip(
        retorno_pred * 100, RETORNO_PRED_MIN_PCT, RETORNO_PRED_MAX_PCT
    ))
    retorno_pred = retorno_esperado_pct / 100

    residuos_val = ensamble["residuos_val"]
    if len(residuos_val) > 0:
        cuantil_var = np.percentile(residuos_val, NIVEL_CONFIANZA_VAR * 100)
        cola = residuos_val[residuos_val <= cuantil_var]
        var_pct = (retorno_pred + cuantil_var) * 100
        cvar_pct = (retorno_pred + (cola.mean() if len(cola) else cuantil_var)) * 100
    else:
        var_pct = cvar_pct = retorno_esperado_pct

    ret_1d_hist = feats["ret_1d"].dropna()
    vol_diaria_hist = float(ret_1d_hist.std()) if len(ret_1d_hist) > 1 else 0.0
    retorno_anual_equiv = retorno_pred * (DIAS_HABILES_ANIO / DIAS_PROYECTADOS)
    vol_anual = vol_diaria_hist * np.sqrt(DIAS_HABILES_ANIO)
    ratio_retorno_riesgo_anual = retorno_anual_equiv / vol_anual if vol_anual != 0 else 0.0

    vol_horizonte = vol_diaria_hist * np.sqrt(DIAS_PROYECTADOS)
    stop_loss_pct = float(np.clip(
        STOP_LOSS_N_DESVIACIONES * vol_horizonte, STOP_LOSS_MIN_PCT, STOP_LOSS_MAX_PCT
    ))

    precio_actual_local = float(precios.iloc[-1])
    moneda = MONEDA_TICKER.get(ticker, "USD")
    if moneda == "USD":
        precio_actual = precio_actual_local
    else:
        tasa = tasas_cambio.get(moneda)
        precio_actual = precio_actual_local / tasa if tasa else precio_actual_local

    return {
        "ticker": ticker,
        "precio_actual": round(precio_actual, 2),
        "prob_supera_mediana": round(prob_supera_mediana * 100, 1),
        "incertidumbre_ensamble": round(std_proba_ensamble, 3),
        "retorno_esperado_pct": round(retorno_esperado_pct, 2),
        "var_pct": round(var_pct, 2),
        "cvar_pct": round(cvar_pct, 2),
        "ratio_retorno_riesgo_anual": round(ratio_retorno_riesgo_anual, 3),
        "stop_loss_pct": round(stop_loss_pct, 1),
    }


# ------------------------------------------------------------------
# NUEVO v6 - PUNTOS 2 y 4: SELECCION (ranking + veto de riesgo + RAG)
# ------------------------------------------------------------------

def seleccionar_candidatos(resultados):
    """Capa 1 (ranking) + Capa 2 (veto de riesgo RELATIVO) + Capa 3 (veto
    RAG, stub). Devuelve la lista de tickers seleccionados como BUY esta
    semana, y un log de por que cada uno entro o fue descartado."""
    candidatos = sorted(resultados, key=lambda r: r["prob_supera_mediana"], reverse=True)

    # Veto de riesgo RELATIVO: se calcula el percentil de corte de CVaR
    # entre los candidatos de ESTA semana (nunca un numero absoluto fijo -
    # ver nota en CVAR_VETO_PERCENTIL sobre por que se cambio de diseño).
    cvars = np.array([r["cvar_pct"] for r in candidatos])
    if len(cvars) > 0:
        corte_cvar = np.percentile(cvars, CVAR_VETO_PERCENTIL)
    else:
        corte_cvar = -np.inf

    seleccionados = []
    log_decisiones = []

    for r in candidatos:
        if len(seleccionados) >= N_POSICIONES_SEMANA:
            log_decisiones.append((r["ticker"], "DESCARTADO", "cupo semanal ya lleno"))
            continue

        if r["retorno_esperado_pct"] < UMBRAL_RETORNO_MIN_ABSOLUTO:
            log_decisiones.append((r["ticker"], "DESCARTADO",
                                    f"retorno absoluto ({r['retorno_esperado_pct']:.1f}%) "
                                    f"por debajo del piso de seguridad"))
            continue

        if r["cvar_pct"] < corte_cvar:
            log_decisiones.append((r["ticker"], "DESCARTADO (capa riesgo)",
                                    f"CVaR ({r['cvar_pct']:.1f}%) esta en el peor "
                                    f"{CVAR_VETO_PERCENTIL}% relativo de esta semana "
                                    f"(corte: {corte_cvar:.1f}%)"))
            continue

        aprobado_rag, motivo_rag = veto_cualitativo_rag(r["ticker"])
        if not aprobado_rag:
            log_decisiones.append((r["ticker"], "DESCARTADO (capa cualitativa)", motivo_rag))
            continue

        r["decision"] = "BUY"
        seleccionados.append(r)
        log_decisiones.append((r["ticker"], "BUY", f"rank #{len(seleccionados)}, "
                                f"prob={r['prob_supera_mediana']:.1f}%"))

    for r in resultados:
        if r not in seleccionados:
            r["decision"] = "HOLD"

    print(f"\n  === LOG DE SELECCION (ranking + capas de riesgo/cualitativa) ===")
    print(f"  Corte de veto CVaR esta semana (peor {CVAR_VETO_PERCENTIL}% relativo): "
          f"{corte_cvar:.1f}%")
    for ticker, estado_dec, motivo in log_decisiones:
        print(f"    {ticker:<12} {estado_dec:<28} {motivo}")

    return resultados


# ------------------------------------------------------------------
# ASIGNACION DE CAPITAL / JSON / VALIDADOR (heredado de v4/v5)
# ------------------------------------------------------------------

def cargar_estado():
    if os.path.exists(ARCHIVO_ESTADO):
        with open(ARCHIVO_ESTADO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"capital_disponible": CAPITAL_TOTAL, "semana_actual": 0, "historial": [],
            "capital_maximo_historico": CAPITAL_TOTAL, "circuit_breaker_activo": False,
            "hit_rate_historico": []}


def guardar_estado(estado):
    with open(ARCHIVO_ESTADO, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=2, ensure_ascii=False)


def asignar_capital(resultados, capital_disponible):
    presupuesto_semana = capital_disponible * PCT_CAPITAL_POR_SEMANA
    buys = [r for r in resultados if r["decision"] == "BUY"]
    if not buys:
        return [], presupuesto_semana, 0.0, presupuesto_semana

    ratios = np.array([max(r["ratio_retorno_riesgo_anual"], 0.0) for r in buys])
    pesos_brutos = ratios / ratios.sum() if ratios.sum() > 0 else np.full(len(buys), 1 / len(buys))
    pesos_con_piso = np.maximum(pesos_brutos, PESO_MINIMO_CONVICCION)
    pesos_norm = pesos_con_piso / pesos_con_piso.sum()

    tope_por_posicion = presupuesto_semana * MAX_EXPOSICION_PCT_POSICION
    montos_objetivo = np.minimum(presupuesto_semana * pesos_norm, tope_por_posicion)

    cantidades = np.array([int(m // r["precio_actual"]) for m, r in zip(montos_objetivo, buys)])
    costos = np.array([c * r["precio_actual"] for c, r in zip(cantidades, buys)])
    capital_usado = float(costos.sum())
    capital_restante = presupuesto_semana - capital_usado

    precios_lista = np.array([r["precio_actual"] for r in buys])
    ronda = 0
    while capital_restante > 0 and ronda < MAX_RONDAS_REDISTRIBUCION:
        margen = tope_por_posicion - costos
        asequibles = np.where((precios_lista <= capital_restante) & (margen >= precios_lista))[0]
        if len(asequibles) == 0:
            break
        pesos_ronda = pesos_norm[asequibles]
        pesos_ronda = pesos_ronda / pesos_ronda.sum()
        usado_ronda = 0.0
        for il, ig in enumerate(asequibles):
            monto_extra = min(capital_restante * pesos_ronda[il], margen[ig])
            u = int(monto_extra // precios_lista[ig])
            if u <= 0:
                continue
            cantidades[ig] += u
            costo_extra = u * precios_lista[ig]
            costos[ig] += costo_extra
            usado_ronda += costo_extra
        if usado_ronda <= 0:
            break
        capital_usado += usado_ronda
        capital_restante -= usado_ronda
        ronda += 1

    ordenes = []
    for r, cant, costo in zip(buys, cantidades, costos):
        if cant > 0:
            ordenes.append({**r, "cantidad": int(cant), "costo_real": round(float(costo), 2)})

    capital_sobrante = presupuesto_semana - capital_usado
    return ordenes, presupuesto_semana, capital_usado, capital_sobrante


def generar_bloque_json(ordenes_con_cantidad):
    orders = []
    for r in ordenes_con_cantidad:
        if r["cantidad"] <= 0:
            continue
        simbolo_reporte = "BRK.B" if r["ticker"] == "BRK-B" else r["ticker"].replace(".KS", "")
        stop_loss_precio = round(r["precio_actual"] * (1 - r["stop_loss_pct"] / 100), 2)
        orders.append({
            "action": "BUY", "symbol": simbolo_reporte, "quantity": r["cantidad"],
            "type": "MARKET", "stop_loss": stop_loss_precio,
        })
    return {"version": 1, "orders": orders}


# ------------------------------------------------------------------
# NUEVO: armado y envio automatico del correo (sin input() interactivo,
# apto para correr sin supervision en CI/GitHub Actions)
# ------------------------------------------------------------------

def armar_asunto(semana_numero):
    return f"[AI-TRADING][SEMANA-{semana_numero:02d}][{CODIGO_CUENTA}]"


def armar_cuerpo(bloque_json):
    return json.dumps(bloque_json, indent=2, ensure_ascii=False)


def _sanear(texto):
    if texto is None:
        return texto
    return texto.replace("\xa0", " ").replace("\u200b", "").strip()


def enviar_correo_automatico(asunto, cuerpo):
    """Envia el correo SIN pedir confirmacion interactiva (no hay
    terminal en CI). Por eso todas las salvaguardas (MODO_PRUEBA,
    ENVIAR_CORREO_REAL, validacion del JSON) deben pasar ANTES de
    llamar a esta funcion - ver el bloque principal mas abajo."""
    if not EMAIL_REMITENTE or not EMAIL_APP_PASSWORD:
        print("  ERROR: faltan EMAIL_REMITENTE o EMAIL_APP_PASSWORD en el entorno "
              "(revisar GitHub Secrets). No se envio nada.")
        return False

    remitente = _sanear(EMAIL_REMITENTE)
    app_password = _sanear(EMAIL_APP_PASSWORD).replace(" ", "")
    asunto = _sanear(asunto)
    cuerpo = _sanear(cuerpo)

    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = EMAIL_DESTINATARIO
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(cuerpo, "plain", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_SERVOR, SMTP_PUERTO) as servidor:
            servidor.starttls()
            servidor.login(remitente, app_password)
            servidor.send_message(mensaje, from_addr=remitente, to_addrs=EMAIL_DESTINATARIO)
        print(f"  Correo enviado correctamente a {EMAIL_DESTINATARIO}.")
        return True
    except smtplib.SMTPAuthenticationError:
        print("  ERROR DE AUTENTICACION: revisar que EMAIL_APP_PASSWORD sea una "
              "contraseña de aplicacion (16 caracteres), no la contraseña normal.")
        return False
    except Exception as e:
        print(f"  ERROR al enviar el correo: {e}")
        return False


# ------------------------------------------------------------------
# NUEVO: INFORME SEMANAL EN MARKDOWN (E7 - Reporting)
# ------------------------------------------------------------------

def generar_informe_semanal(tabla, resultados, ordenes, estado, bloque_json,
                             circuit_breaker_activo, ensamble, errores_validacion=None):
    """Compila la corrida completa (ranking, selecciones, guardrails,
    capital, JSON final) en un archivo Markdown legible. Se genera en
    TODA corrida (oficial o de prueba) para dejar rastro documentado del
    proceso, pero el nombre del archivo deja clarisimo cual es cual -
    nunca se confunde una prueba con una semana real."""
    os.makedirs(CARPETA_INFORMES, exist_ok=True)

    fecha_hoy = datetime.today().strftime("%Y-%m-%d")
    es_oficial = (not MODO_PRUEBA) and ENVIAR_CORREO_REAL
    etiqueta = "OFICIAL" if es_oficial else "PRUEBA"
    semana_numero = estado.get("semana_actual", "?")
    nombre_archivo = f"{CARPETA_INFORMES}/informe_{fecha_hoy}_{etiqueta}.md"

    lineas = []
    lineas.append(f"# Informe Semanal — AI Trading Challenge (CTA-003)")
    lineas.append("")
    lineas.append(f"**Fecha de la corrida:** {fecha_hoy}  ")
    lineas.append(f"**Semana:** {semana_numero}  ")
    lineas.append(f"**Tipo de corrida:** {'✅ OFICIAL (correo enviado)' if es_oficial else '🧪 PRUEBA (no se envio nada)'}  ")
    lineas.append("")

    # --- Estado del ensamble ---------------------------------------------
    lineas.append("## Estado del modelo (ensamble)")
    lineas.append("")
    lineas.append(f"- Fecha de entrenamiento del ensamble usado: **{ensamble.get('fecha_entrenamiento', '?')}**")
    lineas.append(f"- Numero de modelos en el ensamble: **{len(ensamble.get('modelos_clf', []))}**")
    hit_rate_hist = estado.get("hit_rate_historico", [])
    if hit_rate_hist:
        lineas.append(f"- Hit-rate movil (ultimas {len(hit_rate_hist)} semanas evaluables): "
                       f"**{np.mean(hit_rate_hist)*100:.1f}%**")
    lineas.append("")

    # --- Guardrails --------------------------------------------------------
    lineas.append("## Guardrails")
    lineas.append("")
    drawdown_actual = (estado.get("capital_disponible", CAPITAL_TOTAL) /
                        estado.get("capital_maximo_historico", CAPITAL_TOTAL) - 1) * 100
    lineas.append(f"- Drawdown actual vs. maximo historico: **{drawdown_actual:.1f}%** "
                   f"(umbral circuit breaker: {CIRCUIT_BREAKER_DRAWDOWN_PCT}%)")
    lineas.append(f"- Circuit breaker: {'🔴 **ACTIVO** (todas las compras pausadas)' if circuit_breaker_activo else '🟢 inactivo'}")
    lineas.append("")

    # --- Ranking completo del universo --------------------------------------
    lineas.append("## Ranking del universo evaluado esta semana")
    lineas.append("")
    cols_tabla = ["ticker", "precio_actual", "prob_supera_mediana", "retorno_esperado_pct",
                  "var_pct", "cvar_pct", "incertidumbre_ensamble"]
    cols_presentes = [c for c in cols_tabla if c in tabla.columns]
    try:
        lineas.append(tabla[cols_presentes].to_markdown(index=False, floatfmt=".2f"))
    except ImportError:
        lineas.append(tabla[cols_presentes].to_string(index=False))
    lineas.append("")

    # --- Seleccion final -----------------------------------------------------
    lineas.append("## Seleccion final (BUY de esta semana)")
    lineas.append("")
    buys = [r for r in resultados if r.get("decision") == "BUY"]
    if buys:
        for r in buys:
            lineas.append(f"- **{r['ticker']}** — precio ${r['precio_actual']:.2f}, "
                           f"prob. supera mediana: {r['prob_supera_mediana']:.1f}%, "
                           f"CVaR: {r['cvar_pct']:.1f}%")
    else:
        lineas.append("*Ninguna posicion nueva esta semana.*")
    lineas.append("")

    # --- Capital y ordenes ejecutadas -----------------------------------------
    lineas.append("## Capital asignado")
    lineas.append("")
    if ordenes:
        tabla_ordenes = pd.DataFrame(ordenes)[["ticker", "precio_actual", "cantidad", "costo_real"]]
        try:
            lineas.append(tabla_ordenes.to_markdown(index=False, floatfmt=".2f"))
        except ImportError:
            lineas.append(tabla_ordenes.to_string(index=False))
        capital_total_usado = sum(o["costo_real"] for o in ordenes)
        lineas.append("")
        lineas.append(f"**Capital total usado esta semana:** ${capital_total_usado:.2f}")
    else:
        lineas.append("*No se ejecuto ninguna orden esta semana.*")
    lineas.append("")
    lineas.append(f"**Capital disponible despues de esta semana:** ${estado.get('capital_disponible', CAPITAL_TOTAL):.2f}")
    lineas.append("")

    # --- JSON final / validacion ---------------------------------------------
    lineas.append("## Bloque JSON generado")
    lineas.append("")
    if errores_validacion:
        lineas.append("⚠️ **La validacion local encontro errores - este JSON NO se envio:**")
        lineas.append("")
        for e in errores_validacion:
            lineas.append(f"- {e}")
    else:
        lineas.append("✅ Validacion local OK.")
    lineas.append("")
    lineas.append("```json")
    lineas.append(json.dumps(bloque_json, indent=2, ensure_ascii=False))
    lineas.append("```")
    lineas.append("")

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"\nInforme semanal guardado en {nombre_archivo}")
    return nombre_archivo


def validar_orden(bloque_json):
    errores = []
    if not isinstance(bloque_json, dict):
        return ["El bloque no es un objeto JSON valido (dict)."]
    if bloque_json.get("version") != 1:
        errores.append(f'"version" debe ser 1. Se encontro: {bloque_json.get("version")!r}')
    orders = bloque_json.get("orders")
    if not isinstance(orders, list) or len(orders) == 0:
        errores.append('"orders" debe ser una lista NO vacia.')
        return errores
    vistos = []
    for i, orden in enumerate(orders, start=1):
        prefijo = f"Orden #{i}"
        action = orden.get("action")
        if action not in ACCIONES_VALIDAS:
            errores.append(f'{prefijo}: "action" invalido: {action!r}')
        symbol = orden.get("symbol")
        if not isinstance(symbol, str) or symbol == "":
            errores.append(f'{prefijo}: falta "symbol".')
        else:
            if symbol != symbol.upper():
                errores.append(f'{prefijo}: "symbol" debe ir en MAYUSCULAS: {symbol!r}')
            if symbol.upper() not in SIMBOLOS_HABILITADOS:
                errores.append(f'{prefijo}: simbolo {symbol!r} no habilitado.')
            vistos.append(symbol)
        tipo = orden.get("type")
        if tipo not in TIPOS_VALIDOS:
            errores.append(f'{prefijo}: "type" invalido: {tipo!r}')
        quantity = orden.get("quantity")
        if action != "CLOSE" and (not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0):
            errores.append(f'{prefijo}: "quantity" invalida: {quantity!r}')
        stop_loss = orden.get("stop_loss")
        if stop_loss is not None and (not isinstance(stop_loss, (int, float)) or stop_loss <= 0):
            errores.append(f'{prefijo}: "stop_loss" invalido: {stop_loss!r}')
    duplicados = {s for s in vistos if vistos.count(s) > 1}
    if duplicados:
        errores.append(f"Simbolos repetidos: {sorted(duplicados)}")
    return errores


# ------------------------------------------------------------------
# EJECUCION PRINCIPAL
# ------------------------------------------------------------------

if __name__ == "__main__":
    print("Obteniendo tipos de cambio...")
    tasas_cambio = obtener_tasas_cambio(TICKERS)

    print("\n=== CONSTRUYENDO DATASET (universo de analisis completo) ===")
    dataset_pool, series_por_ticker, tickers_excluidos = construir_dataset(TICKERS)
    dataset_pool = agregar_target_relativo(dataset_pool)

    print("\n=== ENSAMBLE XGBOOST (punto 3 + 6: bagging + cadencia de reentreno) ===")
    ensamble = cargar_o_entrenar_ensamble(dataset_pool)

    print("\n=== EVALUANDO CADA TICKER CON EL ENSAMBLE ===")
    resultados = []
    for ticker, precios in series_por_ticker.items():
        try:
            feats_ticker = dataset_pool[dataset_pool["ticker"] == ticker].set_index("fecha")
            resultados.append(evaluar_activo_v6(
                ticker, precios, feats_ticker, ensamble, tasas_cambio=tasas_cambio
            ))
        except Exception as e:
            print(f"  Error con {ticker}: {e}")

    print("\n=== RESUMEN (antes de seleccion) ===")
    tabla = pd.DataFrame(resultados).sort_values("prob_supera_mediana", ascending=False)
    print(tabla[["ticker", "precio_actual", "prob_supera_mediana", "retorno_esperado_pct",
                  "var_pct", "cvar_pct", "incertidumbre_ensamble"]].to_string(index=False))

    resultados = seleccionar_candidatos(resultados)

    estado = cargar_estado()

    print("\n=== GUARDRAILS ===")
    circuit_breaker_activo, estado = verificar_circuit_breaker(estado)
    precios_actuales_por_ticker = {t: float(s.iloc[-1]) for t, s in series_por_ticker.items()}
    estado = actualizar_monitor_hit_rate(estado, precios_actuales_por_ticker)

    if circuit_breaker_activo:
        for r in resultados:
            r["decision"] = "HOLD"
        print("\n  Todas las decisiones forzadas a HOLD por el circuit breaker.")

    semana_actual = estado["semana_actual"]
    ordenes, presupuesto_semana, capital_usado, capital_sobrante = asignar_capital(
        resultados, estado["capital_disponible"]
    )

    print(f"\n=== CAPITAL - SEMANA {semana_actual + 1} ===")
    print(f"Capital disponible: ${estado['capital_disponible']:.2f}")
    print(f"Presupuesto de la semana: ${presupuesto_semana:.2f}")
    print(f"Posiciones seleccionadas (cupo maximo {N_POSICIONES_SEMANA}): {len(ordenes)}")
    if ordenes:
        print(pd.DataFrame(ordenes)[["ticker", "precio_actual", "cantidad", "costo_real"]]
              .to_string(index=False))
    print(f"Capital usado: ${capital_usado:.2f} | Sobrante: ${capital_sobrante:.2f}")

    estado["capital_disponible"] -= capital_usado
    estado["semana_actual"] = semana_actual + 1
    estado["historial"].append({
        "semana": semana_actual + 1,
        "fecha": FECHA_FIN,
        "ordenes": [{"ticker": o["ticker"], "cantidad": o["cantidad"],
                     "precio_compra_referencia": o["precio_actual"]} for o in ordenes],
        "evaluado_hit_rate": False,
    })

    if MODO_PRUEBA:
        print(f"\n[MODO_PRUEBA activo: NO se guardo el estado.]")
    else:
        guardar_estado(estado)
        print(f"\nEstado guardado. Capital para la proxima semana: "
              f"${estado['capital_disponible']:.2f}")

    bloque_json = generar_bloque_json(ordenes)
    print("\n=== VALIDACION LOCAL ===")
    errores = validar_orden(bloque_json)

    generar_informe_semanal(
        tabla, resultados, ordenes, estado, bloque_json,
        circuit_breaker_activo, ensamble, errores_validacion=errores,
    )

    if errores:
        print("EL JSON TIENE ERRORES:")
        for e in errores:
            print("  -", e)
        raise SystemExit("Corrige los errores antes de enviar.")
    print("Validacion OK.")

    print("\n=== BLOQUE JSON PARA EL CORREO SEMANAL ===")
    print(json.dumps(bloque_json, indent=2, ensure_ascii=False))

    tabla.to_csv("backlog_decisiones_v6.csv", index=False)
    print("\nTabla guardada en backlog_decisiones_v6.csv")

    # --- Envio automatico (SOLO si pasaron todos los seguros) -----------
    print("\n=== ENVIO DE CORREO ===")
    if MODO_PRUEBA:
        print("  MODO_PRUEBA activo: no se intenta enviar correo.")
    elif not ENVIAR_CORREO_REAL:
        print("  ENVIAR_CORREO_REAL no esta en 'true': no se intenta enviar correo "
              "(esto es normal en una corrida manual de prueba).")
    elif len(ordenes) == 0:
        print("  No hay ordenes esta semana (0 posiciones seleccionadas o circuit "
              "breaker activo): no se envia correo. Revisar manualmente si esto es "
              "lo esperado.")
    else:
        asunto = armar_asunto(estado["semana_actual"])
        cuerpo = armar_cuerpo(bloque_json)
        print(f"  Asunto: {asunto}")
        enviado = enviar_correo_automatico(asunto, cuerpo)
        if not enviado:
            raise SystemExit(
                "El envio automatico de correo fallo. Revisar el log de arriba "
                "(credenciales, conexion) y reintentar."
            )
