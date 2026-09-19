# Modelos de evaluación tipada y el colapso entre conflicto e ignorancia: un estudio de caso sobre Jev

**Maikel Leyva-Vázquez**¹,²,³

¹ Universidad Bernardo O'Higgins (UBO), Santiago, Chile. ² Universidad Bolivariana del Ecuador (UBE), Guayaquil, Ecuador. ³ Universidad de Guayaquil, Guayaquil, Ecuador.

*Borrador v0.2 — destino: NCML. Nota de campo, no línea Q1 propia. Revisión aplicada tras ronda adversarial de 5 modelos y un segundo experimento (tipo Choice).*

---

## Resumen

Los modelos de chat basados en LLM devuelven texto libre que debe interpretarse; una categoría de herramientas que emergió en septiembre de 2026, los *modelos de evaluación tipada* ("System One models"), devuelven en su lugar un objeto tipado directamente utilizable por software. Jev (TypeSafe AI, reportado por el fabricante como lanzado el 15 de septiembre de 2026) es el primer ejemplo comercial de esta categoría. Este trabajo lo ubica dentro de un panorama de cinco categorías de interacción con modelos de IA y examina, con un experimento mínimo, una predicción derivada de la teoría de decisión anotada: que una salida colapsada a una sola probabilidad calibrada no puede distinguir *conflicto genuino* de *ignorancia genuina*. Para el tipo de pregunta más simple de Jev (`boolean`/Noul), el experimento es consistente con esa predicción: los casos de conflicto (probabilidad 0,50–0,57) y de ignorancia (0,46–0,48) caen en la misma banda estrecha, indistinguibles sin más contexto. Pero un segundo experimento, con el tipo `Choice` del mismo modelo y un esquema que nombra explícitamente "evidencia en conflicto" y "evidencia insuficiente" como opciones, separa ambos casos con probabilidad 1,0 en los cuatro casos completados. El hallazgo central, por tanto, no es que Jev colapse per se, sino que **el mismo modelo preserva o destruye la distinción según el tipo de pregunta y el esquema que se le declare** — un riesgo de diseño de interfaz, no una limitación intrínseca de la categoría. Se discuten las implicaciones para quien construya sobre modelos de evaluación tipada, y se identifica una pregunta abierta concreta para trabajo futuro.

**Palabras clave:** modelos de evaluación tipada; System One models; LLM-as-judge; lógica paraconsistente anotada; colapso representacional; abstención tipada; Jev.

---

## 1. Introducción

Un modelo de chat convencional, ante la pregunta "¿se aprobó el reembolso?", puede responder "Sí, parece que sí, aunque no estoy completamente seguro..." — una cadena de texto no estructurada que el software que la consume debe volver a parsear o interpretar, sin un score explícito ni una garantía de formato. Una categoría de herramientas que emergió en septiembre de 2026, los *modelos de evaluación tipada*, invierte esa relación: se le entrega al modelo un *estado* (el contexto o la evidencia disponible) y un esquema de *preguntas*, cada una con un tipo declarado, y el modelo devuelve, para cada pregunta, un valor en ese tipo junto con una probabilidad calibrada.

TypeSafe AI llama a su primer modelo de este tipo "System One" — la contraparte rápida e intuitiva del razonamiento lento y deliberado ("System Two") que persiguen los LLM de frontera [1]. Según el fabricante, Jev no genera texto: selecciona entre las opciones de un esquema provisto por quien lo llama, por lo que devolver un valor mal formado o fuera del conjunto declarado sería estructuralmente imposible [2] — una garantía de formato, no una garantía de corrección del contenido. El fabricante reporta entre 20 y 200 veces más velocidad y hasta 400 veces menos costo que un LLM de frontera para esta clase de tareas [3], y un método de entrenamiento propio, *Reinforcement Learning for Calibrated Decisions* (RLCD), orientado a calibración explícita [4]. Ninguna de estas cifras fue auditada de forma independiente en este trabajo; se reportan como afirmaciones del fabricante, no como hechos verificados.

