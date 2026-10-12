"""
REPORTE VISUAL - R3 (Epica E7: Reporting y Visualizacion)
AI Trading Challenge - CTA-003 - Equipo Anzoategui y Rayo
============================================================
Construye, a partir de estado_portafolio.json (generado por
modelo_trading_v6.py), un reporte con:
  - Equity curve (patrimonio total: efectivo + valor de mercado real
    de las posiciones, dia a dia, no solo el precio de compra)
  - P&L acumulado
  - Posiciones abiertas actuales (con P&L no realizado por ticker)
  - Operaciones realizadas (historial completo, semana a semana)
  - Metricas de desempeño principales (retorno total, max drawdown,
    hit-rate, semanas/ordenes operadas)

Requiere: estado_portafolio.json real (acumulado desde la Semana 01).
No funciona con datos de ejemplo - sin historial real no hay nada que
graficar.

Uso:
    python reporte_visual_r3.py
    (o import y llamar generar_reporte_r3() desde un notebook)

NOTA: requiere yfinance, pandas, matplotlib, numpy (y opcionalmente
tabulate, para que las tablas del .md salgan bien formateadas).
"""

import json
import os
import time
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf

# ------------------------------------------------------------------
# CONFIGURACION (debe coincidir con modelo_trading_v6.py)
# ------------------------------------------------------------------
ARCHIVO_ESTADO = "estado_portafolio.json"
CAPITAL_TOTAL = 10000.0
CARPETA_REPORTES = "reportes"

# Monedas de los tickers no-USD (debe coincidir con modelo_v6.py).
# FIX (bug KRW): los precios de 005930.KS y 000660.KS vienen en wones;
# hay que convertirlos a USD antes de valorar posiciones, porque el costo
# de compra guardado en el estado ya esta en USD.
MONEDA_TICKER = {"005930.KS": "KRW", "000660.KS": "KRW"}
PAR_FX_A_USD = {"KRW": "KRW=X"}


def cargar_estado(archivo=ARCHIVO_ESTADO):
    if not os.path.exists(archivo):
        raise FileNotFoundError(
            f"No se encontro {archivo}. Este reporte necesita el estado real "
            f"acumulado desde la Semana 01 (no funciona con datos de ejemplo)."
        )
    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)


def descargar_con_reintentos(ticker, intentos=3, espera_segundos=5, **kwargs):
    # Copia liviana de la funcion homonima en modelo_trading_v6.py, para
    # no tener que importar el script completo (que dispararia entrenamiento
    # del ensamble solo para generar un reporte).
    ultimo_error = None
    for intento in range(1, intentos + 1):
        try:
            datos = yf.download(ticker, progress=False, **kwargs)
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


def convertir_serie_a_usd(ticker, serie, inicio, fin):
    """Convierte una serie de precios en moneda local a USD, dia a dia,
    usando el tipo de cambio historico (se rellena hacia adelante en dias
    sin cotizacion FX, p. ej. feriados). Devuelve la serie sin cambios si
    el ticker ya esta en USD. Lanza ValueError si no hay tipo de cambio:
    es preferible excluir el ticker con aviso que valorarlo en la moneda
    equivocada."""
    moneda = MONEDA_TICKER.get(ticker, "USD")
    if moneda == "USD":
        return serie
    par = PAR_FX_A_USD.get(moneda)
    if par is None:
        raise ValueError(f"No hay par FX configurado para {moneda}.")
    fx = descargar_con_reintentos(par, start=inicio, end=fin, auto_adjust=True)["Close"]
    if isinstance(fx, pd.DataFrame):
        fx = fx.iloc[:, 0]
    fx = fx.dropna()
    fx_alineado = fx.reindex(serie.index.union(fx.index)).ffill().bfill().reindex(serie.index)
    return serie / fx_alineado


# ------------------------------------------------------------------
# 1) OPERACIONES REALIZADAS (historial -> tabla plana)
# ------------------------------------------------------------------

def construir_tabla_operaciones(estado):
    """Aplana el historial semanal en una tabla: una fila por orden
    ejecutada, con fecha, ticker, cantidad, precio de compra y costo."""
    filas = []
    for entrada in estado.get("historial", []):
        fecha = entrada["fecha"]
        semana = entrada["semana"]
        for o in entrada.get("ordenes", []):
            filas.append({
                "semana": semana,
                "fecha": fecha,
                "ticker": o["ticker"],
                "cantidad": o["cantidad"],
                "precio_compra": o["precio_compra_referencia"],
                "costo": o["cantidad"] * o["precio_compra_referencia"],
            })
    if not filas:
        return pd.DataFrame(columns=["semana", "fecha", "ticker", "cantidad",
                                      "precio_compra", "costo"])
    tabla = pd.DataFrame(filas)
    tabla["fecha"] = pd.to_datetime(tabla["fecha"])
    return tabla.sort_values(["semana", "ticker"]).reset_index(drop=True)


