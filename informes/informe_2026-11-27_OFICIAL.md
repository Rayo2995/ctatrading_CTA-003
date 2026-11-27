# Informe Semanal — AI Trading Challenge (CTA-003)

**Fecha de la corrida:** 2026-11-27  
**Semana:** 14  
**Resultado de esta corrida:** ✅ Correo enviado al profesor esta semana.  

## Estado del modelo (ensamble)

- Fecha de entrenamiento del ensamble usado: **2026-11-20**
- Numero de modelos en el ensamble: **5**
- Hit-rate movil (ultimas 2 semanas evaluables): **12.5%**

## Guardrails

- Patrimonio total al momento de la corrida (efectivo + posiciones): **$8,592.33** (maximo historico: $10,199.86)
- Drawdown actual vs. maximo historico: **-15.8%** (umbral circuit breaker: -20.0%)
- Circuit breaker: 🟢 inactivo

## Ranking del universo evaluado esta semana

| ticker    |   precio_actual |   prob_supera_mediana |   retorno_esperado_pct |   var_pct |   cvar_pct |   incertidumbre_ensamble |
|:----------|----------------:|----------------------:|-----------------------:|----------:|-----------:|-------------------------:|
| NVDA      |          149.30 |                 71.20 |                  30.00 |     -3.88 |     -17.35 |                     0.17 |
| QQQ       |          633.93 |                 71.00 |                  10.12 |    -23.76 |     -37.23 |                     0.04 |
| 000660.KS |          769.19 |                 70.10 |                  16.43 |    -17.45 |     -30.92 |                     0.11 |
| SPY       |          716.70 |                 69.40 |                   5.03 |    -28.85 |     -42.32 |                     0.07 |
| TSM       |          342.34 |                 59.80 |                  11.82 |    -22.06 |     -35.53 |                     0.09 |
| AAPL      |          355.58 |                 57.60 |                   2.54 |    -31.34 |     -44.81 |                     0.05 |
| NEM       |          101.44 |                 53.50 |                   8.00 |    -25.88 |     -39.35 |                     0.04 |
| TRGP      |          285.53 |                 49.70 |                   4.39 |    -29.49 |     -42.96 |                     0.03 |
| GDX       |           73.89 |                 47.90 |                   7.89 |    -25.99 |     -39.46 |                     0.06 |
| BRK-B     |          579.32 |                 46.90 |                   2.74 |    -31.14 |     -44.61 |                     0.03 |
| MSFT      |          489.93 |                 43.10 |                   0.49 |    -33.39 |     -46.86 |                     0.10 |
| XLE       |           60.90 |                 40.80 |                   2.23 |    -31.65 |     -45.12 |                     0.03 |
| 005930.KS |          127.55 |                 37.00 |                   2.38 |    -31.50 |     -44.97 |                     0.13 |
| MRK       |          140.29 |                 35.00 |                   3.24 |    -30.64 |     -44.11 |                     0.03 |
| KO        |           97.59 |                 32.00 |                   1.55 |    -32.33 |     -45.79 |                     0.01 |
| XLV       |          183.68 |                 27.60 |                   1.64 |    -32.23 |     -45.70 |                     0.02 |

## Log de seleccion (ranking + capa de riesgo + capa cualitativa)

- ✅ **NVDA** — BUY: rank #1, prob=71.2%
- ✅ **QQQ** — BUY: rank #2, prob=71.0%
- ✅ **000660.KS** — BUY: rank #3, prob=70.1%
- ✅ **SPY** — BUY: rank #4, prob=69.4%
- ✅ **TSM** — BUY: rank #5, prob=59.8%
- ✅ **AAPL** — BUY: rank #6, prob=57.6%
- ⛔ **NEM** — DESCARTADO: cupo semanal ya lleno
- ⛔ **TRGP** — DESCARTADO: cupo semanal ya lleno
- ⛔ **GDX** — DESCARTADO: cupo semanal ya lleno
- ⛔ **BRK-B** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MSFT** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLE** — DESCARTADO: cupo semanal ya lleno
- ⛔ **005930.KS** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MRK** — DESCARTADO: cupo semanal ya lleno
- ⛔ **KO** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLV** — DESCARTADO: cupo semanal ya lleno

## Guardrail cualitativo (RAG) — noticias revisadas

- **SPY**: [RAG/openrouter] No se detecta una noticia material y negativa reciente sobre SPY; las noticias se centran en un rebote inicial del mercado y no en fraude, quiebra o escándalo grave.
- **QQQ**: [RAG/openrouter] No se detecta una noticia material y negativa reciente que justifique no comprar QQQ; las noticias reflejan volatilidad y especulacion de mercado, no un fraude, regulacion grave o escandalo que vetar la compra.
- **AAPL**: [RAG/openrouter] No hay noticias materiales negativas recientes para AAPL (fraude, investigación regulatoria seria, quiebra, escándalo o retiro masivo); los titulares son competitivos, positivos o irrelevantes para vetar la compra.
- **NVDA**: Error en guardrail RAG (respuesta sin JSON valido: '{"aprobado": false, "motivo": "NVDA suspendió ventas en el Sudeste Asiático por ') - aprobado por defecto (fail-open).
- **000660.KS**: [RAG/openrouter] No hay noticias materiales negativas recientes para SK Hynix; las menciones son de competencia general, warnings de precios o anuncios positivos de payout, sin fraudes, investigaciones regulatorias, quiebras ni salidas ejecutivas negativas.
- **TSM**: [RAG/openrouter] No hay noticias materiales negativas recientes; aranceles eximen chips, inversionistas venden por gestion de cartera no por fundamentos, expansion en Arizona avanza

## Seleccion final (BUY de esta semana)

- **SPY** — precio $716.70, prob. supera mediana: 69.4%, CVaR: -42.3%
- **QQQ** — precio $633.93, prob. supera mediana: 71.0%, CVaR: -37.2%
- **AAPL** — precio $355.58, prob. supera mediana: 57.6%, CVaR: -44.8%
- **NVDA** — precio $149.30, prob. supera mediana: 71.2%, CVaR: -17.4%
- **000660.KS** — precio $769.19, prob. supera mediana: 70.1%, CVaR: -30.9%
- **TSM** — precio $342.34, prob. supera mediana: 59.8%, CVaR: -35.5%

## Capital asignado

| ticker   |   precio_actual |   cantidad |   costo_real |
|:---------|----------------:|-----------:|-------------:|
| NVDA     |          149.30 |          1 |       149.30 |

**Capital total usado esta semana:** $149.30

**Capital disponible despues de esta semana:** $1917.78

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
      "stop_loss": 149.0
    }
  ]
}
```
