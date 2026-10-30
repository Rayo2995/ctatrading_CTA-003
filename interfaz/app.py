"""Interfaz de CTA-003 (Streamlit).

Solo LEE los archivos que ya genera el sistema (estado_portafolio.json,
backlog_decisiones_v6.csv, informes/ y reportes/). No ejecuta el modelo, no
envía correos y no necesita claves: es seguro dejarla pública.

Ejecutar en local (desde la raíz del repo):  streamlit run interfaz/app.py
"""
import io
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import streamlit as st

REPO = "Rayo2995/ctatrading_CTA-003"
RAMA = "main"
RAW = f"https://raw.githubusercontent.com/{REPO}/{RAMA}/"
API = f"https://api.github.com/repos/{REPO}/contents/"
RAIZ = Path(__file__).resolve().parent.parent  # raíz del repo

CAPITAL_INICIAL = 10_000.0
UMBRAL_CIRCUIT_BREAKER = -20.0  # % de caída desde el máximo
PERCENTIL_VETO_CVAR = 20        # se veta el 20 % con peor CVaR de la semana

st.set_page_config(page_title="CTA-003 · Panel", page_icon="📈", layout="wide")


# ----------------------------------------------------------------------
# Lectura de datos (local primero; si no existe, directo desde GitHub)
# ----------------------------------------------------------------------
@st.cache_data(ttl=300, show_spinner=False)
def leer_bytes(ruta: str):
    local = RAIZ / ruta
    if local.exists():
        return local.read_bytes(), "archivos del repositorio"
    resp = requests.get(RAW + ruta, timeout=15)
    resp.raise_for_status()
    return resp.content, "GitHub"


@st.cache_data(ttl=300, show_spinner=False)
def listar(carpeta: str):
    local = RAIZ / carpeta
    if local.is_dir():
        return sorted(p.name for p in local.iterdir())
    resp = requests.get(API + carpeta, timeout=15)
    resp.raise_for_status()
    return sorted(item["name"] for item in resp.json())


def texto(ruta: str) -> str:
    return leer_bytes(ruta)[0].decode("utf-8")


def cargar_datos():
    estado = json.loads(texto("estado_portafolio.json"))
    backlog = pd.read_csv(io.StringIO(texto("backlog_decisiones_v6.csv")))
    informes = [n for n in listar("informes") if n.endswith(".md")]
    reportes = [n for n in listar("reportes") if n.startswith("reporte_r3_") and n.endswith(".md")]
    return estado, backlog, informes, reportes


def info_informe(nombre: str):
    """('2026-10-23', 'OFICIAL') a partir de informe_2026-10-23_OFICIAL.md"""
    m = re.match(r"informe_(\d{4}-\d{2}-\d{2})_(\w+)\.md", nombre)
    return (m.group(1), m.group(2)) if m else (nombre, "?")


def partir_secciones(md: str):
    partes = re.split(r"^## ", md, flags=re.M)
    secciones = {}
    for parte in partes[1:]:
        titulo, _, cuerpo = parte.partition("\n")
        secciones[titulo.strip()] = cuerpo.strip()
    return partes[0], secciones


def buscar(secciones: dict, inicio: str):
    for titulo, cuerpo in secciones.items():
        if titulo.lower().startswith(inicio.lower()):
            return titulo, cuerpo
    return None, None


# ----------------------------------------------------------------------
# Cálculos del portafolio
# ----------------------------------------------------------------------
def calcular_portafolio(estado: dict, backlog: pd.DataFrame):
    precios = dict(zip(backlog["ticker"], backlog["precio_actual"]))
    # costo promedio por ticker (precios de compra ya en USD)
    costo, cantidad = {}, {}
    for semana in estado["historial"]:
        for orden in semana.get("ordenes", []):
            t = orden["ticker"]
            costo[t] = costo.get(t, 0.0) + orden["cantidad"] * orden["precio_compra_referencia"]
            cantidad[t] = cantidad.get(t, 0) + orden["cantidad"]

    filas = []
    for ticker, cant in estado["posiciones"].items():
        costo_prom = costo.get(ticker, 0.0) / cantidad[ticker] if cantidad.get(ticker) else np.nan
        precio = precios.get(ticker, costo_prom)
        valor = cant * precio
        filas.append({
            "Ticker": ticker, "Cantidad": cant, "Costo promedio": costo_prom,
            "Precio actual": precio, "Valor (USD)": valor,
            "P&L (USD)": valor - cant * costo_prom,
            "P&L (%)": (precio / costo_prom - 1) * 100,
        })
    posiciones = pd.DataFrame(filas)
    valor_posiciones = float(posiciones["Valor (USD)"].sum()) if len(posiciones) else 0.0
    efectivo = float(estado["capital_disponible"])
    patrimonio = efectivo + valor_posiciones
    maximo = max(float(estado["capital_maximo_historico"]), patrimonio)
    return {
        "posiciones": posiciones, "efectivo": efectivo, "patrimonio": patrimonio,
        "retorno": (patrimonio / CAPITAL_INICIAL - 1) * 100,
        "drawdown": (patrimonio / maximo - 1) * 100, "maximo": maximo,
    }


