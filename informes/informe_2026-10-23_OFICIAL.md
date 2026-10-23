# Informe Semanal — AI Trading Challenge (CTA-003)

**Fecha de la corrida:** 2026-10-23  
**Semana:** 9  
**Resultado de esta corrida:** ✅ Correo enviado al profesor esta semana.  

## Estado del modelo (ensamble)

- Fecha de entrenamiento del ensamble usado: **2026-10-09**
- Numero de modelos en el ensamble: **5**

## Guardrails

- Patrimonio total al momento de la corrida (efectivo + posiciones): **$9,788.31** (maximo historico: $10,199.86)
- Drawdown actual vs. maximo historico: **-4.0%** (umbral circuit breaker: -20.0%)
- Circuit breaker: 🟢 inactivo

## Ranking del universo evaluado esta semana

| ticker    |   precio_actual |   prob_supera_mediana |   retorno_esperado_pct |   var_pct |   cvar_pct |   incertidumbre_ensamble |
|:----------|----------------:|----------------------:|-----------------------:|----------:|-----------:|-------------------------:|
| TSM       |          412.35 |                 69.60 |                   5.68 |    -17.06 |     -28.10 |                     0.04 |
| GDX       |           81.69 |                 64.00 |                  11.45 |    -11.29 |     -22.33 |                     0.03 |
| NVDA      |          212.21 |                 60.30 |                   6.95 |    -15.79 |     -26.83 |                     0.04 |
| NEM       |          114.11 |                 58.00 |                   4.18 |    -18.57 |     -29.61 |                     0.03 |
| QQQ       |          704.47 |                 57.90 |                   2.32 |    -20.43 |     -31.47 |                     0.09 |
| XLE       |           67.57 |                 56.40 |                   2.59 |    -20.15 |     -31.19 |                     0.07 |
| AAPL      |          348.22 |                 56.30 |                   1.66 |    -21.09 |     -32.13 |                     0.03 |
| 000660.KS |          922.61 |                 49.20 |                   5.04 |    -17.70 |     -28.74 |                     0.20 |
| XLV       |          181.30 |                 46.90 |                   1.64 |    -21.11 |     -32.15 |                     0.03 |
| TRGP      |          289.54 |                 41.20 |                   4.26 |    -18.48 |     -29.52 |                     0.04 |
| MSFT      |          521.08 |                 35.60 |                   1.70 |    -21.04 |     -32.08 |                     0.04 |
| MRK       |          147.24 |                 30.30 |                   0.52 |    -22.23 |     -33.27 |                     0.02 |
| KO        |           95.34 |                 29.50 |                   0.82 |    -21.92 |     -32.96 |                     0.06 |
| SPY       |          763.96 |                 27.70 |                   1.27 |    -21.47 |     -32.51 |                     0.04 |
| 005930.KS |          161.81 |                 25.10 |                  -5.48 |    -28.22 |     -39.26 |                     0.08 |
| BRK-B     |          546.97 |                 19.60 |                  -0.10 |    -22.84 |     -33.88 |                     0.04 |

## Log de seleccion (ranking + capa de riesgo + capa cualitativa)

- ✅ **TSM** — BUY: rank #1, prob=69.6%
- ✅ **GDX** — BUY: rank #2, prob=64.0%
- ✅ **NVDA** — BUY: rank #3, prob=60.3%
- ✅ **NEM** — BUY: rank #4, prob=58.0%
- ✅ **QQQ** — BUY: rank #5, prob=57.9%
- ✅ **XLE** — BUY: rank #6, prob=56.4%
- ⛔ **AAPL** — DESCARTADO: cupo semanal ya lleno
- ⛔ **000660.KS** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLV** — DESCARTADO: cupo semanal ya lleno
- ⛔ **TRGP** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MSFT** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MRK** — DESCARTADO: cupo semanal ya lleno
- ⛔ **KO** — DESCARTADO: cupo semanal ya lleno
- ⛔ **SPY** — DESCARTADO: cupo semanal ya lleno
- ⛔ **005930.KS** — DESCARTADO: cupo semanal ya lleno
- ⛔ **BRK-B** — DESCARTADO: cupo semanal ya lleno

## Guardrail cualitativo (RAG) — noticias revisadas

- **QQQ**: [RAG/openrouter] No se detectó ninguna noticia material negativa (fraude, investigación regulatoria, quiebra, escándalo, retiro masivo de producto o salida abrupta de ejecutivo clave) en los últimos 7 días.
- **NVDA**: [RAG/openrouter] No hay noticias materiales negativas sobre NVDA en los articulos proporcionados; ninguno menciona fraude, investigacion regulatoria, quiebra, escandalo, retiro de producto o salida abrupta de ejecutivo clave.
- **TSM**: [RAG/openrouter] No se identifican noticias materiales y negativas graves en los últimos 7 días; las menciones a riesgos normales de ciclicidad y suministro de materias primas no justifican bloquear la compra.
- **XLE**: [RAG/openrouter] No hay noticias materialmente negativas recientes que justifiquen vetar la compra de XLE esta semana.
- **GDX**: [RAG/openrouter] No se detecta noticia material y negativa reciente sobre GDX; las publicaciones son informativas o de opinión sin señales de fraude, quiebra o eventos graves.
- **NEM**: [RAG/openrouter] No se detectan noticias materiales negativas recientes (fraude, investigación regulatoria, quiebra o escándalo grave); solo hay caída de precio y presión de costos operativos.

## Seleccion final (BUY de esta semana)

- **QQQ** — precio $704.47, prob. supera mediana: 57.9%, CVaR: -31.5%
- **NVDA** — precio $212.21, prob. supera mediana: 60.3%, CVaR: -26.8%
- **TSM** — precio $412.35, prob. supera mediana: 69.6%, CVaR: -28.1%
- **XLE** — precio $67.57, prob. supera mediana: 56.4%, CVaR: -31.2%
- **GDX** — precio $81.69, prob. supera mediana: 64.0%, CVaR: -22.3%
- **NEM** — precio $114.11, prob. supera mediana: 58.0%, CVaR: -29.6%

## Capital asignado

| ticker   |   precio_actual |   cantidad |   costo_real |
|:---------|----------------:|-----------:|-------------:|
| NVDA     |          212.21 |          1 |       212.21 |
| XLE      |           67.57 |          6 |       405.42 |
| GDX      |           81.69 |          5 |       408.45 |
| NEM      |          114.11 |          3 |       342.33 |

**Capital total usado esta semana:** $1368.41

**Capital disponible despues de esta semana:** $3328.11

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
      "stop_loss": 211.79
    },
    {
      "action": "BUY",
      "symbol": "XLE",
      "quantity": 6,
      "type": "MARKET",
      "stop_loss": 67.5
    },
    {
      "action": "BUY",
      "symbol": "GDX",
      "quantity": 5,
      "type": "MARKET",
      "stop_loss": 81.53
    },
    {
      "action": "BUY",
      "symbol": "NEM",
      "quantity": 3,
      "type": "MARKET",
      "stop_loss": 113.88
    }
  ]
}
```
