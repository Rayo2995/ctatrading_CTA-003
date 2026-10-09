# Informe Semanal — AI Trading Challenge (CTA-003)

**Fecha de la corrida:** 2026-10-09  
**Semana:** 7  
**Resultado de esta corrida:** ⚪ Sin ordenes esta semana (0 candidatos seleccionados) - no se genero ni envio JSON.  

## Estado del modelo (ensamble)

- Fecha de entrenamiento del ensamble usado: **2026-10-09**
- Numero de modelos en el ensamble: **5**

## Guardrails

- Drawdown actual vs. maximo historico: **-99.4%** (umbral circuit breaker: -20.0%)
- Circuit breaker: 🔴 **ACTIVO** (todas las compras pausadas)

## Ranking del universo evaluado esta semana

| ticker    |   precio_actual |   prob_supera_mediana |   retorno_esperado_pct |   var_pct |   cvar_pct |   incertidumbre_ensamble |
|:----------|----------------:|----------------------:|-----------------------:|----------:|-----------:|-------------------------:|
| 000660.KS |         1255.34 |                 70.70 |                   9.47 |    -13.27 |     -24.31 |                     0.07 |
| TSM       |          457.99 |                 68.60 |                   7.34 |    -15.40 |     -26.44 |                     0.03 |
| 005930.KS |          195.66 |                 58.90 |                  13.05 |     -9.69 |     -20.73 |                     0.05 |
| NEM       |          115.55 |                 58.80 |                   3.47 |    -19.27 |     -30.31 |                     0.03 |
| GDX       |           86.72 |                 55.30 |                   6.09 |    -16.65 |     -27.69 |                     0.03 |
| NVDA      |          230.48 |                 54.10 |                  12.77 |     -9.97 |     -21.01 |                     0.02 |
| TRGP      |          288.49 |                 52.60 |                   5.33 |    -17.41 |     -28.45 |                     0.07 |
| AAPL      |          340.42 |                 51.50 |                   2.22 |    -20.52 |     -31.56 |                     0.02 |
| QQQ       |          747.58 |                 50.60 |                   2.34 |    -20.40 |     -31.44 |                     0.04 |
| XLE       |           65.24 |                 44.00 |                   1.73 |    -21.01 |     -32.05 |                     0.02 |
| BRK-B     |          511.05 |                 38.80 |                   1.71 |    -21.04 |     -32.08 |                     0.03 |
| MSFT      |          522.61 |                 36.60 |                   1.20 |    -21.54 |     -32.58 |                     0.02 |
| KO        |           87.77 |                 36.50 |                   1.90 |    -20.84 |     -31.88 |                     0.05 |
| MRK       |          142.38 |                 35.40 |                   1.39 |    -21.35 |     -32.39 |                     0.04 |
| XLV       |          168.16 |                 31.90 |                   0.66 |    -22.08 |     -33.12 |                     0.03 |
| SPY       |          773.93 |                 29.60 |                   1.26 |    -21.48 |     -32.52 |                     0.01 |

## Log de seleccion (ranking + capa de riesgo + capa cualitativa)

- ✅ **000660.KS** — BUY: rank #1, prob=70.7%
- ✅ **TSM** — BUY: rank #2, prob=68.6%
- ✅ **005930.KS** — BUY: rank #3, prob=58.9%
- ✅ **NEM** — BUY: rank #4, prob=58.8%
- ✅ **GDX** — BUY: rank #5, prob=55.3%
- ✅ **NVDA** — BUY: rank #6, prob=54.1%
- ⛔ **TRGP** — DESCARTADO: cupo semanal ya lleno
- ⛔ **AAPL** — DESCARTADO: cupo semanal ya lleno
- ⛔ **QQQ** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLE** — DESCARTADO: cupo semanal ya lleno
- ⛔ **BRK-B** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MSFT** — DESCARTADO: cupo semanal ya lleno
- ⛔ **KO** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MRK** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLV** — DESCARTADO: cupo semanal ya lleno
- ⛔ **SPY** — DESCARTADO: cupo semanal ya lleno

## Guardrail cualitativo (RAG) — noticias revisadas

- **NVDA**: Sin noticias recientes para NVDA en los ultimos 7 dias - aprobado por defecto.
- **005930.KS**: Sin noticias recientes para 005930.KS en los ultimos 7 dias - aprobado por defecto.
- **000660.KS**: Sin noticias recientes para 000660.KS en los ultimos 7 dias - aprobado por defecto.
- **TSM**: Sin noticias recientes para TSM en los ultimos 7 dias - aprobado por defecto.
- **GDX**: Sin noticias recientes para GDX en los ultimos 7 dias - aprobado por defecto.
- **NEM**: Sin noticias recientes para NEM en los ultimos 7 dias - aprobado por defecto.

## Seleccion final (BUY de esta semana)

*Ninguna posicion nueva esta semana.*

## Capital asignado

*No se ejecuto ninguna orden esta semana.*

**Capital disponible despues de esta semana:** $7140.68

## Bloque JSON generado

*No se genero bloque JSON esta semana (0 ordenes).*
