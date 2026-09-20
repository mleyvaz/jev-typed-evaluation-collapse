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
P("Experiment 4 (Score type, exploratory): a fourth experiment, not preregistered and "
  "motivated by the prior results, tests whether a purely scalar but ordinal question type "
  "— Score, which returns a probability-weighted mean over a rubric of ordered levels, "
  "not a categorical choice — also preserves the distinction between conflict and "
  "absence of evidence, or collapses like the boolean type. The Score syntax is not "
  "explicitly documented in the public specification consulted; it was determined by trial "
  "and error against the SDK's validation messages, which require an ordered array of levels "
  "(criteria), not a map as in Choice. A five-level rubric on \"evidential determinacy\" was "
  "used (0 = very high confidence, 4 = no confidence at all), deliberately agnostic about the "
  "cause of the uncertainty, and six new states were constructed — three of nominally "
  "increasing conflict intensity and three of nominally increasing evidence-absence "
  "intensity — plus reusing AGREE-SUPPORT as an already-determined control anchor. The "
  "six new states are in Appendix A.")
P("Experiment 5 (μ/λ composition, exploratory): motivated by an idea discussed after the "
  "first four experiments: can an independent (μ, λ) pair, as in annotated paraconsistent "
  "logic (LPA2v, §4), be reconstructed by composing two separate calls to Jev's simplest "
  "type, instead of requiring the model to compute it internally? For each of the six "
  "original states (Appendix A), two boolean questions were asked in the same call: μ = "
  "\"Is there credible evidence supporting the claim that the traffic light was red?\" and "
  "λ = \"Is there credible evidence supporting the claim that the traffic light was NOT red "
  "(i.e., was green)?\", without forcing their probabilities to sum to 1 — independent "
  "questions, not a choice among options. Exploratory, not preregistered, motivated by the "
  "prior results.")
P("Experiment 6 (third indeterminacy coordinate, validated with an expanded dataset): "
  "motivated by whether a third indeterminacy coordinate (I), as in neutrosophic logic "
  "(T, I, F), captures something the (μ, λ) pair of Experiment 5 does not. A seventh state, "
  "AMBIGUOUS, was designed (evidence that is intrinsically vague from a single source — "
  "neither contradictory like TORN nor absent like SILENT), and, alongside μ and λ, I was "
  "asked: \"Is it indeterminate whether [the claim] — that is, does the available evidence "
  "fail to clearly resolve this either way, regardless of the reason why?\" A first "
  "single-call-per-category pilot (n=1, traffic-light domain) suggested I did not "
  "distinguish TORN, SILENT, or AMBIGUOUS from each other — all three fell in the same high "
  "band — but with n=1 that conclusion could not be trusted. An expanded dataset of 20 "
  "heterogeneous domains was then built (traffic light, defective product, workplace "
  "attendance, medical biopsy, bank authorization, weather, contract, inventory, security, "
  "academic submission, vehicle brakes, food-safety inspection, building foundation, "
  "insurance, election, software, customs, veterinary, aviation, real estate), each "
  "instantiating the same 5 categories (TORN, SILENT, AGREE-SUPPORT, AGREE-REFUTE, "
  "AMBIGUOUS) with an identical structural template across domains, for a total of 100 "
  "states (n=20 per category). The full domain list is in Appendix A. A first attempt with "
  "μ/λ questions phrased meta-referentially (\"does it support the direction labeled true "
  "in the state?\") detectably degraded the model's calibration — an AGREE-REFUTE control "
  "that should have given low μ/high λ instead gave values nearly identical to "
  "AGREE-SUPPORT — so μ/λ were reformulated as concrete, domain-specific claims, as in "
  "Experiment 5, and the full dataset was rerun before reporting results.")
P("None of the six experiments averages repetitions within a single state (a single call "
  "per case; limitation in §8) — Experiment 6 gains statistical power by repeating the "
  "case structure across 20 domains, not by repeating the same case. The calls were made on "
  "September 19 and 20, 2026 against the production model, "
  "with no access to its weights or training set.")

