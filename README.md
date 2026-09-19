# Modelos de evaluación tipada y el colapso entre conflicto e ignorancia: un estudio de caso sobre Jev

Nota de campo (destino: NCML) sobre Jev (TypeSafe AI), el primer "System One model" comercial,
examinado con tres experimentos mínimos vía Vercel AI Gateway.

## Contenido

- `paper/manuscript_v0.3.md` — versión actual del manuscrito (fuente).
- `paper/manuscript_v0.3_NCML.docx` / `.pdf` — formato de envío a NCML.
- `paper/manuscript_v0.1.md`, `manuscript_v0.2.md` — versiones anteriores, conservadas para trazabilidad.
- `paper/figures/make_fig1_taxonomy.py` — script que genera la Figura 1 (taxonomía de 5 categorías).
- `experiment/run_experiment.mjs` + `results.json` — Experimento 1 (tipo `boolean`/Noul).
- `experiment/run_experiment_choice.mjs` + `results_choice.json` — Experimento 2 (tipo `Choice`, esquema enriquecido).
- `experiment/run_experiment_choice_binary.mjs` + `results_choice_binary.json` — Experimento 3 (tipo `Choice` binario, sin categorías de escape).
- `ask_models_review_paper.py` + `respuestas_review_paper/` — ronda de revisión adversarial (5 modelos vía OpenRouter) que motivó las revisiones v0.1→v0.2→v0.3.

## Reproducir los experimentos

Requiere Node.js ≥ 22.18 y una llave de [Vercel AI Gateway](https://vercel.com/ai-gateway) propia
(con créditos de pago cargados — el nivel gratuito solo permite unas pocas llamadas antes de un
rate-limit persistente, ver §8 del manuscrito).

```bash
cd experiment
npm install
export AI_GATEWAY_API_KEY=vck_...   # nunca commitear esta llave
node --env-file=.env.local run_experiment.mjs
node --env-file=.env.local run_experiment_choice.mjs
node --env-file=.env.local run_experiment_choice_binary.mjs
```

## Hallazgo central

El mismo modelo (Jev), sobre la misma evidencia, produce tres patrones distintos según el tipo de
pregunta y el esquema declarados: colapsa con `boolean`/Noul (no distingue conflicto de ignorancia),
separa perfecto con `Choice` si el esquema nombra explícitamente esos estados, y exhibe un sesgo
direccional no anticipado con `Choice` binario sin categorías de escape. Detalle completo en
`paper/manuscript_v0.3.md`.

## Autor

Maikel Leyva-Vázquez — Universidad Bernardo O'Higgins (UBO) / Universidad Bolivariana del Ecuador (UBE) / Universidad de Guayaquil (UG).
