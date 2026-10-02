# Informe Semanal — AI Trading Challenge (CTA-003)

**Fecha de la corrida:** 2026-10-02  
**Semana:** 6  
**Resultado de esta corrida:** ⚪ Sin ordenes esta semana (0 candidatos seleccionados) - no se genero ni envio JSON.  

## Estado del modelo (ensamble)

- Fecha de entrenamiento del ensamble usado: **2026-09-18**
- Numero de modelos en el ensamble: **5**

## Guardrails

- Drawdown actual vs. maximo historico: **-99.4%** (umbral circuit breaker: -20.0%)
- Circuit breaker: 🔴 **ACTIVO** (todas las compras pausadas)

## Ranking del universo evaluado esta semana

| ticker    |   precio_actual |   prob_supera_mediana |   retorno_esperado_pct |   var_pct |   cvar_pct |   incertidumbre_ensamble |
|:----------|----------------:|----------------------:|-----------------------:|----------:|-----------:|-------------------------:|
| TSM       |          459.20 |                 73.00 |                   7.54 |    -16.64 |     -28.38 |                     0.05 |
| 005930.KS |          203.41 |                 56.90 |                  16.24 |     -7.95 |     -19.69 |                     0.06 |
| NVDA      |          230.86 |                 56.10 |                  12.24 |    -11.95 |     -23.69 |                     0.04 |
| QQQ       |          742.03 |                 54.50 |                   2.85 |    -21.33 |     -33.07 |                     0.02 |
| GDX       |           86.74 |                 53.70 |                   6.33 |    -17.86 |     -29.60 |                     0.10 |
| AAPL      |          330.32 |                 51.30 |                   2.82 |    -21.36 |     -33.10 |                     0.05 |
| 000660.KS |         1350.93 |                 49.70 |                   6.48 |    -17.70 |     -29.44 |                     0.05 |
| NEM       |          114.67 |                 48.10 |                   2.37 |    -21.81 |     -33.55 |                     0.01 |
| XLE       |           62.70 |                 47.50 |                   2.42 |    -21.76 |     -33.50 |                     0.06 |
| TRGP      |          279.31 |                 47.00 |                   4.75 |    -19.43 |     -31.17 |                     0.02 |
| MRK       |          143.81 |                 40.00 |                   1.69 |    -22.50 |     -34.24 |                     0.05 |
| MSFT      |          512.80 |                 39.90 |                   1.64 |    -22.54 |     -34.28 |                     0.04 |
| BRK-B     |          500.50 |                 38.60 |                   1.93 |    -22.25 |     -33.99 |                     0.01 |
| KO        |           86.10 |                 33.20 |                   1.19 |    -22.99 |     -34.73 |                     0.05 |
| SPY       |          763.99 |                 29.70 |                   1.69 |    -22.49 |     -34.23 |                     0.02 |
| XLV       |          166.20 |                 29.40 |                   0.82 |    -23.36 |     -35.10 |                     0.04 |

## Log de seleccion (ranking + capa de riesgo + capa cualitativa)

- ✅ **TSM** — BUY: rank #1, prob=73.0%
- ✅ **005930.KS** — BUY: rank #2, prob=56.9%
- ✅ **NVDA** — BUY: rank #3, prob=56.1%
- ✅ **QQQ** — BUY: rank #4, prob=54.5%
- ✅ **GDX** — BUY: rank #5, prob=53.7%
- ✅ **AAPL** — BUY: rank #6, prob=51.3%
- ⛔ **000660.KS** — DESCARTADO: cupo semanal ya lleno
- ⛔ **NEM** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLE** — DESCARTADO: cupo semanal ya lleno
- ⛔ **TRGP** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MRK** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MSFT** — DESCARTADO: cupo semanal ya lleno
- ⛔ **BRK-B** — DESCARTADO: cupo semanal ya lleno
- ⛔ **KO** — DESCARTADO: cupo semanal ya lleno
- ⛔ **SPY** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLV** — DESCARTADO: cupo semanal ya lleno

## Guardrail cualitativo (RAG) — noticias revisadas

- **QQQ**: Sin noticias recientes para QQQ en los ultimos 7 dias - aprobado por defecto.
- **AAPL**: Sin noticias recientes para AAPL en los ultimos 7 dias - aprobado por defecto.
- **NVDA**: Sin noticias recientes para NVDA en los ultimos 7 dias - aprobado por defecto.
- **005930.KS**: Sin noticias recientes para 005930.KS en los ultimos 7 dias - aprobado por defecto.
- **TSM**: Sin noticias recientes para TSM en los ultimos 7 dias - aprobado por defecto.
- **GDX**: Sin noticias recientes para GDX en los ultimos 7 dias - aprobado por defecto.

## Seleccion final (BUY de esta semana)

*Ninguna posicion nueva esta semana.*

## Capital asignado

*No se ejecuto ninguna orden esta semana.*

**Capital disponible despues de esta semana:** $7140.68

## Bloque JSON generado

*No se genero bloque JSON esta semana (0 ordenes).*
