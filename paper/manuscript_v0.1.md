# Modelos de evaluación tipada y el colapso entre conflicto e ignorancia: un estudio de caso sobre Jev

**Maikel Leyva-Vázquez**¹,²,³

¹ Universidad Bernardo O'Higgins (UBO), Santiago, Chile. ² Universidad Bolivariana del Ecuador (UBE), Guayaquil, Ecuador. ³ Universidad de Guayaquil, Guayaquil, Ecuador.

*Borrador v0.1 — destino: NCML. Nota de campo, no línea Q1 propia.*

---

## Resumen

Los modelos de chat basados en LLM devuelven texto libre que debe interpretarse; una categoría emergente de herramientas, los *modelos de evaluación tipada* ("System One models"), devuelven en su lugar un objeto tipado —una elección, un puntaje o una probabilidad calibrada— directamente utilizable por software. Jev (TypeSafe AI, lanzado el 15 de septiembre de 2026) es el primer ejemplo comercial de esta categoría y ya cuenta con réplicas de código abierto. Este trabajo lo ubica dentro de un panorama más amplio de cinco categorías de interacción con modelos de IA —mostrando que no es una categoría sin precedente, sino la convergencia entre un juez basado en LLM y un clasificador discriminativo clásico— y lo examina como caso de estudio, contrastando una predicción concreta derivada de la teoría de decisión anotada: que una salida colapsada a una sola probabilidad calibrada no puede distinguir *conflicto genuino* (evidencia fuerte y contradictoria) de *ignorancia genuina* (ausencia de evidencia), porque ambos estados producen el mismo punto de máxima incertidumbre. Un experimento mínimo (n=5 casos completados de 6, vía Vercel AI Gateway) confirma la predicción: los dos casos de conflicto (probabilidad 0,50–0,57) y los dos de ignorancia (0,46–0,48) son indistinguibles entre sí, mientras que un caso de control con evidencia clara produce 0,83. Se discute esta limitación como consecuencia estructural, no como defecto del producto, y se esboza una extensión natural basada en evidencia descompuesta y reglas de combinación tipo PCR6.

**Palabras clave:** modelos de evaluación tipada; System One models; LLM-as-judge; lógica paraconsistente anotada; colapso representacional; abstención tipada; Jev.

---

## 1. Introducción

Un modelo de chat convencional, ante la pregunta "¿se aprobó el reembolso?", puede responder "Sí, parece que sí, aunque no estoy completamente seguro..." — una cadena de texto no estructurada que el software que la consume debe volver a parsear o interpretar, sin un score explícito ni una garantía de formato. Una categoría de herramientas que emergió en septiembre de 2026, los *modelos de evaluación tipada*, invierte esa relación: se le entrega al modelo un *estado* (el contexto o la evidencia disponible) y un esquema de *preguntas*, cada una con un tipo declarado, y el modelo devuelve, para cada pregunta, un valor en ese tipo junto con una probabilidad calibrada — un objeto que el código que lo recibe puede usar directamente en una condición, sin interpretación intermedia.

TypeSafe AI llama a su primer modelo de este tipo "System One" — la contraparte rápida e intuitiva del razonamiento lento y deliberado ("System Two") que persiguen los LLM de frontera [1]. Jev no genera texto: selecciona entre las opciones de un esquema provisto por quien lo llama, por lo que —según el fabricante— devolver un valor mal formado o fuera del conjunto declarado es "matemáticamente imposible" [2]. Se reporta entre 20 y 200 veces más rápido y hasta 400 veces más barato que un LLM de frontera para esta clase de tareas [3], entrenado con un método propio, *Reinforcement Learning for Calibrated Decisions* (RLCD), que optimiza explícitamente la calibración de probabilidades para tareas de tipo System One, no la preferencia humana (RLHF) ni recompensas verificables (RLVR) [4].

A cuatro días de su lanzamiento, la categoría ya tiene ecosistema propio: reproducciones de código abierto como `decider` (fine-tune de Qwen3.5-2B con métricas completas de calibración — NLL, Brier, ECE, AURC, exactitud selectiva al 80 % de cobertura) [5] y `reflex` (reproducción local sobre Apple Silicon) [6], además de listas curadas de integraciones y cobertura periodística que ya advierte "mirar más allá del entusiasmo" [7].

