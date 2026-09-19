// Experimento 4 (exploratorio, no preregistrado): grados de indeterminacion.
// El tipo Score de Jev devuelve un escalar (media ponderada sobre niveles ordenados de una
// rubrica), no una eleccion categorica como Choice. Pregunta: ¿ese escalar ordena
// monotonamente el GRADO de indeterminacion dentro de cada rama (conflicto creciente /
// ausencia de evidencia creciente)? ¿Y en el extremo maximo de cada rama, converge al mismo
// valor (colapso tipo Noul) o los distingue (separacion tipo Choice)?
//
// Rubrica de determinacion (agnostica a la CAUSA de la indeterminacion, solo mide magnitud):
//   0 = certeza muy alta (un solo color, sin ambiguedad)
//   1 = certeza alta (se inclina claramente a un color, con duda menor)
//   2 = moderado (sin base fiable para favorecer un color u otro)
//   3 = certeza baja (casi sin base para juzgar)
//   4 = sin certeza (sin ninguna base para juzgar)

import { experimental_evaluate as evaluate } from 'ai';
import fs from 'node:fs/promises';

const CRITERIA = [
  'Very high confidence: the evidence clearly and unambiguously points to one color.',
  'High confidence: the evidence leans clearly to one color, with minor uncertainty.',
  'Moderate: there is no reliable basis to favor one color over the other.',
  'Low confidence: there is almost no basis to judge the color.',
  'No confidence: there is no basis whatsoever to judge the color.',
];

const ITEMS = [
  {
    id: 'ANCHOR-DETERMINED',
    branch: 'ancla (control, determinado)',
    state:
      'Witness A testified that the traffic light was red at the time of the collision. Witness B, ' +
      'standing nearby with an independent line of sight, separately and independently confirmed ' +
      'that the light was red at that same moment.',
  },
  {
    id: 'CONFLICT-MILD',
    branch: 'conflicto (leve)',
    state:
      "Witness A said the traffic light \"might have been red, but I couldn't say for sure — it " +
      'happened so fast." Witness B said it "could have been green, though I only caught a ' +
      'glimpse." Neither witness is confident in their own account, and both readily admit they ' +
      'might be wrong.',
  },
  {
    id: 'CONFLICT-MODERATE',
    branch: 'conflicto (moderado)',
    state:
      'Witness A, who had a reasonably clear view of the intersection, said the traffic light was ' +
      'red at the moment of the collision. Witness B, who was standing some distance away with a ' +
      'partially obstructed view, said the same traffic light was green at that moment. Both ' +
      'witnesses seem generally credible, though neither had an ideal vantage point.',
  },
  {
    id: 'CONFLICT-SEVERE',
    branch: 'conflicto (severo)',
    state:
      'Sensor 1, a newly calibrated, redundant-triple-checked traffic sensor with a documented ' +
      'error rate of less than 0.001%, recorded the light as RED at 14:03:02.000, with full ' +
      'internal diagnostics confirming normal operation. Sensor 2, an independent sensor of the ' +
      'same specification mounted on the same pole and calibrated the same day, recorded the light ' +
      'as GREEN at the exact same timestamp, 14:03:02.000, with full internal diagnostics ' +
      'confirming normal operation. Both sensors are considered maximally reliable; there is no ' +
      'known explanation for the disagreement.',
  },
  {
    id: 'SILENCE-MILD',
    branch: 'ausencia de evidencia (leve)',
    state:
      'A passing dashcam recorded a few frames of the intersection, but the traffic light itself is ' +
      'out of frame in all of them; only the road surface and nearby cars are visible. No other ' +
      'recording or testimony covers the moment in question.',
  },
  {
    id: 'SILENCE-MODERATE',
    branch: 'ausencia de evidencia (moderada)',
    state:
      'A pedestrian who was not looking at the light mentioned, in an offhand and unprompted remark ' +
      'days later, that they "vaguely recall something about the light," but could not say what ' +
      'color when pressed, or whether they were even looking at the right intersection. No other ' +
      'information exists.',
  },
  {
    id: 'SILENCE-SEVERE',
    branch: 'ausencia de evidencia (severa)',
    state:
      'No witnesses were present at the intersection at the time in question. No traffic cameras ' +
      'were operating in that area that day. There is no record, sensor log, or testimony of any ' +
      'kind describing the state of the traffic light at that moment.',
  },
];

async function runOne(item) {
  const result = await evaluate({
    model: 'typesafe-ai/jev',
    state: item.state,
    questions: {
      determinacy: {
        type: 'score',
        instructions:
          'How determinate (certain) is the available evidence about the color of the traffic ' +
          'light, regardless of which color it points to?',
        criteria: CRITERIA,
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
  console.log(`Corriendo ${ITEMS.length} items (tipo Score, determinacion graduada)...\n`);
  const results = [];
  for (const item of ITEMS) {
    try {
      const r = await runOne(item);
      results.push(r);
      console.log(`[${r.id}] ${r.branch}`);
      console.log(JSON.stringify(r.raw.answers.determinacy, null, 2));
      console.log('---');
    } catch (err) {
      console.error(`[${item.id}] ERROR:`, err.message || err);
      results.push({ ...item, error: String(err.message || err) });
    }
  }
  await fs.writeFile('results_graded_score.json', JSON.stringify(results, null, 2), 'utf-8');
  console.log('\nResultados guardados en results_graded_score.json');
}

main();
