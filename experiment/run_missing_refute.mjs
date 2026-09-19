// Reintenta SOLO el caso AGREE-REFUTE (el unico que fallo por rate-limit en los 3 experimentos)
// ahora que hay credito pagado cargado en el AI Gateway. No toca los demas casos ya verificados.

import { experimental_evaluate as evaluate } from 'ai';
import fs from 'node:fs/promises';

const REFUTE = {
  id: 'AGREE-REFUTE',
  category: 'control: ambas fuentes de acuerdo (refutacion)',
  state:
    'Witness A testified that the traffic light was green, not red, at the time of the collision. ' +
    'Witness B, standing nearby with an independent line of sight, separately and independently ' +
    'confirmed that the light was green at that same moment.',
};

const SCHEMAS = [
  {
    file: 'results.json',
    label: 'Experimento 1 (boolean/Noul)',
    questions: {
      wasRed: {
        type: 'boolean',
        instructions: 'Was the traffic light red at the time in question?',
      },
    },
  },
  {
    file: 'results_choice.json',
    label: 'Experimento 2 (Choice enriquecido)',
    questions: {
      lightState: {
        type: 'choice',
        instructions: 'What was the state of the traffic light at the time in question?',
        criteria: {
          red: 'The evidence indicates the light was red.',
          green: 'The evidence indicates the light was green (not red).',
          conflicting_evidence: 'Reliable sources disagree with each other about the color.',
          insufficient_evidence: 'There is no evidence available to determine the color.',
        },
      },
    },
  },
  {
    file: 'results_choice_binary.json',
    label: 'Experimento 3 (Choice binario)',
    questions: {
      lightState: {
        type: 'choice',
        instructions: 'What was the state of the traffic light at the time in question?',
        criteria: {
          red: 'The evidence indicates the light was red.',
          green: 'The evidence indicates the light was green (not red).',
        },
      },
    },
  },
];

async function main() {
  if (!process.env.AI_GATEWAY_API_KEY) {
    console.error('Falta AI_GATEWAY_API_KEY en el entorno.');
    process.exit(1);
  }

  for (const schema of SCHEMAS) {
    console.log(`\n=== ${schema.label} ===`);
    try {
      const raw = await evaluate({
        model: 'typesafe-ai/jev',
        state: REFUTE.state,
        questions: schema.questions,
      });
      console.log(JSON.stringify(raw.answers, null, 2));

      const existing = JSON.parse(await fs.readFile(schema.file, 'utf-8'));
      const idx = existing.findIndex((r) => r.id === 'AGREE-REFUTE');
      const updated = { id: REFUTE.id, category: REFUTE.category, state: REFUTE.state, raw };
      if (idx >= 0) existing[idx] = updated;
      else existing.push(updated);
      await fs.writeFile(schema.file, JSON.stringify(existing, null, 2), 'utf-8');
      console.log(`Actualizado ${schema.file}`);
    } catch (err) {
      console.error(`ERROR en ${schema.label}:`, err.message || err);
    }
  }
}

main();