Este trabajo no evalúa el rendimiento de Jev en sus tareas previstas (enrutamiento, clasificación, automatización de flujos) — para eso ya existen las métricas de calibración que el propio ecosistema reporta. Antes de examinarlo como caso de estudio (§3-§4), la §2 lo sitúa dentro de un panorama más amplio de categorías de interacción con modelos de IA, para no tratarlo como una novedad sin precedente. Luego se evalúa una pregunta distinta, de representación: **¿qué pierde necesariamente un modelo que colapsa evidencia a una sola probabilidad calibrada, y ese costo es visible en un producto real?**

## 2. Panorama de las categorías de interacción con modelos de IA

La oposición binaria "chat libre vs. tipado" de la Introducción simplifica demasiado el panorama real. La Figura 1 posiciona cinco categorías en dos ejes: qué tan flexible es el esquema de entrada (desde clases fijas decididas en tiempo de entrenamiento hasta lenguaje natural libre en tiempo de llamada) y qué tanto cuesta computacionalmente cada respuesta.

1. **Modelos de chat generativos** — texto libre, sin garantía de formato ni de tipo (GPT, Claude en modo conversación).
2. **LLM con salida forzada (*constrained decoding*)** — sigue siendo un modelo generativo de propósito general por debajo, pero en cada paso de generación se enmascaran a −∞ los logits de cualquier token que rompería una gramática o un esquema JSON declarado, garantizando que el resultado final sea válido [14]. El *function calling* de las APIs comerciales es un caso particular de esta técnica, donde el esquema nombra una herramienta a invocar. El costo sigue siendo el de un LLM completo: lo único que cambia es el formato de salida, no el motor que la produce.
3. **LLM-as-judge** — un LLM de frontera o afinado recibe un criterio de evaluación en lenguaje natural y devuelve un veredicto o puntaje, típicamente parseado de su respuesta en texto. Cuando se afina a una tarea específica para mejorar velocidad y costo, la literatura ya documenta que "degenera en un clasificador específico de tarea", sobreajustado, con una caída de rendimiento drástica fuera del dominio de entrenamiento [15] — exactamente el compromiso que un modelo de evaluación tipada busca evitar entrenando la calibración desde el principio, en vez de heredarla de un afinado posterior.
4. **Clasificadores discriminativos clásicos** — arquitecturas no generativas dedicadas (por ejemplo, un BERT afinado, o una cabeza evidencial tipo EDL), deterministas, con esquema de clases fijado en el entrenamiento. Es la opción más barata y rápida —del orden de 1-10 % del costo de un juez basado en LLM, con latencias de milisegundos de un solo dígito— pero la más rígida: cambiar las clases exige reentrenar.
5. **Jev y sus pares (modelos de evaluación tipada)** — el caso de estudio de este trabajo.

Jev no ocupa un lugar aislado en este mapa: se sitúa en la convergencia de las categorías 3 y 4. Hereda de la categoría 3 (juez basado en LLM) la flexibilidad de aceptar un esquema de preguntas en lenguaje natural, definido en tiempo de llamada y no en tiempo de entrenamiento; hereda de la categoría 4 (clasificador clásico) el costo bajo, la latencia mínima y la garantía de salida tipada por construcción, en vez de por post-procesamiento de una respuesta generada. El propio ecosistema de evaluación de LLM ya converge hacia arquitecturas de dos niveles en 2026 —un clasificador barato que resuelve la mayoría de los casos y escala a un juez de frontera solo cuando el caso es ambiguo [16]— que es, estructuralmente, la misma idea de cascada que la taxonomía de abstención tipada del programa del autor ya formaliza para la decisión bajo evidencia insuficiente o en disputa [12]. La contribución específica de Jev no es entonces una categoría sin precedente, sino una convergencia con un método de entrenamiento de calibración propio (RLCD, §1) — lo cual no reduce su utilidad práctica, pero sí cambia el marco correcto para evaluarlo: no contra "los LLM de chat" en abstracto, sino contra el resto de las categorías 2-4, con las que compite directamente.

![Figura 1](figures/fig1_taxonomy.png)

