# Typed Evaluation Models and the Collapse Between Conflict and Ignorance: A Case Study on Jev

Field note (target: NCML, already published — see below) about Jev (TypeSafe AI), the first
commercial "System One model," examined with six experiments via the Vercel AI Gateway.

**Published version:** [Neutrosophic Computing and Machine Learning, Vol. 45 (2026)](https://fs.unm.edu/NCML_2/index.php/NCML/article/view/186)

## Contents

- `paper/manuscript_v0.3.md` / `manuscript_v0.3_EN.md` — current manuscript, Spanish and English.
- `paper/manuscript_v0.3_NCML.docx` / `.pdf` — Spanish, NCML journal format.
- `paper/manuscript_v0.3_EN_NCML.docx` / `.pdf` — English, NCML journal format (arXiv-ready abstract).
- `paper/manuscript_v0.1.md`, `manuscript_v0.2.md` — earlier versions, kept for traceability.
- `paper/build_ncml.py` / `build_ncml_en.py` — generate the `.docx` from the markdown source; **never edit the `.docx` by hand**.
- `paper/figures/make_fig1_taxonomy.py` (+ `_en.py`) — Figure 1, the 5-category AI-interaction taxonomy.
- `paper/figures/make_linkedin_infographic.py` / `make_linkedin_taxonomy_infographic_es.py` — promotional infographics.

### Experiments

| # | Script | Data | What it tests |
|---|---|---|---|
| 1 | `experiment/run_experiment.mjs` | `results.json` | `boolean`/Noul — does a single scalar collapse conflict and ignorance? |
| 2 | `run_experiment_choice.mjs` | `results_choice.json` | `Choice`, enriched schema (named conflict/insufficient options) |
| 3 | `run_experiment_choice_binary.mjs` | `results_choice_binary.json` | `Choice`, binary (no escape categories) |
| — | `run_missing_refute.mjs` | (updates results*.json) | follow-up call completing the AGREE-REFUTE case after a rate-limit fix |
| 4 | `run_experiment_graded_score.mjs` | `results_graded_score.json` | `Score`, graded determinacy rubric |
| 5 | `run_experiment_dual_noul.mjs` | `results_dual_noul.json` | composing two `boolean` calls (μ/λ) to reconstruct LPA2v's independent pair |
| 6 | `run_experiment_triple_mli.mjs` | `results_triple_mli.json` | n=1 pilot adding a third indeterminacy coordinate (I) |
| 6 | `run_experiment_multidomain_mli.mjs` | `results_multidomain20_mli.json` | validation of I at n=20 per category across 20 heterogeneous domains |

- `ask_models_review_paper.py` + `respuestas_review_paper/` — 5-model adversarial review round (via OpenRouter) that motivated the v0.1→v0.2→v0.3 revisions.

## Reproducing the experiments

Requires Node.js ≥ 22.18 and your own [Vercel AI Gateway](https://vercel.com/ai-gateway) key
(with **paid credits loaded** — the free tier allows only a few calls before a persistent
rate-limit, see §8 of the manuscript).

```bash
cd experiment
npm install
export AI_GATEWAY_API_KEY=vck_...   # never commit this key
node --env-file=.env.local run_experiment.mjs
node --env-file=.env.local run_experiment_choice.mjs
node --env-file=.env.local run_experiment_choice_binary.mjs
node --env-file=.env.local run_experiment_graded_score.mjs
node --env-file=.env.local run_experiment_dual_noul.mjs
node --env-file=.env.local run_experiment_triple_mli.mjs
node --env-file=.env.local run_experiment_multidomain_mli.mjs
```

## Central finding

The same model (Jev), on the same evidence, produces different patterns depending on the
declared question type and schema: it collapses with `boolean`/Noul (conflict and ignorance
indistinguishable), separates perfectly with `Choice` when the schema names those states
explicitly, shows an unanticipated directional bias with binary `Choice`, and — most
importantly — composing two independent `boolean` calls (μ/λ) reconstructs the full lattice of
annotated paraconsistent logic (LPA2v) without the model computing it internally. A sixth
experiment, validated at n=20 across 20 heterogeneous domains, shows a third neutrosophic
indeterminacy coordinate (I) adds real but small information beyond that pair. Full detail in
`paper/manuscript_v0.3_EN.md`.

## Author

Maikel Leyva-Vázquez — Universidad Bernardo O'Higgins (UBO) / Universidad Bolivariana del Ecuador (UBE) / Universidad de Guayaquil (UG).