# ------------------------------------------------------------------ 6
P("6 Results", "Section title")
table(["Case", "Category", "P(red)"],
      [["TORN-1", "genuine conflict (contradictory witnesses)", "0.57"],
       ["TORN-2", "genuine conflict (contradictory sensors)", "0.50"],
       ["SILENT-1", "genuine ignorance (no witnesses or cameras)", "0.46"],
       ["SILENT-2", "genuine ignorance (lost record)", "0.48"],
       ["AGREE-SUPPORT", "control: sources agree (support)", "0.83"],
       ["AGREE-REFUTE", "control: sources agree (refutation)", "0.08"]],
      "Table 2: Experiment 1 (boolean/Noul type) — probability of \"red\".")
P("The two TORN cases (0.50–0.57) and the two SILENT cases (0.46–0.48) fall within a common, "
  "narrow band. Both controls, with unambiguous evidence, yield values far from 0.5 in the "
  "correct direction: 0.83 for support (\"red\" evidence) and 0.08 for refutation (\"green\" "
  "evidence).")
table(["Case", "Category", "Jev's choice", "P(choice)"],
      [["TORN-1", "genuine conflict", "conflicting_evidence", "1.00"],
       ["TORN-2", "genuine conflict", "conflicting_evidence", "1.00"],
       ["SILENT-1", "genuine ignorance", "insufficient_evidence", "1.00"],
       ["SILENT-2", "genuine ignorance", "insufficient_evidence", "1.00"],
       ["AGREE-SUPPORT", "control: sources agree", "red", "1.00"],
       ["AGREE-REFUTE", "control: sources agree", "green", "1.00"]],
      "Table 3: Experiment 2 (Choice type, enriched schema) — choice and probability.")
P("With the Choice type and a schema that explicitly names \"conflicting evidence\" and "
  "\"insufficient evidence\" as first-class options, Jev separates the four experimental "
  "cases (TORN vs. SILENT) with maximum probability and no ambiguity, and correctly "
  "classifies both controls (support → red, refutation → green), both at maximum "
  "probability. The same textual evidence that collapsed to a 0.46-0.57 "
  "band under the boolean type produces a perfect distinction under the Choice type.")
table(["Case", "Category", "P(red)", "P(green)"],
      [["TORN-1", "genuine conflict", "0.85", "0.15"],
       ["TORN-2", "genuine conflict", "0.84", "0.16"],
       ["SILENT-1", "genuine ignorance", "0.67", "0.33"],
       ["SILENT-2", "genuine ignorance", "0.77", "0.23"],
       ["AGREE-SUPPORT", "control: sources agree", "1.00", "0.00"],
       ["AGREE-REFUTE", "control: sources agree", "0.00", "1.00"]],
      "Table 4: Experiment 3 (binary Choice type, red/green, no escape categories).")
P("Without escape categories, Jev does not reproduce the ~0.5 collapse of Experiment 1 nor "
  "the perfect separation of Experiment 2. Instead, a directional bias toward red appears "
  "in TORN and SILENT (0.67-0.85), more pronounced in TORN (0.84-0.85) than in SILENT "
  "(0.67-0.77) — a weak ordinal trend (n=2 per category) that does not allow a firm "
  "conclusion. The refutation control (AGREE-REFUTE), with unambiguous green evidence, does "
  "not follow that bias: it is classified cleanly and correctly (P(red)=0.00), just as "
  "sharply as the support control in the opposite direction. The bias toward red is therefore "
  "not an indiscriminate model artifact — it appears only in cases with ambiguous (TORN) or "
  "absent (SILENT) evidence. It is a third "
  "pattern, unanticipated by either of the two simple hypotheses (symmetric collapse or clean "
  "separation).")

table(["Case", "Branch", "Score (0-4)"],
      [["ANCHOR-DETERMINED", "control (sources agree)", "0.25"],
       ["CONFLICT-MODERATE", "conflict, unequal witness vantage", "1.58"],
       ["CONFLICT-SEVERE", "conflict, maximally reliable sensors", "2.04"],
       ["CONFLICT-MILD", "conflict, self-doubting witnesses", "2.67"],
       ["SILENCE-MODERATE", "absence, vague unreliable rumor", "3.66"],
       ["SILENCE-MILD", "absence, evidence irrelevant to the fact", "3.88"],
       ["SILENCE-SEVERE", "total absence of evidence", "3.95"]],
      "Table 5: Experiment 4 (Score type, graded determinacy).")