**Figura 1.** Posicionamiento de las cinco categorías de interacción con modelos de IA en los ejes flexibilidad de esquema (x) y costo computacional/latencia (y). Jev se ubica en la convergencia entre el juez basado en LLM (categoría 3, flexibilidad de esquema) y el clasificador discriminativo clásico (categoría 4, costo bajo y salida tipada garantizada). Fuente: elaboración propia.

## 3. Taxonomía verificada de tipos en Jev

La documentación oficial de TypeSafe [8] especifica exactamente tres primitivas de pregunta, evaluables en paralelo dentro de una misma llamada:

| Tipo | Qué hace | Qué devuelve |
|---|---|---|
| **Choice** | elegir una opción de un conjunto declarado | opción elegida + probabilidad por cada opción + confianza |
| **Score** | puntuar el estado sobre una rúbrica de niveles ordenados | puntaje + probabilidad por cada nivel + confianza |
| **Noul** | pregunta de sí/no | la probabilidad de que la respuesta sea "sí" |

No hay más tipos que estos tres. Un detalle relevante para este trabajo: la documentación del fabricante llama al tercer tipo **"Noul"**, no "Boolean", y lo describe explícitamente como devolviendo una probabilidad continua en [0,1] — no un valor discreto verdadero/falso. Sin embargo, el SDK de Vercel AI Gateway, que expone `experimental_evaluate` como interfaz de acceso, nombra ese mismo tipo **`boolean`** en su firma de API [9]. Dos fuentes oficiales del mismo fabricante etiquetan el mismo primitivo de forma distinta: una destaca su naturaleza continua (grado de verdad calibrado), la otra sugiere, por nomenclatura, un valor discreto. Esta discrepancia no es solo terminológica: un desarrollador que solo lea la documentación del SDK puede razonablemente esperar un `true`/`false`, cuando lo que realmente recibe es una probabilidad — la misma ambigüedad que la lógica anotada y la neutrosófica resuelven mediante coordenadas explícitas en vez de un nombre de tipo.

## 4. La pregunta representacional

En el marco de lógica paraconsistente anotada (LPA2v) [10], un juicio se representa como un par independiente (μ, λ) — grado de evidencia favorable y grado de evidencia contraria — sin que nada obligue a μ + λ ≤ 1. Dos vértices distinguidos del retículo resultante son el estado **⊤** (inconsistente: μ y λ ambos altos, evidencia fuerte en ambos sentidos) y el estado **⊥** (paracompleto: μ y λ ambos bajos, ausencia de evidencia en cualquier sentido). Estos dos estados son *epistemológicamente opuestos* —uno es exceso de información contradictoria, el otro es carencia total de información— pero comparten una propiedad geométrica: ambos están igual de lejos de los vértices ideales "verdadero" y "falso" [11].

De ahí se sigue un resultado ya formalizado: todo score de cercanía a esos vértices ideales —el grado de certeza del para-analizador, cualquier variante de TOPSIS con norma de Minkowski, el score neutrosófico estándar— es invariante bajo la involución de conflación ρ que intercambia ⊤ y ⊥ [11]. En términos llanos: **un score colapsado no puede distinguir "la evidencia se contradice fuertemente" de "no hay evidencia"**, porque ambos producen el mismo valor de incertidumbre máxima.

Un modelo de evaluación tipada que devuelve una sola probabilidad calibrada por pregunta —exactamente lo que hace el tipo Noul de Jev— es, estructuralmente, un score de este tipo. La predicción es directa: si se le presenta a Jev un caso de conflicto genuino (dos fuentes igualmente creíbles que se contradicen) y un caso de ignorancia genuina (ausencia total de evidencia), ambos deberían producir probabilidades cercanas entre sí y cercanas a 0,5 — indistinguibles para cualquier sistema que consuma esa probabilidad sin más contexto.

## 5. Método

Se diseñaron seis estados (`state`) en inglés, todos formulados sobre el mismo hecho de dominio (si un semáforo estaba en rojo), en cuatro categorías:

- **TORN** (conflicto genuino, n=2): dos fuentes igualmente confiables —testigos bajo juramento o sensores calibrados— reportan valores opuestos sobre el mismo hecho, en el mismo instante.
- **SILENT** (ignorancia genuina, n=2): ausencia documentada de cualquier testigo, cámara o registro.
- **AGREE-SUPPORT** (control, n=1): dos fuentes independientes concuerdan en que el semáforo estaba en rojo.
- **AGREE-REFUTE** (control, n=1): dos fuentes independientes concuerdan en que el semáforo estaba en verde (no rojo).