Este trabajo no evalúa el rendimiento de Jev en sus tareas previstas. Antes de examinarlo como caso de estudio (§3-§6), la §2 lo sitúa dentro de un panorama más amplio de categorías de interacción con modelos de IA. Luego se examina una pregunta de representación —¿qué pierde un modelo que colapsa evidencia a una sola probabilidad calibrada?— y, a partir de un hallazgo inesperado en el propio experimento, se refina esa pregunta hacia una más precisa: **¿la pérdida es del modelo, o del tipo de interfaz elegido para consultarlo?**

## 2. Panorama de las categorías de interacción con modelos de IA

La oposición binaria "chat libre vs. tipado" simplifica demasiado el panorama real. La Figura 1 posiciona cinco categorías en dos ejes: flexibilidad del esquema de entrada y costo computacional.

1. **Modelos de chat generativos** — texto libre, sin garantía de formato ni de tipo.
2. **LLM con salida forzada (*constrained decoding*)** — sigue siendo un modelo generativo de propósito general por debajo, pero en cada paso de generación se restringe el espacio de tokens válidos según una gramática o esquema JSON declarado [12]. El costo sigue siendo el de un LLM completo.
3. **LLM-as-judge** — un LLM de frontera o afinado evalúa según un criterio en lenguaje natural. Cuando se afina a una tarea específica, la literatura documenta que puede degenerar en un clasificador de dominio cerrado, con caída de rendimiento fuera de ese dominio [13].
4. **Clasificadores discriminativos clásicos** — arquitecturas no generativas dedicadas (p. ej. un BERT afinado, o una cabeza evidencial tipo EDL), deterministas, con esquema de clases fijado en el entrenamiento. Se reporta como sustancialmente más barato y rápido que un juez basado en LLM, aunque la cifra exacta varía según la fuente y no se toma aquí como dato preciso.
5. **Jev y sus pares (modelos de evaluación tipada)** — el caso de estudio de este trabajo.

**Nota sobre esta taxonomía:** no es una partición estricta. Las categorías 2 y 3 pueden superponerse en la práctica —un juez basado en LLM puede usar salida forzada para garantizar un veredicto en JSON válido— y se presentan como ejes heurísticos (uso, técnica de decodificación, arquitectura, costo) más que como clases mutuamente excluyentes. Es una síntesis propia de fuentes secundarias, no una revisión sistemática de la literatura de *constrained decoding* y *LLM-as-judge*.

Con esa salvedad, Jev se sitúa en la convergencia de las categorías 3 y 4: hereda de la 3 la flexibilidad de un esquema de preguntas declarado en tiempo de llamada, y de la 4 el costo bajo y la garantía de salida tipada por construcción. El ecosistema de evaluación de LLM converge hacia arquitecturas de dos niveles en 2026 —un clasificador barato que resuelve la mayoría de los casos y escala a un juez de frontera solo cuando el caso es ambiguo [14]— que es, estructuralmente, la misma cascada que una taxonomía de abstención tipada ya formaliza para la decisión bajo evidencia insuficiente o en disputa (síntesis propia del programa de investigación del autor, sin publicar; ver nota en §7).

![Figura 1](figures/fig1_taxonomy.png)

**Figura 1.** Posicionamiento de las cinco categorías de interacción con modelos de IA. Jev se ubica en la convergencia entre el juez basado en LLM (categoría 3) y el clasificador discriminativo clásico (categoría 4). Fuente: elaboración propia.

## 3. Taxonomía verificada de tipos en Jev

La documentación del fabricante [8] especifica tres primitivas de pregunta, evaluables en paralelo dentro de una misma llamada:

