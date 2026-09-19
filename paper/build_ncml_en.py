# -*- coding: utf-8 -*-
"""Formats the Jev / typed evaluation models manuscript (v0.3, English) to the NCML template.
Corresponding author = UG (per Maikel's instruction for this submission)."""
import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING

TPL = r"C:\Users\HP\Documents\NCML_Formato_y_Ejemplo\NCML-paper-template.docx"
FIG = r"C:\Users\HP\Documents\NCML_Jev_TypedModels_2026\paper\figures"
OUT = r"C:\Users\HP\Documents\NCML_Jev_TypedModels_2026\paper\manuscript_v0.3_EN_NCML.docx"

doc = Document(TPL)
body = doc.element.body
for child in list(body):
    if not child.tag.endswith('}sectPr'):
        body.remove(child)

S = {s.name for s in doc.styles}


def P(text="", style="Paper text", align=None, size=None, bold=False, italic=False):
    st = style if style in S else "Normal"
    p = doc.add_paragraph(style=st)
    if align is not None:
        p.alignment = align
    if text:
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        if size:
            r.font.size = Pt(size)
    return p


def rich(parts, style="Paper text", align=None):
    st = style if style in S else "Normal"
    p = doc.add_paragraph(style=st)
    if align is not None:
        p.alignment = align
    for t, o in parts:
        r = p.add_run(t)
        r.bold = o.get("bold", False)
        r.italic = o.get("italic", False)
        if o.get("size"):
            r.font.size = Pt(o["size"])
    return p


def table(headers, rows, legend):
    P(legend, "16_Table_Legend")
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.autofit = True
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = ""
        r = c.paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            r = cells[i].paragraphs[0].add_run(v)
            r.font.size = Pt(9)
            cells[i].paragraphs[0].alignment = (
                WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER)
    P("Source: own elaboration.", "16_Table_Legend")
    return t


def code_block(text, size=8):
    for line in text.strip("\n").split("\n"):
        p = doc.add_paragraph(style="Paper text" if "Paper text" in S else "Normal")
        pf = p.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        r = p.add_run(line if line.strip() else " ")
        r.font.name = "Courier New"
        r.font.size = Pt(size)
    p2 = doc.add_paragraph(style="Paper text" if "Paper text" in S else "Normal")
    p2.paragraph_format.space_after = Pt(6)