# ----------------------------------------------------------------------
# Carga
# ----------------------------------------------------------------------
try:
    estado, backlog, informes, reportes = cargar_datos()
except Exception as error:  # noqa: BLE001
    st.error(f"No se pudieron leer los datos del repositorio: {error}")
    st.stop()

fuente = leer_bytes("estado_portafolio.json")[1]
port = calcular_portafolio(estado, backlog)
ultimo_informe = informes[-1] if informes else None
fecha_ultima, _ = info_informe(ultimo_informe) if ultimo_informe else ("—", "")

# ----------------------------------------------------------------------
# Barra lateral
# ----------------------------------------------------------------------
with st.sidebar:
    st.title("📈 CTA-003")
    st.caption("Sistema automatizado de apoyo a la decisión de inversión · AI Trading Challenge")
    st.write(f"**Semana actual:** {estado['semana_actual']} de 13")
    st.write(f"**Última corrida:** {fecha_ultima}")
    st.caption(f"Datos leídos de: {fuente}. Se refrescan cada 5 minutos.")
    if st.button("🔄 Actualizar datos", width="stretch"):
        st.cache_data.clear()
        st.rerun()
    st.link_button("Repositorio en GitHub", f"https://github.com/{REPO}", width="stretch")
    st.link_button("Ver ejecuciones (Actions)", f"https://github.com/{REPO}/actions", width="stretch")
    st.divider()
    st.caption("Cuenta simulada. Esta interfaz solo muestra información; no ejecuta órdenes "
               "y no es asesoría financiera.")

st.title("Sistema de inversión CTA-003")

tab_panel, tab_ranking, tab_decision, tab_historial, tab_reportes, tab_info = st.tabs(
    ["📊 Panel", "🏁 Ranking", "🗓️ Decisión semanal", "📜 Historial", "🖼️ Reportes", "ℹ️ Cómo funciona"]
)

# ----------------------------------------------------------------------
# Panel
# ----------------------------------------------------------------------
with tab_panel:
    activo = bool(estado["circuit_breaker_activo"])
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Patrimonio", f"${port['patrimonio']:,.2f}", f"{port['patrimonio'] - CAPITAL_INICIAL:+,.2f} USD")
    c2.metric("Retorno total", f"{port['retorno']:+.2f} %")
    c3.metric("Drawdown vs. máximo", f"{port['drawdown']:.2f} %",
              help=f"El circuit breaker se activa si cae a {UMBRAL_CIRCUIT_BREAKER:.0f} % o menos.")
    c4.metric("Efectivo", f"${port['efectivo']:,.2f}")
    c5.metric("Circuit breaker", "🔴 ACTIVO" if activo else "🟢 Inactivo")

    margen = port["drawdown"] - UMBRAL_CIRCUIT_BREAKER
    st.progress(min(max(1 - margen / abs(UMBRAL_CIRCUIT_BREAKER), 0.0), 1.0),
                text=f"Distancia al circuit breaker: faltan {margen:.1f} puntos para llegar a "
                     f"{UMBRAL_CIRCUIT_BREAKER:.0f} %")

    st.subheader("Posiciones abiertas")
    if len(port["posiciones"]):
        st.dataframe(
            port["posiciones"].sort_values("Valor (USD)", ascending=False),
            hide_index=True, width="stretch",
            column_config={
                "Costo promedio": st.column_config.NumberColumn(format="$%.2f"),
                "Precio actual": st.column_config.NumberColumn(format="$%.2f"),
                "Valor (USD)": st.column_config.NumberColumn(format="$%.2f"),
                "P&L (USD)": st.column_config.NumberColumn(format="%+.2f"),
                "P&L (%)": st.column_config.NumberColumn(format="%+.2f %%"),
            },
        )
        distribucion = port["posiciones"].set_index("Ticker")["Valor (USD)"].copy()
        distribucion.loc["EFECTIVO"] = port["efectivo"]
        st.subheader("¿Dónde está el dinero?")
        st.bar_chart(distribucion.sort_values(ascending=False))
    else:
        st.info("Todavía no hay posiciones abiertas.")
    st.caption("Los precios son los de la última corrida del modelo, convertidos a USD "
               "(las acciones coreanas cotizan en wones).")

