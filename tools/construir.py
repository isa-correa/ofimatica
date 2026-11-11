#!/usr/bin/env python3
"""Une preguntas (tools/preguntas.json) y explicaciones (tools/respuestas/*.json) en un archivo de datos por tema (data/word.js, data/excel.js, data/windows.js...).
Entran todas las preguntas: las que aún no tienen explicación salen con su respuesta correcta y un aviso.
Si algo no cuadra, avisa y para. Uso (desde la raíz del proyecto): python3 tools/construir.py"""
import glob, json, re, sys

D = json.load(open("tools/preguntas.json", encoding="utf8"))["preguntas"]
R = {}
for f in sorted(glob.glob("tools/respuestas/*.json")):
    R.update(json.load(open(f, encoding="utf8")))

# Bloques: los apartados del temario. Una pregunta sin explicar va al bloque "pendiente" de su tema.
BLOQUES = {
    "word": [("word-entorno", "Qué es Word, inicio y área de trabajo"),
             ("word-archivo", "Ficha Archivo: guardar, abrir, imprimir, compartir y opciones"),
             ("word-inicio", "Ficha Inicio: portapapeles, fuente, párrafo, estilos y edición"),
             ("word-insertar", "Ficha Insertar: páginas, tablas, ilustraciones, encabezados y texto"),
             ("word-diseno", "Ficha Diseño: temas, formato y fondo de página"),
             ("word-disposicion", "Ficha Disposición: configurar página, párrafo y organizar"),
             ("word-referencias", "Ficha Referencias: tablas de contenido, notas, citas e índices"),
             ("word-correspondencia", "Ficha Correspondencia: sobres, etiquetas y combinar"),
             ("word-revisar", "Ficha Revisar: ortografía, comentarios, control de cambios y proteger"),
             ("word-vista", "Ficha Vista: vistas, mostrar, zoom y ventana"),
             ("word-atajos", "Atajos de teclado"),
             ("word-pendiente", "Word: preguntas aún sin explicar")],
    "excel": [("excel-general", "Excel 365"),
              ("excel-pendiente", "Excel: preguntas aún sin explicar")],
    "windows": [("windows-general", "Windows 11")],
    "access": [("access-general", "Access 365")],
    "outlook": [("outlook-general", "Outlook 365")],
    "internet": [("internet-general", "Internet y redes")],
    "ia": [("ia-general", "Inteligencia artificial y Copilot")],
    "basica": [("basica-general", "Informática básica")],
}
NOMBRES = {"word": "Tema 4 · Word 365", "excel": "Tema 5 · Excel 365", "windows": "Windows 11", "access": "Access 365",
           "outlook": "Outlook 365", "internet": "Internet y redes", "ia": "Inteligencia artificial y Copilot",
           "basica": "Informática básica"}
TEMAS = list(BLOQUES)
validos = {b for bl in BLOQUES.values() for b, _ in bl}
norm = lambda x: re.sub(r"\W+", "", x.lower())
clave = lambda p: norm(p["enunciado"]) + "|" + "|".join(sorted(map(norm, p["opciones"])))
ids = {p["id"] for p in D}
err = []

# Una pregunta repetida en otro test hereda la explicación de la primera que se explicó.
primera = {}
for p in D:
    if p["id"] in R:
        primera.setdefault(clave(p), p["id"])
for p in D:
    if p["id"] not in R and clave(p) in primera:
        r = R[primera[clave(p)]]
        orig = next(q for q in D if q["id"] == primera[clave(p)])
        if p["opciones"] == orig["opciones"]:  # si cambia el orden de las opciones, se explica aparte
            R[p["id"]] = r

salida = []
for p in D:
    q = dict(p)
    r = R.get(p["id"])
    if r:
        if r.get("correcta", p["correcta"]) != p["correcta"]:
            err.append(f"{p['id']}: la explicación da la {r['correcta']} y la plantilla la {p['correcta']}")
        if len(r["justificaciones"]) != len(p["opciones"]):
            err.append(f"{p['id']}: {len(r['justificaciones'])} justificaciones para {len(p['opciones'])} opciones")
        if r["bloque"] not in validos or r["bloque"].endswith("-pendiente") or not r["bloque"].startswith(p["tema"]):
            err.append(f"{p['id']}: bloque {r['bloque']}")
        if re.search("[—–]", json.dumps(r, ensure_ascii=False)):
            err.append(f"{p['id']}: lleva raya o semirraya")
        q.update({k: v for k, v in r.items() if k != "correcta"})
    else:
        q["bloque"] = p["tema"] + "-pendiente"
    del q["tema"]
    salida.append(q)

grupos = {}
for p in salida:
    grupos.setdefault(clave(p), []).append(p)
for g in grupos.values():
    if len(g) > 1:
        if len({norm(p["opciones"][p["correcta"]]) for p in g}) > 1:
            err.append("respuesta distinta en la misma pregunta: " + ", ".join(p["id"] for p in g))
        for p in g:
            p["dup"] = g[0]["id"]
fantasma = set(R) - ids
if fantasma:
    err.append(f"ids desconocidos: {sorted(fantasma)}")
if err:
    sys.exit("\n".join(err))

# Tests completos: los oficiales y los exámenes de clase se pueden hacer enteros, como salieron.
tema_de = {p["id"]: p["tema"] for p in D}
casos = {t: [] for t in TEMAS}
por_test = {}
for p in salida:
    if p["origen"] in ("oficiales", "examenes"):
        por_test.setdefault((tema_de[p["id"]], p["test"]), []).append(p)
for (tema, t), ps in por_test.items():
    ps.sort(key=lambda p: p["n"])
    casos[tema].append({"id": "test-" + ps[0]["id"].rsplit("-", 1)[0], "titulo": t, "texto": "", "corto": True,
                        "ids": [p["id"] for p in ps]})

total = hechas = 0
for tema in TEMAS:
    ps = [p for p in salida if tema_de[p["id"]] == tema]
    usados = {p["bloque"] for p in ps}
    bl = [{"id": a, "nombre": b} for a, b in BLOQUES[tema] if a in usados]
    datos = {"id": tema, "nombre": NOMBRES[tema], "bloques": bl, "calendarios": {}, "casos": casos[tema], "preguntas": ps}
    with open(f"data/{tema}.js", "w", encoding="utf8") as f:
        f.write("window.BANCO = window.BANCO || [];\nwindow.BANCO.push(" + json.dumps(datos, ensure_ascii=False, separators=(",", ":")) + ");\n")
    n = sum(1 for p in ps if "justificaciones" in p)
    total += len(ps); hechas += n
    print(f"{len(ps)} preguntas ({n} explicadas) · {len(casos[tema])} tests completos → data/{tema}.js")
print(f"{hechas} de {total} preguntas explicadas")
