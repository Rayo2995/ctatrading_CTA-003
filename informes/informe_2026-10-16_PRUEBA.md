# Informe Semanal — AI Trading Challenge (CTA-003)

**Fecha de la corrida:** 2026-10-16  
**Semana:** 8  
**Resultado de esta corrida:** 🧪 Corrida de prueba - JSON valido, pero no se envio nada (por diseño).  

## Estado del modelo (ensamble)

- Fecha de entrenamiento del ensamble usado: **2026-10-09**
- Numero de modelos en el ensamble: **5**

## Guardrails

- Patrimonio total al momento de la corrida (efectivo + posiciones): **$9,869.55** (maximo historico: $10,199.86)
- Drawdown actual vs. maximo historico: **-3.2%** (umbral circuit breaker: -20.0%)
- Circuit breaker: 🟢 inactivo

## Ranking del universo evaluado esta semana

| ticker    |   precio_actual |   prob_supera_mediana |   retorno_esperado_pct |   var_pct |   cvar_pct |   incertidumbre_ensamble |
|:----------|----------------:|----------------------:|-----------------------:|----------:|-----------:|-------------------------:|
| TSM       |          422.25 |                 66.10 |                   5.82 |    -16.93 |     -27.97 |                     0.06 |
| GDX       |           87.02 |                 59.10 |                  10.58 |    -12.16 |     -23.20 |                     0.07 |
| NEM       |          115.79 |                 54.10 |                   3.99 |    -18.76 |     -29.80 |                     0.05 |
| NVDA      |          217.23 |                 52.10 |                   9.56 |    -13.18 |     -24.22 |                     0.07 |
| QQQ       |          728.00 |                 49.50 |                   2.59 |    -20.15 |     -31.19 |                     0.04 |
| XLE       |           66.56 |                 47.50 |                   1.38 |    -21.36 |     -32.40 |                     0.05 |
| 000660.KS |          942.25 |                 46.50 |                   5.48 |    -17.26 |     -28.30 |                     0.16 |
| TRGP      |          282.55 |                 45.50 |                   5.04 |    -17.70 |     -28.74 |                     0.04 |
| AAPL      |          342.00 |                 45.10 |                   1.49 |    -21.25 |     -32.29 |                     0.03 |
| MSFT      |          539.44 |                 42.20 |                   1.57 |    -21.17 |     -32.21 |                     0.01 |
| KO        |           92.00 |                 40.30 |                   0.73 |    -22.01 |     -33.05 |                     0.02 |
| XLV       |          177.19 |                 39.80 |                   0.81 |    -21.93 |     -32.97 |                     0.05 |
| BRK-B     |          525.68 |                 33.90 |                   0.92 |    -21.82 |     -32.86 |                     0.04 |
| MRK       |          145.19 |                 32.30 |                  -0.06 |    -22.80 |     -33.84 |                     0.02 |
| SPY       |          771.79 |                 26.40 |                   1.34 |    -21.40 |     -32.44 |                     0.04 |
| 005930.KS |          156.79 |                 25.20 |                  -1.72 |    -24.46 |     -35.50 |                     0.05 |

## Log de seleccion (ranking + capa de riesgo + capa cualitativa)

- ✅ **TSM** — BUY: rank #1, prob=66.1%
- ✅ **GDX** — BUY: rank #2, prob=59.1%
- ✅ **NEM** — BUY: rank #3, prob=54.1%
- ✅ **NVDA** — BUY: rank #4, prob=52.1%
- ✅ **QQQ** — BUY: rank #5, prob=49.5%
- ✅ **XLE** — BUY: rank #6, prob=47.5%
- ⛔ **000660.KS** — DESCARTADO: cupo semanal ya lleno
- ⛔ **TRGP** — DESCARTADO: cupo semanal ya lleno
- ⛔ **AAPL** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MSFT** — DESCARTADO: cupo semanal ya lleno
- ⛔ **KO** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLV** — DESCARTADO: cupo semanal ya lleno
- ⛔ **BRK-B** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MRK** — DESCARTADO: cupo semanal ya lleno
- ⛔ **SPY** — DESCARTADO: cupo semanal ya lleno
- ⛔ **005930.KS** — DESCARTADO: cupo semanal ya lleno

## Guardrail cualitativo (RAG) — noticias revisadas

- **QQQ**: [RAG/openrouter] No se identificaron noticias materiales y negativas recientes (fraude, investigación regulatoria, quiebra, escándalo grave o salida abrupta de ejecutivo clave) que justifiquen evitar la compra del activo.
- **NVDA**: [RAG/openrouter] No se encontraron noticias materiales negativas recientes sobre NVDA; solo ruido general de mercado y notas de otras empresas.
- **TSM**: [RAG/openrouter] No se detecta noticia material negativa reciente; las ganancias récord y el soporte gubernamental refuerzan la perspectiva positiva.
- **XLE**: [RAG/openrouter] No hay noticias materiales negativas recientes; solo se reportan precios, rebalanceo del ETF y actualizaciones sectoriales sin indicios de fraude, investigación regulatoria o escándalo.
- **GDX**: [RAG/openrouter] No se detectaron noticias materiales negativas en los últimos 7 días.
- **NEM**: [RAG/openrouter] No se encontraron noticias materiales negativas en los últimos 7 días.

## Seleccion final (BUY de esta semana)

- **QQQ** — precio $728.00, prob. supera mediana: 49.5%, CVaR: -31.2%
- **NVDA** — precio $217.23, prob. supera mediana: 52.1%, CVaR: -24.2%
- **TSM** — precio $422.25, prob. supera mediana: 66.1%, CVaR: -28.0%
- **XLE** — precio $66.56, prob. supera mediana: 47.5%, CVaR: -32.4%
- **GDX** — precio $87.02, prob. supera mediana: 59.1%, CVaR: -23.2%
- **NEM** — precio $115.79, prob. supera mediana: 54.1%, CVaR: -29.8%

## Capital asignado

| ticker   |   precio_actual |   cantidad |   costo_real |
|:---------|----------------:|-----------:|-------------:|
| NVDA     |          217.23 |          2 |       434.46 |
| TSM      |          422.25 |          1 |       422.25 |
| XLE      |           66.56 |          6 |       399.36 |
| GDX      |           87.02 |          7 |       609.14 |
| NEM      |          115.79 |          5 |       578.95 |

**Capital total usado esta semana:** $2444.16

**Capital disponible despues de esta semana:** $4696.52

## Bloque JSON generado

✅ Validacion local OK.

```json
{
  "version": 1,
  "orders": [
    {
      "action": "BUY",
      "symbol": "NVDA",
      "quantity": 2,
      "type": "MARKET",
      "stop_loss": 216.8
    },
    {
      "action": "BUY",
      "symbol": "TSM",
      "quantity": 1,
      "type": "MARKET",
      "stop_loss": 421.41
    },
    {
      "action": "BUY",
      "symbol": "XLE",
      "quantity": 6,
      "type": "MARKET",
      "stop_loss": 66.49
    },
    {
      "action": "BUY",
      "symbol": "GDX",
      "quantity": 7,
      "type": "MARKET",
      "stop_loss": 86.85
    },
    {
      "action": "BUY",
      "symbol": "NEM",
      "quantity": 5,
      "type": "MARKET",
      "stop_loss": 115.56
    }
  ]
}
```
