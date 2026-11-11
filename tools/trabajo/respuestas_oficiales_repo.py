#!/usr/bin/env python3
"""Genera tools/respuestas/lote-24.json con las explicaciones de las oficiales del repo (tools/oficiales-repo.json).
- Cada una lleva como explicación de la opción correcta la de tools/explicaciones-oficiales/<tema>.json (ampliada), o el texto del repo si falta; las otras opciones quedan vacías y no se muestran.
- Las que son idénticas a una ya explicada no se generan: construir.py les hereda la explicación.
- Las tres que sustituyen a una antigua conservan la explicación antigua con las justificaciones recolocadas al orden nuevo.
Uso (desde la raíz, después de normalizar.py): python3 -I tools/trabajo/respuestas_oficiales_repo.py [preguntas_antiguas.json]"""
import difflib, glob, json, re, sys

D = json.load(open("tools/preguntas.json", encoding="utf8"))["preguntas"]
REPO = json.load(open("tools/oficiales-repo.json", encoding="utf8"))
VIEJAS = {p["id"]: p for p in json.load(open(sys.argv[1], encoding="utf8"))["preguntas"]} if len(sys.argv) > 1 else {}
EXPL = {}
for f in sorted(glob.glob("tools/explicaciones-oficiales/*.json")):
    EXPL.update(json.load(open(f, encoding="utf8")))
R = {}
for f in sorted(glob.glob("tools/respuestas/lote-*.json")):
    if not f.endswith("lote-24.json"):
        R.update(json.load(open(f, encoding="utf8")))
norm = lambda x: re.sub(r"\W+", "", x.lower())
clave = lambda p: norm(p["enunciado"]) + "|" + "|".join(sorted(map(norm, p["opciones"])))
por_rid = {r["rid"]: r for r in REPO["preguntas"]}
id_de = {}  # rid -> id de la plataforma
for r in REPO["preguntas"]:
    e = EXAM = ["2019 · ord.", "2019 · extra", "2022 · ord.", "2022 · extra", "14 dic. 2024", "2024 · extra", "23 mayo 2026", "julio 2026 · extra"].index(r["exam"]) + 1
    letra = {"word": "w", "excel": "x", "windows": "win", "access": "acc", "outlook": "out", "internet": "int", "ia": "ia", "basica": "bas"}[r["cat"]]
    id_de[r["rid"]] = f"{letra}-in-{e:02d}-{r['n']:03d}"


def formato(t):
    """La app solo entiende **negrita**: el código entre comillas invertidas pasa a negrita y la cursiva se quita."""
    t = re.sub(r"`([^`]+)`", r"**\1**", t)
    return re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", t)


def sin_rayas(t):
    t = re.sub(r"\s*[—–]\s*(.+?)\s*[—–]\s*", r", \1, ", t)
    return re.sub(r"\s*[—–]\s*", ": ", t)


salida = {}
# 1. Las que sustituyen a una antigua: se recolocan las justificaciones.
for pid, rid in REPO["sustituye"].items():
    vieja, nueva = VIEJAS[pid], next(p for p in D if p["id"] == pid)
    r = R[pid]
    mapa = []
    for o in nueva["opciones"]:
        mapa.append(max(range(len(vieja["opciones"])), key=lambda j: difflib.SequenceMatcher(None, norm(o), norm(vieja["opciones"][j])).ratio()))
    assert sorted(mapa) == [0, 1, 2, 3], (pid, mapa)
    assert mapa[nueva["correcta"]] == vieja["correcta"], pid
    r = dict(r); r["correcta"] = nueva["correcta"]; r["justificaciones"] = [r["justificaciones"][j] for j in mapa]
    salida[pid] = r
    print("recolocada", pid, mapa)

# 2. Las nuevas.
por_id = {p["id"]: p for p in D}
explicadas = {}
for p in D:
    if p["id"] in R or p["id"] in salida:
        explicadas.setdefault(clave(p), p)
for r in REPO["preguntas"]:
    p = por_id[id_de[r["rid"]]]
    gemela = explicadas.get(clave(p))
    if gemela and gemela["opciones"] == p["opciones"]:
        continue  # hereda
    ex = EXPL.get(p["id"])
    why = formato(sin_rayas(ex["just"] if ex else r["why"]))
    just = ["Es esta. " + why if i == p["correcta"] else "" for i in range(len(p["opciones"]))]
    e = {"bloque": r["bloque"], "precepto": f"Pregunta oficial del INAP · {r['exam'].replace(' · ', ' ')} · nº {r['n']}", "correcta": p["correcta"], "justificaciones": just}
    nota = {"actualizada": "Oficial actualizada: el INAP la redactó para una versión anterior de Windows u Office y aquí está adaptada a Windows 11 y Microsoft 365.",
            "reescrita": "Oficial reescrita para Windows 11: la original se refería a algo que cambió en esa versión."}.get(r["badge"])
    ojo = " ".join(x for x in (ex.get("ojo") if ex else "", nota) if x)
    if ojo:
        e["ojo"] = formato(ojo)
    if ex and ex.get("revisar"):
        e["revisar"] = formato(ex["revisar"])
    salida[p["id"]] = e

json.dump(salida, open("tools/respuestas/lote-24.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(len(salida), "respuestas → tools/respuestas/lote-24.json")
