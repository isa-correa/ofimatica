#!/usr/bin/env python3
"""Pasa los PDF de apuntes/ a tools/trabajo/apuntes.txt, con una cabecera por página:
=== T4 · Tema 4 (temario) · pág 51 · 4.3 Ficha Insertar ===
Hace falta PyMuPDF (import fitz). Uso (desde la raíz): python3 -I tools/trabajo/apuntes2txt.py"""
import os, re
import fitz

S = os.path.dirname(os.path.abspath(__file__))
RAIZ = S + "/../.."
# (archivo, código, nombre, primera página impresa)
DOCS = [("apuntes/tema-4/Tema-4-parte-1.pdf", "T4", "Tema 4 (temario)", 1),
        ("apuntes/tema-4/Tema-4-parte-2.pdf", "T4", "Tema 4 (temario)", 33),
        ("apuntes/tema-4/Esquema-resumen-Word-2026.pdf", "T4-esquema", "Esquema resumen Word", 1),
        ("apuntes/tema-4/Cinta-de-Opciones-Word-365.pdf", "T4-cinta", "Cinta de opciones Word", 1),
        ("apuntes/tema-4/Atajos-Word-365.pdf", "T4-atajos", "Atajos de teclado Word", 1),
        ("apuntes/tema-5/Tema-5-parte-1.pdf", "T5", "Tema 5 (temario)", 1)]
# Apartados del temario de Word, por la página impresa donde empiezan (índice del tema 4).
SECCIONES = {"T4": [(1, "1 a 3. Qué es Word e inicio"), (8, "4. Área de trabajo y cinta de opciones"),
                    (12, "4.1 Ficha Archivo"), (24, "4.2 Ficha Inicio"), (50, "4.3 Ficha Insertar"),
                    (66, "4.4 Ficha Diseño"), (72, "4.5 Ficha Disposición"), (81, "4.6 Ficha Referencias"),
                    (85, "4.7 Ficha Correspondencia"), (88, "4.8 Ficha Revisar"), (94, "4.9 Ficha Vista")]}


def seccion(cod, pag):
    s = [n for p, n in SECCIONES.get(cod, []) if p <= pag]
    return " · " + s[-1] if s else ""


out = []
for f, cod, nombre, ini in DOCS:
    doc = fitz.open(os.path.join(RAIZ, f))
    for i, page in enumerate(doc):
        t = page.get_text()
        t = re.sub(r"Estefanía Dueñas \| Preparadora Informática AGE\s*\n\s*\d*\s*\n?", "", t)
        t = re.sub(r"[ \t\xa0]+", " ", t)
        t = re.sub(r"\n\s*\n+", "\n", t).strip()
        out.append(f"=== {cod} · {nombre} · pág {ini + i}{seccion(cod, ini + i)} ===\n{t}\n")
open(S + "/apuntes.txt", "w", encoding="utf8").write("\n".join(out))
print(len(out), "páginas → tools/trabajo/apuntes.txt")
