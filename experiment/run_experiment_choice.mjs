// Experimento de seguimiento: ¿el tipo Choice de Jev, con opciones explicitas que nombran
// "conflicto" e "insuficiencia", SI separa TORN de SILENT, a diferencia del tipo boolean/Noul?
// Si Choice separa: la tesis del paper se acota al tipo Noul.
// Si Choice tambien colapsa (reparte probabilidad ambigua entre red/green sin marcar el
// motivo): la tesis se generaliza con mas fuerza a toda la categoria.

import { experimental_evaluate as evaluate } from 'ai';
import fs from 'node:fs/promises';

const ITEMS = JSON.parse(await fs.readFile('results.json', 'utf-8'))
  .map(({ id, category, state }) => ({ id, category, state }));

async function runOne(item) {
  const result = await evaluate({
    model: 'typesafe-ai/jev',
    state: item.state,
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
  });
  return { ...item, raw: result };
}

async function main() {
  if (!process.env.AI_GATEWAY_API_KEY) {
    console.error('Falta AI_GATEWAY_API_KEY en el entorno.');
    process.exit(1);
  }
  console.log(`Corriendo ${ITEMS.length} items (tipo Choice) contra typesafe-ai/jev...\n`);
  const results = [];
  for (const item of ITEMS) {
    try {
      const r = await runOne(item);
      results.push(r);
      console.log(`[${r.id}] ${r.category}`);
      console.log(JSON.stringify(r.raw.answers, null, 2));
      console.log('---');
    } catch (err) {
      console.error(`[${item.id}] ERROR:`, err.message || err);
      results.push({ ...item, error: String(err.message || err) });
    }
  }
  await fs.writeFile('results_choice.json', JSON.stringify(results, null, 2), 'utf-8');
  console.log('\nResultados guardados en results_choice.json');
}

main();
