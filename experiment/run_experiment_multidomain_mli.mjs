// Experimento 6 (dataset ampliado): valida mu/lambda/I con n=5 por categoria en vez de n=1,
// cruzando 5 dominios distintos (no solo el semaforo) x 5 categorias (TORN, SILENT,
// AGREE-SUPPORT, AGREE-REFUTE, AMBIGUOUS) = 25 estados. Misma plantilla estructural en los
// 5 dominios para minimizar confusores de diseno (leccion del Experimento 4).
//
// Prediccion declarada ANTES de correr (no ajustada despues):
// (a) mu/lambda deberian separar TORN (ambos altos) de {SILENT, AMBIGUOUS} (ambos bajos) de
//     forma consistente entre dominios;
//     (b) I debería seguir sin distinguir SILENT de AMBIGUOUS de TORN (los tres altos), como
//     ya se vio en el estudio de caso unico del semaforo -- si se repite en 5 dominios,
//     deja de ser anecdota y pasa a ser un patron.

import { experimental_evaluate as evaluate } from 'ai';
import fs from 'node:fs/promises';

function mkDomain(id, subject, claimTrue, claimFalse, reliableA, reliableB, primaryEvidence, secondaryEvidence, ambiguousEvidence) {
  // mu/lambda quedan atados al CONTENIDO concreto del dominio (claimTrue/claimFalse), nunca a
  // una referencia meta ("la direccion TRUE") que Jev no puede resolver desde el texto del
  // estado. Leccion del primer intento (bug encontrado antes de tocar el paper).
  const mu = { type: 'boolean', instructions: `Is there credible evidence supporting the claim that ${claimTrue}?` };
  const lambda = { type: 'boolean', instructions: `Is there credible evidence supporting the claim that ${claimFalse}?` };
  const indeterminacy = {
    type: 'boolean',
    instructions: `Is it indeterminate whether ${claimTrue} — that is, does the available evidence fail to clearly resolve this either way, regardless of the reason why?`,
  };
  return [
    {
      id: `${id}-TORN`,
      domain: id,
      category: 'TORN (conflicto genuino)',
      state:
        `${reliableA} reported that ${claimTrue}. ${reliableB}, with an equally credible basis, ` +
        `reported that ${claimFalse}. Both are considered reliable; there is no indication ` +
        `either one is mistaken.`,
      mu, lambda, indeterminacy,
    },
    {
      id: `${id}-SILENT`,
      domain: id,
      category: 'SILENT (ignorancia genuina)',
      state:
        `No ${primaryEvidence} was available regarding ${subject}. No ${secondaryEvidence} ` +
        `exists either. There is no record of any kind describing whether ${claimTrue}.`,
      mu, lambda, indeterminacy,
    },
    {
      id: `${id}-AGREE-SUPPORT`,
      domain: id,
      category: 'AGREE-SUPPORT (control)',
      state:
        `${reliableA} reported that ${claimTrue}. ${reliableB}, reviewing the matter ` +
        `independently, separately confirmed that ${claimTrue}.`,
      mu, lambda, indeterminacy,
    },
    {
      id: `${id}-AGREE-REFUTE`,
      domain: id,
      category: 'AGREE-REFUTE (control)',
      state:
        `${reliableA} reported that ${claimFalse}. ${reliableB}, reviewing the matter ` +
        `independently, separately confirmed that ${claimFalse}.`,
      mu, lambda, indeterminacy,
    },
    {
      id: `${id}-AMBIGUOUS`,
      domain: id,
      category: 'AMBIGUOUS (evidencia vaga, nueva)',
      state: ambiguousEvidence,
      mu, lambda, indeterminacy,
    },
  ];
}

