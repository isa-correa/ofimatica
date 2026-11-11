#!/usr/bin/env python3
"""Parsea el texto de la pantalla de revision de ace.easy-lms.com (despues de
responder con cualquier opcion y enviar) y devuelve una lista de preguntas
con enunciado, opciones y el indice de la opcion correcta.
Uso: python3 parse_review.py <tema> <categoria> <clase_o_test> < texto.txt > salida.json
"""
import sys, re, json

MARKERS = {"Respuesta equivocada", "Corregir respuesta", "Tu respuesta"}

def parse(text):
    text = re.sub(r"^(\d+)\.\s+", r"\1.\n", text, flags=re.MULTILINE)
    lines = [l.strip() for l in text.split("\n")]
    # localizar inicio: primera linea que sea solo "1."
    start = None
    for i, l in enumerate(lines):
        if re.fullmatch(r"1\.", l):
            start = i
            break
    if start is None:
        raise SystemExit("No se encontro el inicio '1.' en el texto")
    lines = lines[start:]

    preguntas = []
    i = 0
    n = len(lines)
    num_re = re.compile(r"^(\d+)\.$")
    while i < n:
        m = num_re.match(lines[i])
        if not m:
            i += 1
            continue
        qnum = int(m.group(1))
        i += 1
        # enunciado: puede repetirse en 1 o 2 lineas identicas; acumulamos hasta linea vacia
        enun_lines = []
        while i < n and lines[i] != "":
            enun_lines.append(lines[i])
            i += 1
        # quitar duplicados exactos consecutivos (la web repite el enunciado dos veces en autoevaluacion)
        dedup = []
        for l in enun_lines:
            if not dedup or dedup[-1] != l:
                dedup.append(l)
        enunciado = dedup[0] if dedup else ""
        # saltar lineas vacias
        while i < n and lines[i] == "":
            i += 1
        # linea "Obtuvo X de Y punto(s)"
        obtuvo = ""
        if i < n and lines[i].startswith("Obtuvo"):
            obtuvo = lines[i]
            i += 1
        while i < n and lines[i] == "":
            i += 1
        # opciones hasta el siguiente "N+1." o fin
        opciones = []
        correcta = None
        cur_opt = None
        seen_marker = False
        done_opciones = False
        nota = []
        while i < n:
            l = lines[i]
            if num_re.match(l):
                break
            if l == "":
                i += 1
                # una linea en blanco tras haber visto ya algun marcador
                # cierra el bloque de opciones (lo que sigue es nota/explicacion)
                if seen_marker:
                    done_opciones = True
                continue
            if done_opciones:
                # texto residual (explicacion) hasta la siguiente pregunta: se ignora
                nota.append(l)
                i += 1
                continue
            if l in MARKERS:
                if l == "Corregir respuesta" and cur_opt is not None:
                    correcta = len(opciones) - 1
                seen_marker = True
                i += 1
                continue
            # es texto de opcion
            opciones.append(l)
            cur_opt = l
            i += 1
        preguntas.append({
            "n": qnum,
            "enunciado": enunciado,
            "opciones": opciones,
            "correcta": correcta,
        })
    return preguntas

if __name__ == "__main__":
    text = sys.stdin.read()
    preguntas = parse(text)
    print(json.dumps(preguntas, ensure_ascii=False, indent=1))