# ------------------------------------------------------------------
# 2) EQUITY CURVE (patrimonio real dia a dia: efectivo + posiciones)
# ------------------------------------------------------------------

def construir_equity_curve(tabla_ops):
    """Reconstruye el patrimonio total (efectivo + valor de mercado de
    las posiciones) desde la primera operacion hasta hoy, usando precios
    HISTORICOS reales dia a dia (no solo el precio de compra), para que
    la curva refleje el valor de mercado real, no solo cuanto se gasto."""
    if tabla_ops.empty:
        raise ValueError("El historial esta vacio: no hay operaciones que graficar.")

    fecha_inicio = tabla_ops["fecha"].min()
    fecha_fin = datetime.today()

    tickers_operados = sorted(tabla_ops["ticker"].unique())
    print(f"Descargando historico de precios para {len(tickers_operados)} "
          f"tickers operados: {tickers_operados}")

    precios_por_ticker = {}
    for ticker in tickers_operados:
        try:
            datos = descargar_con_reintentos(
                ticker, start=fecha_inicio.strftime("%Y-%m-%d"),
                end=fecha_fin.strftime("%Y-%m-%d"), auto_adjust=True
            )["Close"]
            if isinstance(datos, pd.DataFrame):
                datos = datos.iloc[:, 0]
            datos = datos.dropna()
            datos = convertir_serie_a_usd(
                ticker, datos,
                fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d"),
            )
            precios_por_ticker[ticker] = datos.dropna()
        except Exception as e:
            print(f"  Aviso: no se pudo descargar precios de {ticker} ({e}). "
                  f"Se excluye del calculo de equity.")

    calendario = pd.bdate_range(fecha_inicio, fecha_fin)

    filas_equity = []
    for dia in calendario:
        ops_hasta_hoy = tabla_ops[tabla_ops["fecha"] <= dia]
        posiciones_dia = ops_hasta_hoy.groupby("ticker")["cantidad"].sum()
        efectivo_gastado = ops_hasta_hoy["costo"].sum()
        efectivo_disponible = CAPITAL_TOTAL - efectivo_gastado

        valor_posiciones = 0.0
        for ticker, cantidad in posiciones_dia.items():
            serie = precios_por_ticker.get(ticker)
            if serie is None or cantidad <= 0:
                continue
            precios_hasta_hoy = serie[serie.index <= dia]
            if len(precios_hasta_hoy) == 0:
                continue
            precio_dia = float(precios_hasta_hoy.iloc[-1])
            valor_posiciones += cantidad * precio_dia

        patrimonio_total = efectivo_disponible + valor_posiciones
        filas_equity.append({
            "fecha": dia,
            "efectivo": efectivo_disponible,
            "valor_posiciones": valor_posiciones,
            "patrimonio_total": patrimonio_total,
        })

    equity = pd.DataFrame(filas_equity).set_index("fecha")
    equity["pnl_absoluto"] = equity["patrimonio_total"] - CAPITAL_TOTAL
    equity["pnl_pct"] = equity["pnl_absoluto"] / CAPITAL_TOTAL * 100
    equity["maximo_historico"] = equity["patrimonio_total"].cummax()
    equity["drawdown_pct"] = (equity["patrimonio_total"] / equity["maximo_historico"] - 1) * 100
    return equity, precios_por_ticker


# ------------------------------------------------------------------
# 3) POSICIONES ABIERTAS ACTUALES (con P&L no realizado por ticker)
# ------------------------------------------------------------------

