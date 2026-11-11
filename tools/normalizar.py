#!/usr/bin/env python3
"""Limpia informatica-todo.json y deja las preguntas con un id estable en tools/preguntas.json.
La respuesta correcta ya viene de la plantilla (pantalla de revisión de easy-lms).
Además incorpora tools/oficiales-repo.json: las 226 oficiales del INAP del repo isa-correa/ofimatica (Windows, Word, Excel,
Access, Outlook, Internet, IA e informática básica), actualizadas a Windows 11 y Microsoft 365.
Uso (desde la raíz del proyecto): python3 tools/normalizar.py"""
import json, re

ORIGEN, DESTINO = "informatica-todo.json", "tools/preguntas.json"
ABBR = {"autoevaluacion": "au", "oficiales": "of", "examenes": "ex", "votaciones": "vo"}
NOMBRE = {"Autoevaluacion": "Autoevaluación", "Oficial": "Oficial", "Examen": "Examen", "Votaciones Clase": "Votaciones clase"}
TEMAS = {"4": "word", "5": "excel"}
LETRA = {"word": "w", "excel": "x"}
# Preguntas que dependen de una imagen que no tenemos. No entran hasta que se añada la imagen.
SIN_IMAGEN = {"w-ex-05-004", "w-ex-06-005", "w-ex-06-006"}
REPO = "tools/oficiales-repo.json"
LETRA_REPO = {"word": "w", "excel": "x", "windows": "win", "access": "acc", "outlook": "out", "internet": "int", "ia": "ia", "basica": "bas"}
EXAMENES_REPO = ["2019 · ord.", "2019 · extra", "2022 · ord.", "2022 · extra", "14 dic. 2024", "2024 · extra",
                 "23 mayo 2026", "julio 2026 · extra"]  # en orden cronológico
norm = lambda x: re.sub(r"\W+", "", x.lower())
clave = lambda p: norm(p["enunciado"]) + "|" + "|".join(sorted(map(norm, p["opciones"])))


def limpio(t):
    return re.sub(r"[ \t]+", " ", t.replace("\xa0", " ")).strip()


def oficiales_del_repo(preguntas):
    """Añade al final las oficiales del repo. Las tres que ya estaban en un test oficial de clase con otra redacción
    sustituyen a la antigua (campo "sustituye"). Si una es idéntica a otra ya existente, copia su orden de opciones
    para que construir.py las trate como repetida y herede la explicación."""
    repo = json.load(open(REPO, encoding="utf8"))
    por_id = {p["id"]: p for p in preguntas}
    por_rid = {r["rid"]: r for r in repo["preguntas"]}
    for pid, rid in repo["sustituye"].items():
        r, p = por_rid[rid], por_id[pid]
        p["enunciado"], p["opciones"], p["correcta"] = r["enunciado"], r["opciones"], r["correcta"]
    existentes = {}
    for p in preguntas:
        existentes.setdefault(clave(p), p)
    for r in repo["preguntas"]:
        e = EXAMENES_REPO.index(r["exam"]) + 1
        p = {"id": f"{LETRA_REPO[r['cat']]}-in-{e:02d}-{r['n']:03d}", "tema": r["cat"], "origen": "oficiales",
             "test": "INAP " + r["exam"].replace(" · ", " "), "n": r["n"], "enunciado": limpio(r["enunciado"]),
             "opciones": [limpio(o) for o in r["opciones"]], "correcta": r["correcta"]}
        ya = existentes.get(clave(p))
        if ya and norm(ya["opciones"][ya["correcta"]]) == norm(p["opciones"][p["correcta"]]):
            p["opciones"], p["correcta"] = list(ya["opciones"]), ya["correcta"]
        preguntas.append(p)
    return len(repo["preguntas"])


def main():
    d = json.load(open(ORIGEN, encoding="utf8"))
    preguntas, fuera = [], []
    for grupo, tests in d.items():
        cuenta = {}  # numeración de tests por tema dentro de cada grupo
        for t in tests:
            m = re.match(r"Tema (\d+) - .*\((.+?) (\d+)( parte \d+)?\)$", t["test"])
            if not m:
                raise SystemExit("título de test no reconocido: " + t["test"])
            tema = TEMAS[m.group(1)]
            cuenta[tema] = cuenta.get(tema, 0) + 1
            it = cuenta[tema]
            titulo = NOMBRE.get(m.group(2), m.group(2)) + " " + m.group(3) + (m.group(4) or "")
            for q in t["preguntas"]:
                pid = f"{LETRA[tema]}-{ABBR[grupo]}-{it:02d}-{q['n']:03d}"
                if pid in SIN_IMAGEN:
                    fuera.append(pid)
                    continue
                enun = "\n".join(limpio(x) for x in q["enunciado"].split("\n") if x.strip())
                preguntas.append({"id": pid, "tema": tema, "origen": grupo, "test": titulo, "n": q["n"],
                                  "enunciado": enun, "opciones": [limpio(o) for o in q["opciones"]],
                                  "correcta": q["correcta"]})
    n_repo = oficiales_del_repo(preguntas)
    json.dump({"preguntas": preguntas}, open(DESTINO, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print(n_repo, "oficiales del repo incorporadas")
    print(len(preguntas), "preguntas →", DESTINO, "·", len(fuera), "apartadas por faltar la imagen:", ", ".join(fuera))


main()