| Tipo | Qué hace | Qué devuelve |
|---|---|---|
| **Choice** | elegir una opción de un conjunto declarado (`criteria`: mapa de opción → descripción) | opción elegida + probabilidad por cada opción |
| **Score** | puntuar el estado sobre una rúbrica de niveles ordenados | puntaje + probabilidad por cada nivel |
| **Noul** | pregunta de sí/no | la probabilidad de que la respuesta sea "sí" |

La documentación llama al tercer tipo "Noul", no "Boolean", y lo describe como una probabilidad continua en [0,1] — no un valor discreto. El SDK de Vercel AI Gateway, que expone `experimental_evaluate` como interfaz de acceso, nombra ese mismo tipo `boolean` en su firma de API [9]. Verificado directamente contra el objeto de respuesta (§5): el campo `providerMetadata.typesafe.confidence` existe en el esquema pero llega **vacío (`{}`)** en los cinco casos ejecutados con el tipo `boolean` — no hay, en ese tipo, ningún campo adicional de confianza o composición de evidencia más allá de la probabilidad única.

## 4. La pregunta representacional

En el marco de lógica paraconsistente anotada (LPA2v) [10], un juicio se representa como un par independiente (μ, λ). Dos vértices del retículo resultante, **⊤** (evidencia fuerte en ambos sentidos) y **⊥** (ausencia de evidencia en cualquier sentido), son epistemológicamente opuestos pero comparten una propiedad geométrica: ambos están igual de lejos de los vértices "verdadero" y "falso" [11]. De ahí un resultado ya formalizado: todo score de cercanía a esos vértices es invariante bajo la involución que intercambia ⊤ y ⊥ [11].

Este trabajo no aplica ese teorema de forma literal a Jev — hacerlo exigiría que Jev calculara explícitamente un par (μ, λ) independiente, cosa que no está documentada. La conexión es una analogía motivadora, no una consecuencia deductiva del teorema. El argumento que sí es deductivamente válido, y que este trabajo pone a prueba, es más simple: **ningún mapa de un espacio de evidencia de dos o más dimensiones (apoyo, oposición, magnitud, insuficiencia) a un único escalar en [0,1] puede ser inyectivo**; dos estados de evidencia distintos pueden, por pura cardinalidad, colapsar al mismo número. Un modelo que solo expone ese escalar —como el tipo Noul de Jev— no puede, en principio, garantizar que conflicto e ignorancia produzcan valores distintos.

## 5. Método

Se diseñaron seis estados (`state`) en inglés sobre el mismo hecho de dominio (si un semáforo estaba en rojo), en cuatro categorías: **TORN** (conflicto genuino, n=2, dos fuentes igualmente confiables que se contradicen), **SILENT** (ignorancia genuina, n=2, ausencia documentada de evidencia), **AGREE-SUPPORT** (control, n=1, fuentes que concuerdan en "rojo") y **AGREE-REFUTE** (control, n=1, fuentes que concuerdan en "no rojo"). Los seis estados completos están disponibles en el repositorio de datos (§10).

**Experimento 1 (tipo `boolean`/Noul):** una llamada por estado a `typesafe-ai/jev` vía `experimental_evaluate` del SDK `ai` v7.0.107, pregunta única: *"Was the traffic light red at the time in question?"*

**Experimento 2 (tipo `Choice`, de seguimiento):** los mismos seis estados, una sola pregunta `lightState` de tipo `choice` con cuatro opciones explícitas: `red`, `green`, `conflicting_evidence` ("reliable sources disagree with each other about the color") e `insufficient_evidence` ("there is no evidence available to determine the color"). Este segundo experimento se diseñó *después* de observar los resultados del Experimento 1, a partir de una revisión adversarial que señaló la necesidad de probar si el colapso era propio del modelo o del tipo de pregunta — se declara explícitamente como no preregistrado y motivado por los datos.

Ninguno de los dos experimentos promedia repeticiones (una sola llamada por caso; limitación en §8). Las llamadas se hicieron el 19 de septiembre de 2026 contra el modelo en producción, sin acceso a sus pesos ni a su conjunto de entrenamiento.