def construir_tabla_posiciones_actuales(estado, tabla_ops, precios_por_ticker):
    posiciones = estado.get("posiciones", {})
    filas = []
    for ticker, cantidad in posiciones.items():
        if cantidad <= 0:
            continue
        ops_ticker = tabla_ops[tabla_ops["ticker"] == ticker]
        costo_total = float(ops_ticker["costo"].sum())
        precio_prom_compra = (costo_total / ops_ticker["cantidad"].sum()
                               if len(ops_ticker) else np.nan)

        serie = precios_por_ticker.get(ticker)
        precio_actual = float(serie.dropna().iloc[-1]) if serie is not None and len(serie) else np.nan

        valor_actual = cantidad * precio_actual if not np.isnan(precio_actual) else np.nan
        pnl_no_realizado = valor_actual - costo_total if not np.isnan(valor_actual) else np.nan
        pnl_pct = (pnl_no_realizado / costo_total * 100) if costo_total else np.nan

        filas.append({
            "ticker": ticker, "cantidad": cantidad,
            "precio_promedio_compra": round(precio_prom_compra, 2),
            "precio_actual": round(precio_actual, 2) if not np.isnan(precio_actual) else None,
            "costo_total": round(costo_total, 2),
            "valor_actual": round(valor_actual, 2) if not np.isnan(valor_actual) else None,
            "pnl_no_realizado": round(pnl_no_realizado, 2) if not np.isnan(pnl_no_realizado) else None,
            "pnl_pct": round(pnl_pct, 2) if not np.isnan(pnl_pct) else None,
        })
    return pd.DataFrame(filas).sort_values("valor_actual", ascending=False, na_position="last")


# ------------------------------------------------------------------
# 4) METRICAS DE DESEMPEÑO PRINCIPALES
# ------------------------------------------------------------------

def calcular_metricas(estado, equity, tabla_ops):
    patrimonio_actual = equity["patrimonio_total"].iloc[-1]
    retorno_total_pct = (patrimonio_actual / CAPITAL_TOTAL - 1) * 100
    max_drawdown_pct = equity["drawdown_pct"].min()

    hit_rate_hist = estado.get("hit_rate_historico", [])
    hit_rate_promedio = float(np.mean(hit_rate_hist)) if hit_rate_hist else None

    semanas_operadas = tabla_ops["semana"].nunique() if not tabla_ops.empty else 0
    total_ordenes = len(tabla_ops)
    tickers_distintos = tabla_ops["ticker"].nunique() if not tabla_ops.empty else 0

    return {
        "patrimonio_actual": round(float(patrimonio_actual), 2),
        "capital_inicial": CAPITAL_TOTAL,
        "retorno_total_pct": round(float(retorno_total_pct), 2),
        "max_drawdown_pct": round(float(max_drawdown_pct), 2),
        "hit_rate_promedio_pct": round(hit_rate_promedio * 100, 1) if hit_rate_promedio is not None else None,
        "semanas_operadas": int(semanas_operadas),
        "total_ordenes_ejecutadas": int(total_ordenes),
        "tickers_distintos_operados": int(tickers_distintos),
        "circuit_breaker_activo": estado.get("circuit_breaker_activo", False),
    }


# ------------------------------------------------------------------
# 5) GRAFICOS (matplotlib -> PNG)
# ------------------------------------------------------------------

def generar_graficos(equity, tabla_ops, tabla_posiciones, carpeta=CARPETA_REPORTES):
    os.makedirs(carpeta, exist_ok=True)
    rutas = {}

    # --- Equity curve ---
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(equity.index, equity["patrimonio_total"], label="Patrimonio total", linewidth=2)
    ax.plot(equity.index, equity["efectivo"], label="Efectivo", linestyle="--", alpha=0.6)
    ax.axhline(CAPITAL_TOTAL, color="gray", linestyle=":", label="Capital inicial")
    ax.set_title("Equity Curve — CTA-003")
    ax.set_ylabel("USD")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))
    fig.autofmt_xdate()
    ruta = f"{carpeta}/equity_curve.png"
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    rutas["equity_curve"] = ruta

    # --- P&L acumulado ---
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(equity.index, equity["pnl_absoluto"], 0, color="seagreen", alpha=0.3)
    ax.plot(equity.index, equity["pnl_absoluto"], color="seagreen", linewidth=1.5)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("P&L Acumulado — CTA-003")
    ax.set_ylabel("USD")
    fig.autofmt_xdate()
    ruta = f"{carpeta}/pnl_acumulado.png"
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    rutas["pnl_acumulado"] = ruta

    # --- Posiciones abiertas (valor actual por ticker) ---
    if not tabla_posiciones.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(tabla_posiciones["ticker"], tabla_posiciones["valor_actual"])
        ax.set_title("Valor actual por posicion abierta")
        ax.set_ylabel("USD")
        plt.xticks(rotation=45, ha="right")
        ruta = f"{carpeta}/posiciones_abiertas.png"
        fig.savefig(ruta, dpi=150, bbox_inches="tight")
        plt.close(fig)
        rutas["posiciones_abiertas"] = ruta

    # --- Operaciones por semana ---
    if not tabla_ops.empty:
        ops_por_semana = tabla_ops.groupby("semana").size()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(ops_por_semana.index.astype(str), ops_por_semana.values)
        ax.set_title("Operaciones ejecutadas por semana")
        ax.set_xlabel("Semana")
        ax.set_ylabel("N° de ordenes")
        ruta = f"{carpeta}/operaciones_por_semana.png"
        fig.savefig(ruta, dpi=150, bbox_inches="tight")
        plt.close(fig)
        rutas["operaciones_por_semana"] = ruta

    return rutas


