# Cómo explicar las preguntas

Es una app de estudio para la oposición C1 (Cuerpo General Administrativo), parte de informática: Word 365 (tema 4) y Excel 365 (tema 5). La usuaria estudia con estas explicaciones, así que un error enseña algo falso.

**Aquí la respuesta correcta ya viene dada** (campo `correcta`, de la plantilla de la academia). El trabajo es explicarla bien, apoyándote en los apuntes de la academia.

## Material
Rutas relativas a la raíz del proyecto.
- `tools/trabajo/lotes/lote-NN.json`: tus preguntas, con `enunciado`, `opciones` y `correcta` (índice desde 0).
- `python3 -I tools/trabajo/consulta.py buscar "interlineado"`: dónde sale una expresión en los apuntes (no distingue tildes ni mayúsculas). Con varias expresiones, solo las páginas donde salen todas.
- `python3 -I tools/trabajo/consulta.py pag T4 34`: una página entera. Documentos: `T4` (temario de Word, págs. 1 a 97), `T4-esquema` (esquema resumen), `T4-cinta` (cinta de opciones), `T4-atajos` (atajos de teclado), `T5` (temario de Excel, de momento solo la parte 1).
- `python3 -I tools/trabajo/consulta.py indice`: todas las páginas con su apartado.

## Método, pregunta a pregunta
1. **Busca en los apuntes antes de escribir.** Nada de memoria: estas preguntas cambian un nombre de ficha, un grupo, un atajo o una medida para pillarte. Compara cada opción con lo que dicen los apuntes.
2. Fíjate en si pide la correcta o la **incorrecta / falsa / NO**.
3. Si los apuntes no lo tratan, explica con lo que sabes de Word o Excel 365 en español, con cuidado, y añade `revisar` diciendo que no está en los apuntes.
4. **Si crees que la plantilla se equivoca**, no cambies `correcta`: explica la respuesta de la plantilla lo mejor que puedas y pon en `revisar` qué opción te parece buena y por qué (con la página de los apuntes). Lo mismo si dos opciones parecen válidas.
5. Los atajos de teclado son los de Word en español (CTRL + N es negrita, CTRL + K cursiva, CTRL + S subrayado). Compruébalos en `T4-atajos`.
6. Nunca inventes una ruta de menú, un nombre de grupo ni una página.

## Salida
Escribe con la herramienta Write un JSON en `tools/respuestas/lote-NN.json`, UTF-8, un objeto cuya clave es el id de cada pregunta:
```json
{"w-of-01-001": {
  "bloque": "word-inicio",
  "precepto": "Tema 4 · 4.2 Ficha Inicio, grupo Párrafo (pág. 34)",
  "correcta": 2,
  "justificaciones": ["...", "...", "...", "..."],
  "ojo": "opcional",
  "revisar": "opcional, solo si hay duda real"
}}
```
- `correcta`: la misma que trae el lote. **No reordenes las opciones.**
- `justificaciones`: una por opción, en el mismo orden, y tantas como opciones haya.
- `precepto`: dónde está en los apuntes: tema, apartado, grupo o cuadro si ayuda, y página. Por ejemplo "Tema 4 · 4.1 Ficha Archivo, Imprimir (pág. 18)" o "Atajos de teclado Word (pág. 2)".
- `bloque`, según de qué trata la pregunta, no del test:
  - Word: `word-entorno` (qué es Word, inicio, área de trabajo, cinta en general; págs. 1 a 11) · `word-archivo` (ficha Archivo, Backstage, guardar, imprimir, compartir, Opciones de Word; 12 a 23) · `word-inicio` (portapapeles, fuente, párrafo, estilos, buscar y reemplazar; 24 a 49) · `word-insertar` (portada, tablas, imágenes, encabezado y pie, cuadros de texto, símbolos; 50 a 65) · `word-diseno` (temas, marca de agua, color y bordes de página; 66 a 71) · `word-disposicion` (márgenes, orientación, tamaño, columnas, saltos, ajustar texto; 72 a 80) · `word-referencias` (tabla de contenido, notas al pie, citas, índices; 81 a 84) · `word-correspondencia` (sobres, etiquetas, combinar correspondencia; 85 a 87) · `word-revisar` (ortografía, comentarios, control de cambios, comparar, proteger; 88 a 93) · `word-vista` (vistas, regla, zoom, ventanas, macros; 94 a 97) · `word-atajos` (preguntas cuyo centro es un atajo de teclado).
  - Excel: `excel-general` (de momento, todas).
- `ojo`: solo cuando aporte algo: la trampa de la pregunta, la palabra cambiada, la confusión típica. Una o dos frases.
- Comillas tipográficas “así” dentro de los textos, para no romper el JSON.
- Al terminar: `python3 -I tools/trabajo/validar.py NN` y corrige hasta que diga OK. Luego `python3 tools/construir.py`.

## El idioma de las explicaciones
Como unos buenos apuntes de academia, para alguien que no es informático: frases cortas, palabras de todos los días, tuteando.
- **La correcta** empieza por "Es esta." y explica por qué, con la ficha, el grupo o el comando clave en **negrita**. Si ayuda, la ruta para llegar (Inicio > Párrafo > Interlineado) o una forma de recordarlo.
- **Las incorrectas** empiezan por "No." y dicen **qué falla exactamente en esa opción**: qué te han cambiado y dónde está de verdad esa herramienta o qué hace. Nunca "No, porque no es así": eso no enseña nada. Cada opción tiene su razón propia.
- **Si pide la incorrecta**: en la que hay que marcar di "Esta es la falsa, y por eso es la que hay que marcar." y explica qué falla; en las demás, "Es verdadera, así que no se marca." y por qué es verdadera.
- Si una opción es "todas son correctas" o "ninguna", explícalo en función de las otras.
- Solo se usa `**negrita**`, sin otro formato.
- Prohibido usar raya (—) o semirraya (–) como puntuación: usa coma, dos puntos, paréntesis o punto. Rangos: "de 1 a 12". El validador las rechaza.
- Nada de relleno ("cabe señalar", "es importante destacar") ni de mencionar que eres una IA. No copies párrafos de los apuntes: explica, y cita entre comillas solo la frase corta que importa.
- Largo orientativo: la correcta de 2 a 4 frases, cada incorrecta de 1 a 2.

## Ejemplo del tono buscado (ilustrativo)
Pregunta: "¿Qué sangría desplaza todo el párrafo hacia la derecha salvo la primera línea?" Opciones: Izquierda · Derecha · Especial primera línea · Especial francesa. Correcta: 3.
```json
{
 "bloque": "word-inicio",
 "precepto": "Tema 4 · 4.2 Ficha Inicio, grupo Párrafo, sangrías (pág. 34)",
 "correcta": 3,
 "justificaciones": [
  "No. La sangría **izquierda** separa del margen izquierdo el párrafo entero, incluida la primera línea.",
  "No. La sangría **derecha** añade espacio entre el párrafo y el margen derecho. No mueve nada hacia la derecha.",
  "No. La **primera línea** es justo lo contrario: solo se desplaza la primera línea y el resto se queda en su sitio.",
  "Es esta. La sangría **especial francesa** mete hacia dentro todas las líneas menos la primera, que queda más a la izquierda. Se usa mucho en bibliografías. Por defecto mide 1,25 cm."
 ],
 "ojo": "Primera línea y francesa son opuestas: en la primera línea se mueve solo la primera; en la francesa se mueven todas menos la primera."
}
```