## 6. Resultados

**Experimento 1 — tipo `boolean`/Noul:**

| Caso | Categoría | P(rojo) |
|---|---|---|
| TORN-1 | conflicto genuino (testigos contradictorios) | 0,57 |
| TORN-2 | conflicto genuino (sensores contradictorios) | 0,50 |
| SILENT-1 | ignorancia genuina (sin testigos ni cámaras) | 0,46 |
| SILENT-2 | ignorancia genuina (registro perdido) | 0,48 |
| AGREE-SUPPORT | control: fuentes de acuerdo (apoyo) | 0,83 |
| AGREE-REFUTE | control: fuentes de acuerdo (refutación) | sin datos (rate-limit, §8) |

Los dos casos TORN (0,50–0,57) y los dos SILENT (0,46–0,48) caen en una banda común y estrecha. El único control completado con evidencia inequívoca (AGREE-SUPPORT) produce 0,83, alejado de 0,5.

**Experimento 2 — tipo `Choice` con esquema enriquecido:**

| Caso | Categoría | Elección de Jev | P(elección) |
|---|---|---|---|
| TORN-1 | conflicto genuino | *conflicting_evidence* | 1,00 |
| TORN-2 | conflicto genuino | *conflicting_evidence* | 1,00 |
| SILENT-1 | ignorancia genuina | *insufficient_evidence* | 1,00 |
| SILENT-2 | ignorancia genuina | *insufficient_evidence* | 1,00 |
| AGREE-SUPPORT | control: fuentes de acuerdo | *red* | 1,00 |
| AGREE-REFUTE | control: fuentes de acuerdo | sin datos (rate-limit, §8) | — |

Con el tipo `Choice` y un esquema que nombra explícitamente "evidencia en conflicto" y "evidencia insuficiente" como opciones de primera clase, Jev separa los cuatro casos experimentales (TORN vs. SILENT) con probabilidad máxima y sin ambigüedad, y clasifica correctamente el control de apoyo. La misma evidencia textual que colapsó a una banda de 0,46–0,57 bajo el tipo `boolean` produce una distinción perfecta bajo el tipo `Choice`.

## 7. Discusión

El patrón del Experimento 1 es consistente con la predicción de la §4: bajo el tipo Noul, Jev no distingue *por qué* la evidencia no es clara. Pero el Experimento 2 obliga a corregir la interpretación: **la pérdida no es una propiedad del modelo Jev, sino del tipo de pregunta y del esquema declarados para consultarlo.** El tipo `boolean` fuerza, por definición, una salida en un espacio de un solo grado de libertad — no hay forma de que devuelva "conflicto" o "insuficiencia" aunque internamente el modelo los distinga. El tipo `Choice`, cuando el esquema incluye esas categorías como opciones nombradas, sí tiene espacio representacional para expresarlas, y el modelo lo aprovecha con una nitidez que no se anticipaba (probabilidad 1,0, no una tendencia difusa).

Esto reencuadra la contribución del trabajo: no es "Jev tiene una limitación representacional inherente", sino **"el diseño del esquema de consulta determina si la distinción sobrevive, y el tipo más simple y barato de usar (Noul, una sola pregunta de sí/no) es precisamente el que la destruye por construcción"**. Es un riesgo de uso, no un defecto de ingeniería del producto — y es trasladable a cualquier sistema que, por conveniencia, reduzca una decisión compleja a una pregunta de sí/no en vez de a una elección entre un conjunto de estados epistémicos nombrados explícitamente.

Queda una pregunta abierta que este trabajo no resuelve: ¿el tipo `Choice` separa los casos porque *puede* representar la distinción, o porque el esquema usado ya nombraba "conflicto" e "insuficiencia" como opciones disponibles? Es decir, ¿un `Choice` con solo dos opciones (`red`/`green`, sin las categorías de escape) reproduciría el mismo colapso que Noul, repartiendo probabilidad ambigua entre ambas? Este trabajo no corrió esa condición adicional — es el experimento de seguimiento más obvio y barato para una próxima iteración, y se señala explícitamente en vez de asumir una respuesta.