P("The clean contrast is at the extremes: CONFLICT-SEVERE (2.04, \"moderate,\" with 0.97 "
  "probability concentrated on that level) and SILENCE-SEVERE (3.95, \"no confidence,\" 0.97 "
  "probability on that level) are separated by nearly two points on a five-level scale — "
  "the Score type, although it also returns a scalar, does not collapse severe conflict and "
  "total absence to the same value, unlike the boolean type (Experiment 1). The control "
  "anchor (AGREE-SUPPORT) confirms that the maximum-determinacy extreme works as expected "
  "(0.25, near \"very high confidence\").")
P("The three intermediate points in each branch, however, do not order monotonically as "
  "intended by design: within conflict, CONFLICT-MODERATE (1.58) turns out more determinate "
  "than CONFLICT-SEVERE (2.04) and CONFLICT-MILD (2.67), reversing the intended severity "
  "order; within absence, SILENCE-MODERATE (3.66) turns out less indeterminate than "
  "SILENCE-MILD (3.88). On review, CONFLICT-MODERATE has an unintentional design asymmetry "
  "(one witness with a \"reasonably clear view\" versus one with a \"partially obstructed "
  "view\") that likely introduces a differential-credibility cue absent from the other two "
  "cases in that branch — that is, the \"degree\" manipulation was not well controlled, "
  "and the result does not support a claim that Score finely orders the degree of "
  "indeterminacy within a branch. These six intermediate cases are reported for transparency "
  "(Appendix C), but are not interpreted as evidence of monotonic tracking of degree.")

table(["Case", "Category", "μ (supports red)", "λ (supports not-red)", "Vertex"],
      [["TORN-1", "genuine conflict", "0.86", "0.84", "⊤ (both high)"],
       ["TORN-2", "genuine conflict", "0.64", "0.62", "⊤ (both high)"],
       ["SILENT-1", "genuine ignorance", "0.04", "0.04", "⊥ (both low)"],
       ["SILENT-2", "genuine ignorance", "0.05", "0.04", "⊥ (both low)"],
       ["AGREE-SUPPORT", "control: support", "0.91", "0.06", "\"true\""],
       ["AGREE-REFUTE", "control: refutation", "0.06", "0.92", "\"false\""]],
      "Table 6: Experiment 5 (μ/λ composition, independent pair).")
P("Composing two independent boolean calls — one for evidence in favor, one against, "
  "without forcing them to sum to 1 — reconstructs the four canonical vertices of "
  "LPA2v's lattice (§4), and separates TORN from SILENT more sharply than Experiment 1: "
  "both TORN cases fall in the both-values-high region (⊤, inconsistent) and both "
  "SILENT cases in the both-values-low region (⊥, paracomplete) — exactly the "
  "distinction a single boolean call could not make. The magnitude differs between TORN-1 "
  "(0.86/0.84) and TORN-2 (0.64/0.62); with n=1 per case it cannot be established whether "
  "that is a real signal or sample noise.")

table(["Category", "μ", "λ", "I"],
      [["TORN", "0.80 ± 0.04", "0.84 ± 0.04", "0.85 ± 0.02"],
       ["SILENT", "0.04 ± 0.01", "0.10 ± 0.05", "0.96 ± 0.01"],
       ["AGREE-SUPPORT", "0.91 ± 0.02", "0.05 ± 0.01", "0.13 ± 0.05"],
       ["AGREE-REFUTE", "0.04 ± 0.01", "0.91 ± 0.02", "0.12 ± 0.05"],
       ["AMBIGUOUS", "0.13 ± 0.04", "0.15 ± 0.06", "0.95 ± 0.02"]],
      "Table 7: Experiment 6 — 20-domain dataset (n=20 per category, mean ± SD).")
