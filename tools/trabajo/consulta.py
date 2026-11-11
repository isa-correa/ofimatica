#!/usr/bin/env python3
"""Consulta de los apuntes (tools/trabajo/apuntes.txt). Uso:
  consulta.py buscar "interlineado"         dónde sale una expresión (sin distinguir tildes ni mayúsculas)
  consulta.py buscar "sangría" "francesa"   páginas donde salen todas esas expresiones
  consulta.py pag T4 51                      una página entera (T4, T4-esquema, T4-cinta, T4-atajos, T5)
  consulta.py indice                         lista de páginas con su apartado
"""
import os, re, sys, unicodedata

S = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 2:
    sys.exit(__doc__)
txt = open(S + "/apuntes.txt", encoding="utf8").read()
partes = re.split(r"(?m)^(=== .+ ===)$", txt)[1:]
PAGS = [(partes[i], partes[i + 1].strip()) for i in range(0, len(partes), 2)]


def plano(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


modo = sys.argv[1]
if modo == "indice":
    for cab, _ in PAGS:
        print(cab)
elif modo == "pag":
    cod, n = sys.argv[2], sys.argv[3]
    hit = [(c, t) for c, t in PAGS if c.startswith(f"=== {cod} ·") and f"· pág {n}" in c and re.search(rf"pág {n}\b", c)]
    for c, t in hit:
        print(c); print(t)
    if not hit:
        print("no existe esa página")
elif modo == "buscar":
    pats = [plano(p) for p in sys.argv[2:]]
    vistos = 0
    for cab, t in PAGS:
        pt = plano(t)
        if not all(p in pt for p in pats):
            continue
        lineas = t.split("\n")
        pl = [plano(l) for l in lineas]
        idx = [i for i, l in enumerate(pl) if pats[0] in l] or [0]
        print(cab)
        ult = -99
        for i in idx[:4]:
            if i - ult < 5:
                continue
            print("\n".join(lineas[max(0, i - 2):i + 6])[:900]); print("  ...")
            ult = i
        vistos += 1
        if vistos >= 8:
            print("(hay más páginas; afina la búsqueda)"); break
    if not vistos:
        print("sin resultados")
else:
    sys.exit(__doc__)
