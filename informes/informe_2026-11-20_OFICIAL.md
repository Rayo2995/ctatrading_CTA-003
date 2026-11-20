# Informe Semanal — AI Trading Challenge (CTA-003)

**Fecha de la corrida:** 2026-11-20  
**Semana:** 13  
**Resultado de esta corrida:** ✅ Correo enviado al profesor esta semana.  

## Estado del modelo (ensamble)

- Fecha de entrenamiento del ensamble usado: **2026-11-20**
- Numero de modelos en el ensamble: **5**
- Hit-rate movil (ultimas 1 semanas evaluables): **25.0%**

## Guardrails

- Patrimonio total al momento de la corrida (efectivo + posiciones): **$8,602.73** (maximo historico: $10,199.86)
- Drawdown actual vs. maximo historico: **-15.7%** (umbral circuit breaker: -20.0%)
- Circuit breaker: 🟢 inactivo

## Ranking del universo evaluado esta semana

| ticker    |   precio_actual |   prob_supera_mediana |   retorno_esperado_pct |   var_pct |   cvar_pct |   incertidumbre_ensamble |
|:----------|----------------:|----------------------:|-----------------------:|----------:|-----------:|-------------------------:|
| 000660.KS |          889.21 |                 87.00 |                  30.00 |     -3.88 |     -17.35 |                     0.09 |
| QQQ       |          645.04 |                 76.60 |                   5.14 |    -28.74 |     -42.21 |                     0.04 |
| TSM       |          352.09 |                 71.70 |                  14.36 |    -19.52 |     -32.99 |                     0.04 |
| SPY       |          715.87 |                 71.70 |                   3.78 |    -30.09 |     -43.56 |                     0.04 |
| GDX       |           72.00 |                 59.20 |                   9.79 |    -24.09 |     -37.56 |                     0.04 |
| NEM       |          100.05 |                 55.60 |                  10.62 |    -23.26 |     -36.73 |                     0.06 |
| AAPL      |          349.21 |                 54.70 |                   2.83 |    -31.05 |     -44.52 |                     0.02 |
| BRK-B     |          572.04 |                 52.10 |                   2.77 |    -31.11 |     -44.57 |                     0.06 |
| 005930.KS |          148.00 |                 51.00 |                   7.39 |    -26.49 |     -39.96 |                     0.07 |
| TRGP      |          285.42 |                 47.00 |                   5.08 |    -28.80 |     -42.27 |                     0.03 |
| NVDA      |          145.98 |                 46.10 |                  12.53 |    -21.35 |     -34.82 |                     0.08 |
| MSFT      |          498.30 |                 44.00 |                  -0.21 |    -34.08 |     -47.55 |                     0.07 |
| XLE       |           60.89 |                 42.10 |                   2.39 |    -31.49 |     -44.96 |                     0.05 |
| KO        |           96.09 |                 37.30 |                   1.73 |    -32.15 |     -45.61 |                     0.02 |
| MRK       |          132.81 |                 36.40 |                  -0.93 |    -34.81 |     -48.28 |                     0.06 |
| XLV       |          177.46 |                 31.20 |                   1.35 |    -32.52 |     -45.99 |                     0.04 |

## Log de seleccion (ranking + capa de riesgo + capa cualitativa)

- ✅ **000660.KS** — BUY: rank #1, prob=87.0%
- ✅ **QQQ** — BUY: rank #2, prob=76.6%
- ✅ **SPY** — BUY: rank #3, prob=71.7%
- ⛔ **TSM** — DESCARTADO (capa cualitativa): [RAG/openrouter] TSMC actions fell 4.76% this week, marking its worst decline since 1991 amid a broader AI chip sell‑off.
- ✅ **GDX** — BUY: rank #4, prob=59.2%
- ✅ **NEM** — BUY: rank #5, prob=55.6%
- ✅ **AAPL** — BUY: rank #6, prob=54.7%
- ⛔ **BRK-B** — DESCARTADO: cupo semanal ya lleno
- ⛔ **005930.KS** — DESCARTADO: cupo semanal ya lleno
- ⛔ **TRGP** — DESCARTADO: cupo semanal ya lleno
- ⛔ **NVDA** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MSFT** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLE** — DESCARTADO: cupo semanal ya lleno
- ⛔ **KO** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MRK** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLV** — DESCARTADO: cupo semanal ya lleno

## Guardrail cualitativo (RAG) — noticias revisadas

- **SPY**: [RAG/openrouter] No hay noticias materiales negativas sobre SPY; solo volatilidad de mercado y rebalanceo normal del ETF.
- **QQQ**: [RAG/openrouter] Las noticias solo reflejan ventas netas de ETFs y una baja generalizada del mercado/rotación en acciones de IA, además de rebalances ordinarios de cartera; no hay fraude, investigación regulatoria grave, quiebra ni salida escandalosa de ejecutivos.
- **AAPL**: [RAG/openrouter] No hay noticias materiales negativas graves; predominan rumores de desarrollo de IA, competencia y valoración, no fraude, investigación regulatoria ni crisis.
- **000660.KS**: [RAG/openrouter] No hay noticias materiales negativas específicas de SK Hynix (000660.KS); solo ruido sectorial y caídas de precio por el entorno de chips.
- **TSM**: [RAG/openrouter] TSMC actions fell 4.76% this week, marking its worst decline since 1991 amid a broader AI chip sell‑off.
- **GDX**: [RAG/openrouter] No hay noticias de riesgo material negativo; las fluctuaciones de precio del oro y los mineros son normales en el contexto macroeconómico actual.
- **NEM**: [RAG/openrouter] Las noticias negativas recientes son principalmente un retroceso sectorial por precios del oro y expectativas macro, sin fraude, investigación regulatoria grave, quiebra ni salida abrupta de ejecutivos.

## Seleccion final (BUY de esta semana)

- **SPY** — precio $715.87, prob. supera mediana: 71.7%, CVaR: -43.6%
- **QQQ** — precio $645.04, prob. supera mediana: 76.6%, CVaR: -42.2%
- **AAPL** — precio $349.21, prob. supera mediana: 54.7%, CVaR: -44.5%
- **000660.KS** — precio $889.21, prob. supera mediana: 87.0%, CVaR: -17.4%
- **GDX** — precio $72.00, prob. supera mediana: 59.2%, CVaR: -37.6%
- **NEM** — precio $100.05, prob. supera mediana: 55.6%, CVaR: -36.7%

## Capital asignado

| ticker   |   precio_actual |   cantidad |   costo_real |
|:---------|----------------:|-----------:|-------------:|
| GDX      |           72.00 |          3 |       216.00 |
| NEM      |          100.05 |          2 |       200.10 |

**Capital total usado esta semana:** $416.10

**Capital disponible despues de esta semana:** $2067.08

## Bloque JSON generado

✅ Validacion local OK.

```json
{
  "version": 1,
  "orders": [
    {
      "action": "BUY",
      "symbol": "GDX",
      "quantity": 3,
      "type": "MARKET",
      "stop_loss": 71.86
    },
    {
      "action": "BUY",
      "symbol": "NEM",
      "quantity": 2,
      "type": "MARKET",
      "stop_loss": 99.85
    }
  ]
}
```
