#!/usr/bin/env python3
"""Uso: validar.py <NN>. Comprueba tools/respuestas/lote-NN.json contra el lote de entrada."""
import json, os, re, sys
S = os.path.dirname(os.path.abspath(__file__))
n = sys.argv[1].zfill(2)
L = json.load(open(f"{S}/lotes/lote-{n}.json", encoding="utf8"))
try:
    R = json.load(open(f"{S}/../respuestas/lote-{n}.json", encoding="utf8"))
except Exception as e:
    sys.exit(f"JSON no válido: {e}")
B = {"word-entorno", "word-archivo", "word-inicio", "word-insertar", "word-diseno", "word-disposicion", "word-referencias",
     "word-correspondencia", "word-revisar", "word-vista", "word-atajos", "excel-general"}
err = []
ids = {q["id"]: q for q in L["preguntas"]}
for i in ids:
    if i not in R: err.append(f"{i}: falta")
for i, r in R.items():
    if i not in ids: err.append(f"{i}: id que no es de este lote"); continue
    q = ids[i]
    falta = [k for k in ("bloque", "precepto", "correcta", "justificaciones") if k not in r]
    if falta: err.append(f"{i}: falta {', '.join(falta)}"); continue
    if r["bloque"] not in B or not r["bloque"].startswith(q["tema"]): err.append(f"{i}: bloque {r['bloque']}")
    if r["correcta"] != q["correcta"]: err.append(f"{i}: correcta {r['correcta']}, la plantilla dice {q['correcta']} (no se cambia: usa revisar)")
    if len(r["justificaciones"]) != len(q["opciones"]): err.append(f"{i}: {len(r['justificaciones'])} justificaciones, {len(q['opciones'])} opciones")
    if re.search("[—–]", json.dumps(r, ensure_ascii=False)): err.append(f"{i}: raya o semirraya")
    if "revisar" in r and not isinstance(r["revisar"], str): err.append(f"{i}: revisar debe ser texto")
    for j, t in enumerate(r["justificaciones"]):
        if len(t) < 25: err.append(f"{i}: justificación {j} demasiado corta")
        if not re.match(r"(Es esta\.|No\.|Esta es la falsa|Es verdadera)", t): err.append(f"{i}: justificación {j} no empieza como toca")
print("\n".join(err) if err else f"OK lote {n}: {len(R)} respuestas")
