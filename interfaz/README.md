# Interfaz de CTA-003 (Streamlit)

Panel web de solo lectura. Muestra el patrimonio, las posiciones, el ranking del modelo,
las decisiones semanales (informes), el historial de compras y los reportes visuales.
**No ejecuta el modelo, no envía correos y no necesita claves.**

## Ejecutar en local
Desde la **raíz del repo** (importante: así las rutas coinciden con las de la nube):

    pip install -r interfaz/requirements.txt
    streamlit run interfaz/app.py

## Desplegar gratis (Streamlit Community Cloud)
1. Sube la carpeta `interfaz/` al repositorio (rama `main`).
2. Entra a https://share.streamlit.io con tu cuenta de GitHub y elige **Create app**.
3. Repositorio `Rayo2995/ctatrading_CTA-003`, rama `main`, archivo principal `interfaz/app.py`.
4. **Deploy**. La primera construcción tarda entre 1 y 3 minutos.

El `requirements.txt` de esta carpeta tiene prioridad sobre el de la raíz, así que no se
instalan xgboost ni scikit-learn.

## De dónde salen los datos
`estado_portafolio.json`, `backlog_decisiones_v6.csv`, `informes/` y `reportes/`.
La app lee primero los archivos del repositorio y, si no los encuentra, los descarga de GitHub.
Los datos se guardan en caché 5 minutos; el botón **Actualizar datos** los vuelve a leer.

## Notas
- Los precios son los de la última corrida del modelo (no en tiempo real).
- "Drawdown vs. máximo" compara el patrimonio actual con el máximo registrado; el reporte visual
  muestra otra métrica (el máximo drawdown de toda la curva), por eso pueden diferir un poco.