P("The μ/λ pattern from Experiment 5 replicates with high consistency across the "
  "20 domains: TORN clearly separates from {SILENT, AMBIGUOUS} (both low), and the controls "
  "land where expected. On I, three two-tailed Welch's t-tests show the three "
  "\"undetermined\" categories are statistically distinguishable from one another, though "
  "with very different magnitudes: TORN vs. SILENT (mean difference 0.109; t=-25.80; "
  "df=26.7), TORN vs. AMBIGUOUS (difference 0.096; t=-17.67; df=38.0), and SILENT vs. "
  "AMBIGUOUS (difference 0.014; t=3.22; df=26.8; p≈0.003). The first two are large, "
  "highly robust differences; the third is real but an order of magnitude smaller, and its "
  "magnitude (0.014) is comparable to the within-category standard deviation "
  "(0.008–0.017) — significant at the population level, but insufficient to "
  "confidently classify a single new case.")

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
P("The AGREE-REFUTE case, completed in a follow-up call after resolving the rate limit (§8), "
  "offers an additional — uncontrolled, but informative — test of that lexical "
  "hypothesis. Its text also literally contains the word \"red\" (\"the traffic light was "
  "green, not red\"), in an explicit negation clause. If the bias were a simple surface "
  "count of that word's occurrences, some pull toward red would be expected here too. "
  "Instead, Jev classifies this case with probability 1.00 toward green (P(red)=0.00) — "
  "as clean as the support control's pull toward red. This does not rule out the lexical "
  "confound outright, but it does narrow its scope: the red bias in Experiment 3 is not a "
  "blind count of lexical occurrences, and it concentrates on cases with ambiguous or absent "
  "evidence.")
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
P("Experiment 4 adds a nuance to this explanation: the Score type also returns a scalar (a "
  "probability-weighted mean over ordered levels), and yet it clearly separates severe "
  "conflict from total absence of evidence (2.04 vs. 3.95). This suggests that the relevant "
  "variable is not scalar-vs-categorical, but what question the schema forces: the boolean "
  "type forces an answer about the first-order fact (\"is it red?\"), where conflict and "
  "absence are, by the argument in §4, indistinguishable in principle; the Score type, as "
  "used here, was declared over a second-order question (\"how determinate is the "
  "evidence?\"), which can, in principle, differentiate how much information there is from "
  "what that information says. The limitation is that this experiment did not manage (§6) to "
  "show that Score reliably orders intermediate degrees of indeterminacy, so the conclusion "
  "is limited to the extremes contrast, not a fine-grained scale.")
P("Experiment 5 closes the loop opened in §4 in a way that was not anticipated: Jev does not "
  "need to compute an independent (μ, λ) pair internally for that pair to exist — "
  "it can be reconstructed by composing two calls to the simplest, cheapest type the model "
  "offers, one oriented for and one against, without forcing their outputs to sum to 1. That "
  "composition cleanly separates TORN from SILENT where a single boolean call (Experiment 1) "
  "could not, and recovers the four canonical vertices of LPA2v's lattice with higher "
  "fidelity than Choice's discrete approximation (4 labels, not a continuum) or Score's "
  "one-dimensional one. The limitation is the usual one: n=1 per case, no repetition; the "
  "magnitude difference between TORN-1 and TORN-2 cannot be attributed to a cause with this "
  "data; and whether this composition generalizes to domains other than the traffic light, "
  "or to evidence with more than two sources, remains an open question.")
P("Experiment 6 corrects, with data, a hasty reading by the analysis itself: looking at the "
  "ranges of an n=5-per-domain pilot, it was concluded that I \"does not distinguish\" "
  "SILENT from AMBIGUOUS. The Welch's t-test on the n=20 dataset shows it does distinguish "
  "them, though with a magnitude an order smaller than the one separating TORN from both. "
  "The lesson is twofold: first, I does carry information (μ, λ) alone do not "
  "expose — contrary to the pilot's first impression — which answers, with qualification, "
  "the motivating question of whether a third neutrosophic coordinate captures something "
  "genuine; second, that information has scientific value (it confirms the coordinate is "
  "not redundant) but limited operational value: the SILENT-AMBIGUOUS difference (0.014) is "
  "of the same order as the within-category standard deviation (0.008–0.017), so it "
  "does not allow confidently classifying a single new case from I alone. For anyone "
  "wanting to use I as a third coordinate, the honest recommendation is: it serves to "
  "corroborate at the aggregate level that the distinction exists, and is a useful "
  "component alongside (μ, λ) for separating conflict from non-conflict; it does "
  "not serve, with this design, as a case-by-case classifier of why something is "
  "undetermined within the non-conflict region. Alternative phrasings of the I question, "
  "which might widen that separation, were not tested.")