const ITEMS = [
  ...mkDomain(
    'TRAFFIC',
    'the traffic light',
    'the traffic light was red at the moment of the collision',
    'the traffic light was green (not red) at the moment of the collision',
    'Witness A, a police officer with a clear view of the intersection, testified under oath',
    'Witness B, a bystander with an equally clear view, testified under oath',
    'witnesses were present at the intersection',
    'traffic camera recording',
    'A single grainy photograph shows the traffic light mid-transition, rendered as an ' +
      'indistinct orange-red blur due to motion blur and low light. The photo technician who ' +
      'examined the image says its quality makes it impossible to tell whether the light had ' +
      'already reached red or was still yellow. There is only this one photograph; no other ' +
      'witness, sensor, or recording of the moment exists.'
  ),
  ...mkDomain(
    'PRODUCT',
    'the returned phone',
    "the phone's screen was cracked upon arrival",
    "the phone's screen was NOT cracked upon arrival",
    'Inspector A, a certified quality-control technician who examined the returned phone,',
    'Inspector B, an equally certified technician who examined the same phone independently,',
    'inspection photo was taken when the phone was received',
    'inspector examination before the phone was resold',
    'A single blurry phone-camera photo of the device exists, taken in poor lighting; the ' +
      'technician who reviewed it says the image quality makes it impossible to tell whether ' +
      'the faint line across the screen is a crack or a reflection. No other inspection or ' +
      'record exists.'
  ),
  ...mkDomain(
    'ATTENDANCE',
    "the employee's presence at the 9am meeting",
    'the employee was present at the 9am meeting',
    'the employee was NOT present at the 9am meeting',
    'Colleague A, who sat near the meeting room entrance,',
    'Colleague B, who sat near the same entrance with an equally clear view,',
    'attendance sheet was circulated at the meeting',
    'video recording of the meeting',
    'A single security-camera frame from the meeting room door shows a partially obstructed ' +
      'figure entering; the security officer who reviewed the frame says the image is too ' +
      'obstructed to tell whether it was the employee in question or someone else. No other ' +
      'record of the meeting exists.'
  ),
  ...mkDomain(
    'MEDICAL',
    'the biopsy result',
    'the biopsy sample was malignant',
    'the biopsy sample was benign (not malignant)',
    'Pathologist A, reviewing the biopsy slide,',
    'Pathologist B, an equally qualified pathologist reviewing the same slide independently,',
    'pathologist reviewed the biopsy slide before it was misplaced',
    'digital scan of the slide',
    'A single, poorly preserved biopsy slide exists, with tissue degradation that the lab ' +
      'reports makes cellular structure impossible to assess reliably. No other slide or ' +
      'record from the biopsy exists.'
  ),
  ...mkDomain(
    'FINANCE',
    "the account holder's authorization",
    'the account holder authorized the wire transfer',
    'the account holder did NOT authorize the wire transfer',
    'Bank officer A, reviewing the authorization log,',
    'Bank officer B, an equally qualified officer reviewing the same log independently,',
    'authorization log was recorded for that transaction',
    'call recording of the authorization',
    'A single, partially corrupted audio recording of the authorization call exists; the ' +
      'auditor who reviewed it says the corrupted segments make it impossible to tell whether ' +
      "the account holder's voice confirmed or declined the transfer. No other record of the " +
      'call exists.'
  ),
  ...mkDomain(
    'WEATHER',
    'whether it was raining at the time of the incident',
    'it was raining at the time of the incident',
    'it was NOT raining at the time of the incident',
    'Witness A, standing under the awning near the scene,',
    'Witness B, standing at the same location with an equally clear view,',
    'weather station reading was available for that exact time and location',
    'dashcam or security footage from the area',
    'A single smartphone photo from a passerby shows wet-looking pavement, but the ' +
      'meteorologist who reviewed it says reflections from nearby sprinklers make it ' +
      'impossible to tell whether the wetness was from rain or irrigation. No other weather ' +
      'record exists.'
  ),
  ...mkDomain(
    'CONTRACT',
    'the contract clause',
    'the contract clause was signed by both parties',
    'the contract clause was NOT signed by both parties',
    'Paralegal A, who filed the signed contract,',
    'Paralegal B, who reviewed the same file independently,',
    'notarized copy of the signature page was filed',
    'digital signature log exists for that document',
    'A single scanned copy of the signature page exists, but the scan is smudged where one ' +
      'signature should be, and the records clerk who examined it says it is impossible to ' +
      'tell whether a signature is present under the smudge. No other copy of the page exists.'
  ),
  ...mkDomain(
    'INVENTORY',
    'the warehouse stock',
    'the warehouse had the item in stock on that date',
    'the warehouse did NOT have the item in stock on that date',
    'Warehouse clerk A, who checked the shelf that day,',
    'Warehouse clerk B, who checked the same shelf independently that day,',
    'inventory count was logged for that date',
    'barcode scan record exists for the shelf',
    'A single inventory photo from that date exists, but the item in question is partially ' +
      'hidden behind other boxes, and the auditor who reviewed it says it is impossible to ' +
      'tell whether the item itself is present or just its empty packaging. No other ' +
      'inventory record exists.'
  ),
  ...mkDomain(
    'SECURITY',
    'the door',
    'the door was locked at closing time',
    'the door was NOT locked at closing time',
    'Security guard A, who did the closing walkthrough,',
    'Security guard B, who did an independent check at the same time,',
    'electronic lock log was recorded for that door',
    'security camera footage of the door at closing time exists',
    'A single photo of the door taken by a cleaner exists, but the angle makes the lock ' +
      'mechanism impossible to see clearly, and the facilities manager who reviewed it says ' +
      'it is impossible to tell whether the door was locked or merely closed. No other record ' +
      'exists.'
  ),
  ...mkDomain(
    'ACADEMIC',
    "the student's submission",
    'the student submitted the assignment before the deadline',
    'the student did NOT submit the assignment before the deadline',
    'Teaching assistant A, who checked the submission portal,',
    'Teaching assistant B, who checked the same portal independently,',
    'timestamped submission record was logged by the portal',
    'email confirmation of the submission exists',
    'A single screenshot of the submission portal exists, but the timestamp field is cut off ' +
      'at the edge of the image, and the administrator who reviewed it says it is impossible ' +
      'to tell whether the submission was before or after the deadline. No other record exists.'
  ),
  ...mkDomain(
    'VEHICLE',
    "the car's brakes",
    "the car's brakes were functioning properly before the accident",
    "the car's brakes were NOT functioning properly before the accident",
    'Mechanic A, who inspected the car after the accident,',
    'Mechanic B, an equally qualified mechanic who inspected the same car independently,',
    'maintenance record was kept for the brake system',
    'onboard diagnostic log exists for the vehicle',
    'A single photo of the brake pads exists, taken at an odd angle in low light; the ' +
      'mechanic who reviewed it says it is impossible to tell whether the wear pattern shown ' +
      'is within or beyond the safe limit. No other inspection record exists.'
  ),
  ...mkDomain(
    'FOODSAFETY',
    'the health inspection',
    'the restaurant kitchen passed the health inspection that day',
    'the restaurant kitchen did NOT pass the health inspection that day',
    'Health inspector A, who conducted the inspection,',
    'Health inspector B, who conducted an independent review of the same kitchen that day,',
    'inspection report was filed for that visit',
    'photo log taken during the inspection exists',
    'A single inspection checklist exists, but the pass/fail box is ambiguously marked ' +
      'between two checkboxes, and the records officer who reviewed it says it is impossible ' +
      'to tell which result was intended. No other copy of the report exists.'
  ),
  ...mkDomain(
    'CONSTRUCTION',
    "the building's foundation",
    "the building's foundation met code specifications",
    "the building's foundation did NOT meet code specifications",
    'Structural engineer A, who reviewed the foundation plans,',
    'Structural engineer B, an equally qualified engineer who reviewed the same plans independently,',
    'certified inspection report was filed for the foundation',
    'soil test results exist from the construction site',
    "A single set of foundation measurements exists, but the surveyor's notes are partly " +
      'illegible due to water damage, and the reviewing engineer says it is impossible to ' +
      'tell whether the recorded depth met the required specification. No other measurement ' +
      'record exists.'
  ),
  ...mkDomain(
    'INSURANCE',
    "the claimant's injury location",
    "the claimant's injury occurred on company property",
    "the claimant's injury did NOT occur on company property",
    'Claims investigator A, who reviewed the incident report,',
    'Claims investigator B, who reviewed the same incident independently,',
    'incident report was filed at the time of the injury',
    'security camera footage covering the location exists',
    'A single photo taken by the claimant exists, showing a location near the property ' +
      'boundary, but the adjuster who reviewed it says it is impossible to tell from the ' +
      "image whether the spot shown is inside or outside the company's property line. No " +
      'other record of the location exists.'
  ),
  ...mkDomain(
    'ELECTION',
    'the ballot receipt time',
    'the ballot was received before the polling deadline',
    'the ballot was NOT received before the polling deadline',
    'Poll worker A, who logged incoming ballots,',
    'Poll worker B, who logged the same batch of ballots independently,',
    'time-stamped receipt log was kept for incoming ballots',
    'postal tracking record exists for the ballot',
    'A single date stamp on the ballot envelope exists, but the ink is smeared, and the ' +
      'election official who reviewed it says it is impossible to tell whether the stamped ' +
      'time was before or after the deadline. No other record of receipt exists.'
  ),
  ...mkDomain(
    'SOFTWARE',
    'the deployment',
    'the deployed code included the security patch',
    'the deployed code did NOT include the security patch',
    'Engineer A, who reviewed the deployment log,',
    'Engineer B, who reviewed the same deployment log independently,',
    'deployment log was recorded for that release',
    'version-control commit history exists for the release',
    'A single deployment log file exists, but the relevant entry is truncated due to a ' +
      'logging error, and the on-call engineer who reviewed it says it is impossible to tell ' +
      "whether the patch's commit hash appears in the truncated portion. No other record of " +
      'the deployment exists.'
  ),
  ...mkDomain(
    'CUSTOMS',
    'the shipment declaration',
    'the shipment declared its full contents accurately',
    'the shipment did NOT declare its full contents accurately',
    'Customs officer A, who inspected the shipment,',
    'Customs officer B, who inspected the same shipment independently,',
    'inspection report was filed for that shipment',
    'manifest cross-check record exists for the shipment',
    "A single photo of the shipment's contents exists, but several items are stacked out of " +
      'view, and the reviewing officer says it is impossible to tell from the image whether ' +
      'the declared list matches what is shown. No other inspection record exists.'
  ),
  ...mkDomain(
    'VETERINARY',
    "the animal's symptoms",
    'the animal showed symptoms of the disease before treatment',
    'the animal did NOT show symptoms of the disease before treatment',
    'Veterinarian A, who examined the animal at intake,',
    'Veterinarian B, an equally qualified vet who examined the same animal independently at intake,',
    'intake examination record was kept for the animal',
    'intake photo log exists for the animal',
    "A single intake photo of the animal exists, but the animal's fur obscures the area in " +
      'question, and the reviewing veterinarian says it is impossible to tell from the image ' +
      'whether the symptom was present at intake. No other examination record exists.'
  ),
  ...mkDomain(
    'AVIATION',
    "the aircraft's pre-flight check",
    "the aircraft's pre-flight check was completed",
    "the aircraft's pre-flight check was NOT completed",
    'Ground crew member A, who signed off on the checklist,',
    'Ground crew member B, who reviewed the same checklist independently,',
    'signed pre-flight checklist was filed for that aircraft',
    'hangar log recording the inspection time exists',
    'A single photo of the checklist board exists, but the final sign-off line is out of ' +
      'frame, and the maintenance supervisor who reviewed it says it is impossible to tell ' +
      'from the image whether that line was completed. No other record of the checklist exists.'
  ),
  ...mkDomain(
    'REALESTATE',
    'the property disclosure',
    'the property disclosure included the known defect',
    'the property disclosure did NOT include the known defect',
    'Realtor A, who prepared the disclosure form,',
    'Realtor B, who reviewed the same disclosure form independently,',
    'signed disclosure form was filed with the sale',
    'email correspondence referencing the disclosure exists',
    'A single scanned copy of the disclosure form exists, but the relevant checkbox is ' +
      'obscured by a coffee stain, and the title officer who reviewed it says it is ' +
      'impossible to tell from the scan whether that box was checked. No other copy of the ' +
      'form exists.'
  ),
];

