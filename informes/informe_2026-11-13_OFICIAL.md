# Informe Semanal — AI Trading Challenge (CTA-003)

**Fecha de la corrida:** 2026-11-13  
**Semana:** 12  
**Resultado de esta corrida:** ✅ Correo enviado al profesor esta semana.  

## Estado del modelo (ensamble)

- Fecha de entrenamiento del ensamble usado: **2026-10-30**
- Numero de modelos en el ensamble: **5**
- Hit-rate movil (ultimas 1 semanas evaluables): **25.0%**

## Guardrails

- Patrimonio total al momento de la corrida (efectivo + posiciones): **$9,324.43** (maximo historico: $10,199.86)
- Drawdown actual vs. maximo historico: **-8.6%** (umbral circuit breaker: -20.0%)
- Circuit breaker: 🟢 inactivo

## Ranking del universo evaluado esta semana

| ticker    |   precio_actual |   prob_supera_mediana |   retorno_esperado_pct |   var_pct |   cvar_pct |   incertidumbre_ensamble |
|:----------|----------------:|----------------------:|-----------------------:|----------:|-----------:|-------------------------:|
| 000660.KS |          938.44 |                 87.10 |                  22.83 |     -2.56 |     -14.61 |                     0.08 |
| QQQ       |          688.17 |                 76.20 |                   9.23 |    -16.16 |     -28.21 |                     0.03 |
| BRK-B     |          589.83 |                 74.00 |                   4.86 |    -20.53 |     -32.58 |                     0.02 |
| TSM       |          405.49 |                 70.80 |                   7.45 |    -17.94 |     -29.99 |                     0.05 |
| SPY       |          757.12 |                 67.00 |                   3.13 |    -22.25 |     -34.31 |                     0.02 |
| GDX       |           81.84 |                 66.90 |                   8.71 |    -16.68 |     -28.73 |                     0.08 |
| AAPL      |          354.88 |                 57.10 |                   4.64 |    -20.75 |     -32.80 |                     0.04 |
| NEM       |          112.64 |                 51.70 |                   7.26 |    -18.12 |     -30.18 |                     0.03 |
| MSFT      |          523.00 |                 48.00 |                   6.18 |    -19.21 |     -31.26 |                     0.05 |
| NVDA      |          166.19 |                 47.80 |                  10.05 |    -15.34 |     -27.39 |                     0.06 |
| XLV       |          187.83 |                 45.90 |                   2.97 |    -22.42 |     -34.47 |                     0.04 |
| 005930.KS |          155.66 |                 41.40 |                   2.28 |    -23.10 |     -35.16 |                     0.09 |
| KO        |           97.44 |                 41.20 |                   1.34 |    -24.04 |     -36.10 |                     0.04 |
| XLE       |           64.33 |                 34.10 |                   3.51 |    -21.88 |     -33.93 |                     0.03 |
| TRGP      |          296.30 |                 32.10 |                   4.16 |    -21.22 |     -33.28 |                     0.06 |
| MRK       |          146.95 |                 31.00 |                   0.57 |    -24.82 |     -36.87 |                     0.04 |

## Log de seleccion (ranking + capa de riesgo + capa cualitativa)

- ✅ **000660.KS** — BUY: rank #1, prob=87.1%
- ✅ **QQQ** — BUY: rank #2, prob=76.2%
- ✅ **BRK-B** — BUY: rank #3, prob=74.0%
- ✅ **TSM** — BUY: rank #4, prob=70.8%
- ✅ **SPY** — BUY: rank #5, prob=67.0%
- ✅ **GDX** — BUY: rank #6, prob=66.9%
- ⛔ **AAPL** — DESCARTADO: cupo semanal ya lleno
- ⛔ **NEM** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MSFT** — DESCARTADO: cupo semanal ya lleno
- ⛔ **NVDA** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLV** — DESCARTADO: cupo semanal ya lleno
- ⛔ **005930.KS** — DESCARTADO: cupo semanal ya lleno
- ⛔ **KO** — DESCARTADO: cupo semanal ya lleno
- ⛔ **XLE** — DESCARTADO: cupo semanal ya lleno
- ⛔ **TRGP** — DESCARTADO: cupo semanal ya lleno
- ⛔ **MRK** — DESCARTADO: cupo semanal ya lleno

## Guardrail cualitativo (RAG) — noticias revisadas

- **SPY**: [RAG/openrouter] Solo hay ruido de mercado general (PPI alto, rendimientos del Tesoro sobre 5%, posible alza de tasas) y una noticia idiosincratica de Nvidia (salida de su CEO); no hay fraude, investigacion regulatoria ni escandalo que afecte a SPY como activo.
- **QQQ**: [RAG/openrouter] Solo hay volatilidad de mercado, inflacion PPI alta y una correccion del 10%; no existe fraude, investigacion regulatoria, quiebra ni escandalo grave especifico del ETF QQQ, por lo que no se justifica vetar la compra.
- **BRK-B**: [RAG/openrouter] No se detecta una noticia material y negativa reciente sobre Berkshire Hathaway (BRK-B); las menciones se centran en valoraciones, buybacks y comparativas positivas, sin señales graves que justifiquen no comprar.
- **000660.KS**: [RAG/openrouter] Las caídas de SK hynix responden a la volatilidad sectorial tras la salida de Jensen Huang en Nvidia y a titulares técnicos/políticos sobre CXMT; no hay fraude, investigación regulatoria contra SK hynix, quiebra ni salida negativa de un ejecutivo clave de la propia empresa, por lo que no se justifica vetar la compra.
- **TSM**: [RAG/openrouter] No se detectaron noticias materiales y negativas recientes que justifiquen evitar la compra de TSM; las caídas sectoriales fueron mitigadas por datos positivos de TSMC y falta una señal grave comprobada.
- **GDX**: [RAG/openrouter] No hay noticias materiales negativas recientes; solo flujos de ETF y opiniones macroeconómicas.

## Seleccion final (BUY de esta semana)

- **SPY** — precio $757.12, prob. supera mediana: 67.0%, CVaR: -34.3%
- **QQQ** — precio $688.17, prob. supera mediana: 76.2%, CVaR: -28.2%
- **BRK-B** — precio $589.83, prob. supera mediana: 74.0%, CVaR: -32.6%
- **000660.KS** — precio $938.44, prob. supera mediana: 87.1%, CVaR: -14.6%
- **TSM** — precio $405.49, prob. supera mediana: 70.8%, CVaR: -30.0%
- **GDX** — precio $81.84, prob. supera mediana: 66.9%, CVaR: -28.7%

## Capital asignado

| ticker   |   precio_actual |   cantidad |   costo_real |
|:---------|----------------:|-----------:|-------------:|
| GDX      |           81.84 |          2 |       163.68 |

**Capital total usado esta semana:** $163.68

**Capital disponible despues de esta semana:** $2483.18

## Bloque JSON generado

✅ Validacion local OK.

```json
{
  "version": 1,
  "orders": [
    {
      "action": "BUY",
      "symbol": "GDX",
      "quantity": 2,
      "type": "MARKET",
      "stop_loss": 81.68
    }
  ]
}
```