# ------------------------------------------------------------------ 8
P("8 Limitations", "Section title")
P("(a) [RESOLVED 2026-09-19] The AGREE-REFUTE control initially failed due to the Vercel AI "
  "Gateway free tier's rate limit in all three experiments, even with a payment method "
  "already on file — the provider requires loaded paid credits, not just a card on file. "
  "That step was completed the same day (a $20 credit purchase), and the case was run in an "
  "independent follow-up call; all three experiments now have n=6/6 complete cases; "
  "(b) a single call per case in each experiment, with no "
  "repetition to estimate variance — critical for Experiment 3, whose pattern (n=2 per "
  "category) does not allow distinguishing a real trend from sample noise; (c) Experiments 2 "
  "and 3 were motivated by prior results and were not preregistered — explicitly declared as "
  "such; (d) the lexical-bias explanation for Experiment 3 (§7) is plausible and received "
  "additional support from the AGREE-REFUTE case, but was not "
  "tested in a controlled way; (e) this is a four-day-old product at the time of writing — "
  "its behavior and limits may change without notice, and these results should be read as a "
  "snapshot of 2026-09-19; (f) the speed, cost, and training-method (RLCD) figures are vendor "
  "claims, not independently audited in this work; (g) the five-category taxonomy in §2 is "
  "the author's own synthesis, not a systematic review; (h) Experiment 4 (Score type, "
  "exploratory, not preregistered) shares limitations (b)-(c) above (a single call per case, "
  "no repetition, data-motivated), and in addition the intermediate-degree contrast within "
  "each branch turned out non-monotonic, with at least one identified design confound "
  "(vantage asymmetry in CONFLICT-MODERATE, §6); only the extremes contrast (severe conflict "
  "vs. severe absence) is reported as a finding, not a fine-grained degree scale; (i) "
  "Experiment 5 (μ/λ composition, exploratory, not preregistered) shares the "
  "single-call-per-case limitation; the magnitude difference between TORN-1 and TORN-2 "
  "(0.86/0.84 vs. 0.64/0.62) cannot be attributed to a cause without more repetitions; and "
  "whether the composition generalizes beyond the traffic-light domain, or to states with "
  "more than two evidence sources, was not tested; (j) Experiment 6, although validated "
  "with n=20 per category across 20 heterogeneous domains, shares the same structural "
  "template across domains (two reporting sources / total absence / one vague source) — it "
  "does not cover other forms of conflict or indeterminacy (numerical evidence, time "
  "series, more than two sources, partial rather than total disagreement); the I question "
  "was phrased only one way, without testing alternative phrasings that might widen the "
  "SILENT/AMBIGUOUS separation; and the author's own n=1 pilot led to a conclusion the "
  "expanded data corrected — a concrete reminder of why this work repeatedly declares the "
  "n=1 limitation in Experiments 1-5.")

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
  "the input text. A fourth, exploratory experiment, with the Score type, suggests that the "
  "relevant variable is not scalar-vs-categorical but what question each type forces — a "
  "scalar over \"how determinate is the evidence\" does separate severe conflict from total "
  "absence, though it did not manage to establish a fine-grained scale of intermediate "
  "degrees. A fifth experiment closed the loop opened by annotated decision theory in §4: "
  "composing two independent boolean calls — for and against, without forcing them to sum "
  "to 1 — reconstructs that theory's (μ, λ) pair without Jev computing it "
  "internally, and the lattice's four canonical vertices appeared where expected. A sixth "
  "experiment, validated on a dataset of 20 heterogeneous domains (n=20 per category), "
  "tested whether a third neutrosophic indeterminacy coordinate (I) captures something "
  "(μ, λ) do not: the answer is affirmative but qualified — I statistically "
  "distinguishes conflict from non-conflict (large effect) and, with smaller but still "
  "significant magnitude (p≈0.003), total absence of evidence from intrinsically vague "
  "evidence, though the latter distinction is too small relative to single-case noise to be "
  "useful case by case. The experiment's own process — a wrong conclusion at n=1, "
  "corrected at n=20 — illustrates in practice the sample-size limitation this work "
  "repeatedly declares.")
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
  "(run_experiment_choice_binary.mjs, results_choice_binary.json), the follow-up call that "
  "completed the AGREE-REFUTE case (run_missing_refute.mjs), Experiment 4 "
  "(run_experiment_graded_score.mjs, results_graded_score.json), Experiment 5 "
  "(run_experiment_dual_noul.mjs, results_dual_noul.json), Experiment 6 "
  "(run_experiment_triple_mli.mjs + results_triple_mli.json, n=1 pilot; "
  "run_experiment_multidomain_mli.mjs + results_multidomain20_mli.json, 20-domain dataset), "
  "the Figure 1 script "
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

