# -*- coding: utf-8 -*-
"""Revision adversarial del paper NCML sobre Jev/modelos de evaluacion tipada: verificar
veracidad de cada afirmacion factual, criticar el diseno experimental y el argumento, y dar
correcciones concretas antes de considerarlo listo para enviar."""
import os, json, time, re, concurrent.futures as cf
import urllib.request

KEY = os.environ["OPENROUTER_API_KEY"]
MODELS = [
    "openai/gpt-6-astra-pro",
    "anthropic/claude-opus-5",
    "google/gemini-3.1-pro-preview",
    "x-ai/grok-4.6",
    "deepseek/deepseek-v4-pro",
]

MANUSCRIPT = open("paper/manuscript_v0.1.md", encoding="utf-8").read()

SYSTEM = """Eres un comite de revision compuesto por: (1) un revisor de veracidad, cuyo unico trabajo
es marcar cada afirmacion factual verificable como CONFIRMADA, NO VERIFICABLE POR TI, o
PROBABLEMENTE FALSA/EXAGERADA, sin dar el beneficio de la duda; (2) un metodologo que evalua si el
experimento (n=5, una sola llamada por caso) sostiene el lenguaje usado ("confirma la prediccion");
(3) un editor que evalua si el argumento central (Jev como convergencia de dos categorias, el
colapso conflicto/ignorancia) es solido y esta bien enmarcado. No elogies genericamente. Responde en
espanol neutro, sin voseo, maximo 900 palabras."""

USER = f"""MANUSCRITO COMPLETO (borrador v0.1, destino NCML, nota de campo no Q1):
<<<
{MANUSCRIPT}
>>>

TAREA (secciones exactas):

## 1. Verificacion de afirmaciones factuales
Lista cada afirmacion factual especifica y verificable sobre Jev/TypeSafe AI/Vercel AI Gateway (fecha
de lanzamiento, fundador, velocidad/costo relativo, metodo de entrenamiento RLCD, los 3 tipos de
pregunta, el nombre "Noul" vs "boolean" del SDK, existencia de decider/reflex). Para cada una: marca
CONFIRMADA (si tu conocimiento la corrobora independientemente), NO VERIFICABLE (si no tienes forma de
confirmarla de forma independiente mas alla de lo que dice el propio manuscrito), o
SOSPECHOSA/EXAGERADA (si algo suena a marketing sin respaldo o es internamente inconsistente).

## 2. Critica metodologica del experimento
Con n=5 casos completados, una sola llamada por caso, un solo tipo de pregunta de los tres que ofrece
Jev, y un solo dominio (semaforos): ¿el lenguaje del paper ("confirma la prediccion") esta justificado,
o es sobreclaim para esa n? ¿Que le falta al diseno para sostener esa afirmacion con mas rigor (sin
pedir que se rehaga todo el experimento)?

## 3. Critica del argumento central
¿La taxonomia de 5 categorias (chat generativo, salida forzada, LLM-as-judge, clasificador clasico,
Jev como convergencia de 3 y 4) es defendible, o hay una categoria mal ubicada, redundante, o una mejor
forma de agruparlas? ¿La conexion con el teorema de invarianza por reflexion de AET (colapso
conflicto/ignorancia) es una aplicacion valida, o hay un salto logico entre "un score de cercania en un
reticulo anotado" y "una probabilidad calibrada de un producto comercial de proposito distinto"?

## 4. Las 3-5 correcciones mas importantes antes de enviar
Lista priorizada, concreta y accionable (no generica).

## 5. Veredicto
Una frase: ¿esta nota de campo, con las correcciones anteriores aplicadas, es publicable en una revista
no indexada de bajo riesgo (NCML) tal como esta planteada, o tiene un problema de fondo que ni las
correcciones resuelven?"""

os.makedirs("respuestas_review_paper", exist_ok=True)


def call(model):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": USER}],
        "max_tokens": 8000,
        "temperature": 0.3,
    }).encode()
    err = None
    for _ in range(3):
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions", data=body,
            headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
                     "HTTP-Referer": "https://mleyvaz.github.io", "X-Title": "NCML Jev paper review"})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                data = json.loads(r.read())
            txt = data["choices"][0]["message"].get("content") or data["choices"][0]["message"].get("reasoning") or ""
            return model, txt, data.get("usage", {}), None
        except Exception as e:
            err = str(e)
            if hasattr(e, "read"):
                try:
                    err += " | " + e.read().decode()[:400]
                except Exception:
                    pass
            time.sleep(5)
    return model, "", {}, err


def fname(model):
    return "respuestas_review_paper/" + re.sub(r"[^a-z0-9.-]+", "_", model) + ".md"


t0 = time.time()
results = []
with cf.ThreadPoolExecutor(len(MODELS)) as ex:
    for model, txt, usage, err in ex.map(call, MODELS):
        with open(fname(model), "w", encoding="utf-8") as f:
            f.write(f"# {model}\n\n" + (txt if txt else f"ERROR: {err}"))
        results.append(model)
        print(f"{model}: {len(txt)} chars, usage={usage}, err={err}", flush=True)

with open("respuestas_review_paper/_CONSOLIDADO.md", "w", encoding="utf-8") as f:
    f.write("# Revision adversarial del paper NCML (Jev / modelos de evaluacion tipada)\n\n")
    f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M')} - Modelos: {len(MODELS)} - tiempo {time.time() - t0:.0f}s\n\n")
    for model in results:
        f.write(open(fname(model), encoding="utf-8").read() + "\n\n---\n\n")
print("done", round(time.time() - t0))
