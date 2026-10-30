# Informe Semanal — AI Trading Challenge (CTA-003)

**Fecha de la corrida:** 2026-10-30  
**Semana:** 10  
**Resultado de esta corrida:** ✅ Correo enviado al profesor esta semana.  

## Estado del modelo (ensamble)

- Fecha de entrenamiento del ensamble usado: **2026-10-30**
- Numero de modelos en el ensamble: **5**
- Hit-rate movil (ultimas 1 semanas evaluables): **25.0%**

## Guardrails

- Patrimonio total al momento de la corrida (efectivo + posiciones): **$9,857.19** (maximo historico: $10,199.86)
- Drawdown actual vs. maximo historico: **-3.4%** (umbral circuit breaker: -20.0%)
- Circuit breaker: 🟢 inactivo

## Ranking del universo evaluado esta semana

| ticker    |   precio_actual |   prob_supera_mediana |   retorno_esperado_pct |   var_pct |   cvar_pct |   incertidumbre_ensamble |
|:----------|----------------:|----------------------:|-----------------------:|----------:|-----------:|-------------------------:|
| TSM       |          431.81 |                 72.20 |                   8.02 |    -17.37 |     -29.42 |                     0.03 |
| QQQ       |          715.34 |                 69.60 |                   3.13 |    -22.26 |     -34.31 |                     0.03 |
| TRGP      |          312.37 |                 68.70 |                   8.22 |    -17.17 |     -29.22 |                     0.04 |
| GDX       |           81.33 |                 68.00 |                  10.56 |    -14.82 |     -26.88 |                     0.04 |
| NEM       |          111.80 |                 60.10 |                   6.10 |    -19.29 |     -31.34 |                     0.04 |
| NVDA      |          213.66 |                 57.60 |                   8.13 |    -17.26 |     -29.31 |                     0.03 |
| XLE       |           68.71 |                 56.60 |                   2.37 |    -23.02 |     -35.07 |                     0.01 |
| BRK-B     |          541.96 |                 49.60 |                   1.91 |    -23.48 |     -35.53 |                     0.03 |
| XLV       |          184.04 |                 48.00 |                   2.09 |    -23.30 |     -35.35 |                     0.04 |
| AAPL      |          348.91 |                 47.40 |                   1.91 |    -23.48 |     -35.53 |                     0.03 |
| KO        |           92.82 |                 41.40 |                   2.33 |    -23.06 |     -35.12 |                     0.07 |
| 000660.KS |         1138.52 |                 41.00 |                   6.02 |    -19.37 |     -31.42 |                     0.17 |
| SPY       |          769.36 |                 34.50 |                   1.33 |    -24.06 |     -36.11 |                     0.06 |
| MSFT      |          530.14 |                 33.80 |                   0.96 |    -24.43 |     -36.48 |                     0.04 |
| 005930.KS |          173.09 |                 32.90 |                  -2.30 |    -27.69 |     -39.74 |                     0.15 |
| MRK       |          146.33 |                 31.50 |                   2.21 |    -23.18 |     -35.23 |                     0.06 |

## Log de seleccion (ranking + capa de riesgo + capa cualitativa)

- ✅ **TSM** — BUY: rank #1, prob=72.2%
- ✅ **QQQ** — BUY: rank #2, prob=69.6%
- ✅ **TRGP** — BUY: rank #3, prob=68.7%
- ✅ **GDX** — BUY: rank #4, prob=68.0%
- ✅ **NEM** — BUY: rank #5, prob=60.1%
- ✅ **NVDA** — BUY: rank #6, prob=57.6%
- ⛔ **XLE** — DESCARTADO: cupo semanal ya lleno
- ⛔ **BRK-B** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLV** — DESCARTADO: cupo semanal ya lleno
- ⛔ **AAPL** — DESCARTADO: cupo semanal ya lleno
- ⛔ **KO** — DESCARTADO: cupo semanal ya lleno
- ⛔ **000660.KS** — DESCARTADO: cupo semanal ya lleno
- ⛔ **SPY** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MSFT** — DESCARTADO: cupo semanal ya lleno
- ⛔ **005930.KS** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MRK** — DESCARTADO: cupo semanal ya lleno

## Guardrail cualitativo (RAG) — noticias revisadas

- **QQQ**: [RAG/openrouter] Solo hay noticias rutinarias del fondo, articulos de comparacion de ETFs y expansion internacional positiva; ningun evento material negativo.
- **NVDA**: [RAG/openrouter] No se detectaron noticias materiales negativas recientes específicas de NVDA; solo ruido general de mercado y noticias de otros activos.
- **TSM**: [RAG/openrouter] No hay noticias materiales y negativas específicas sobre TSM en los últimos 7 días
- **TRGP**: [RAG/openrouter] No existen noticias materiales y negativas que justifiquen vetar la compra; solo hay previsiones de earnings y valoraciones neutras.
- **GDX**: [RAG/openrouter] No se detectan noticias materialmente negativas o escándalos graves en los últimos 7 días
- **NEM**: [RAG/openrouter] No hay noticia material y negativa reciente que justifique evitar la compra de NEM.

## Seleccion final (BUY de esta semana)

- **QQQ** — precio $715.34, prob. supera mediana: 69.6%, CVaR: -34.3%
- **NVDA** — precio $213.66, prob. supera mediana: 57.6%, CVaR: -29.3%
- **TSM** — precio $431.81, prob. supera mediana: 72.2%, CVaR: -29.4%
- **TRGP** — precio $312.37, prob. supera mediana: 68.7%, CVaR: -29.2%
- **GDX** — precio $81.33, prob. supera mediana: 68.0%, CVaR: -26.9%
- **NEM** — precio $111.80, prob. supera mediana: 60.1%, CVaR: -31.3%

## Capital asignado

| ticker   |   precio_actual |   cantidad |   costo_real |
|:---------|----------------:|-----------:|-------------:|
| NVDA     |          213.66 |          1 |       213.66 |
| GDX      |           81.33 |          3 |       243.99 |
| NEM      |          111.80 |          2 |       223.60 |

**Capital total usado esta semana:** $681.25

**Capital disponible despues de esta semana:** $2646.86

## Bloque JSON generado

✅ Validacion local OK.

```json
{
  "version": 1,
  "orders": [
    {
      "action": "BUY",
      "symbol": "NVDA",
      "quantity": 1,
      "type": "MARKET",
      "stop_loss": 213.23
    },
    {
      "action": "BUY",
      "symbol": "GDX",
      "quantity": 3,
      "type": "MARKET",
      "stop_loss": 81.17
    },
    {
      "action": "BUY",
      "symbol": "NEM",
      "quantity": 2,
      "type": "MARKET",
      "stop_loss": 111.58
    }
  ]
}
```