P("The six new states for Experiment 4 (the seventh case, ANCHOR-DETERMINED, reuses the "
  "AGREE-SUPPORT text):")

estados_exp4 = [
    ("CONFLICT-MILD (conflict, mild)",
     'Witness A said the traffic light "might have been red, but I couldn\'t say for sure — '
     'it happened so fast." Witness B said it "could have been green, though I only caught a '
     'glimpse." Neither witness is confident in their own account, and both readily admit '
     'they might be wrong.'),
    ("CONFLICT-MODERATE (conflict, moderate)",
     "Witness A, who had a reasonably clear view of the intersection, said the traffic light "
     "was red at the moment of the collision. Witness B, who was standing some distance away "
     "with a partially obstructed view, said the same traffic light was green at that moment. "
     "Both witnesses seem generally credible, though neither had an ideal vantage point."),
    ("CONFLICT-SEVERE (conflict, severe)",
     "Sensor 1, a newly calibrated, redundant-triple-checked traffic sensor with a documented "
     "error rate of less than 0.001%, recorded the light as RED at 14:03:02.000, with full "
     "internal diagnostics confirming normal operation. Sensor 2, an independent sensor of "
     "the same specification mounted on the same pole and calibrated the same day, recorded "
     "the light as GREEN at the exact same timestamp, 14:03:02.000, with full internal "
     "diagnostics confirming normal operation. Both sensors are considered maximally "
     "reliable; there is no known explanation for the disagreement."),
    ("SILENCE-MILD (absence, mild)",
     "A passing dashcam recorded a few frames of the intersection, but the traffic light "
     "itself is out of frame in all of them; only the road surface and nearby cars are "
     "visible. No other recording or testimony covers the moment in question."),
    ("SILENCE-MODERATE (absence, moderate)",
     'A pedestrian who was not looking at the light mentioned, in an offhand and unprompted '
     'remark days later, that they "vaguely recall something about the light," but could not '
     'say what color when pressed, or whether they were even looking at the right '
     'intersection. No other information exists.'),
    ("SILENCE-SEVERE (absence, severe)",
     "No witnesses were present at the intersection at the time in question. No traffic "
     "cameras were operating in that area that day. There is no record, sensor log, or "
     "testimony of any kind describing the state of the traffic light at that moment."),
]
for titulo, texto in estados_exp4:
    P(titulo, bold=True)
    P(texto, italic=True)

P("Experiment 6 pilot's AMBIGUOUS state (intrinsically vague evidence, traffic-light "
  "domain):", bold=True)
P("A single grainy photograph shows the traffic light mid-transition, rendered as an "
  "indistinct orange-red blur due to motion blur and low light. The photo technician who "
  "examined the image says its quality makes it impossible to tell whether the light had "
  "already reached red or was still yellow. There is only this one photograph; no other "
  "witness, sensor, or recording of the moment exists.", italic=True)

P("The 20 domains of Experiment 6's expanded dataset.", bold=True)
P("Each domain instantiates the same 5-category template (TORN, SILENT, AGREE-SUPPORT, "
  "AGREE-REFUTE, AMBIGUOUS) used above for the traffic light, substituting the subject, the "
  "disputed claim, the sources, and the vague-evidence description. One full worked example "
  "(WEATHER) is shown, and for the remaining 19, the subject and disputed claim; the "
  "complete parameters are in run_experiment_multidomain_mli.mjs in the repository, "
  "generated programmatically by the mkDomain() function to avoid the wording confounds of "
  "Experiment 4.")
P("Full example — WEATHER:", bold=True)
P("TORN: \"Witness A, standing under the awning near the scene, reported that it was "
  "raining at the time of the incident. Witness B, standing at the same location with an "
  "equally credible basis, reported that it was NOT raining at the time of the incident. "
  "Both are considered reliable; there is no indication either one is mistaken.\"", italic=True)
P("SILENT: \"No weather station reading was available regarding whether it was raining at "
  "the time of the incident. No dashcam or security footage from the area exists either. "
  "There is no record of any kind describing whether it was raining at the time of the "
  "incident.\"", italic=True)
P("AGREE-SUPPORT / AGREE-REFUTE: both sources agree it was raining / was not raining, "
  "worded in parallel to the TORN pattern.")
