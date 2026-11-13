#!/usr/bin/env python3
"""
generar_puntajes_v6.py - Puntajes fuera de muestra del modelo v6 (Moisés y Rayo)
para la prueba común (comparar_modelos.py).

Va en la raíz del repo ctatrading_CTA-003, junto a modelo_v6.py, y REUTILIZA
sus funciones (features, target relativo, entrenamiento del ensamble y
predicción), así se evalúa el modelo tal como está, sin reescribirlo.

Walk-forward:
  - Cada viernes D (desde --inicio) se predice con un ensamble entrenado SOLO
    con filas cuya etiqueta a DIAS_PROYECTADOS (30 días hábiles) ya terminó
    antes o en D. Nada posterior a D entra al entrenamiento.
  - Se reentrena cada SEMANAS_ENTRE_REENTRENOS (3) semanas, como en producción.
  - No incluye CVaR, filtros de riesgo ni el veto RAG: la prueba mide solo
    el ranking.

Salidas (formato de la guía, sección 4):
  puntajes_v6_prob.csv      puntaje = probabilidad promedio de superar la mediana
  puntajes_v6_retorno.csv   puntaje = retorno esperado promedio (opcional)
  precios_comunes.csv       cierre diario ajustado, en USD (coreanas convertidas
                            con el tipo de cambio HISTÓRICO de cada día)

Uso:
  python generar_puntajes_v6.py
  python generar_puntajes_v6.py --inicio 2024-01-05 --semilla 42
  for s in 42 43 44 45 46; do python generar_puntajes_v6.py --semilla $s --sufijo _s$s; done
"""
import argparse
import contextlib
import io

import numpy as np
import pandas as pd

import modelo_v6 as m


def descargar_series():
    series = {}
    for t in m.TICKERS:
        try:
            series[t] = m.obtener_serie_close(t)
        except Exception as e:
            print(f"  Se excluye {t}: {e}")
    return series


def precios_en_usd(series):
    """Cierres diarios en USD. Usa el tipo de cambio de cada día, no el último."""
    fx = {}
    for moneda in {m.MONEDA_TICKER[t] for t in series if t in m.MONEDA_TICKER}:
        par = m.PAR_FX_A_USD[moneda]
        s = m.descargar_con_reintentos(par, start=m.FECHA_INICIO, end=m.FECHA_FIN, auto_adjust=True)["Close"]
        if isinstance(s, pd.DataFrame):
            s = s.iloc[:, 0]
        fx[moneda] = s.dropna()
    filas = []
    for t, p in series.items():
        moneda = m.MONEDA_TICKER.get(t, "USD")
        if moneda != "USD":
            tasa = fx[moneda].reindex(p.index, method="ffill")  # KRW=X = wones por dólar
            p = (p / tasa).dropna()
        filas.append(pd.DataFrame({"fecha": p.index, "ticker": t, "cierre": p.values}))
    return pd.concat(filas, ignore_index=True)


def construir_pool(series, categorias):
    """Features (todas miran hacia atrás) + target crudo + fecha en que termina la etiqueta."""
    bloques = []
    for t, p in series.items():
        f = m.calcular_features(p)
        f["target_ret_fwd"] = p.shift(-m.DIAS_PROYECTADOS) / p - 1
        f["fin_etiqueta"] = pd.Series(p.index, index=p.index).shift(-m.DIAS_PROYECTADOS)
        f["ticker"] = t
        f["fecha"] = f.index
        bloques.append(f)
    pool = pd.concat(bloques, ignore_index=True)
    pool["ticker"] = pd.Categorical(pool["ticker"], categories=categorias)
    return pool


def pool_hasta(pool, D):
    """Filas hasta D. La etiqueta solo existe si su ventana de 30 días ya terminó en D."""
    p = pool[pool["fecha"] <= D].copy()
    p.loc[~(p["fin_etiqueta"] <= D), "target_ret_fwd"] = np.nan
    return m.agregar_target_relativo(p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inicio", default="2024-01-05", help="primer viernes a puntuar")
    ap.add_argument("--semilla", type=int, default=m.SEMILLA_BASE)
    ap.add_argument("--sufijo", default="")
    ap.add_argument("--min-filas", type=int, default=2000, help="filas mínimas de entrenamiento")
    a = ap.parse_args()
    m.SEMILLA_BASE = a.semilla  # entrenar_ensamble lee esta variable global

    print("Descargando precios...")
    series = descargar_series()
    precios_en_usd(series).to_csv(f"precios_comunes{a.sufijo}.csv", index=False)

    categorias = sorted(series)
    pool = construir_pool(series, categorias)

    # Nunca se puntúa el día de hoy: si se corre un viernes, el cierre puede estar incompleto.
    ayer = pd.Timestamp.today().normalize() - pd.Timedelta(days=1)
    ultimo_dia = min(min(p.index.max() for p in series.values()), ayer)
    viernes = pd.date_range(a.inicio, ultimo_dia, freq="W-FRI")
    version = f"v6_wf_s{a.semilla}"
    filas, ensamble, ultimo_reentreno, corte = [], None, None, None

    for D in viernes:
        p = pool_hasta(pool, D)
        reentrenar = ensamble is None or (D - ultimo_reentreno).days >= m.SEMANAS_ENTRE_REENTRENOS * 7
        if reentrenar:
            entreno = p.dropna(subset=m.FEATURE_COLS + ["target_ret_fwd", "label_supera_mediana"])
            if len(entreno) < a.min_filas:
                print(f"{D.date()}: solo {len(entreno)} filas de entrenamiento, se omite.")
                continue
            with contextlib.redirect_stdout(io.StringIO()):  # silencia los prints del ensamble
                ensamble = m.entrenar_ensamble(p)
            ultimo_reentreno, corte = D, entreno["fecha"].max()
            assert entreno["fin_etiqueta"].max() <= D, "fuga: una etiqueta termina después de D"
            print(f"{D.date()}: reentrenado con {len(entreno)} filas (última fila de entrenamiento {corte.date()}).")

        for t in categorias:
            ft = p[p["ticker"] == t]
            if ft.empty:
                continue
            fila = ft.iloc[[-1]]
            if (D - fila["fecha"].iloc[0]).days > 4 or fila[m.FEATURE_COLS].isna().any(axis=None):
                print(f"  {D.date()} {t}: sin dato de esa semana, se omite.")
                continue
            prob, ret, _ = m.predecir_ensamble(ensamble, fila[m.FEATURE_COLS + ["ticker"]])
            filas.append((D.date(), t, prob, ret, corte.date()))

    out = pd.DataFrame(filas, columns=["fecha", "ticker", "prob", "ret", "fecha_corte_entrenamiento"])
    for col, nombre in (("prob", "prob"), ("ret", "retorno")):
        d = out[["fecha", "ticker", col, "fecha_corte_entrenamiento"]].rename(columns={col: "puntaje"})
        d["version_modelo"] = f"{version}_{nombre}"
        d.to_csv(f"puntajes_v6_{nombre}{a.sufijo}.csv", index=False)
    semanas = out["fecha"].nunique()
    print(f"\nListo: {semanas} semanas, {out['ticker'].nunique()} activos. "
          f"Archivos: puntajes_v6_prob{a.sufijo}.csv, puntajes_v6_retorno{a.sufijo}.csv, precios_comunes{a.sufijo}.csv")


if __name__ == "__main__":
    main()