async function runOne(item) {
  const result = await evaluate({
    model: 'typesafe-ai/jev',
    state: item.state,
    questions: {
      mu: item.mu,
      lambda: item.lambda,
      indeterminacy: item.indeterminacy,
    },
  });
  return { ...item, raw: result };
}

async function main() {
  if (!process.env.AI_GATEWAY_API_KEY) {
    console.error('Falta AI_GATEWAY_API_KEY en el entorno.');
    process.exit(1);
  }
  console.log(`Corriendo ${ITEMS.length} items (5 dominios x 5 categorias) contra typesafe-ai/jev...\n`);
  const results = [];
  for (const item of ITEMS) {
    try {
      const r = await runOne(item);
      results.push(r);
      const { mu, lambda, indeterminacy } = r.raw.answers;
      console.log(`[${r.id}] mu=${mu.probability} lambda=${lambda.probability} I=${indeterminacy.probability}`);
    } catch (err) {
      console.error(`[${item.id}] ERROR:`, err.message || err);
      results.push({ ...item, error: String(err.message || err) });
    }
  }
  await fs.writeFile('results_multidomain20_mli.json', JSON.stringify(results, null, 2), 'utf-8');

  // resumen por categoria
  const byCat = {};
  for (const r of results) {
    if (r.error) continue;
    const cat = r.category;
    byCat[cat] = byCat[cat] || { mu: [], lambda: [], I: [] };
    byCat[cat].mu.push(r.raw.answers.mu.probability);
    byCat[cat].lambda.push(r.raw.answers.lambda.probability);
    byCat[cat].I.push(r.raw.answers.indeterminacy.probability);
  }
  const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
  console.log('\n=== Resumen por categoria (media, n=5 por celda) ===');
  for (const [cat, v] of Object.entries(byCat)) {
    console.log(
      `${cat}: mu=${mean(v.mu).toFixed(2)} lambda=${mean(v.lambda).toFixed(2)} I=${mean(v.I).toFixed(2)}` +
        ` | rangos mu[${Math.min(...v.mu)}-${Math.max(...v.mu)}] lambda[${Math.min(...v.lambda)}-${Math.max(...v.lambda)}] I[${Math.min(...v.I)}-${Math.max(...v.I)}]`
    );
  }
  console.log('\nResultados guardados en results_multidomain20_mli.json');
}

main();
