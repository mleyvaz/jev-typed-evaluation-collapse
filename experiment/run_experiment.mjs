// Experimento: ¿Jev (typesafe-ai/jev) distingue CONFLICTO genuino (TORN) de IGNORANCIA genuina (SILENT)?
// Prediccion desde AET (project_aet_symmetry_framework.md, Def. 8*, invarianza por reflexion ρ):
// un score/probabilidad de cercania NO puede distinguir "evidencia fuerte y contradictoria" de
// "sin evidencia", porque ambos colapsan a una region de baja certeza. Si Jev muestra el mismo
// patron, es evidencia empirica en vivo del mismo problema representacional.
//
// Requiere: variable de entorno AI_GATEWAY_API_KEY con una llave del AI Gateway de Vercel
// (vercel.com/ai-gateway -> "Get API key"). No hardcodear la llave en este archivo.

import { experimental_evaluate as evaluate } from 'ai';

const ITEMS = [
  {
    id: 'TORN-1',
    category: 'TORN (conflicto genuino)',
    state:
      'Witness A, a police officer with a clear view of the intersection, testified under oath ' +
      'that the traffic light was red at the moment of the collision. Witness B, a bystander ' +
      'standing next to Witness A with an equally clear view, testified under oath that the same ' +
      'traffic light was green at that exact moment. Both witnesses are considered reliable by the ' +
      'investigating officer; there is no indication either one is lying.',
  },
  {
    id: 'TORN-2',
    category: 'TORN (conflicto genuino)',
    state:
      'Sensor 1, a calibrated high-precision traffic sensor, recorded the light as RED at 14:03:02. ' +
      'Sensor 2, an equally calibrated high-precision sensor mounted on the same pole, recorded the ' +
      'light as GREEN at the same timestamp, 14:03:02. Both sensors passed their most recent ' +
      'calibration check with no faults reported.',
  },
  {
    id: 'SILENT-1',
    category: 'SILENT (ignorancia genuina)',
    state:
      'No witnesses were present at the intersection at the time in question. No traffic cameras ' +
      'were operating in that area that day. There is no record, sensor log, or testimony of any ' +
      'kind describing the state of the traffic light at that moment.',
  },
  {
    id: 'SILENT-2',
    category: 'SILENT (ignorancia genuina)',
    state:
      "The traffic light's camera log for that day was permanently lost in a server failure before " +
      'any backup was made. No witnesses have come forward. No other observation of the light exists ' +
      'in any form.',
  },
  {
    id: 'AGREE-SUPPORT',
    category: 'control: ambas fuentes de acuerdo (apoyo)',
    state:
      'Witness A testified that the traffic light was red at the time of the collision. Witness B, ' +
      'standing nearby with an independent line of sight, separately and independently confirmed ' +
      'that the light was red at that same moment.',
  },
  {
    id: 'AGREE-REFUTE',
    category: 'control: ambas fuentes de acuerdo (refutacion)',
    state:
      'Witness A testified that the traffic light was green, not red, at the time of the collision. ' +
      'Witness B, standing nearby with an independent line of sight, separately and independently ' +
      'confirmed that the light was green at that same moment.',
  },
];

async function runOne(item) {
  const result = await evaluate({
    model: 'typesafe-ai/jev',
    state: item.state,
    questions: {
      wasRed: {
        type: 'boolean',
        instructions: 'Was the traffic light red at the time in question?',
      },
    },
  });
  return { ...item, raw: result };
}

async function main() {
  if (!process.env.AI_GATEWAY_API_KEY) {
    console.error(
      'Falta AI_GATEWAY_API_KEY en el entorno. Sacar una llave en https://vercel.com/ai-gateway ' +
        '("Get API key") y exportarla antes de correr este script, ej.:\n' +
        '  set AI_GATEWAY_API_KEY=vck_...   (cmd)\n' +
        '  $env:AI_GATEWAY_API_KEY="vck_..." (PowerShell)\n' +
        '  export AI_GATEWAY_API_KEY=vck_... (bash)'
    );
    process.exit(1);
  }

  console.log(`Corriendo ${ITEMS.length} items contra typesafe-ai/jev...\n`);

  const results = [];
  for (const item of ITEMS) {
    try {
      const r = await runOne(item);
      results.push(r);
      console.log(`[${r.id}] ${r.category}`);
      console.log(JSON.stringify(r.raw, null, 2));
      console.log('---');
    } catch (err) {
      console.error(`[${item.id}] ERROR:`, err.message || err);
      results.push({ ...item, error: String(err.message || err) });
    }
  }

  const outPath = new URL('./results.json', import.meta.url);
  await import('node:fs/promises').then((fs) =>
    fs.writeFile(outPath, JSON.stringify(results, null, 2), 'utf-8')
  );
  console.log(`\nResultados guardados en ${outPath.pathname}`);
  console.log(
    '\nPregunta clave para el paper: ¿la confianza/probabilidad de TORN-1/TORN-2 se parece a la ' +
      'de SILENT-1/SILENT-2? Si sí, Jev colapsa conflicto e ignorancia igual que predice AET.'
  );
}

main();
