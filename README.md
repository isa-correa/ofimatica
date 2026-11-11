# Test de oposición C1 AGE: informática

Exámenes tipo test de Word 365 (tema 4) y Excel 365 (tema 5) con las respuestas explicadas a partir de los apuntes, más las 226 preguntas oficiales del INAP de ofimática (Windows 11, Word, Excel, Access, Outlook, Internet, IA e informática básica) de los ocho exámenes de ingreso libre, actualizadas a Windows 11 y Microsoft 365. Es la misma app que la de contratos y subvenciones, con estadísticas propias (claves `informatica-*` en el navegador).

Se publica tal cual en GitHub Pages: solo hay que subir `index.html`, `favicon.svg`, `css`, `js` y `data`. La carpeta `apuntes` no se publica.

## Pestañas
- **Examen**: preguntas mezcladas por tema, bloque del temario y procedencia (oficiales, exámenes de clase, votaciones, autoevaluación).
- **Tests completos**: los exámenes de clase y los oficiales, enteros y en su orden.
- **Apuntes**: aparece sola cuando exista `data/esquemas.js`. Todavía no está.

Las preguntas sin explicar ya salen, con su respuesta correcta (la de la plantilla) y un aviso en la justificación. Están en el bloque "aún sin explicar" de su tema y van pasando a su bloque a medida que se explican.

## Flujo
1. `python3 tools/normalizar.py`: de `informatica-todo.json` y `tools/oficiales-repo.json` a `tools/preguntas.json`, con un id estable por pregunta (`w-of-01-003`: Word, oficial 1, pregunta 3; `win-in-03-045`: Windows, INAP 2022 ordinaria, nº 45). Tres preguntas que dependen de una imagen que no tenemos están apartadas (`SIN_IMAGEN`).
2. `python3 -I tools/trabajo/apuntes2txt.py`: pasa los PDF de `apuntes/` a texto, página a página. Hace falta PyMuPDF.
3. `python3 -I tools/trabajo/hacer_lotes.py`: reparte lo que falta por explicar en lotes de 25 en `tools/trabajo/lotes/`.
4. Cada lote se explica siguiendo `tools/trabajo/INSTRUCCIONES.md` y se guarda en `tools/respuestas/lote-NN.json`. Se comprueba con `python3 -I tools/trabajo/validar.py NN`.
5. `python3 tools/construir.py`: genera un archivo por tema en `data/` (word, excel, windows, access, outlook, internet, ia, basica). Sube el número `?v=` en `index.html` para que el móvil no use la versión antigua.

Para añadir tests nuevos (por ejemplo más de Excel): se meten en `informatica-todo.json`, se repiten los pasos 1, 3 y 5. Los ids de lo ya explicado no cambian mientras los tests nuevos vayan al final de su grupo.

## Oficiales del INAP
`tools/oficiales-repo.json` guarda las 226 preguntas oficiales que había en el repo `isa-correa/ofimatica`, ya con su texto actualizado a Windows 11 y Microsoft 365. Entran como procedencia «Oficiales», en tests completos por convocatoria (INAP 2019 ord., 2019 extra, 2022 ord., 2022 extra, 14 dic. 2024, 2024 extra, 23 mayo 2026 y julio 2026 extra). Sus explicaciones salen de `tools/trabajo/respuestas_oficiales_repo.py` (`tools/respuestas/lote-24.json`): la opción correcta lleva la explicación del repo y las demás un aviso genérico, a la espera de explicarlas con los apuntes. Las plantillas de 2026 son provisionales. Las preguntas que ya estaban en la plataforma con la misma redacción se unen como repetidas.

## Probar en local
```bash
python3 -m http.server 8765
```
y abrir http://localhost:8765.