# ----------------------------------------------------------------------
# Ranking
# ----------------------------------------------------------------------
with tab_ranking:
    st.subheader("Evaluación del universo (última corrida)")
    corte = float(np.percentile(backlog["cvar_pct"], PERCENTIL_VETO_CVAR))
    ultimas_ordenes = next((s for s in reversed(estado["historial"]) if s.get("ordenes")), None)
    comprados = {o["ticker"] for o in ultimas_ordenes["ordenes"]} if ultimas_ordenes else set()

    tabla = backlog.sort_values("prob_supera_mediana", ascending=False).copy()
    tabla["Estado"] = np.where(
        tabla["ticker"].isin(comprados), "🟢 Comprado en la última orden",
        np.where(tabla["cvar_pct"] < corte, "🔴 Bajo el corte de CVaR", "—"),
    )
    tabla["stop_loss_pct"] = tabla["stop_loss_pct"] * 100
    tabla = tabla.rename(columns={
        "ticker": "Ticker", "precio_actual": "Precio (USD)",
        "prob_supera_mediana": "Prob. superar mediana (%)",
        "retorno_esperado_pct": "Retorno esperado (%)", "var_pct": "VaR 5 % (%)",
        "cvar_pct": "CVaR (%)", "incertidumbre_ensamble": "Incertidumbre",
        "ratio_retorno_riesgo_anual": "Ratio R/R anual", "stop_loss_pct": "Stop-loss (%)",
    })
    st.dataframe(
        tabla, hide_index=True, width="stretch",
        column_config={
            "Prob. superar mediana (%)": st.column_config.ProgressColumn(
                min_value=0, max_value=100, format="%.1f"),
            "Precio (USD)": st.column_config.NumberColumn(format="$%.2f"),
        },
    )
    st.caption(f"**CVaR relativo:** el corte de esta semana es el percentil {PERCENTIL_VETO_CVAR} de los CVaR "
               f"de los {len(backlog)} activos = **{corte:.1f} %**. Quien queda por debajo se veta (aquí se marca 🔴 aunque ya estuviera fuera del cupo por ranking). "
               "El estado 🟢 indica que el activo está en la última orden enviada.")
    st.bar_chart(backlog.set_index("ticker")["prob_supera_mediana"].sort_values(ascending=False),
                 y_label="Probabilidad de superar la mediana (%)")

# ----------------------------------------------------------------------
# Decisión semanal (informes)
# ----------------------------------------------------------------------
with tab_decision:
    incluir_pruebas = st.checkbox("Incluir corridas de prueba", value=False)
    opciones = [n for n in informes if incluir_pruebas or "OFICIAL" in n]
    if not opciones:
        opciones = informes
    if not opciones:
        st.info("Aún no hay informes en la carpeta informes/.")
    else:
        elegido = st.selectbox(
            "Informe", options=list(reversed(opciones)),
            format_func=lambda n: " · ".join(info_informe(n)) if n.endswith(".md") else n,
        )
        md = texto(f"informes/{elegido}")
        cabecera, secciones = partir_secciones(md)

        fecha_i, tipo_i = info_informe(elegido)
        semana = re.search(r"\*\*Semana:\*\*\s*(\d+)", cabecera)
        resultado = re.search(r"\*\*Resultado de esta corrida:\*\*\s*(.+)", cabecera)
        k1, k2, k3 = st.columns(3)
        k1.metric("Fecha de la corrida", fecha_i)
        k2.metric("Semana", semana.group(1) if semana else "—")
        k3.metric("Tipo", tipo_i)
        if resultado:
            st.info(resultado.group(1).strip())

        for inicio, abierto in [("Seleccion final", True), ("Capital asignado", True),
                                ("Guardrail cualitativo", True), ("Log de seleccion", False),
                                ("Guardrails", False), ("Estado del modelo", False),
                                ("Ranking del universo", False)]:
            titulo, cuerpo = buscar(secciones, inicio)
            if titulo:
                with st.expander(titulo, expanded=abierto):
                    st.markdown(cuerpo)

        titulo_json, cuerpo_json = buscar(secciones, "Bloque JSON")
        if cuerpo_json:
            hallado = re.search(r"```(?:json)?\s*(.*?)```", cuerpo_json, re.S)
            with st.expander("Bloque JSON de órdenes", expanded=False):
                try:
                    st.json(json.loads(hallado.group(1))) if hallado else st.markdown(cuerpo_json)
                except json.JSONDecodeError:
                    st.code(hallado.group(1) if hallado else cuerpo_json)

