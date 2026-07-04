# -*- coding: utf-8 -*-
"""POP 2025 Reconstruido PUCP — Problemas 52 a 62 (Probabilidad y Estadística)."""
from mh import *

PROBLEMS_4 = [

# ─────────────────────────────── P52 ──────────────────────────────
dict(n=52, tema="Probabilidad", sub="Permutaciones", dif=2,
enun="Se tienen 4 libros diferentes que se deben colocar en un estante. ¿De cuántas maneras se "
     "pueden ordenar los libros en dicho estante si 2 de ellos siempre deben estar juntos?",
opts=["4", "6", "3", "12"], ans=3,
steps=[
 dict(t="Amarra los que van juntos",
  d=para("Truco del «bloque»: los 2 libros inseparables se tratan como <b>un solo paquete</b>. "
     "Ahora hay 3 objetos para ordenar: el paquete y los otros 2 libros.")),
 dict(t="Ordena los objetos",
  d=disp("3! = 6 maneras de ubicar los 3 objetos")),
 dict(t="Ordena dentro del paquete",
  d=para("Dentro del bloque, los 2 libros pueden ir AB o BA:")+
    disp("2! = 2 maneras")),
 dict(t="Multiplica",
  d=disp("3!"+TIMES+"2! = 6"+TIMES+"2 = "+hl("12 maneras"))),
],
idea="Elementos que deben ir juntos = un bloque. Total = (permutación de bloques) × (permutación interna del bloque)."),

# ─────────────────────────────── P53 ──────────────────────────────
dict(n=53, tema="Probabilidad", sub="Probabilidad simple", dif=1,
enun="Se tienen 32 caramelos de tres sabores: fresa, piña y limón. La probabilidad de extraer uno "
     "de fresa es 0,25; uno de piña es 0,625; y uno de limón es 0,125. ¿En cuánto excede la cantidad "
     "de caramelos de piña a los de limón?",
opts=["8", "4", "16", "12"], ans=2,
steps=[
 dict(t="Convierte probabilidades en cantidades",
  d=para("La probabilidad de cada sabor es su fracción del total. Multiplica por 32:")+
    disp("Fresa: 0,25"+TIMES+"32 = 8&nbsp;&nbsp;&nbsp;Piña: 0,625"+TIMES+"32 = 20&nbsp;&nbsp;&nbsp;Limón: 0,125"+TIMES+"32 = 4")+
    para("Control: 8 + 20 + 4 = 32 &#10003; (y 0,25 + 0,625 + 0,125 = 1 &#10003;).")),
 dict(t="Resta",
  d=disp("20 &minus; 4 = "+hl("16 caramelos"))),
],
idea="Probabilidad × total = cantidad. Verifica siempre que las probabilidades sumen 1: es tu control de calidad gratis."),

# ─────────────────────────────── P54 ──────────────────────────────
dict(n=54, tema="Probabilidad", sub="Eventos sucesivos", dif=2,
enun="Se realizará un sorteo con dos premios: uno de $1 000 y otro de $2 000. Se venden en total "
     "100 boletos, de los cuales cinco son míos. ¿Cuál es la probabilidad de que gane $3 000?",
opts=[fr("1","495"), fr("1","500"), fr("1","250"), fr("1","375")], ans=0,
steps=[
 dict(t="Interpreta «ganar $3 000»",
  d=para("Solo se llega a $3 000 ganando <b>ambos</b> premios ($1 000 + $2 000). "
     "Necesito que los dos boletos sorteados sean míos.")),
 dict(t="Primer premio",
  d=disp(v("P")+"(1.º mío) = "+fr("5","100"))),
 dict(t="Segundo premio (sin reposición)",
  d=para("Ya salió uno de mis boletos; quedan 4 míos entre 99:")+
    disp(v("P")+"(2.º mío) = "+fr("4","99"))),
 dict(t="Multiplica",
  d=disp(fr("5","100")+CDOT+fr("4","99")+" = "+fr("20","9 900")+" = "+hl(fr("1","495")))),
],
idea="«Ganar ambos premios» = evento compuesto sin reposición: multiplica probabilidades actualizando el total en cada paso."),

# ─────────────────────────────── P55 ──────────────────────────────
dict(n=55, tema="Probabilidad", sub="Eventos sucesivos", dif=2,
enun="Una caja contiene 9 esferas numeradas del 1 al 9. Se extraen sucesivamente y sin reposición "
     "tres esferas. Halle la probabilidad de que los números mostrados sean alternadamente "
     "IMPAR – PAR – IMPAR.",
opts=[fr("10","63"), fr("5","42"), fr("25","126"), fr("2","21")], ans=0,
steps=[
 dict(t="Cuenta pares e impares",
  d=para("Del 1 al 9 hay <b>5 impares</b> (1, 3, 5, 7, 9) y <b>4 pares</b> (2, 4, 6, 8).")),
 dict(t="Multiplica paso a paso (sin reposición)",
  d=para("&bull; 1.ª impar: "+fr("5","9")+"<br>&bull; 2.ª par (quedan 8): "+fr("4","8")+
     "<br>&bull; 3.ª impar (quedan 4 impares de 7): "+fr("4","7"))),
 dict(t="Producto",
  d=disp(fr("5","9")+CDOT+fr("4","8")+CDOT+fr("4","7")+" = "+fr("80","504")+" = "+hl(fr("10","63")))),
],
idea="Extracciones sucesivas sin reposición: multiplica actualizando numerador (los que quedan del tipo pedido) y denominador (total restante)."),

# ─────────────────────────────── P56 ──────────────────────────────
dict(n=56, tema="Estadística", sub="Promedio ponderado", dif=2,
enun="En un curso de Cálculo en la PUCP, el promedio se calcula con el promedio de prácticas "
     "(peso 3), el promedio de exámenes (peso 3) y la nota del examen final (peso 4). Un estudiante "
     "obtuvo 10 en prácticas y 8 en exámenes. ¿Cuánto debe obtener como mínimo en el examen final "
     "para aprobar, si la nota mínima aprobatoria es 11?",
opts=["13", "14", "15", "16"], ans=1,
steps=[
 dict(t="Escribe el promedio ponderado",
  d=para("Los pesos son 3, 3 y 4 (suman 10). Con "+v("f")+" la nota del final:")+
    disp("Promedio = "+fr("3"+CDOT+"10 + 3"+CDOT+"8 + 4"+CDOT+v("f"), "10")+" "+GEQ+" 11")),
 dict(t="Resuelve la desigualdad",
  d=disp("30 + 24 + 4"+v("f")+" "+GEQ+" 110"+IMPL+"4"+v("f")+" "+GEQ+" 56"+IMPL+hl(v("f")+" "+GEQ+" 14"))),
 dict(t="Interpreta",
  d=para("Con 14 en el final: (30 + 24 + 56)/10 = 11 exacto: aprueba justo. Con 13 saldría 10,6: no alcanza. "
     "Mínimo: "+hl("14")+".")),
],
idea="Promedio ponderado = Σ(nota × peso) ÷ Σ(pesos). Plantea la desigualdad ≥ nota mínima y despeja."),

# ─────────────────────────────── P57 ──────────────────────────────
dict(n=57, tema="Estadística", sub="Lectura de tablas", dif=1,
enun="La tabla detalla el consumo de cereales en un almacén (en kilogramos): "
     "trigo 25 200, cebada 9 000, arroz 15 800; total 50 000. Marca la respuesta correcta.",
opts=["El consumo de trigo es 2,8 veces el de cebada.",
      "El consumo de trigo y cebada es 10% del total.",
      "El consumo de cebada y arroz es mayor que el de trigo.",
      "El consumo de trigo es 50% del total."], ans=0, fig="fig57",
steps=[
 dict(t="Evalúa cada afirmación con la tabla",
  d=para("<b>A:</b> ¿25 200 = 2,8 × 9 000? "+ARROW+" 2,8 × 9 000 = 25 200 &#10003; <b>Correcta.</b>")),
 dict(t="Descarta las demás",
  d=para("<b>B:</b> 25 200 + 9 000 = 34 200, que es el 68,4% del total, no el 10% &#10007;<br>"
     "<b>C:</b> 9 000 + 15 800 = 24 800 &lt; 25 200 &#10007; (por muy poco, ¡pero menor!)<br>"
     "<b>D:</b> 25 200/50 000 = 50,4%, no exactamente 50% &#10007;")),
 dict(t="Moraleja",
  d=para("La C y la D están diseñadas para caer por aproximación mental («24 800 ≈ 25 200», «50,4 ≈ 50»). "
     "En lectura de tablas, calcula exacto antes de marcar.")),
],
idea="En preguntas de tabla, verifica cada alternativa con la operación exacta: las trampas viven en los «casi iguales»."),

# ─────────────────────────────── P58 ──────────────────────────────
dict(n=58, tema="Estadística", sub="Histogramas", dif=2,
enun="El siguiente gráfico muestra las notas de los alumnos de un centro de idiomas. "
     "¿Qué tanto por ciento del total de alumnos tuvieron nota menor que 90?",
opts=["90%", "87,5%", "85,5%", "92,5%"], ans=1, fig="fig58",
steps=[
 dict(t="Lee las alturas de las barras",
  d=para("Del histograma: [50; 60&#10217; "+ARROW+" 10 alumnos, [60; 70&#10217; "+ARROW+" 20, "
     "[70; 80&#10217; "+ARROW+" 10, [80; 90&#10217; "+ARROW+" 16, [90; 100] "+ARROW+" 8.")),
 dict(t="Calcula el total",
  d=disp("10 + 20 + 10 + 16 + 8 = 64 alumnos")),
 dict(t="Suma los que están debajo de 90",
  d=para("Nota menor que 90 = todas las barras salvo la última:")+
    disp("10 + 20 + 10 + 16 = 56 alumnos")),
 dict(t="Convierte a porcentaje",
  d=disp(fr("56","64")+TIMES+"100% = "+fr("7","8")+TIMES+"100% = "+hl("87,5%"))+
    para("Atajo: en vez de sumar 4 barras, quita la que no cumple: 1 &minus; 8/64 = 1 &minus; 1/8 = 7/8.")),
],
idea="«Menor que el último corte» = total − última barra. Trabajar con el complemento (1 − 8/64) es más rápido y con menos errores."),

# ─────────────────────────────── P59 ──────────────────────────────
dict(n=59, tema="Estadística", sub="Histogramas", dif=2,
enun="El siguiente gráfico muestra las notas de los alumnos de un centro de idiomas. "
     "¿Qué tanto por ciento del total de alumnos tuvieron nota menor que 90?",
opts=["90%", "87,5%", "85,5%", "92,5%"], ans=1, fig="fig58", dup=58,
steps=[
 dict(t="Pregunta repetida",
  d=para("Es exactamente el problema 58 (el examen reconstruido lo duplica). Mismo histograma, misma lectura.")),
 dict(t="Resolución exprés",
  d=disp("Total = 64&nbsp;&nbsp;&nbsp;&nbsp;con nota &lt; 90: 64 &minus; 8 = 56")+
    disp(fr("56","64")+" = 0,875 = "+hl("87,5%"))),
],
idea="Idéntico al 58: complemento de la última barra, 7/8 = 87,5%."),

# ─────────────────────────────── P60 ──────────────────────────────
dict(n=60, tema="Probabilidad", sub="Probabilidad total", dif=2,
enun="En un restaurante, el 60% de las personas comen ceviche, de las cuales el 40% son mujeres. "
     "Además, el 40% de las personas que no están comiendo ceviche son hombres. ¿Cuál es la "
     "probabilidad de que al escoger una persona al azar, esta sea mujer?",
opts=[fr("9","20"), fr("6","25"), fr("4","25"), fr("12","25")], ans=3, fig="fig60",
steps=[
 dict(t="Toma 100 personas (base cómoda)",
  d=para("60 comen ceviche y 40 no. Ahora reparte por sexo dentro de cada grupo.")),
 dict(t="Mujeres en cada grupo",
  d=para("&bull; Con ceviche: 40% de 60 = <b>24 mujeres</b>.<br>"
     "&bull; Sin ceviche: si el 40% son hombres, el 60% son mujeres: 60% de 40 = <b>24 mujeres</b>.")),
 dict(t="Probabilidad total",
  d=disp(v("P")+"(mujer) = "+fr("24 + 24","100")+" = "+fr("48","100")+" = "+hl(fr("12","25")))+
    para("Curioso y elegante: ambos grupos aportan exactamente 24 mujeres.")),
],
idea="Probabilidad total con base 100: reparte el total en ramas (ceviche/no ceviche) y suma las mujeres de cada rama. Ojo al «40% son hombres» ⇒ 60% mujeres."),

# ─────────────────────────────── P61 ──────────────────────────────
dict(n=61, tema="Estadística", sub="Promedio ponderado", dif=1,
enun="En un colegio de alto rendimiento, el promedio de notas está distribuido así: el 30% tiene "
     "promedio 17, el 20% promedio 18, el 10% promedio 14 y el resto tiene promedio 20. "
     "¿Cuál es el promedio de todos los alumnos considerados?",
opts=["18,6", "17,9", "19,3", "18,1"], ans=3,
steps=[
 dict(t="Halla el grupo restante",
  d=disp("100% &minus; 30% &minus; 20% &minus; 10% = 40% con promedio 20")),
 dict(t="Pondera cada grupo",
  d=disp("0,30"+TIMES+"17 = 5,1&nbsp;&nbsp;&nbsp;0,20"+TIMES+"18 = 3,6&nbsp;&nbsp;&nbsp;"
         "0,10"+TIMES+"14 = 1,4&nbsp;&nbsp;&nbsp;0,40"+TIMES+"20 = 8,0")),
 dict(t="Suma",
  d=disp("5,1 + 3,6 + 1,4 + 8,0 = "+hl("18,1"))),
],
idea="Promedio general = Σ(proporción × promedio del grupo). No olvides calcular primero el porcentaje del grupo «resto»."),

# ─────────────────────────────── P62 ──────────────────────────────
dict(n=62, tema="Estadística", sub="Promedio ponderado", dif=2,
enun="Un alumno de la facultad de Letras de la PUCP obtiene su promedio en Matemática 1 con la "
     "fórmula:"+disp("Promedio = "+fr("3"+v("P")+"<sub>P</sub> + 3"+v("E")+"<sub>P</sub> + 4"+v("E")+"<sub>F</sub>", "10"))+
     "donde "+v("P")+"<sub>P</sub> = promedio de prácticas, "+v("E")+"<sub>P</sub> = examen parcial y "+
     v("E")+"<sub>F</sub> = examen final. Si obtuvo 10 en prácticas y 8 en el parcial, ¿cuánto debe "
     "obtener como mínimo en el examen final para aprobar, si la nota mínima aprobatoria es 11?",
opts=["13", "14", "15", "16"], ans=1, dup=56,
steps=[
 dict(t="Mismo modelo que el problema 56",
  d=para("La fórmula es el mismo promedio ponderado 3-3-4 del problema 56, ahora escrita explícitamente.")),
 dict(t="Plantea y resuelve",
  d=disp(fr("3(10) + 3(8) + 4"+v("E")+"<sub>F</sub>","10")+" "+GEQ+" 11"+IMPL+
         "54 + 4"+v("E")+"<sub>F</sub> "+GEQ+" 110"+IMPL+"4"+v("E")+"<sub>F</sub> "+GEQ+" 56"+IMPL+
         hl(v("E")+"<sub>F</sub> "+GEQ+" 14"))+
    para("Necesita mínimo "+hl("14")+" (con 14 el promedio da 11,0 exacto).")),
],
idea="Igual que el 56: Σ(nota × peso)/10 ≥ 11 ⇒ el final debe aportar lo que falta: 4E_F ≥ 56."),
]