P("AMBIGUOUS: \"A single smartphone photo from a passerby shows wet-looking pavement, but "
  "the meteorologist who reviewed it says reflections from nearby sprinklers make it "
  "impossible to tell whether the wetness was from rain or irrigation. No other weather "
  "record exists.\"", italic=True)
P("The other 19 domains (subject → disputed claim):", bold=True)
table(["Domain", "Disputed claim"],
      [["TRAFFIC", "the traffic light was red"],
       ["PRODUCT", "the phone's screen was cracked upon arrival"],
       ["ATTENDANCE", "the employee was present at the 9am meeting"],
       ["MEDICAL", "the biopsy sample was malignant"],
       ["FINANCE", "the account holder authorized the wire transfer"],
       ["CONTRACT", "the contract clause was signed by both parties"],
       ["INVENTORY", "the warehouse had the item in stock on that date"],
       ["SECURITY", "the door was locked at closing time"],
       ["ACADEMIC", "the student submitted the assignment before the deadline"],
       ["VEHICLE", "the car's brakes were functioning properly before the accident"],
       ["FOODSAFETY", "the restaurant kitchen passed the health inspection that day"],
       ["CONSTRUCTION", "the building's foundation met code specifications"],
       ["INSURANCE", "the claimant's injury occurred on company property"],
       ["ELECTION", "the ballot was received before the polling deadline"],
       ["SOFTWARE", "the deployed code included the security patch"],
       ["CUSTOMS", "the shipment declared its full contents accurately"],
       ["VETERINARY", "the animal showed symptoms of the disease before treatment"],
       ["AVIATION", "the aircraft's pre-flight check was completed"],
       ["REALESTATE", "the property disclosure included the known defect"]],
      "Table 8: The other 19 domains of the Experiment 6 dataset.")

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

P("Experiment 4 (Score, graded determinacy):", bold=True)
code_block("""
const result = await evaluate({
  model: 'typesafe-ai/jev',
  state: STATE_TEXT,
  questions: {
    determinacy: {
      type: 'score',
      instructions: 'How determinate (certain) is the available evidence about the color of the traffic light, regardless of which color it points to?',
      criteria: [
        'Very high confidence: the evidence clearly and unambiguously points to one color.',
        'High confidence: the evidence leans clearly to one color, with minor uncertainty.',
        'Moderate: there is no reliable basis to favor one color over the other.',
        'Low confidence: there is almost no basis to judge the color.',
        'No confidence: there is no basis whatsoever to judge the color.',
      ], // ordered array, not a map
    },
  },
});
""")

P("Experiment 5 (μ/λ composition, two independent boolean questions):", bold=True)
code_block("""
const result = await evaluate({
  model: 'typesafe-ai/jev',
  state: STATE_TEXT, // one of the six states in Appendix A
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
// mu and lambda are not forced to sum to 1: independent questions, not a choice.
""")

P("Experiment 6 (third coordinate I, 20-domain dataset):", bold=True)
code_block("""
function mkDomain(id, subject, claimTrue, claimFalse, reliableA, reliableB,
                   primaryEvidence, secondaryEvidence, ambiguousEvidence) {
  const mu = { type: 'boolean',
    instructions: `Is there credible evidence supporting the claim that ${claimTrue}?` };
  const lambda = { type: 'boolean',
    instructions: `Is there credible evidence supporting the claim that ${claimFalse}?` };
  const indeterminacy = { type: 'boolean',
    instructions: `Is it indeterminate whether ${claimTrue} — that is, does the available `
      + `evidence fail to clearly resolve this either way, regardless of the reason why?` };
  return [ /* TORN, SILENT, AGREE-SUPPORT, AGREE-REFUTE, AMBIGUOUS, each with a state built
              from the template and {mu, lambda, indeterminacy} */ ];
}
// 20 calls to mkDomain(...) generate the 100 states; see run_experiment_multidomain_mli.mjs
// in the repository for the 20 full parameter sets.

const result = await evaluate({
  model: 'typesafe-ai/jev',
  state: STATE_TEXT,
  questions: { mu: item.mu, lambda: item.lambda, indeterminacy: item.indeterminacy },
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
AGREE-REFUTE:   {"wasRed":{"type":"boolean","probability":0.08}}
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
AGREE-REFUTE:   {"lightState":{"choice":"green","probabilities":
                  {"red":0,"green":1,"conflicting_evidence":0,"insufficient_evidence":0}}}
""")

