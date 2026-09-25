# Informe Semanal — AI Trading Challenge (CTA-003)

**Fecha de la corrida:** 2026-09-25  
**Semana:** 4  
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
| 005930.KS |          209.54 |                 74.30 |                  16.36 |     -7.82 |     -19.56 |                     0.05 |
| GDX       |           92.35 |                 68.70 |                  10.56 |    -13.63 |     -25.37 |                     0.05 |
| TSM       |          451.15 |                 68.20 |                   8.46 |    -15.73 |     -27.47 |                     0.01 |
| NEM       |          121.30 |                 67.90 |                   7.11 |    -17.07 |     -28.81 |                     0.05 |
| 000660.KS |         1366.61 |                 58.40 |                  10.37 |    -13.81 |     -25.55 |                     0.09 |
| TRGP      |          283.15 |                 57.30 |                   7.09 |    -17.09 |     -28.83 |                     0.03 |
| QQQ       |          741.10 |                 57.00 |                   3.18 |    -21.01 |     -32.75 |                     0.03 |
| AAPL      |          335.92 |                 54.10 |                   2.08 |    -22.10 |     -33.84 |                     0.04 |
| NVDA      |          224.58 |                 51.40 |                  11.02 |    -13.17 |     -24.91 |                     0.04 |
| XLE       |           62.60 |                 45.60 |                   2.49 |    -21.69 |     -33.43 |                     0.05 |
| MRK       |          147.98 |                 44.40 |                   2.37 |    -21.81 |     -33.55 |                     0.02 |
| MSFT      |          497.93 |                 42.00 |                   2.20 |    -21.98 |     -33.72 |                     0.04 |
| BRK-B     |          505.18 |                 36.60 |                   2.20 |    -21.98 |     -33.72 |                     0.02 |
| SPY       |          767.18 |                 36.30 |                   1.69 |    -22.49 |     -34.23 |                     0.02 |
| KO        |           88.10 |                 34.30 |                   1.38 |    -22.80 |     -34.54 |                     0.03 |
| XLV       |          169.87 |                 26.80 |                   0.74 |    -23.45 |     -35.19 |                     0.04 |

## Log de seleccion (ranking + capa de riesgo + capa cualitativa)

- ✅ **005930.KS** — BUY: rank #1, prob=74.3%
- ✅ **GDX** — BUY: rank #2, prob=68.7%
- ✅ **TSM** — BUY: rank #3, prob=68.2%
- ✅ **NEM** — BUY: rank #4, prob=67.9%
- ✅ **000660.KS** — BUY: rank #5, prob=58.4%
- ✅ **TRGP** — BUY: rank #6, prob=57.3%
- ⛔ **QQQ** — DESCARTADO: cupo semanal ya lleno
- ⛔ **AAPL** — DESCARTADO: cupo semanal ya lleno
- ⛔ **NVDA** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLE** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MRK** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MSFT** — DESCARTADO: cupo semanal ya lleno
- ⛔ **BRK-B** — DESCARTADO: cupo semanal ya lleno
- ⛔ **SPY** — DESCARTADO: cupo semanal ya lleno
- ⛔ **KO** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLV** — DESCARTADO: cupo semanal ya lleno

## Guardrail cualitativo (RAG) — noticias revisadas

- **005930.KS**: Error en guardrail RAG ('NoneType' object has no attribute 'strip') - aprobado por defecto (fail-open).
- **000660.KS**: [RAG/openrouter] No se encontraron noticias materiales y negativas recientes (ej. fraude, investigación regulatoria grave, escándalo, etc.) que justifiquen vetar la compra.
- **TSM**: Error en guardrail RAG ('NoneType' object has no attribute 'strip') - aprobado por defecto (fail-open).
- **TRGP**: Error en guardrail RAG ('NoneType' object has no attribute 'strip') - aprobado por defecto (fail-open).
- **GDX**: Error en guardrail RAG (Expecting value: line 1 column 13 (char 12)) - aprobado por defecto (fail-open).
- **NEM**: Error en guardrail RAG ('NoneType' object has no attribute 'strip') - aprobado por defecto (fail-open).

## Seleccion final (BUY de esta semana)

*Ninguna posicion nueva esta semana.*

## Capital asignado

*No se ejecuto ninguna orden esta semana.*

**Capital disponible despues de esta semana:** $7140.68

## Bloque JSON generado

*No se genero bloque JSON esta semana (0 ordenes).*
