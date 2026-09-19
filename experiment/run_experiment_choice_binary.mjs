// Experimento 3 (cierre de la pregunta abierta de §7/8): Choice con SOLO las opciones
// originales {red, green}, SIN categorias de escape (conflicting_evidence,
// insufficient_evidence). Prueba si el colapso Noul se debe al tipo de pregunta (Choice vs
// boolean) o al esquema (presencia o ausencia de categorias que nombren conflicto/ignorancia).
// Prediccion si la explicacion de esquema es correcta: TORN y SILENT deberian repartir
// probabilidad de forma ambigua entre red/green (similar al colapso de Noul), sin la nitidez
// p=1.0 del Experimento 2.

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
  console.log(`Corriendo ${ITEMS.length} items (Choice binario red/green) contra typesafe-ai/jev...\n`);
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
  await fs.writeFile('results_choice_binary.json', JSON.stringify(results, null, 2), 'utf-8');
  console.log('\nResultados guardados en results_choice_binary.json');
}

main();