Para cada estado se hizo una sola llamada a `typesafe-ai/jev` vía la función `experimental_evaluate` del SDK `ai` (v7.0.107) de Vercel, expuesta a través del AI Gateway, con una única pregunta de tipo `boolean`: *"Was the traffic light red at the time in question?"*. No se promediaron repeticiones (limitación reconocida en §8). Las llamadas se hicieron el 19 de septiembre de 2026 contra el modelo en producción, sin acceso a sus pesos ni a su conjunto de entrenamiento.

## 6. Resultados

| Caso | Categoría | P(rojo) |
|---|---|---|
| TORN-1 | conflicto genuino (testigos contradictorios) | 0,57 |
| TORN-2 | conflicto genuino (sensores contradictorios) | 0,50 |
| SILENT-1 | ignorancia genuina (sin testigos ni cámaras) | 0,46 |
| SILENT-2 | ignorancia genuina (registro perdido) | 0,48 |
| AGREE-SUPPORT | control: ambas fuentes de acuerdo (apoyo) | 0,83 |
| AGREE-REFUTE | control: ambas fuentes de acuerdo (refutación) | *sin datos — limitación del nivel gratuito, ver §8* |

Los dos casos TORN (0,50–0,57) y los dos casos SILENT (0,46–0,48) caen en una banda estrecha común, sin separación visible entre categorías. El único caso completado con evidencia inequívoca (AGREE-SUPPORT) produce una probabilidad marcadamente distinta y alejada de 0,5 (0,83), lo que descarta que el modelo simplemente devuelva valores cercanos a 0,5 por defecto: cuando la evidencia es clara, el modelo lo refleja con claridad.

## 7. Discusión

El patrón observado es exactamente el predicho en §4: Jev distingue *evidencia clara* de *evidencia no clara*, pero no distingue **por qué** no es clara. Un sistema río abajo que reciba solo la probabilidad 0,48 no puede saber si debe (a) pedir más evidencia porque no hay ninguna, o (b) escalar a un humano porque dos fuentes fiables se contradicen — dos acciones correctas completamente distintas, para las que la taxonomía de abstención tipada ya distingue tipos formales separados (ignorancia/inespecificidad vs. conflicto/discordia) [12].

Esto no es un defecto de ingeniería de Jev — es la consecuencia esperable de que el *tipo* Noul, por diseño, comprime la evidencia a un solo número antes de que el llamador pueda inspeccionar su composición. La misma limitación se aplicaría, por la misma razón formal, a cualquier modelo de evaluación tipada que devuelva una probabilidad calibrada única en vez de evidencia descompuesta — incluidas las réplicas de código abierto de la categoría [5,6], y en general a la categoría 4 completa del panorama de la §2 cuando se implementa con una sola cabeza de salida.

Una extensión natural, no evaluada aquí, sería un modelo de evaluación tipada que en vez de una sola probabilidad devuelva **evidencia no negativa separada** por hipótesis (a favor, en contra, e idealmente una masa de "conflicto" explícita) — lo que permitiría, en una capa posterior, aplicar una regla de combinación tipo PCR6 que redistribuya proporcionalmente el conflicto detectado en vez de promediarlo con la ignorancia. Esa dirección conecta directamente con el trabajo en curso del programa de razonamiento evidencial del autor [13] y queda fuera del alcance de esta nota de campo.

## 8. Limitaciones

Este es un estudio mínimo, no una evaluación exhaustiva: (a) n=5 casos completados (6 diseñados), sobre un solo hecho de dominio (semáforos) y un solo tipo de pregunta (`boolean`/Noul) de los tres que ofrece Jev; (b) una sola llamada por caso, sin repetición para estimar varianza del propio modelo; (c) el caso de control AGREE-REFUTE no se pudo completar por el límite de tasa del nivel gratuito del AI Gateway, incluso tras añadir un método de pago — el proveedor distingue entre "tarjeta en archivo" y "créditos de pago cargados", y el segundo requisito no se cumplió en el momento del experimento; (d) es un producto de cuatro días de antigüedad al momento de escribir esto — su comportamiento, documentación y límites de tasa pueden cambiar sin aviso, y estos resultados deben leerse como una fotografía del 19-sep-2026, no como una caracterización estable; (e) no hay forma de verificar independientemente el método de entrenamiento (RLCD) declarado por el fabricante — se reporta tal como lo documenta la fuente primaria [4], sin auditoría propia; (f) la taxonomía de cinco categorías de la §2 es una síntesis propia de fuentes secundarias, no una revisión sistemática de la literatura de *constrained decoding* y *LLM-as-judge*.

