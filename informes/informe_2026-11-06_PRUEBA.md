# Informe Semanal — AI Trading Challenge (CTA-003)

**Fecha de la corrida:** 2026-11-06  
**Semana:** 11  
**Resultado de esta corrida:** ⚪ Sin ordenes esta semana (0 candidatos seleccionados) - no se genero ni envio JSON.  

## Estado del modelo (ensamble)

- Fecha de entrenamiento del ensamble usado: **2026-10-30**
- Numero de modelos en el ensamble: **5**
- Hit-rate movil (ultimas 1 semanas evaluables): **25.0%**

## Guardrails

- Patrimonio total al momento de la corrida (efectivo + posiciones): **$9,468.20** (maximo historico: $10,199.86)
- Drawdown actual vs. maximo historico: **-7.2%** (umbral circuit breaker: -20.0%)
- Circuit breaker: 🟢 inactivo

## Ranking del universo evaluado esta semana

| ticker    |   precio_actual |   prob_supera_mediana |   retorno_esperado_pct |   var_pct |   cvar_pct |   incertidumbre_ensamble |
|:----------|----------------:|----------------------:|-----------------------:|----------:|-----------:|-------------------------:|
| 000660.KS |          943.23 |                 90.80 |                  30.00 |      4.61 |      -7.44 |                     0.03 |
| QQQ       |          647.05 |                 75.20 |                  10.16 |    -15.23 |     -27.28 |                     0.04 |
| SPY       |          733.00 |                 68.80 |                   4.00 |    -21.38 |     -33.44 |                     0.06 |
| BRK-B     |          572.33 |                 64.30 |                   3.70 |    -21.68 |     -33.74 |                     0.05 |
| TSM       |          353.10 |                 63.10 |                   8.15 |    -17.23 |     -29.29 |                     0.06 |
| NVDA      |          181.60 |                 58.00 |                  13.73 |    -11.66 |     -23.71 |                     0.05 |
| AAPL      |          344.17 |                 53.80 |                   5.07 |    -20.32 |     -32.38 |                     0.02 |
| GDX       |           85.75 |                 50.90 |                   6.91 |    -18.48 |     -30.53 |                     0.05 |
| MSFT      |          535.93 |                 50.10 |                   5.55 |    -19.84 |     -31.89 |                     0.05 |
| XLV       |          184.91 |                 47.50 |                   2.23 |    -23.16 |     -35.21 |                     0.04 |
| TRGP      |          271.82 |                 45.40 |                   8.16 |    -17.22 |     -29.28 |                     0.03 |
| 005930.KS |          150.37 |                 45.20 |                   0.01 |    -25.37 |     -37.43 |                     0.14 |
| KO        |           95.73 |                 43.20 |                   1.95 |    -23.44 |     -35.49 |                     0.04 |
| XLE       |           61.63 |                 38.90 |                   4.04 |    -21.35 |     -33.40 |                     0.07 |
| MRK       |          146.94 |                 34.10 |                   3.75 |    -21.63 |     -33.69 |                     0.04 |
| NEM       |          119.71 |                 29.20 |                   2.04 |    -23.35 |     -35.40 |                     0.04 |

## Log de seleccion (ranking + capa de riesgo + capa cualitativa)

- ✅ **000660.KS** — BUY: rank #1, prob=90.8%
- ✅ **QQQ** — BUY: rank #2, prob=75.2%
- ✅ **SPY** — BUY: rank #3, prob=68.8%
- ✅ **BRK-B** — BUY: rank #4, prob=64.3%
- ✅ **TSM** — BUY: rank #5, prob=63.1%
- ⛔ **NVDA** — DESCARTADO (capa cualitativa): [RAG/openrouter] El reciente AI selloff borró $450 bn de valor de NVIDIA y dejó fuera a su CEO de la lista de los 10 más ricos, indicando una amenaza material.
- ✅ **AAPL** — BUY: rank #6, prob=53.8%
- ⛔ **GDX** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MSFT** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLV** — DESCARTADO: cupo semanal ya lleno
- ⛔ **TRGP** — DESCARTADO: cupo semanal ya lleno
- ⛔ **005930.KS** — DESCARTADO: cupo semanal ya lleno
- ⛔ **KO** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLE** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MRK** — DESCARTADO: cupo semanal ya lleno
- ⛔ **NEM** — DESCARTADO: cupo semanal ya lleno

## Guardrail cualitativo (RAG) — noticias revisadas

- **SPY**: [RAG/openrouter] Las noticias son comentarios generales de mercado y rebalanceo normal del ETF; no hay eventos materiales negativos especificos de SPY (fraude, investigacion regulatoria, quiebra, escandalo grave).
- **QQQ**: [RAG/openrouter] No hay noticias negativas graves específicas sobre QQQ en los últimos 7 días.
- **BRK-B**: [RAG/openrouter] No hay noticias materiales negativas sobre BRK-B en los últimos 7 días
- **AAPL**: [RAG/openrouter] No se detecta una noticia material y negativa reciente que justifique rechazar la compra de AAPL esta semana; las noticias son principalmente ruido de mercado e IA.
- **NVDA**: [RAG/openrouter] El reciente AI selloff borró $450 bn de valor de NVIDIA y dejó fuera a su CEO de la lista de los 10 más ricos, indicando una amenaza material.
- **000660.KS**: [RAG/openrouter] No hay noticias recientes serias y específicas sobre Samsung que afecten directamente el valor del activo.
- **TSM**: [RAG/openrouter] No hay noticias materialmente negativas que justifiquen evitar la compra esta semana.

## Seleccion final (BUY de esta semana)

- **SPY** — precio $733.00, prob. supera mediana: 68.8%, CVaR: -33.4%
- **QQQ** — precio $647.05, prob. supera mediana: 75.2%, CVaR: -27.3%
- **BRK-B** — precio $572.33, prob. supera mediana: 64.3%, CVaR: -33.7%
- **AAPL** — precio $344.17, prob. supera mediana: 53.8%, CVaR: -32.4%
- **000660.KS** — precio $943.23, prob. supera mediana: 90.8%, CVaR: -7.4%
- **TSM** — precio $353.10, prob. supera mediana: 63.1%, CVaR: -29.3%

## Capital asignado

*No se ejecuto ninguna orden esta semana.*

**Capital disponible despues de esta semana:** $2646.86

## Bloque JSON generado

*No se genero bloque JSON esta semana (0 ordenes).*
