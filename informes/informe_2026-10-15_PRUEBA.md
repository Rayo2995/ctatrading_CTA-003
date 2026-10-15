# Informe Semanal — AI Trading Challenge (CTA-003)

**Fecha de la corrida:** 2026-10-15  
**Semana:** 8  
**Resultado de esta corrida:** 🧪 Corrida de prueba - JSON valido, pero no se envio nada (por diseño).  

## Estado del modelo (ensamble)

- Fecha de entrenamiento del ensamble usado: **2026-10-09**
- Numero de modelos en el ensamble: **5**

## Guardrails

- Drawdown actual vs. maximo historico: **-54.1%** (umbral circuit breaker: -20.0%)
- Circuit breaker: 🟢 inactivo

## Ranking del universo evaluado esta semana

| ticker    |   precio_actual |   prob_supera_mediana |   retorno_esperado_pct |   var_pct |   cvar_pct |   incertidumbre_ensamble |
|:----------|----------------:|----------------------:|-----------------------:|----------:|-----------:|-------------------------:|
| TSM       |          430.00 |                 67.60 |                   6.54 |    -16.20 |     -27.24 |                     0.04 |
| NEM       |          111.56 |                 56.00 |                   3.69 |    -19.05 |     -30.09 |                     0.04 |
| GDX       |           83.40 |                 55.60 |                   7.98 |    -14.76 |     -25.80 |                     0.01 |
| AAPL      |          342.96 |                 51.00 |                   1.57 |    -21.18 |     -32.22 |                     0.04 |
| QQQ       |          728.95 |                 50.80 |                   2.64 |    -20.10 |     -31.14 |                     0.05 |
| XLE       |           67.63 |                 49.10 |                   0.99 |    -21.75 |     -32.79 |                     0.06 |
| TRGP      |          290.91 |                 49.00 |                   4.42 |    -18.32 |     -29.36 |                     0.06 |
| 005930.KS |          173.09 |                 48.90 |                   4.31 |    -18.43 |     -29.47 |                     0.07 |
| NVDA      |          221.30 |                 44.90 |                  10.11 |    -12.64 |     -23.68 |                     0.05 |
| MSFT      |          533.69 |                 42.20 |                   1.70 |    -21.04 |     -32.08 |                     0.04 |
| KO        |           91.78 |                 40.10 |                   0.65 |    -22.09 |     -33.13 |                     0.02 |
| 000660.KS |         1058.71 |                 39.00 |                   3.83 |    -18.91 |     -29.95 |                     0.14 |
| BRK-B     |          526.35 |                 38.70 |                   0.93 |    -21.81 |     -32.85 |                     0.06 |
| XLV       |          173.96 |                 36.50 |                   1.08 |    -21.66 |     -32.70 |                     0.04 |
| MRK       |          147.37 |                 27.00 |                  -0.19 |    -22.93 |     -33.97 |                     0.04 |
| SPY       |          769.60 |                 26.90 |                   1.36 |    -21.38 |     -32.42 |                     0.04 |

## Log de seleccion (ranking + capa de riesgo + capa cualitativa)

- ✅ **TSM** — BUY: rank #1, prob=67.6%
- ✅ **NEM** — BUY: rank #2, prob=56.0%
- ✅ **GDX** — BUY: rank #3, prob=55.6%
- ✅ **AAPL** — BUY: rank #4, prob=51.0%
- ✅ **QQQ** — BUY: rank #5, prob=50.8%
- ✅ **XLE** — BUY: rank #6, prob=49.1%
- ⛔ **TRGP** — DESCARTADO: cupo semanal ya lleno
- ⛔ **005930.KS** — DESCARTADO: cupo semanal ya lleno
- ⛔ **NVDA** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MSFT** — DESCARTADO: cupo semanal ya lleno
- ⛔ **KO** — DESCARTADO: cupo semanal ya lleno
- ⛔ **000660.KS** — DESCARTADO: cupo semanal ya lleno
- ⛔ **BRK-B** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLV** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MRK** — DESCARTADO: cupo semanal ya lleno
- ⛔ **SPY** — DESCARTADO: cupo semanal ya lleno

## Guardrail cualitativo (RAG) — noticias revisadas

- **QQQ**: Sin noticias recientes para QQQ en los ultimos 7 dias - aprobado por defecto.
- **AAPL**: Sin noticias recientes para AAPL en los ultimos 7 dias - aprobado por defecto.
- **TSM**: Sin noticias recientes para TSM en los ultimos 7 dias - aprobado por defecto.
- **XLE**: Sin noticias recientes para XLE en los ultimos 7 dias - aprobado por defecto.
- **GDX**: Sin noticias recientes para GDX en los ultimos 7 dias - aprobado por defecto.
- **NEM**: Sin noticias recientes para NEM en los ultimos 7 dias - aprobado por defecto.

## Seleccion final (BUY de esta semana)

- **QQQ** — precio $728.95, prob. supera mediana: 50.8%, CVaR: -31.1%
- **AAPL** — precio $342.96, prob. supera mediana: 51.0%, CVaR: -32.2%
- **TSM** — precio $430.00, prob. supera mediana: 67.6%, CVaR: -27.2%
- **XLE** — precio $67.63, prob. supera mediana: 49.1%, CVaR: -32.8%
- **GDX** — precio $83.40, prob. supera mediana: 55.6%, CVaR: -25.8%
- **NEM** — precio $111.56, prob. supera mediana: 56.0%, CVaR: -30.1%

## Capital asignado

| ticker   |   precio_actual |   cantidad |   costo_real |
|:---------|----------------:|-----------:|-------------:|
| AAPL     |          342.96 |          1 |       342.96 |
| TSM      |          430.00 |          1 |       430.00 |
| XLE      |           67.63 |          8 |       541.04 |
| GDX      |           83.40 |          7 |       583.80 |
| NEM      |          111.56 |          5 |       557.80 |

**Capital total usado esta semana:** $2455.60

**Capital disponible despues de esta semana:** $4685.08

## Bloque JSON generado

✅ Validacion local OK.

```json
{
  "version": 1,
  "orders": [
    {
      "action": "BUY",
      "symbol": "AAPL",
      "quantity": 1,
      "type": "MARKET",
      "stop_loss": 342.62
    },
    {
      "action": "BUY",
      "symbol": "TSM",
      "quantity": 1,
      "type": "MARKET",
      "stop_loss": 429.14
    },
    {
      "action": "BUY",
      "symbol": "XLE",
      "quantity": 8,
      "type": "MARKET",
      "stop_loss": 67.56
    },
    {
      "action": "BUY",
      "symbol": "GDX",
      "quantity": 7,
      "type": "MARKET",
      "stop_loss": 83.23
    },
    {
      "action": "BUY",
      "symbol": "NEM",
      "quantity": 5,
      "type": "MARKET",
      "stop_loss": 111.34
    }
  ]
}
```
