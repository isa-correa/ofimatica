#!/usr/bin/env python3
"""Reparte las preguntas sin explicar en lotes de ~25 en tools/trabajo/lotes/.
Orden: Word (oficiales, exámenes de clase, votaciones, autoevaluación) y luego Excel.
Las repetidas solo van en su primera aparición. Lo ya explicado o ya repartido no vuelve a salir.
Uso: python3 -I tools/trabajo/hacer_lotes.py [tamaño]"""
import glob, json, os, re, sys
S = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(S + "/../preguntas.json", encoding="utf8"))["preguntas"]
tam = int(sys.argv[1]) if len(sys.argv) > 1 else 25
hechas, usadas = set(), set()
for f in glob.glob(S + "/../respuestas/*.json"):
    hechas |= set(json.load(open(f, encoding="utf8")))
for f in glob.glob(S + "/lotes/*.json"):
    usadas |= {p["id"] for p in json.load(open(f, encoding="utf8"))["preguntas"]}
norm = lambda x: re.sub(r"\W+", "", x.lower())
clave = lambda p: norm(p["enunciado"]) + "|" + "|".join(map(norm, p["opciones"]))
ORDEN = {"oficiales": 0, "examenes": 1, "votaciones": 2, "autoevaluacion": 3}
D.sort(key=lambda p: (p["tema"] != "word", ORDEN[p["origen"]]))  # sort estable: respeta el orden de cada test
vistas, pend = {}, []
for p in D:
    vistas.setdefault(clave(p), p["id"])
for p in D:
    if p["id"] not in hechas and p["id"] not in usadas and vistas[clave(p)] == p["id"]:
        pend.append(p)
n = max([0] + [int(re.search(r"(\d+)", os.path.basename(f)).group(1)) for f in glob.glob(S + "/lotes/lote-*.json")])
ini = n
for i in range(0, len(pend), tam):
    n += 1
    json.dump({"preguntas": pend[i:i + tam]}, open(f"{S}/lotes/lote-{n:02d}.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(n - ini, "lotes nuevos (", len(pend), "preguntas ), del", ini + 1, "al", n)