P("Experiment 3 — binary Choice:", bold=True)
code_block("""
TORN-1:         {"lightState":{"choice":"red","probabilities":{"red":0.85,"green":0.15}}}
TORN-2:         {"lightState":{"choice":"red","probabilities":{"red":0.84,"green":0.16}}}
SILENT-1:       {"lightState":{"choice":"red","probabilities":{"red":0.67,"green":0.33}}}
SILENT-2:       {"lightState":{"choice":"red","probabilities":{"red":0.77,"green":0.23}}}
AGREE-SUPPORT:  {"lightState":{"choice":"red","probabilities":{"red":1,"green":0}}}
AGREE-REFUTE:   {"lightState":{"choice":"green","probabilities":{"red":0,"green":1}}}
""")

P("Experiment 4 — Score (graded determinacy):", bold=True)
code_block("""
ANCHOR-DETERMINED:
  {"determinacy":{"score":0.25,"probabilities":{"0":0.75,"1":0.25,"2":0,"3":0,"4":0}}}
CONFLICT-MILD:
  {"determinacy":{"score":2.67,"probabilities":{"0":0,"1":0,"2":0.36,"3":0.62,"4":0.02}}}
CONFLICT-MODERATE:
  {"determinacy":{"score":1.58,"probabilities":{"0":0,"1":0.43,"2":0.56,"3":0.01,"4":0}}}
CONFLICT-SEVERE:
  {"determinacy":{"score":2.04,"probabilities":{"0":0,"1":0,"2":0.97,"3":0.02,"4":0.01}}}
SILENCE-MILD:
  {"determinacy":{"score":3.88,"probabilities":{"0":0,"1":0,"2":0.03,"3":0.07,"4":0.90}}}
SILENCE-MODERATE:
  {"determinacy":{"score":3.66,"probabilities":{"0":0,"1":0,"2":0.02,"3":0.30,"4":0.68}}}
SILENCE-SEVERE:
  {"determinacy":{"score":3.95,"probabilities":{"0":0,"1":0,"2":0.02,"3":0.01,"4":0.97}}}
""")

P("Experiment 5 — μ/λ composition:", bold=True)
code_block("""
TORN-1:         {"mu":{"probability":0.86},"lambda":{"probability":0.84}}
TORN-2:         {"mu":{"probability":0.64},"lambda":{"probability":0.62}}
SILENT-1:       {"mu":{"probability":0.04},"lambda":{"probability":0.04}}
SILENT-2:       {"mu":{"probability":0.05},"lambda":{"probability":0.04}}
AGREE-SUPPORT:  {"mu":{"probability":0.91},"lambda":{"probability":0.06}}
AGREE-REFUTE:   {"mu":{"probability":0.06},"lambda":{"probability":0.92}}
""")

P("Experiment 6 — pilot (n=1, traffic-light domain, with I added):", bold=True)
code_block("""
TORN-1:         mu=0.87  lambda=0.84  I=0.89
TORN-2:         mu=0.65  lambda=0.60  I=0.88
SILENT-1:       mu=0.04  lambda=0.04  I=0.97
SILENT-2:       mu=0.05  lambda=0.04  I=0.95
AGREE-SUPPORT:  mu=0.92  lambda=0.06  I=0.14
AGREE-REFUTE:   mu=0.06  lambda=0.92  I=0.12
AMBIGUOUS:      mu=0.12  lambda=0.06  I=0.97
""")

P("Experiment 6 — 20-domain dataset (n=20 per category). The full 100 rows are in "
  "results_multidomain20_mli.json in the repository; the per-category summary is in "
  "Table 7. Sample, WEATHER domain:", bold=True)
code_block("""
WEATHER-TORN:           mu=0.81  lambda=0.85  I=0.84
WEATHER-SILENT:         mu=0.03  lambda=0.05  I=0.97
WEATHER-AGREE-SUPPORT:  mu=0.92  lambda=0.04  I=0.09
WEATHER-AGREE-REFUTE:   mu=0.04  lambda=0.88  I=0.12
WEATHER-AMBIGUOUS:      mu=0.13  lambda=0.14  I=0.95
""")

doc.save(OUT)
print("NCML English format ->", OUT)
