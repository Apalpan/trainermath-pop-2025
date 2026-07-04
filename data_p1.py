# -*- coding: utf-8 -*-
"""POP 2025 Reconstruido PUCP — Problemas 1 a 16 (Aritmética)."""
from mh import *

PROBLEMS_1 = [

# ─────────────────────────────── P1 ───────────────────────────────
dict(n=1, tema="Aritmética", sub="Múltiplos y restos", dif=2,
enun="Un libro tiene de 500 a 600 páginas. Si se cuentan de 3 en 3, sobran 2; "
     "de 5 en 5, sobran 4; de 7 en 7, sobran 6. ¿Cuántas páginas tiene el libro?",
opts=["524", "536", "527", "566"], ans=0,
steps=[
 dict(t="Detecta el patrón oculto",
  d=para("Mira lo que sobra en cada caso: con 3 sobran <b>2</b> (falta 1 para completar), con 5 sobran <b>4</b> "
     "(falta 1), con 7 sobran <b>6</b> (falta 1). En los tres casos <b>falta exactamente 1 página</b> "
     "para que el conteo salga exacto. Ese es el truco del problema: no trabajes con lo que sobra, "
     "sino con lo que falta.")),
 dict(t="Traduce a múltiplos",
  d=para("Si al número de páginas "+v("N")+" le sumamos 1, el conteo de 3 en 3, de 5 en 5 y de 7 en 7 "
     "saldría exacto. Es decir:")+
    disp(v("N")+" + 1 = múltiplo común de 3, 5 y 7")),
 dict(t="Usa el MCM",
  d=para("El menor número que es múltiplo de 3, 5 y 7 a la vez es su MCM. Como son primos entre sí:")+
    disp("MCM(3; 5; 7) = 3"+CDOT+"5"+CDOT+"7 = 105")+
    para("Entonces "+v("N")+" + 1 = 105"+v("k")+" para algún entero "+v("k")+", o sea "+v("N")+" = 105"+v("k")+" &minus; 1.")),
 dict(t="Ubica el valor entre 500 y 600",
  d=para("Probamos valores de "+v("k")+": con "+v("k")+" = 5, "+v("N")+" = 525 &minus; 1 = <b>524</b> &#10003;. "
     "Con "+v("k")+" = 6, "+v("N")+" = 629 (se pasa). El único valor en el rango es 524.")),
 dict(t="Verifica",
  d=para("524 &divide; 3 = 174 y sobran <b>2</b> &#10003; &nbsp;·&nbsp; 524 &divide; 5 = 104 y sobran <b>4</b> &#10003; "
     "&nbsp;·&nbsp; 524 &divide; 7 = 74 y sobran <b>6</b> &#10003;. Todo cuadra.")),
],
idea="Cuando a todos los conteos les falta lo mismo (aquí, 1), suma esa cantidad y aparece un múltiplo común: N + 1 = MCM·k."),

# ─────────────────────────────── P2 ───────────────────────────────
dict(n=2, tema="Aritmética", sub="Conteo de números", dif=2,
enun="¿Cuántos números impares de cuatro cifras son múltiplos de 5 y no tienen la cifra siete?",
opts=["1204", "648", "900", "764"], ans=1,
steps=[
 dict(t="Fija la última cifra",
  d=para("Un múltiplo de 5 termina en 0 o en 5. Pero el número debe ser <b>impar</b>, así que la última "
     "cifra solo puede ser <b>5</b>. Ya no hay elección ahí: 1 posibilidad.")),
 dict(t="Cuenta las opciones de cada cifra",
  d=para("El número es "+v("a")+v("b")+v("c")+"5. Ahora contamos cuántos valores puede tomar cada cifra "
     "recordando la restricción: <b>no puede aparecer el 7</b>.")+
    para("&bull; Primera cifra "+v("a")+": de 1 a 9, sin el 7 "+ARROW+" <b>8</b> opciones.<br>"
     "&bull; Segunda cifra "+v("b")+": de 0 a 9, sin el 7 "+ARROW+" <b>9</b> opciones.<br>"
     "&bull; Tercera cifra "+v("c")+": de 0 a 9, sin el 7 "+ARROW+" <b>9</b> opciones.<br>"
     "&bull; Cuarta cifra: solo el 5 "+ARROW+" <b>1</b> opción.")),
 dict(t="Multiplica (principio de conteo)",
  d=para("Cada elección es independiente, así que multiplicamos:")+
    disp("8"+TIMES+"9"+TIMES+"9"+TIMES+"1 = "+hl("648"))),
],
idea="«Impar y múltiplo de 5» obliga a terminar en 5. Después solo es contar opciones por casilla y multiplicar."),

# ─────────────────────────────── P3 ───────────────────────────────
dict(n=3, tema="Aritmética", sub="MCD y divisores", dif=2,
enun="Se tiene un terreno rectangular de dimensiones 120 m y 192 m. Se quiere dividir en parcelas "
     "cuadradas todas iguales, donde el área de cada una sea de por lo menos 60 m². "
     "¿Cuántas parcelas se obtendrán, si dicha cantidad es máxima?",
opts=["240", "320", "800", "360"], ans=3, fig="fig3",
steps=[
 dict(t="¿Qué lados puede tener la parcela?",
  d=para("Para que las parcelas cuadradas de lado "+v("L")+" encajen exactas sin sobrar terreno, "+v("L")+
     " debe dividir a 120 y a 192 a la vez. Es decir, "+v("L")+" debe ser un <b>divisor común</b> de ambos.")+
    para("Calculamos MCD(120; 192): 120 = 2³·3·5 y 192 = 2⁶·3 "+ARROW+" MCD = 2³·3 = <b>24</b>. "
     "Los lados posibles son los divisores de 24: 1, 2, 3, 4, 6, 8, 12 y 24.")),
 dict(t="Aplica la condición del área",
  d=para("El área de cada parcela debe cumplir "+v("L")+"² "+GEQ+" 60. Probamos: 6² = 36 (no), "
     "<b>8² = 64</b> (sí), 12² = 144 (sí), 24² = 576 (sí). Quedan "+v("L")+" = 8, 12 o 24.")),
 dict(t="Maximiza la cantidad de parcelas",
  d=para("Cuantas <b>más</b> parcelas queremos, <b>más pequeña</b> debe ser cada una. De los valores "
     "permitidos, el menor lado es "+v("L")+" = 8 m.")),
 dict(t="Cuenta las parcelas",
  d=disp(fr("120","8")+TIMES+fr("192","8")+" = 15"+TIMES+"24 = "+hl("360 parcelas"))+
    para("Verificación del área: cada parcela mide 8"+TIMES+"8 = 64 m² "+GEQ+" 60 m² &#10003;.")),
],
idea="Parcelas cuadradas exactas ⇒ el lado divide al MCD. Máxima cantidad ⇒ el menor lado que cumpla la condición de área."),

# ─────────────────────────────── P4 ───────────────────────────────
dict(n=4, tema="Aritmética", sub="Planteo de ecuaciones", dif=1,
enun="Si una persona sube la escalera de un gimnasio de 4 en 4 escalones, daría 4 pasos más que "
     "si la sube de 5 en 5. ¿Cuántos escalones tiene dicha escalera?",
opts=["80", "90", "60", "100"], ans=0,
steps=[
 dict(t="Nombra lo que buscas",
  d=para("Sea "+v("N")+" el total de escalones. Subiendo de 4 en 4 se dan "+fr(v("N"),"4")+
     " pasos, y de 5 en 5 se dan "+fr(v("N"),"5")+" pasos.")),
 dict(t="Traduce la comparación",
  d=para("«De 4 en 4 daría 4 pasos más que de 5 en 5»:")+
    disp(fr(v("N"),"4")+" = "+fr(v("N"),"5")+" + 4")),
 dict(t="Resuelve",
  d=para("Multiplicamos todo por 20 (el MCM de 4 y 5) para eliminar denominadores:")+
    disp("5"+v("N")+" = 4"+v("N")+" + 80"+IMPL+hl(v("N")+" = 80"))),
 dict(t="Verifica",
  d=para("Con 80 escalones: de 4 en 4 son 20 pasos; de 5 en 5 son 16 pasos. "
     "Diferencia: 20 &minus; 16 = 4 pasos &#10003;.")),
],
idea="Pasos = total ÷ tamaño del paso. La diferencia de pasos da una ecuación lineal directa."),

# ─────────────────────────────── P5 ───────────────────────────────
dict(n=5, tema="Aritmética", sub="Magnitudes y conversión", dif=1,
enun="En el planeta «X» los días tienen 10 horas, cada hora tiene 10 minutos y cada minuto tiene "
     "24 segundos. Los segundos del planeta «X» son equivalentes a los de la Tierra. "
     "¿Cuántos días del planeta «X» equivalen a un día del planeta Tierra?",
opts=["28", "40", "24", "36"], ans=3,
steps=[
 dict(t="Lleva todo a segundos (la unidad común)",
  d=para("El segundo es la única unidad que vale lo mismo en los dos planetas, así que convertimos "
     "ambos días a segundos.")),
 dict(t="Día del planeta X",
  d=disp("10 h"+TIMES+"10 min"+TIMES+"24 s = 2 400 segundos")),
 dict(t="Día de la Tierra",
  d=disp("24 h"+TIMES+"60 min"+TIMES+"60 s = 86 400 segundos")),
 dict(t="Compara",
  d=disp(fr("86 400","2 400")+" = "+hl("36 días de «X»"))+
    para("Un día terrestre contiene 36 días del planeta X.")),
],
idea="Cuando dos sistemas de medida difieren, convierte todo a la unidad que comparten y divide."),

# ─────────────────────────────── P6 ───────────────────────────────
dict(n=6, tema="Aritmética", sub="Variación proporcional", dif=3,
enun="Se tiene la expresión:"+disp(v("A")+" = "+v("B")+CDOT+sq(fr(v("n"), v("C")+"³")))+
     "¿En qué fracción aumenta "+v("n")+", si "+v("A")+" disminuye en sus "+fr("3","7")+
     " y "+v("C")+" aumenta en sus "+fr("4","3")+"?",
opts=[fr("27","112"), fr("112","27"), fr("27","112"), fr("85","27")], ans=3,
steps=[
 dict(t="Despeja n",
  d=para("Nos preguntan por "+v("n")+", así que primero lo dejamos solo. Elevamos al cuadrado y despejamos:")+
    disp(v("A")+"² = "+v("B")+"²"+CDOT+fr(v("n"), v("C")+"³")+IMPL+
         v("n")+" = "+fr(v("A")+"²"+CDOT+v("C")+"³", v("B")+"²"))+
    para(v("B")+" no cambia, así que "+v("n")+" es proporcional a "+v("A")+"²"+CDOT+v("C")+"³.")),
 dict(t="Traduce los cambios a factores",
  d=para("&bull; «"+v("A")+" disminuye en sus "+fr("3","7")+"» significa que pierde 3 de cada 7 partes: queda "+
     fr("4","7")+" de su valor.<br>&bull; «"+v("C")+" aumenta en sus "+fr("4","3")+
     "» significa que gana 4 por cada 3 partes: queda 1 + "+fr("4","3")+" = "+fr("7","3")+" de su valor.")),
 dict(t="Calcula el factor total de n",
  d=para("Como "+v("n")+" &prop; "+v("A")+"²"+CDOT+v("C")+"³, el nuevo valor es:")+
    disp(v("n")+"&prime; = "+mrow("(",fr("4","7"),")² ",CDOT," (",fr("7","3"),")³ ",CDOT," ",v("n"))+
         " = "+fr("16","49")+CDOT+fr("343","27")+CDOT+v("n")+" = "+hl(fr("112","27")+CDOT+v("n"))))
 ,
 dict(t="Cuidado: piden el aumento, no el nuevo valor",
  d=para("El valor nuevo es "+fr("112","27")+" del original (esa es la alternativa trampa). "
     "El <b>aumento</b> es lo que se ganó:")+
    disp(v("n")+"&prime; &minus; "+v("n")+" = "+mrow("(",fr("112","27")," &minus; 1)",CDOT,v("n"))+
         " = "+hl(fr("85","27")+CDOT+v("n")))+
    para(v("n")+" aumenta en sus "+fr("85","27")+".")),
],
idea="«Disminuye en sus a/b» ⇒ queda (b−a)/b. «Aumenta en sus a/b» ⇒ queda (b+a)/b. Y el aumento pedido es el factor final menos 1.",
nota="En el examen reconstruido las alternativas A y C aparecen repetidas (27/112); es una errata de la reconstrucción. La respuesta consistente es 85/27."),

# ─────────────────────────────── P7 ───────────────────────────────
dict(n=7, tema="Aritmética", sub="Porcentajes", dif=2,
enun="El precio de un objeto sufre dos descuentos sucesivos del 20%. ¿En qué porcentaje debe "
     "aumentar el precio que quedó para obtener el precio original?",
opts=["52,60%", "36%", "64%", "56,25%"], ans=3,
steps=[
 dict(t="Trabaja con un precio cómodo",
  d=para("Supón que el precio original es 100 (con porcentajes, elegir 100 siempre simplifica).")),
 dict(t="Aplica los dos descuentos",
  d=para("Cada descuento del 20% deja el 80% (factor 0,8):")+
    disp("100"+TIMES+"0,8"+TIMES+"0,8 = 64")+
    para("Ojo: dos descuentos del 20% <b>no</b> son 40%; el segundo se aplica sobre un precio ya rebajado.")),
 dict(t="Calcula el aumento necesario",
  d=para("Hay que pasar de 64 a 100, es decir, recuperar 36 unidades... pero ¡sobre una base de 64!")+
    disp(fr("100 &minus; 64","64")+TIMES+"100% = "+fr("36","64")+TIMES+"100% = "+hl("56,25%"))),
 dict(t="Por qué 36% es la trampa",
  d=para("36% sería correcto si la base fuera 100, pero el aumento se aplica sobre 64 (el precio que quedó). "
     "Un porcentaje siempre se mide respecto de su base.")),
],
idea="Descuentos sucesivos se multiplican como factores (0,8 × 0,8 = 0,64). Para volver al original: (100 − final)/final."),

# ─────────────────────────────── P8 ───────────────────────────────
dict(n=8, tema="Aritmética", sub="Porcentajes", dif=1,
enun="Después de una batalla murieron el 5% de los soldados de un ejército, el 20% de los "
     "sobrevivientes estaban heridos y 380 resultaron ilesos. ¿Cuántos soldados tenía dicho ejército en total?",
opts=["400", "500", "600", "700"], ans=1,
steps=[
 dict(t="Sigue la cadena de porcentajes",
  d=para("Sea "+v("T")+" el total. Murió el 5%, así que sobrevive el 95%: 0,95"+v("T")+". "
     "De esos sobrevivientes, el 20% está herido, así que el 80% está ileso.")),
 dict(t="Plantea la ecuación de los ilesos",
  d=disp("0,95"+CDOT+"0,80"+CDOT+v("T")+" = 380"+IMPL+"0,76"+v("T")+" = 380")),
 dict(t="Despeja",
  d=disp(v("T")+" = "+fr("380","0,76")+" = "+hl("500 soldados"))),
 dict(t="Verifica",
  d=para("De 500: mueren 25 (5%), quedan 475. Heridos: 95 (20% de 475). Ilesos: 475 &minus; 95 = 380 &#10003;.")),
],
idea="Porcentajes encadenados = producto de factores: «queda el 95% y de eso el 80%» ⇒ 0,95 × 0,80 = 0,76 del total."),

# ─────────────────────────────── P9 ───────────────────────────────
dict(n=9, tema="Aritmética", sub="Fracciones y porcentajes", dif=1,
enun="El 75% del planeta es agua y el 25% restante es tierra. Si los "+fr("3","5")+
     " de la tierra es cultivable, ¿qué porcentaje representa el terreno cultivable respecto del total?",
opts=["15%", "10%", "5%", "12,5%"], ans=0,
steps=[
 dict(t="Identifica la parte de la parte",
  d=para("El terreno cultivable es una fracción ("+fr("3","5")+") aplicada sobre otra fracción (el 25% "
     "del planeta). «De» significa multiplicar.")),
 dict(t="Multiplica",
  d=disp(fr("3","5")+TIMES+"25% = "+fr("75","5")+"% = "+hl("15%"))),
 dict(t="Interpreta",
  d=para("De cada 100 unidades de superficie del planeta, 25 son tierra y de ellas 15 se pueden cultivar. "
     "El cultivable es el <b>15%</b> del total.")),
],
idea="«Los 3/5 de la tierra» = 3/5 × 25%. La palabra «de» entre fracciones y porcentajes siempre es una multiplicación."),

# ─────────────────────────────── P10 ──────────────────────────────
dict(n=10, tema="Álgebra", sub="Progresión aritmética", dif=2,
enun="El cuarto y noveno término de una progresión aritmética son 9 y &minus;6 respectivamente. "
     "¿Hasta qué término se debe sumar para obtener como resultado &minus;21?",
opts=["12", "13", "14", "15"], ans=2,
steps=[
 dict(t="Encuentra la razón",
  d=para("Entre el término 4 y el término 9 hay 5 saltos de razón "+v("d")+":")+
    disp(v("a")+"<sub>9</sub> &minus; "+v("a")+"<sub>4</sub> = 5"+v("d")+IMPL+
         "&minus;6 &minus; 9 = 5"+v("d")+IMPL+hl(v("d")+" = &minus;3"))),
 dict(t="Encuentra el primer término",
  d=disp(v("a")+"<sub>4</sub> = "+v("a")+"<sub>1</sub> + 3"+v("d")+IMPL+
         "9 = "+v("a")+"<sub>1</sub> &minus; 9"+IMPL+hl(v("a")+"<sub>1</sub> = 18"))+
    para("La progresión es 18, 15, 12, 9, 6, 3, 0, &minus;3, &minus;6, ...")),
 dict(t="Plantea la suma de n términos",
  d=disp(v("S")+"<sub>"+v("n")+"</sub> = "+fr(v("n"),"2")+mrow("[2",v("a"),"<sub>1</sub> + (",v("n"),"&minus;1)",v("d"),"]")+
         " = "+fr(v("n"),"2")+"[36 &minus; 3("+v("n")+"&minus;1)] = &minus;21")),
 dict(t="Resuelve la cuadrática",
  d=para("Multiplicando por 2 y ordenando:")+
    disp(v("n")+"(39 &minus; 3"+v("n")+") = &minus;42"+IMPL+v("n")+"² &minus; 13"+v("n")+" &minus; 14 = 0"+IMPL+
         "("+v("n")+" &minus; 14)("+v("n")+" + 1) = 0")+
    para("Como "+v("n")+" debe ser positivo: "+hl(v("n")+" = 14")+".")),
 dict(t="Verifica con la suma directa",
  d=para("Suma de los 14 primeros: "+fr("14","2")+"·(18 + "+v("a")+"<sub>14</sub>) = 7·(18 &minus; 21) = 7·(&minus;3) = &minus;21 &#10003; "
     "(donde "+v("a")+"<sub>14</sub> = 18 + 13·(&minus;3) = &minus;21).")),
],
idea="En una PA: aₘ − aₙ = (m−n)·d. Con a₁ y d, la suma Sₙ produce una cuadrática en n; descarta la raíz negativa."),

# ─────────────────────────────── P11 ──────────────────────────────
dict(n=11, tema="Álgebra", sub="Progresión aritmética", dif=1,
enun="En una progresión aritmética, la diferencia del décimo y segundo término es 48. "
     "Calcular la diferencia del sexto y cuarto término.",
opts=["6", "12", "18", "24"], ans=1,
steps=[
 dict(t="Cuenta los saltos",
  d=para("Del término 2 al término 10 hay 10 &minus; 2 = 8 saltos de razón:")+
    disp(v("a")+"<sub>10</sub> &minus; "+v("a")+"<sub>2</sub> = 8"+v("d")+" = 48"+IMPL+hl(v("d")+" = 6"))),
 dict(t="Aplica lo mismo al otro par",
  d=para("Del término 4 al término 6 hay 2 saltos:")+
    disp(v("a")+"<sub>6</sub> &minus; "+v("a")+"<sub>4</sub> = 2"+v("d")+" = 2"+TIMES+"6 = "+hl("12"))),
],
idea="aₘ − aₙ = (m − n)·d: la diferencia entre términos solo depende de cuántos saltos hay entre ellos."),

# ─────────────────────────────── P12 ──────────────────────────────
dict(n=12, tema="Aritmética", sub="Conteo de números", dif=2,
enun="¿Cuántos números impares de cuatro cifras son múltiplos de 5 y no tienen la cifra siete?",
opts=["1 204", "648", "900", "764"], ans=1, dup=2,
steps=[
 dict(t="Es el mismo problema 2 del examen",
  d=para("El examen reconstruido repite esta pregunta (apareció como problema 2). La resolvemos igual de rápido.")),
 dict(t="Última cifra obligada",
  d=para("Múltiplo de 5 e impar "+ARROW+" termina en <b>5</b>.")),
 dict(t="Cuenta y multiplica",
  d=para("Primera cifra: 8 opciones (1–9 sin el 7); segunda y tercera: 9 opciones cada una (0–9 sin el 7); última: fija.")+
    disp("8"+TIMES+"9"+TIMES+"9 = "+hl("648"))),
],
idea="Idéntico al problema 2: terminar en 5 es obligatorio, luego se cuenta casilla por casilla."),

# ─────────────────────────────── P13 ──────────────────────────────
dict(n=13, tema="Aritmética", sub="MCD y divisores", dif=1,
enun="Calcular el MCD de 24, 72 y 120.",
opts=["24", "120", "4", "360"], ans=0,
steps=[
 dict(t="Observa antes de calcular",
  d=para("72 = 3"+TIMES+"24 y 120 = 5"+TIMES+"24: los tres números son múltiplos de 24. "
     "Si el menor de los números divide a los demás, él mismo es el MCD.")),
 dict(t="Confirma con descomposición",
  d=disp("24 = 2³"+CDOT+"3&nbsp;&nbsp;&nbsp;72 = 2³"+CDOT+"3²&nbsp;&nbsp;&nbsp;120 = 2³"+CDOT+"3"+CDOT+"5")+
    para("Tomamos los factores comunes con su menor exponente: 2³"+CDOT+"3 = "+hl("24")+".")),
 dict(t="Descarta la trampa",
  d=para("360 es el MCM (el mínimo común múltiplo), no el MCD. Es el error clásico de este tipo de pregunta.")),
],
idea="Si el menor número divide a todos los demás, ese número ya es el MCD. Y no confundas MCD (común a los divisores) con MCM."),

# ─────────────────────────────── P14 ──────────────────────────────
dict(n=14, tema="Aritmética", sub="Fracciones", dif=2,
enun="Si&nbsp;&nbsp;"+v("A")+" = "+mrow("(",fr("1",fr("1","3")),")³ + (",fr("1",fr("2","5")),")² + (",fr("1",fr("4","11")),")")+
     ",&nbsp;&nbsp;calcular "+sq(v("A"))+".",
opts=["5", "6", "7", "8"], ans=1,
steps=[
 dict(t="Invierte cada fracción compuesta",
  d=para("Dividir 1 entre una fracción es lo mismo que <b>invertirla</b>:")+
    disp(fr("1",fr("1","3"))+" = 3&nbsp;&nbsp;&nbsp;&nbsp;"+fr("1",fr("2","5"))+" = "+fr("5","2")+
         "&nbsp;&nbsp;&nbsp;&nbsp;"+fr("1",fr("4","11"))+" = "+fr("11","4"))),
 dict(t="Aplica las potencias",
  d=disp("3³ = 27&nbsp;&nbsp;&nbsp;&nbsp;"+mrow("(",fr("5","2"),")² = ",fr("25","4")))),
 dict(t="Suma",
  d=disp(v("A")+" = 27 + "+fr("25","4")+" + "+fr("11","4")+" = 27 + "+fr("36","4")+" = 27 + 9 = "+hl("36"))+
    para("Bonito detalle: "+fr("25","4")+" y "+fr("11","4")+" ya tienen el mismo denominador y suman exactamente 9.")),
 dict(t="Responde lo pedido",
  d=disp(sq(v("A"))+" = "+sq("36")+" = "+hl("6"))),
],
idea="1 ÷ (a/b) = b/a. Tras invertir, agrupa las fracciones de igual denominador antes de sumar.",
nota="En el PDF reconstruido la línea «calcular …» quedó cortada; con las alternativas 5–8, lo pedido es √A (A = 36 ⇒ 6)."),

# ─────────────────────────────── P15 ──────────────────────────────
dict(n=15, tema="Aritmética", sub="MCD y divisores", dif=2,
enun="Si MCD(5"+v("m")+"; 11"+v("m")+") = 49, calcular:"+disp(sq(v("m")+" &minus; 13")+" + "+sq(v("m")+" + 15")),
opts=["13", "14", "15", "16"], ans=1,
steps=[
 dict(t="Usa la propiedad del MCD con factor común",
  d=para("Si multiplicas dos números por una misma cantidad, el MCD queda multiplicado por ella:")+
    disp("MCD(5"+v("m")+"; 11"+v("m")+") = "+v("m")+CDOT+"MCD(5; 11)")),
 dict(t="Halla m",
  d=para("5 y 11 son primos entre sí, así que MCD(5; 11) = 1:")+
    disp(v("m")+CDOT+"1 = 49"+IMPL+hl(v("m")+" = 49"))),
 dict(t="Evalúa la expresión",
  d=disp(sq("49 &minus; 13")+" + "+sq("49 + 15")+" = "+sq("36")+" + "+sq("64")+" = 6 + 8 = "+hl("14"))),
],
idea="MCD(ka; kb) = k·MCD(a; b). Con a y b primos entre sí, el MCD «hereda» directamente el factor común k."),

# ─────────────────────────────── P16 ──────────────────────────────
dict(n=16, tema="Aritmética", sub="Progresión geométrica", dif=2,
enun="De un recipiente A, el primer día se sacan 5 litros, el segundo día 10 litros, el tercer día "
     "20 litros y así sucesivamente. De un recipiente B, el primer día se sacan 2 litros, el segundo "
     "día 4 litros, el tercer día 8 litros y así sucesivamente. La extracción se realizó la misma "
     "cantidad de días y lo extraído de cada recipiente el último día se diferencia en 96 litros. "
     "¿Cuántos litros se extrajeron de los dos recipientes?",
opts=["441", "442", "443", "444"], ans=0,
steps=[
 dict(t="Reconoce las dos progresiones",
  d=para("Ambas extracciones se duplican cada día (razón 2):")+
    para("&bull; Recipiente A: 5, 10, 20, ... "+ARROW+" día "+v("n")+": 5"+CDOT+"2<sup>"+v("n")+"&minus;1</sup><br>"
     "&bull; Recipiente B: 2, 4, 8, ... "+ARROW+" día "+v("n")+": 2"+CDOT+"2<sup>"+v("n")+"&minus;1</sup>")),
 dict(t="Usa el dato del último día",
  d=disp("5"+CDOT+"2<sup>"+v("n")+"&minus;1</sup> &minus; 2"+CDOT+"2<sup>"+v("n")+"&minus;1</sup> = 96"+IMPL+
         "3"+CDOT+"2<sup>"+v("n")+"&minus;1</sup> = 96"+IMPL+"2<sup>"+v("n")+"&minus;1</sup> = 32")+
    para("Como 32 = 2⁵: "+hl(v("n")+" = 6 días")+".")),
 dict(t="Suma las dos progresiones geométricas",
  d=para("Suma de una PG: "+v("S")+" = "+v("a")+"<sub>1</sub>·"+fr(v("r")+"<sup>"+v("n")+"</sup> &minus; 1", v("r")+" &minus; 1")+
     ". Con razón 2 y 6 días: 2⁶ &minus; 1 = 63.")+
    disp(v("S")+"<sub>A</sub> = 5"+CDOT+"63 = 315&nbsp;&nbsp;&nbsp;&nbsp;"+v("S")+"<sub>B</sub> = 2"+CDOT+"63 = 126")),
 dict(t="Total",
  d=disp("315 + 126 = "+hl("441 litros"))+
    para("Verificación del dato: día 6 "+ARROW+" A saca 160 L y B saca 64 L; 160 &minus; 64 = 96 &#10003;.")),
],
idea="Dos PG con la misma razón: su diferencia día a día también es una PG. Y la suma con razón 2 vale a₁·(2ⁿ − 1)."),
]