## 9. Conclusión

Los modelos de evaluación tipada representan una mejora genuina de costo, velocidad y estructura frente a los LLM de chat para tareas de decisión automatizada, y no surgen de la nada: son la convergencia entre el juez basado en LLM (flexibilidad de esquema) y el clasificador discriminativo clásico (costo y determinismo). Pero heredan, por diseño representacional, el mismo colapso entre conflicto e ignorancia que ya está caracterizado formalmente en la teoría de decisión anotada y neutrosófica: una probabilidad calibrada única no puede, por construcción, portar simultáneamente la intensidad del apoyo, la intensidad de la oposición y la magnitud total de evidencia disponible. Tratar esa probabilidad como suficiente para automatizar una decisión sin inspeccionar su origen arriesga tratar por igual "no sé" y "no me pongo de acuerdo" — dos motivos de abstención que exigen respuestas operativas distintas.

---

## Referencias

[1] TypeSafe AI. *Introducing System One Models & Jev*. TypeSafe AI Blog, 15-sep-2026. https://typesafe.ai/blog/introducing-system-one-models-and-jev

[2] DataCamp. *Jev: TypeSafe's System One Model That Never Hallucinates*. https://www.datacamp.com/blog/system-one-models-jev

[3] Vercel. *TypeSafe AI's Jev now available on AI Gateway*. Vercel Changelog. https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway

[4] explainx.ai. *How Does Jev Work? RLCD & Parallel Inference Explained*. 2026. https://www.explainx.ai/blog/how-does-jev-work-rlcd-system-one-model-explained-2026

[5] Mapika. *decider: One-pass typed decisions with calibrated probabilities, fine-tuned from Qwen3.5-2B*. GitHub. https://github.com/Mapika/decider

[6] nateGeorge. *reflex: A small open decision model — a Jev / System One re-creation on Qwen3.5*. GitHub. https://github.com/nateGeorge/reflex

[7] Eliot, L. *New 'Reinforcement Learning For Calibrated Decisions' Makes AI Headlines But Look Past The Hype*. Forbes, 18-sep-2026.

[8] TypeSafe AI. *Introduction — Question Types*. https://docs.typesafe.ai/introduction

[9] Vercel. *Jev API, Pricing & Playground*. AI Gateway Models. https://vercel.com/ai-gateway/models/jev

[10] da Costa, N.C.A., Abe, J.M., Subrahmanian, V.S. (1991). Remarks on annotated logic. *Zeitschrift für Mathematische Logik und Grundlagen der Mathematik*, 37.

[11] Leyva-Vázquez, M. (2026). *Conflation-Invariant TOPSIS Scores and Panel-Level Abstention in Annotated Evidence* [manuscrito en preparación]. Preprint SSRN 7441661.

[12] [autocitar taxonomía de 7 tipos de abstención del programa de razonamiento evidencial — nodo interno, formalizar cita pública cuando el Paper 4 se publique]

[13] Leyva-Vázquez, M. et al. *Deep PCR6: programa empírico de fusión evidencial* [en preparación, no público].

[14] *Flexible and Efficient Grammar-Constrained Decoding*. arXiv:2502.05111, 2026.

[15] *An Empirical Study of LLM-as-a-Judge for LLM Evaluation: Fine-tuned Judge Model is not a General Substitute for GPT-4*. arXiv:2403.02839.

[16] *A survey on LLM-as-a-judge*. ScienceDirect, 2026. https://www.sciencedirect.com/science/article/pii/S2666675825004564

---

*Datos y script del experimento: `Documents\NCML_Jev_TypedModels_2026\experiment\` (`run_experiment.mjs`, `results.json`). Figura: `Documents\NCML_Jev_TypedModels_2026\paper\figures\make_fig1_taxonomy.py`. Reproducible con una llave de AI Gateway propia.*