# ----------------------------------------------------------------------
# Historial
# ----------------------------------------------------------------------
with tab_historial:
    st.subheader("Compras por semana")
    filas, detalle = [], {}
    for semana in estado["historial"]:
        ordenes = semana.get("ordenes", [])
        if not ordenes:
            continue
        invertido = sum(o["cantidad"] * o["precio_compra_referencia"] for o in ordenes)
        filas.append({"Semana": semana["semana"], "Fecha": semana["fecha"],
                      "Órdenes": len(ordenes), "Invertido (USD)": invertido,
                      "Evaluada en hit-rate": "Sí" if semana.get("evaluado_hit_rate") else "No"})
        detalle[semana["semana"]] = pd.DataFrame(ordenes).rename(columns={
            "ticker": "Ticker", "cantidad": "Cantidad",
            "precio_compra_referencia": "Precio de compra (USD)"})
    if filas:
        resumen = pd.DataFrame(filas)
        st.dataframe(resumen, hide_index=True, width="stretch",
                     column_config={"Invertido (USD)": st.column_config.NumberColumn(format="$%.2f")})
        st.bar_chart(resumen.set_index("Semana")["Invertido (USD)"])
        for fila in filas:
            with st.expander(f"Semana {fila['Semana']} · {fila['Fecha']}"):
                st.dataframe(detalle[fila["Semana"]], hide_index=True, width="stretch")
    else:
        st.info("Todavía no hay compras registradas.")

    sin_ordenes = [s["semana"] for s in estado["historial"] if not s.get("ordenes")]
    if sin_ordenes:
        st.caption(f"Semanas sin órdenes: {', '.join(str(s) for s in sin_ordenes)} "
                   "(corridas de prueba antiguas o con el circuit breaker activo por el error de moneda ya corregido).")

    st.subheader("Monitor de hit-rate")
    if estado["hit_rate_historico"]:
        st.line_chart(pd.Series(estado["hit_rate_historico"], name="Hit-rate"))
    else:
        st.info("Aún no hay semanas evaluadas: cada compra se evalúa 42 días después. "
                "La alerta se activa si el promedio de las últimas 6 semanas baja de 40 %.")

# ----------------------------------------------------------------------
# Reportes
# ----------------------------------------------------------------------
with tab_reportes:
    if reportes:
        ultimo = reportes[-1]
        md_reporte = texto(f"reportes/{ultimo}")
        st.caption(f"Reporte visual más reciente: {ultimo}")
        metricas = re.search(r"## Métricas principales\s*(.*?)\n## ", md_reporte, re.S)
        if metricas:
            st.markdown(metricas.group(1).strip())
        imagenes = [("equity_curve.png", "Curva de patrimonio"), ("pnl_acumulado.png", "P&L acumulado"),
                    ("posiciones_abiertas.png", "Posiciones abiertas"),
                    ("operaciones_por_semana.png", "Operaciones por semana")]
        col_a, col_b = st.columns(2)
        for i, (archivo, titulo) in enumerate(imagenes):
            try:
                (col_a if i % 2 == 0 else col_b).image(leer_bytes(f"reportes/{archivo}")[0],
                                                        caption=titulo, width="stretch")
            except Exception:  # noqa: BLE001
                (col_a if i % 2 == 0 else col_b).warning(f"No se pudo cargar {archivo}")
        st.caption("Las imágenes se sobrescriben en cada corrida: siempre muestran el último estado.")
    else:
        st.info("Aún no hay reportes visuales.")

# ----------------------------------------------------------------------
# Cómo funciona
# ----------------------------------------------------------------------
with tab_info:
    st.markdown(
        """
### Flujo semanal
1. **Datos:** 16 activos (acciones y ETFs) desde 2023, con yfinance. Los precios coreanos se convierten de wones a USD.
2. **Ensamble XGBoost:** 5 clasificadores + 5 regresores (150 árboles, profundidad 4) estiman la probabilidad de superar la mediana del grupo y el retorno esperado a 30 sesiones. Se reentrena cada 21 días.
3. **Selección:** ranking por probabilidad y cuatro filtros en orden: cupo de 6 posiciones, piso de retorno (-5 %), veto por CVaR relativo (peor 20 %) y veto cualitativo con un LLM que lee noticias (Finnhub / Google News + OpenRouter).
4. **Capital:** 35 % del efectivo, repartido por ratio retorno/riesgo, máximo 25 % del presupuesto por posición y solo acciones enteras.
5. **Protecciones:** circuit breaker (-20 % de patrimonio desde el máximo), monitor de hit-rate (alerta bajo 40 %) y validación del JSON.
6. **Salida:** correo con las órdenes en JSON, informe semanal y reporte visual.

### Automatización
Dos workflows de GitHub Actions: la **corrida semanal** (viernes 13:00 UTC = 8:00 a. m. en Bogotá) y el **reporte visual**, que se dispara al terminar la primera.
Las corridas manuales son de prueba por defecto: no envían correo ni guardan estado.
        """
    )
    st.warning("Cuenta simulada. Los resultados pasados no garantizan resultados futuros.")
