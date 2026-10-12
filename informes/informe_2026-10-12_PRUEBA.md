# Informe Semanal — AI Trading Challenge (CTA-003)

**Fecha de la corrida:** 2026-10-12  
**Semana:** 8  
**Resultado de esta corrida:** 🧪 Corrida de prueba - JSON valido, pero no se envio nada (por diseño).  

## Estado del modelo (ensamble)

- Fecha de entrenamiento del ensamble usado: **2026-10-09**
- Numero de modelos en el ensamble: **5**

## Guardrails

- Drawdown actual vs. maximo historico: **-52.4%** (umbral circuit breaker: -20.0%)
- Circuit breaker: 🟢 inactivo

## Ranking del universo evaluado esta semana

| ticker    |   precio_actual |   prob_supera_mediana |   retorno_esperado_pct |   var_pct |   cvar_pct |   incertidumbre_ensamble |
|:----------|----------------:|----------------------:|-----------------------:|----------:|-----------:|-------------------------:|
| 000660.KS |         1251.68 |                 70.70 |                   9.47 |    -13.27 |     -24.31 |                     0.07 |
| TSM       |          453.31 |                 66.30 |                   7.32 |    -15.42 |     -26.46 |                     0.02 |
| 005930.KS |          195.09 |                 58.90 |                  13.05 |     -9.69 |     -20.73 |                     0.05 |
| NEM       |          117.84 |                 53.70 |                   3.55 |    -19.19 |     -30.23 |                     0.03 |
| GDX       |           89.28 |                 52.40 |                   7.57 |    -15.18 |     -26.22 |                     0.08 |
| TRGP      |          286.70 |                 51.80 |                   5.16 |    -17.59 |     -28.63 |                     0.06 |
| NVDA      |          229.28 |                 50.80 |                  12.77 |     -9.98 |     -21.02 |                     0.03 |
| QQQ       |          751.27 |                 49.20 |                   2.36 |    -20.38 |     -31.42 |                     0.04 |
| AAPL      |          336.64 |                 46.20 |                   2.05 |    -20.70 |     -31.74 |                     0.05 |
| XLE       |           65.08 |                 45.30 |                   1.63 |    -21.12 |     -32.16 |                     0.02 |
| BRK-B     |          515.62 |                 44.20 |                   1.57 |    -21.17 |     -32.21 |                     0.06 |
| MSFT      |          535.07 |                 41.60 |                   1.79 |    -20.95 |     -31.99 |                     0.03 |
| KO        |           88.05 |                 37.80 |                   1.81 |    -20.93 |     -31.97 |                     0.02 |
| XLV       |          170.81 |                 30.80 |                   0.93 |    -21.81 |     -32.85 |                     0.03 |
| SPY       |          778.57 |                 26.90 |                   1.24 |    -21.50 |     -32.54 |                     0.04 |
| MRK       |          145.60 |                 25.10 |                  -0.12 |    -22.87 |     -33.91 |                     0.03 |

## Log de seleccion (ranking + capa de riesgo + capa cualitativa)

- ✅ **000660.KS** — BUY: rank #1, prob=70.7%
- ✅ **TSM** — BUY: rank #2, prob=66.3%
- ✅ **005930.KS** — BUY: rank #3, prob=58.9%
- ✅ **NEM** — BUY: rank #4, prob=53.7%
- ✅ **GDX** — BUY: rank #5, prob=52.4%
- ✅ **TRGP** — BUY: rank #6, prob=51.8%
- ⛔ **NVDA** — DESCARTADO: cupo semanal ya lleno
- ⛔ **QQQ** — DESCARTADO: cupo semanal ya lleno
- ⛔ **AAPL** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLE** — DESCARTADO: cupo semanal ya lleno
- ⛔ **BRK-B** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MSFT** — DESCARTADO: cupo semanal ya lleno
- ⛔ **KO** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLV** — DESCARTADO: cupo semanal ya lleno
- ⛔ **SPY** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MRK** — DESCARTADO: cupo semanal ya lleno

## Guardrail cualitativo (RAG) — noticias revisadas

- **005930.KS**: Sin noticias recientes para 005930.KS en los ultimos 7 dias - aprobado por defecto.
- **000660.KS**: Sin noticias recientes para 000660.KS en los ultimos 7 dias - aprobado por defecto.
- **TSM**: Sin noticias recientes para TSM en los ultimos 7 dias - aprobado por defecto.
- **TRGP**: Sin noticias recientes para TRGP en los ultimos 7 dias - aprobado por defecto.
- **GDX**: Sin noticias recientes para GDX en los ultimos 7 dias - aprobado por defecto.
- **NEM**: Sin noticias recientes para NEM en los ultimos 7 dias - aprobado por defecto.

## Seleccion final (BUY de esta semana)

- **005930.KS** — precio $195.09, prob. supera mediana: 58.9%, CVaR: -20.7%
- **000660.KS** — precio $1251.68, prob. supera mediana: 70.7%, CVaR: -24.3%
- **TSM** — precio $453.31, prob. supera mediana: 66.3%, CVaR: -26.5%
- **TRGP** — precio $286.70, prob. supera mediana: 51.8%, CVaR: -28.6%
- **GDX** — precio $89.28, prob. supera mediana: 52.4%, CVaR: -26.2%
- **NEM** — precio $117.84, prob. supera mediana: 53.7%, CVaR: -30.2%

## Capital asignado

| ticker    |   precio_actual |   cantidad |   costo_real |
|:----------|----------------:|-----------:|-------------:|
| 005930.KS |          195.09 |          3 |       585.27 |
| TRGP      |          286.70 |          2 |       573.40 |
| GDX       |           89.28 |          6 |       535.68 |
| NEM       |          117.84 |          5 |       589.20 |

**Capital total usado esta semana:** $2283.55

**Capital disponible despues de esta semana:** $4857.13

## Bloque JSON generado

✅ Validacion local OK.

```json
{
  "version": 1,
  "orders": [
    {
      "action": "BUY",
      "symbol": "005930",
      "quantity": 3,
      "type": "MARKET",
      "stop_loss": 194.7
    },
    {
      "action": "BUY",
      "symbol": "TRGP",
      "quantity": 2,
      "type": "MARKET",
      "stop_loss": 286.41
    },
    {
      "action": "BUY",
      "symbol": "GDX",
      "quantity": 6,
      "type": "MARKET",
      "stop_loss": 89.1
    },
    {
      "action": "BUY",
      "symbol": "NEM",
      "quantity": 5,
      "type": "MARKET",
      "stop_loss": 117.6
    }
  ]
}
```