Dicho esto, el argumento deductivo de la §4 (ningún escalar único puede ser inyectivo sobre un espacio de evidencia de mayor dimensión) sigue aplicando al tipo Noul específicamente, y a cualquier interfaz —de Jev o de sus réplicas [5,6]— que fuerce una salida de un solo grado de libertad. La recomendación práctica para quien construya sobre modelos de evaluación tipada es concreta: si la distinción entre conflicto e ignorancia importa para la decisión río abajo, no usar el tipo booleano más simple disponible; usar un tipo con un esquema de opciones que nombre esos estados explícitamente, como ya permite la propia API de Jev.

## 8. Limitaciones

(a) n=5 casos completados de 6 por experimento (el control AGREE-REFUTE falló por límite de tasa del nivel gratuito de Vercel AI Gateway en ambos experimentos, incluso con un método de pago ya registrado — el proveedor exige créditos de pago cargados, no solo una tarjeta en archivo, y ese paso no se completó); (b) una sola llamada por caso en cada experimento, sin repetición para estimar varianza; (c) el Experimento 2 fue motivado por los resultados del Experimento 1 y no estaba preregistrado — se declara así explícitamente; (d) no se probó si un esquema `Choice` con solo las opciones originales (`red`/`green`, sin categorías de escape) también colapsaría — pregunta abierta señalada en §7; (e) es un producto de cuatro días de antigüedad al momento de escribir esto — su comportamiento y límites pueden cambiar sin aviso, y estos resultados son una fotografía del 19-sep-2026; (f) las cifras de velocidad, costo y método de entrenamiento (RLCD) son afirmaciones del fabricante, no auditadas de forma independiente en este trabajo; (g) la taxonomía de cinco categorías de la §2 es síntesis propia, no revisión sistemática.

## 9. Conclusión

El experimento inicial de este trabajo pareció confirmar que los modelos de evaluación tipada heredan, por diseño representacional, el colapso entre conflicto e ignorancia ya caracterizado en la teoría de decisión anotada. Un segundo experimento, motivado por revisión adversarial, mostró que esa conclusión era incompleta: el mismo modelo, consultado con un tipo de pregunta distinto y un esquema más rico, separa ambos estados con probabilidad máxima. La lección que sobrevive no es sobre los límites de Jev como producto, sino sobre el riesgo de reducir decisiones epistémicamente complejas al tipo de interfaz más simple disponible. Un escalar único —sea un score de cercanía en un retículo anotado o una probabilidad calibrada de un modelo comercial— no puede, por construcción, distinguir "no sé" de "no nos ponemos de acuerdo"; pero la solución no requiere una arquitectura nueva ni una extensión teórica: puede bastar con nombrar esos dos estados como opciones explícitas del esquema, algo que la propia interfaz ya permite y que este trabajo no había probado hasta someterse a revisión.

---

## 10. Referencias y datos

**Referencias**

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

[12] *Flexible and Efficient Grammar-Constrained Decoding*. arXiv:2502.05111, 2026.

[13] *An Empirical Study of LLM-as-a-Judge for LLM Evaluation: Fine-tuned Judge Model is not a General Substitute for GPT-4*. arXiv:2403.02839.

[14] *A survey on LLM-as-a-judge*. ScienceDirect, 2026.

**Datos y código:** `Documents\NCML_Jev_TypedModels_2026\experiment\` — `run_experiment.mjs` + `results.json` (Experimento 1), `run_experiment_choice.mjs` + `results_choice.json` (Experimento 2). Figura: `paper\figures\make_fig1_taxonomy.py`. Reproducible con una llave propia de AI Gateway.