# ------------------------------------------------------------------
# 6) REPORTE FINAL (Markdown con graficos embebidos + tablas)
# ------------------------------------------------------------------

def generar_reporte_r3(archivo_estado=ARCHIVO_ESTADO):
    estado = cargar_estado(archivo_estado)
    tabla_ops = construir_tabla_operaciones(estado)
    equity, precios_por_ticker = construir_equity_curve(tabla_ops)
    tabla_posiciones = construir_tabla_posiciones_actuales(estado, tabla_ops, precios_por_ticker)
    metricas = calcular_metricas(estado, equity, tabla_ops)
    rutas_graficos = generar_graficos(equity, tabla_ops, tabla_posiciones)

    fecha_hoy = datetime.today().strftime("%Y-%m-%d")
    os.makedirs(CARPETA_REPORTES, exist_ok=True)
    ruta_md = f"{CARPETA_REPORTES}/reporte_r3_{fecha_hoy}.md"

    lineas = []
    lineas.append("# Reporte Visual de Desempeño — CTA-003 (R3, Sprint 8)")
    lineas.append("")
    lineas.append(f"**Generado el:** {fecha_hoy}")
    lineas.append("")

    lineas.append("## Métricas principales")
    lineas.append("")
    lineas.append(f"- Patrimonio actual: **${metricas['patrimonio_actual']:.2f}** "
                   f"(capital inicial: ${metricas['capital_inicial']:.2f})")
    lineas.append(f"- Retorno total: **{metricas['retorno_total_pct']:.2f}%**")
    lineas.append(f"- Máximo drawdown: **{metricas['max_drawdown_pct']:.2f}%**")
    if metricas["hit_rate_promedio_pct"] is not None:
        lineas.append(f"- Hit-rate promedio: **{metricas['hit_rate_promedio_pct']:.1f}%**")
    lineas.append(f"- Semanas operadas: **{metricas['semanas_operadas']}**")
    lineas.append(f"- Órdenes ejecutadas en total: **{metricas['total_ordenes_ejecutadas']}**")
    lineas.append(f"- Tickers distintos operados: **{metricas['tickers_distintos_operados']}**")
    lineas.append(f"- Circuit breaker: "
                   f"{'🔴 activo' if metricas['circuit_breaker_activo'] else '🟢 inactivo'}")
    lineas.append("")

    lineas.append("## Equity Curve")
    lineas.append("")
    lineas.append(f"![Equity Curve]({os.path.basename(rutas_graficos['equity_curve'])})")
    lineas.append("")

    lineas.append("## P&L Acumulado")
    lineas.append("")
    lineas.append(f"![P&L Acumulado]({os.path.basename(rutas_graficos['pnl_acumulado'])})")
    lineas.append("")

    if "posiciones_abiertas" in rutas_graficos:
        lineas.append("## Posiciones Abiertas")
        lineas.append("")
        lineas.append(f"![Posiciones Abiertas]({os.path.basename(rutas_graficos['posiciones_abiertas'])})")
        lineas.append("")
        try:
            lineas.append(tabla_posiciones.to_markdown(index=False))
        except ImportError:
            lineas.append(tabla_posiciones.to_string(index=False))
        lineas.append("")

    if "operaciones_por_semana" in rutas_graficos:
        lineas.append("## Operaciones Realizadas")
        lineas.append("")
        lineas.append(f"![Operaciones por semana]({os.path.basename(rutas_graficos['operaciones_por_semana'])})")
        lineas.append("")
        try:
            lineas.append(tabla_ops.to_markdown(index=False))
        except ImportError:
            lineas.append(tabla_ops.to_string(index=False))
        lineas.append("")

    with open(ruta_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"\nReporte R3 generado en: {ruta_md}")
    print(f"Gráficos guardados en: {CARPETA_REPORTES}/")
    return ruta_md, metricas


if __name__ == "__main__":
    generar_reporte_r3()
