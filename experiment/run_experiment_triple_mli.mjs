// Experimento 6 (exploratorio): ¿aporta I (indeterminacion) algo que mu/lambda no den ya?
// Prediccion a probar (declarada ANTES de correr, no ajustada despues): si I es solo un
// espejo de "mu y lambda se parecen entre si" (ambos altos en TORN, ambos bajos en SILENT),
// no añade una dimension nueva. Si en cambio I distingue AMBIGUOUS (evidencia intrinsecamente
// borrosa, una sola fuente) de TORN (fuentes claras mtras, pero contradictorias entre si),
// eso si seria una tercera coordenada genuina, no derivable de mu/lambda solos.
//
// Se agrega un septimo estado, AMBIGUOUS, disenado para NO ser ni conflicto (una sola fuente,
// no dos que se contradicen) ni ausencia (SI hay evidencia) sino vaguedad intrinseca de esa
// unica fuente.

import { experimental_evaluate as evaluate } from 'ai';
import fs from 'node:fs/promises';

const BASE_ITEMS = JSON.parse(await fs.readFile('results.json', 'utf-8'))
  .map(({ id, category, state }) => ({ id, category, state }));

const AMBIGUOUS = {
  id: 'AMBIGUOUS',
  category: 'evidencia intrinsecamente vaga (nueva, no conflicto ni ausencia)',
  state:
    'A single grainy photograph shows the traffic light mid-transition, rendered as an ' +
    'indistinct orange-red blur due to motion blur and low light. The photo technician who ' +
    'examined the image says its quality makes it impossible to tell whether the light had ' +
    'already reached red or was still yellow. There is only this one photograph; no other ' +
    'witness, sensor, or recording of the moment exists.',
};

const ITEMS = [...BASE_ITEMS, AMBIGUOUS];

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
      indeterminacy: {
        type: 'boolean',
        instructions: 'Is it indeterminate whether the light was red — that is, does the available evidence fail to clearly resolve this question either way, regardless of the reason why?',
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
  console.log(`Corriendo ${ITEMS.length} items (mu/lambda/indeterminacy) contra typesafe-ai/jev...\n`);
  const results = [];
  for (const item of ITEMS) {
    try {
      const r = await runOne(item);
      results.push(r);
      const { mu, lambda, indeterminacy } = r.raw.answers;
      console.log(`[${r.id}] ${r.category}`);
      console.log(`  mu (apoya ROJO)        = ${mu.probability}`);
      console.log(`  lambda (apoya NO-ROJO) = ${lambda.probability}`);
      console.log(`  I (indeterminado)      = ${indeterminacy.probability}`);
      console.log('---');
    } catch (err) {
      console.error(`[${item.id}] ERROR:`, err.message || err);
      results.push({ ...item, error: String(err.message || err) });
    }
  }
  await fs.writeFile('results_triple_mli.json', JSON.stringify(results, null, 2), 'utf-8');
  console.log('\nResultados guardados en results_triple_mli.json');
}

main();
