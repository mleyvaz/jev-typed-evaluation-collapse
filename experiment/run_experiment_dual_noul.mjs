// Experimento 5 (exploratorio, idea no probada de conversacion): ¿se puede reconstruir
// un par independiente (mu, lambda), como en LPA2v, componiendo DOS llamadas Noul/boolean
// separadas -una preguntando el grado de apoyo A FAVOR, otra el grado de apoyo EN CONTRA-
// en vez de una sola pregunta boolean que fuerza una unica direccion?
//
// Prediccion si la idea funciona: TORN (conflicto) -> mu alto Y lambda alto (vertice TOP,
// inconsistente); SILENT (ignorancia) -> mu bajo Y lambda bajo (vertice BOTTOM, paracompleto);
// AGREE-SUPPORT -> mu alto, lambda bajo; AGREE-REFUTE -> mu bajo, lambda alto.
// Si TORN y SILENT no se distinguen en este par tampoco, la idea no aporta nada nuevo.

import { experimental_evaluate as evaluate } from 'ai';
import fs from 'node:fs/promises';

const ITEMS = JSON.parse(await fs.readFile('results.json', 'utf-8'))
  .map(({ id, category, state }) => ({ id, category, state }));

async function runOne(item) {
  const result = await evaluate({
    model: 'typesafe-ai/jev',
    state: item.state,
    questions: {
      mu: {
        type: 'boolean',
        instructions: 'Is there credible evidence supporting the claim that the traffic light was red?',
      },
      lambda: {
        type: 'boolean',
        instructions: 'Is there credible evidence supporting the claim that the traffic light was NOT red (i.e., was green)?',
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
  console.log(`Corriendo ${ITEMS.length} items (mu/lambda independientes) contra typesafe-ai/jev...\n`);
  const results = [];
  for (const item of ITEMS) {
    try {
      const r = await runOne(item);
      results.push(r);
      const mu = r.raw.answers.mu.probability;
      const lambda = r.raw.answers.lambda.probability;
      console.log(`[${r.id}] ${r.category}`);
      console.log(`  mu (apoya ROJO)     = ${mu}`);
      console.log(`  lambda (apoya NO-ROJO) = ${lambda}`);
      console.log('---');
    } catch (err) {
      console.error(`[${item.id}] ERROR:`, err.message || err);
      results.push({ ...item, error: String(err.message || err) });
    }
  }
  await fs.writeFile('results_dual_noul.json', JSON.stringify(results, null, 2), 'utf-8');
  console.log('\nResultados guardados en results_dual_noul.json');
}

main();