def figure(img, caption, width_cm=13.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.space_before = Pt(8)
    pf.space_after = Pt(2)
    p.add_run().add_picture(os.path.join(FIG, img), width=Cm(width_cm))
    P(caption, "13_Figure_Caption", align=WD_ALIGN_PARAGRAPH.CENTER)


# ------------------------------------------------------------------ cover
P("Typed Evaluation Models and the Collapse Between Conflict and Ignorance: "
  "A Case Study on Jev", "Title of the Journal", WD_ALIGN_PARAGRAPH.CENTER)
P("Modelos de evaluación tipada y el colapso entre conflicto e ignorancia: "
  "un estudio de caso sobre Jev", "Normal", WD_ALIGN_PARAGRAPH.CENTER, size=12, italic=True)
P()
P("Maikel Yelandi Leyva Vázquez 1,2,3,*", "Authors", WD_ALIGN_PARAGRAPH.CENTER)

afil = [
    "1 Universidad Bernardo O'Higgins, Santiago, Chile.",
    "2 Universidad Bolivariana del Ecuador, Guayaquil, Ecuador.",
    "3 Universidad de Guayaquil, Guayaquil, Ecuador. E-mail: maikel.leyvav@ug.edu.ec. "
    "ORCID: https://orcid.org/0000-0001-7911-5879",
]
for a in afil:
    P(a, "05_Keywords", WD_ALIGN_PARAGRAPH.CENTER, size=8)
P("* Corresponding author: maikel.leyvav@ug.edu.ec",
  "05_Keywords", WD_ALIGN_PARAGRAPH.CENTER, size=8)
P()

# ------------------------------------------------------------------ abstracts
rich([("Abstract. ", {"bold": True}),
      ("Chat-based LLMs return free text that must be interpreted; a category of tools that "
       "emerged in September 2026, typed evaluation models (\"System One models\"), instead "
       "return a typed object directly usable by software. Jev (TypeSafe AI, reported by the "
       "vendor as launched on September 15, 2026) is the first commercial example of this "
       "category. This work situates it within a five-category landscape of AI model "
       "interaction and tests, with a minimal experiment, a prediction derived from annotated "
       "decision theory: that an output collapsed to a single calibrated probability cannot "
       "distinguish genuine conflict from genuine ignorance. For Jev's simplest question type "
       "(boolean/Noul), the experiment is consistent with that prediction: conflict cases "
       "(probability 0.50-0.57) and ignorance cases (0.46-0.48) fall within the same narrow "
       "band. But a second experiment, using the same model's Choice type with a schema that "
       "explicitly names \"conflicting evidence\" and \"insufficient evidence\" as options, "
       "separates both cases with probability 1.0 in all four completed cases. A third "
       "experiment, with Choice restricted to the two original options (no escape categories), "
       "reproduces neither the collapse nor the clean separation: an unanticipated directional "
       "bias appears, possibly tied to lexical cues in the input text. The central finding is "
       "therefore not that Jev collapses per se, but that the same model preserves, destroys, "
       "or unpredictably distorts the distinction depending on the question type and declared "
       "schema — an interface design risk more complex than a single follow-up experiment "
       "could anticipate.", {})],
     "Abstract")
rich([("Keywords: ", {"bold": True}),
      ("typed evaluation models; System One models; LLM-as-judge; annotated paraconsistent "
       "logic; representational collapse; typed abstention; Jev.", {})], "Keywords")
P()
rich([("Resumen. ", {"bold": True}),
      ("Los modelos de chat basados en LLM devuelven texto libre que debe interpretarse; una "
       "categoría de herramientas que emergió en septiembre de 2026, los modelos de evaluación "
       "tipada (\"System One models\"), devuelven en su lugar un objeto tipado directamente "
       "utilizable por software. Jev (TypeSafe AI, reportado por el fabricante como lanzado el "
       "15 de septiembre de 2026) es el primer ejemplo comercial de esta categoría. Este trabajo "
       "lo ubica dentro de un panorama de cinco categorías de interacción con modelos de IA y "
       "examina, con un experimento mínimo, una predicción derivada de la teoría de decisión "
       "anotada: que una salida colapsada a una sola probabilidad calibrada no puede distinguir "
       "conflicto genuino de ignorancia genuina. Para el tipo de pregunta más simple de Jev "
       "(boolean/Noul), el experimento es consistente con esa predicción. Un segundo "
       "experimento, con el tipo Choice y un esquema enriquecido, separa ambos casos con "
       "probabilidad 1,0. Un tercer experimento, con Choice restringido a las opciones "
       "originales, no reproduce ni el colapso ni la separación perfecta: aparece un sesgo "
       "direccional no anticipado. El hallazgo central no es que Jev colapse per se, sino que "
       "el mismo modelo preserva, destruye, o distorsiona la distinción según el tipo de "
       "pregunta y el esquema declarado.", {})],
     "Abstract")
rich([("Palabras clave: ", {"bold": True}),
      ("modelos de evaluación tipada; System One models; LLM-as-judge; lógica paraconsistente "
       "anotada; colapso representacional; abstención tipada; Jev.", {})], "Keywords")

# ------------------------------------------------------------------ 1
P("1 Introduction", "Section title")
P("A conventional chat model, faced with the question \"was the refund approved?\", might "
  "answer \"Yes, it seems so, although I'm not entirely sure...\" — an unstructured string of "
  "text that the consuming software must re-parse or interpret, with no explicit score and no "
  "format guarantee. A category of tools that emerged in September 2026, typed evaluation "
  "models, inverts that relationship: the model is given a state (the available context or "
  "evidence) and a schema of questions, each with a declared type, and the model returns, for "
  "each question, a value of that type together with a calibrated probability.")
P("TypeSafe AI calls its first model of this kind \"System One\" — the fast, intuitive "
  "counterpart to the slow, deliberate reasoning (\"System Two\") pursued by frontier LLMs "
  "[1]. According to the vendor, Jev does not generate text: it selects among the options of "
  "a schema supplied by the caller, so returning a malformed value or one outside the "
  "declared set would be structurally impossible [2] — a format guarantee, not a guarantee of "
  "content correctness. The vendor reports 20 to 200 times more speed and up to 400 times "
  "lower cost than a frontier LLM for this class of tasks [3], and a proprietary training "
  "method, Reinforcement Learning for Calibrated Decisions (RLCD), aimed at explicit "
  "calibration [4]. None of these figures were independently audited in this work; they are "
  "reported as vendor claims, not as verified facts.")
P("This work does not evaluate Jev's performance on its intended tasks. Before examining it "
  "as a case study (§3-§6), §2 situates it within a broader landscape of AI model interaction "
  "categories. A representational question is then examined — what does a model that "
  "collapses evidence to a single calibrated probability lose? — and, following an "
  "unexpected finding in the experiment itself, that question is refined into a more precise "
  "one: is the loss a property of the model, or of the type of interface chosen to query it?")

# ------------------------------------------------------------------ 2
P("2 Landscape of AI Model Interaction Categories", "Section title")
P("The binary opposition \"free chat vs. typed\" oversimplifies the real landscape. Figure 1 "
  "positions five categories along two axes: computational cost and rigidity/timing of the "
  "decision schema's fixation — not \"input flexibility,\" a formulation from an earlier "
  "version of this figure that led to a misreading (it suggested that a generative chat model "
  "was less flexible than a typed model, when it is exactly the opposite in terms of what it "
  "can be asked). The correct axis runs from a schema fixed at training time (category 4, the "
  "most rigid) to a schema declared at each call (categories 2, 3, and 5), to the total "
  "absence of a schema (category 1, free text — the maximum possible expressive freedom, but "
  "with zero structural guarantee on the response).")
P("1. Generative chat models — free text, no guarantee of format or type. This is the "
  "no-schema extreme of the axis: it accepts any question, but offers no guarantee about the "
  "shape of the answer.")
P("2. LLM with forced output (constrained decoding) — still a general-purpose generative "
  "model underneath, but at each generation step the space of valid tokens is restricted "
  "according to a declared grammar or JSON schema [12]. The cost remains that of a full LLM.")
P("3. LLM-as-judge — a frontier or fine-tuned LLM evaluates according to a natural-language "
  "criterion. When fine-tuned to a specific task, the literature documents that it can "
  "degenerate into a closed-domain classifier, with a performance drop outside that domain "
  "[13].")
P("4. Classical discriminative classifiers — dedicated non-generative architectures (e.g., a "
  "fine-tuned BERT, or an evidential head such as EDL), deterministic, with a class schema "
  "fixed at training time. Reported as substantially cheaper and faster than an LLM-based "
  "judge, although the exact figure varies by source and is not taken here as precise data.")
P("5. Jev and its peers (typed evaluation models) — the case study of this work.")
P("Note on this taxonomy: it is not a strict partition. Categories 2 and 3 can overlap in "
  "practice — an LLM-based judge can use forced output to guarantee a valid JSON verdict — "
  "and are presented as heuristic axes (use, decoding technique, architecture, cost) rather "
  "than as mutually exclusive classes. It is the author's own synthesis of secondary sources, "
  "not a systematic review of the constrained-decoding and LLM-as-judge literature.")
P("With that caveat, Jev sits at the convergence of categories 3 and 4: it inherits from "
  "category 3 the flexibility of a question schema declared at call time, and from category 4 "
  "the low cost and the guarantee of typed output by construction. The LLM evaluation "
  "ecosystem is converging toward two-tier architectures in 2026 — a cheap classifier that "
  "resolves most cases and escalates to a frontier judge only when the case is ambiguous "
  "[14] — which is, structurally, the same cascade that a typed-abstention taxonomy already "
  "formalizes for decision-making under insufficient or disputed evidence (the author's own "
  "unpublished research-program synthesis; see note in §7).")

figure("fig1_taxonomy_en.png",
       "Figure 1: Positioning of the five AI model interaction categories according to "
       "schema rigidity/timing (x-axis: fixed at training → declared at each call → no "
       "schema) and computational cost (y-axis). Jev sits at the convergence between the "
       "LLM-based judge (category 3) and the classical discriminative classifier (category "
       "4); generative chat (category 1) occupies the no-schema extreme — maximum expressive "
       "freedom, zero structural guarantee. Source: own elaboration.")

# ------------------------------------------------------------------ 3
P("3 Verified Taxonomy of Types in Jev", "Section title")
P("The vendor's documentation [8] specifies three question primitives, evaluable in "
  "parallel within a single call.")
table(["Type", "What it does", "What it returns"],
      [["Choice", "pick one option from a declared set (criteria: option→description map)",
        "chosen option + probability per option"],
       ["Score", "rate the state on a rubric of ordered levels",
        "score + probability per level"],
       ["Noul", "yes/no question", "the probability that the answer is \"yes\""]],
      "Table 1: Question primitives supported by Jev.")
P("The documentation calls the third type \"Noul,\" not \"Boolean,\" and describes it as a "
  "continuous probability in [0,1] — not a discrete value. The Vercel AI Gateway SDK, which "
  "exposes experimental_evaluate as the access interface, names that same type boolean in its "
  "API signature [9]. Verified directly against the response object (§5): the field "
  "providerMetadata.typesafe.confidence exists in the schema but arrives empty ({}) in all "
  "five cases run with the boolean type — there is, for that type, no additional confidence "
  "or evidence-composition field beyond the single probability.")

# ------------------------------------------------------------------ 4
P("4 The Representational Question", "Section title")
P("In the annotated paraconsistent logic framework (LPA2v) [10], a judgment is represented "
  "as an independent pair (μ, λ). Two distinguished vertices of the resulting lattice, ⊤ "
  "(inconsistent: strong evidence in both directions) and ⊥ (paracomplete: absence of "
  "evidence in either direction), are epistemologically opposite but share a geometric "
  "property: both are equally far from the \"true\" and \"false\" ideal vertices [11]. From "
  "this a result already formalized follows: every closeness score to those ideal vertices is "
  "invariant under the involution that swaps ⊤ and ⊥ [11].")
P("This work does not apply that theorem literally to Jev — doing so would require Jev to "
  "explicitly compute an independent pair (μ, λ), which is undocumented. The connection is a "
  "motivating analogy, not a deductive consequence of the theorem. The argument that is "
  "deductively valid, and that this work puts to the test, is simpler: no map from an "
  "evidence space of two or more dimensions (support, opposition, magnitude, insufficiency) "
  "to a single scalar in [0,1] can be injective; two distinct evidence states can, by pure "
  "cardinality, collapse to the same number. A model that exposes only that scalar — like "
  "Jev's Noul type — cannot, in principle, guarantee that conflict and ignorance produce "
  "distinct values.")

# ------------------------------------------------------------------ 5
P("5 Method", "Section title")
P("Six states (state) were designed in English on the same domain fact (whether a traffic "
  "light was red), in four categories: TORN (genuine conflict, n=2, two equally credible "
  "sources that contradict each other), SILENT (genuine ignorance, n=2, documented absence of "
  "evidence), AGREE-SUPPORT (control, n=1, sources agreeing on \"red\"), and AGREE-REFUTE "
  "(control, n=1, sources agreeing on \"not red\").")
P("Experiment 1 (boolean/Noul type): one call per state to typesafe-ai/jev via "
  "experimental_evaluate from the ai SDK v7.0.107, single question: \"Was the traffic light "
  "red at the time in question?\"")
P("Experiment 2 (Choice type, follow-up): the same six states, a single lightState question "
  "of type choice with four explicit options: red, green, conflicting_evidence (\"reliable "
  "sources disagree with each other about the color\"), and insufficient_evidence (\"there is "
  "no evidence available to determine the color\"). This second experiment was designed after "
  "observing the results of Experiment 1, prompted by an adversarial review that flagged the "
  "need to test whether the collapse was a property of the model or of the question type — it "
  "is explicitly declared as not preregistered and data-motivated.")
P("Experiment 3 (binary Choice, closing the open question): the same six states, the same "
  "lightState question of type choice, but with only the two original options: red and "
  "green, no escape categories. Tests whether the perfect separation of Experiment 2 depends "
  "on the schema being able to name conflict/insufficiency, or whether it is a general "
  "property of the Choice type independent of the schema. Also data-motivated, not "
  "preregistered.")
P("None of the three experiments averages repetitions (a single call per case; limitation "
  "in §8). The calls were made on September 19, 2026 against the production model, with no "
  "access to its weights or training set.")

# ------------------------------------------------------------------ 6
P("6 Results", "Section title")
table(["Case", "Category", "P(red)"],
      [["TORN-1", "genuine conflict (contradictory witnesses)", "0.57"],
       ["TORN-2", "genuine conflict (contradictory sensors)", "0.50"],
       ["SILENT-1", "genuine ignorance (no witnesses or cameras)", "0.46"],
       ["SILENT-2", "genuine ignorance (lost record)", "0.48"],
       ["AGREE-SUPPORT", "control: sources agree (support)", "0.83"],
       ["AGREE-REFUTE", "control: sources agree (refutation)", "no data (rate-limit, §8)"]],
      "Table 2: Experiment 1 (boolean/Noul type) — probability of \"red\".")
P("The two TORN cases (0.50–0.57) and the two SILENT cases (0.46–0.48) fall within a common, "
  "narrow band. The only completed control with unambiguous evidence (AGREE-SUPPORT) yields "
  "0.83, far from 0.5.")
table(["Case", "Category", "Jev's choice", "P(choice)"],
      [["TORN-1", "genuine conflict", "conflicting_evidence", "1.00"],
       ["TORN-2", "genuine conflict", "conflicting_evidence", "1.00"],
       ["SILENT-1", "genuine ignorance", "insufficient_evidence", "1.00"],
       ["SILENT-2", "genuine ignorance", "insufficient_evidence", "1.00"],
       ["AGREE-SUPPORT", "control: sources agree", "red", "1.00"],
       ["AGREE-REFUTE", "control: sources agree", "no data (rate-limit, §8)", "—"]],
      "Table 3: Experiment 2 (Choice type, enriched schema) — choice and probability.")
P("With the Choice type and a schema that explicitly names \"conflicting evidence\" and "
  "\"insufficient evidence\" as first-class options, Jev separates the four experimental "
  "cases (TORN vs. SILENT) with maximum probability and no ambiguity, and correctly "
  "classifies the support control. The same textual evidence that collapsed to a 0.46-0.57 "
  "band under the boolean type produces a perfect distinction under the Choice type.")
table(["Case", "Category", "P(red)", "P(green)"],
      [["TORN-1", "genuine conflict", "0.85", "0.15"],
       ["TORN-2", "genuine conflict", "0.84", "0.16"],
       ["SILENT-1", "genuine ignorance", "0.67", "0.33"],
       ["SILENT-2", "genuine ignorance", "0.77", "0.23"],
       ["AGREE-SUPPORT", "control: sources agree", "1.00", "0.00"],
       ["AGREE-REFUTE", "control: sources agree", "no data (rate-limit, §8)", "—"]],
      "Table 4: Experiment 3 (binary Choice type, red/green, no escape categories).")
P("Without escape categories, Jev does not reproduce the ~0.5 collapse of Experiment 1 nor "
  "the perfect separation of Experiment 2. Instead, a directional bias toward red appears "
  "across all six cases, more pronounced in TORN (0.84-0.85) than in SILENT (0.67-0.77) — a "
  "weak ordinal trend (n=2 per category) that does not allow a firm conclusion. It is a third "
  "pattern, unanticipated by either of the two simple hypotheses (symmetric collapse or clean "
  "separation).")

# ------------------------------------------------------------------ 7
P("7 Discussion", "Section title")
P("The pattern in Experiment 1 is consistent with the prediction in §4: under the Noul type, "
  "Jev does not distinguish why the evidence is unclear. But Experiment 2 forces a correction "
  "of the interpretation: the loss is not a property of the Jev model, but of the question "
  "type and schema declared to query it. The boolean type forces, by definition, an output in "
  "a one-degree-of-freedom space — there is no way for it to return \"conflict\" or "
  "\"insufficiency\" even if the model internally distinguishes them. The Choice type, when "
  "the schema includes those categories as named options, does have representational room to "
  "express them, and the model exploits it with a sharpness that was not anticipated "
  "(probability 1.0, not a diffuse tendency).")
P("This reframes the contribution of the work: it is not \"Jev has an inherent "
  "representational limitation,\" but rather that the design of the query schema determines "
  "whether the distinction survives, and the simplest, cheapest type to use (Noul, a single "
  "yes/no question) is precisely the one that destroys it by construction. This is a usage "
  "risk, not a product engineering defect.")
P("Experiment 3 answers the open question from v0.2 only partially, and in a more "
  "uncomfortable way than either of the two simple answers that were anticipated. The "
  "hypothesis \"Choice always separates, regardless of the schema\" is ruled out: without "
  "escape categories, there is no clean separation (0.84 is not 1.00, and SILENT does not "
  "approach 0.5 from the other side). But the alternative hypothesis \"without escape "
  "categories, Choice collapses just like Noul\" is also ruled out: there is no symmetric "
  "collapse toward 0.5 in any case — all values, including the SILENT cases with no evidence "
  "whatsoever, lean toward red.")
P("The most honest explanation available with this data, without over-interpreting an n=2 "
  "per cell, is a possible lexical confound in the design of the stimulus itself: the TORN "
  "and AGREE-SUPPORT states literally contain the word \"red\" in the text (someone asserts "
  "it, even if it is contested), while the SILENT states do not mention either \"red\" or "
  "\"green\" at all. If the model partly weighs the surface presence of the word naming an "
  "option — and not only whether that assertion is credible or disputed — that would produce "
  "exactly the observed pattern. This explanation is plausible and testable, but this work "
  "did not test it in a controlled way — it remains a genuine open question, not a closed "
  "finding.")
P("What does hold up across the three experiments together: the deductive argument in §4 (no "
  "single scalar can be injective over a higher-dimensional evidence space) explains the "
  "collapse of the Noul type, but does not predict or explain the pattern of Experiment 3 — a "
  "Choice with two options is not a single injective scalar in the same way, and yet it "
  "failed to achieve the separation that its representational space would in principle "
  "allow. The practical recommendation stands, but becomes more cautious: to preserve the "
  "distinction between conflict and ignorance, avoiding the boolean type is not enough — the "
  "Choice schema must also explicitly name those states as first-class options, and it is "
  "worth empirically verifying that the model is not responding to superficial lexical cues "
  "in the state rather than to the actual structure of the evidence.")

# ------------------------------------------------------------------ 8
P("8 Limitations", "Section title")
P("(a) n=5 completed cases out of 6 in each of the three experiments (the AGREE-REFUTE "
  "control failed due to the Vercel AI Gateway free tier's rate limit in all three, even with "
  "a payment method already on file — the provider requires loaded paid credits, not just a "
  "card on file, and that step was not completed; it is the only case that could never be "
  "observed, under any condition); (b) a single call per case in each experiment, with no "
  "repetition to estimate variance — critical for Experiment 3, whose pattern (n=2 per "
  "category) does not allow distinguishing a real trend from sample noise; (c) Experiments 2 "
  "and 3 were motivated by prior results and were not preregistered — explicitly declared as "
  "such; (d) the lexical-bias explanation for Experiment 3 (§7) is plausible but was not "
  "tested in a controlled way; (e) this is a four-day-old product at the time of writing — "
  "its behavior and limits may change without notice, and these results should be read as a "
  "snapshot of 2026-09-19; (f) the speed, cost, and training-method (RLCD) figures are vendor "
  "claims, not independently audited in this work; (g) the five-category taxonomy in §2 is "
  "the author's own synthesis, not a systematic review.")

# ------------------------------------------------------------------ 9
P("9 Conclusion", "Section title")
P("The first experiment in this work seemed to confirm that typed evaluation models inherit, "
  "by representational design, the collapse between conflict and ignorance already formally "
  "characterized in annotated decision theory. A second experiment showed that conclusion to "
  "be incomplete: the same model, with a Choice schema that explicitly names the disputed "
  "epistemic states, separates conflict from ignorance with maximum probability. A third "
  "experiment, designed to isolate whether that separation depended on the schema or on the "
  "question type, showed that reality is messier than either of those two stories: without "
  "escape categories, Jev neither collapses symmetrically nor separates cleanly, but instead "
  "exhibits an unanticipated directional bias, possibly tied to superficial lexical cues in "
  "the input text.")
P("The lesson that survives all three experiments is not about a fixed limit of Jev as a "
  "product, but about two distinct and equally real risks for anyone building on typed "
  "evaluation models: first, reducing an epistemically complex decision to the simplest "
  "available interface type (boolean/Noul) discards information by construction; second, "
  "even a more expressive interface (Choice) can fail in non-obvious ways — biased, not "
  "simply \"less informative\" — when the schema does not explicitly name the states that "
  "matter.")

# ------------------------------------------------------------------ declarations
P("Conflict of Interest", "Section title")
P("The author declares no conflict of interest.")
P("Data and Code Availability", "Section title")
P("Public repository: https://github.com/mleyvaz/jev-typed-evaluation-collapse — includes "
  "the script and results of Experiment 1 (run_experiment.mjs, results.json), Experiment 2 "
  "(run_experiment_choice.mjs, results_choice.json), Experiment 3 "
  "(run_experiment_choice_binary.mjs, results_choice_binary.json), the Figure 1 script "
  "(make_fig1_taxonomy.py), and the adversarial review round that motivated the v0.1 → v0.2 "
  "→ v0.3 revisions.")

# ------------------------------------------------------------------ references
P("References", "Section title")
refs = [
    "TypeSafe AI. Introducing System One Models & Jev. TypeSafe AI Blog, 2026-09-15.",
    "DataCamp. Jev: TypeSafe's System One Model That Never Hallucinates. datacamp.com/blog/system-one-models-jev",
    "Vercel. TypeSafe AI's Jev now available on AI Gateway. Vercel Changelog.",
    "explainx.ai. How Does Jev Work? RLCD & Parallel Inference Explained. 2026.",
    "Mapika. decider: One-pass typed decisions with calibrated probabilities, fine-tuned from Qwen3.5-2B. GitHub.",
    "nateGeorge. reflex: A small open decision model — a Jev / System One re-creation on Qwen3.5. GitHub.",
    "Eliot, L. New 'Reinforcement Learning For Calibrated Decisions' Makes AI Headlines But Look Past The Hype. Forbes, 2026-09-18.",
    "TypeSafe AI. Introduction — Question Types. docs.typesafe.ai/introduction",
    "Vercel. Jev API, Pricing & Playground. AI Gateway Models.",
    "da Costa, N.C.A., Abe, J.M., Subrahmanian, V.S. (1991). Remarks on annotated logic. Zeitschrift für Mathematische Logik und Grundlagen der Mathematik, 37.",
    "Leyva-Vázquez, M. (2026). Conflation-Invariant TOPSIS Scores and Panel-Level Abstention in Annotated Evidence [manuscript in preparation]. Preprint SSRN 7441661.",
    "Park, K., Zhou, T., D'Antoni, L. (2025). Flexible and Efficient Grammar-Constrained Decoding. arXiv:2502.05111. Also in ICML 2025.",
    "Huang, H., Bu, X., Zhou, H., Qu, Y., Liu, J., Yang, M., Xu, B., Zhao, T. (2024). An Empirical Study of LLM-as-a-Judge for LLM Evaluation: Fine-tuned Judge Model is not a General Substitute for GPT-4. arXiv:2403.02839. Findings of ACL 2025.",
    "Gu, J., Jiang, X., Shi, Z., Tian, H., Zhai, X., Xu, C., et al. (2026). A survey on LLM-as-a-judge. The Innovation, 7(6), 101253.",
]
for i, r in enumerate(refs, 1):
    P(f"[{i}]\t{r}", "18_References")

P()
P("Received: September 19, 2026.   Accepted: —",
  "Received and accepted", WD_ALIGN_PARAGRAPH.RIGHT)

# ------------------------------------------------------------------ Appendix A
P("Appendix A. Input States (verbatim)", "Section title")
P("The six states (state) used across the three experiments, identical in each — only the "
  "declared question (questions) changes.")

estados = [
    ("TORN-1 (genuine conflict)",
     "Witness A, a police officer with a clear view of the intersection, testified under oath "
     "that the traffic light was red at the moment of the collision. Witness B, a bystander "
     "standing next to Witness A with an equally clear view, testified under oath that the "
     "same traffic light was green at that exact moment. Both witnesses are considered "
     "reliable by the investigating officer; there is no indication either one is lying."),
    ("TORN-2 (genuine conflict)",
     "Sensor 1, a calibrated high-precision traffic sensor, recorded the light as RED at "
     "14:03:02. Sensor 2, an equally calibrated high-precision sensor mounted on the same "
     "pole, recorded the light as GREEN at the same timestamp, 14:03:02. Both sensors passed "
     "their most recent calibration check with no faults reported."),
    ("SILENT-1 (genuine ignorance)",
     "No witnesses were present at the intersection at the time in question. No traffic "
     "cameras were operating in that area that day. There is no record, sensor log, or "
     "testimony of any kind describing the state of the traffic light at that moment."),
    ("SILENT-2 (genuine ignorance)",
     "The traffic light's camera log for that day was permanently lost in a server failure "
     "before any backup was made. No witnesses have come forward. No other observation of the "
     "light exists in any form."),
    ("AGREE-SUPPORT (control, support)",
     "Witness A testified that the traffic light was red at the time of the collision. "
     "Witness B, standing nearby with an independent line of sight, separately and "
     "independently confirmed that the light was red at that same moment."),
    ("AGREE-REFUTE (control, refutation)",
     "Witness A testified that the traffic light was green, not red, at the time of the "
     "collision. Witness B, standing nearby with an independent line of sight, separately and "
     "independently confirmed that the light was green at that same moment."),
]
for titulo, texto in estados:
    P(titulo, bold=True)
    P(texto, italic=True)

# ------------------------------------------------------------------ Appendix B
P("Appendix B. Call Code, per Experiment", "Section title")

P("Experiment 1 (boolean/Noul):", bold=True)
code_block("""
import { experimental_evaluate as evaluate } from 'ai';

const result = await evaluate({
  model: 'typesafe-ai/jev',
  state: STATE_TEXT, // one of the six states in Appendix A
  questions: {
    wasRed: {
      type: 'boolean',
      instructions: 'Was the traffic light red at the time in question?',
    },
  },
});
""")

P("Experiment 2 (Choice, enriched schema):", bold=True)
code_block("""
const result = await evaluate({
  model: 'typesafe-ai/jev',
  state: STATE_TEXT,
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
""")

P("Experiment 3 (binary Choice, no escape categories):", bold=True)
code_block("""
const result = await evaluate({
  model: 'typesafe-ai/jev',
  state: STATE_TEXT,
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
""")

# ------------------------------------------------------------------ Appendix C
P("Appendix C. Full Response (answers) per Case", "Section title")
P("The answers object returned by Jev for each completed case, unedited (the full response "
  "object also includes usage, warnings, rounding, and providerMetadata, available in the "
  "results*.json files in the repository).")

P("Experiment 1 — boolean/Noul:", bold=True)
code_block("""
TORN-1:         {"wasRed":{"type":"boolean","probability":0.57}}
TORN-2:         {"wasRed":{"type":"boolean","probability":0.50}}
SILENT-1:       {"wasRed":{"type":"boolean","probability":0.46}}
SILENT-2:       {"wasRed":{"type":"boolean","probability":0.48}}
AGREE-SUPPORT:  {"wasRed":{"type":"boolean","probability":0.83}}
AGREE-REFUTE:   ERROR - GatewayRateLimitError (free-tier rate limit, S8)
""")

P("Experiment 2 — enriched Choice:", bold=True)
code_block("""
TORN-1:         {"lightState":{"choice":"conflicting_evidence","probabilities":
                  {"red":0,"green":0,"conflicting_evidence":1,"insufficient_evidence":0}}}
TORN-2:         {"lightState":{"choice":"conflicting_evidence","probabilities":
                  {"red":0,"green":0,"conflicting_evidence":1,"insufficient_evidence":0}}}
SILENT-1:       {"lightState":{"choice":"insufficient_evidence","probabilities":
                  {"red":0,"green":0,"conflicting_evidence":0,"insufficient_evidence":1}}}
SILENT-2:       {"lightState":{"choice":"insufficient_evidence","probabilities":
                  {"red":0,"green":0,"conflicting_evidence":0,"insufficient_evidence":1}}}
AGREE-SUPPORT:  {"lightState":{"choice":"red","probabilities":
                  {"red":1,"green":0,"conflicting_evidence":0,"insufficient_evidence":0}}}
AGREE-REFUTE:   ERROR - GatewayRateLimitError (free-tier rate limit, S8)
""")

P("Experiment 3 — binary Choice:", bold=True)
code_block("""
TORN-1:         {"lightState":{"choice":"red","probabilities":{"red":0.85,"green":0.15}}}
TORN-2:         {"lightState":{"choice":"red","probabilities":{"red":0.84,"green":0.16}}}
SILENT-1:       {"lightState":{"choice":"red","probabilities":{"red":0.67,"green":0.33}}}
SILENT-2:       {"lightState":{"choice":"red","probabilities":{"red":0.77,"green":0.23}}}
AGREE-SUPPORT:  {"lightState":{"choice":"red","probabilities":{"red":1,"green":0}}}
AGREE-REFUTE:   ERROR - GatewayRateLimitError (free-tier rate limit, S8)
""")

doc.save(OUT)
print("NCML English format ->", OUT)
