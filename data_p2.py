# -*- coding: utf-8 -*-
"""POP 2025 Reconstruido PUCP — Problemas 17 a 34 (Álgebra)."""
from mh import *

PROBLEMS_2 = [

# ─────────────────────────────── P17 ──────────────────────────────
dict(n=17, tema="Álgebra", sub="Teoría de exponentes", dif=2,
enun="Se conoce lo siguiente:"+
     disp(v("A")+" = "+fr("5<sup>"+v("x")+"+4</sup> &minus; 5<sup>"+v("x")+"+2</sup>", "5<sup>"+v("x")+"</sup>")+
     "&nbsp;&nbsp;&nbsp;&nbsp;"+v("B")+" = "+fr("3<sup>"+v("y")+"+5</sup> &minus; 3<sup>"+v("y")+"+3</sup>", "3<sup>"+v("y")+"</sup>"))+
     "Calcule el valor de "+fr("36"+v("A"), v("B"))+".",
opts=["200", "150", "50", "100"], ans=3,
steps=[
 dict(t="Divide cada potencia entre el denominador",
  d=para("Al dividir potencias de la misma base se restan los exponentes; la "+v("x")+" desaparece:")+
    disp(v("A")+" = 5<sup>"+v("x")+"+4&minus;"+v("x")+"</sup> &minus; 5<sup>"+v("x")+"+2&minus;"+v("x")+"</sup> = 5⁴ &minus; 5² = 625 &minus; 25 = "+hl("600"))),
 dict(t="Lo mismo con B",
  d=disp(v("B")+" = 3⁵ &minus; 3³ = 243 &minus; 27 = "+hl("216"))+
    para("Ese es el sentido del problema: las variables solo estaban de adorno.")),
 dict(t="Evalúa lo pedido",
  d=disp(fr("36"+CDOT+"600","216")+" = "+fr("21 600","216")+" = "+hl("100"))),
],
idea="a^(x+k)/a^x = a^k: cuando toda la expresión comparte base, las variables del exponente se cancelan solas."),

# ─────────────────────────────── P18 ──────────────────────────────
dict(n=18, tema="Álgebra", sub="Ecuaciones exponenciales", dif=1,
enun="Resolver: (25)<sup>3"+v("x")+" + 1</sup> = (625)<sup>"+v("x")+" &minus; 3</sup>",
opts=["CS = {7}", "CS = {&minus;2}", "CS = {&minus;7}", "CS = {2}"], ans=2,
steps=[
 dict(t="Lleva todo a base 5",
  d=para("25 = 5² y 625 = 5⁴, así que reescribimos ambos lados:")+
    disp("5<sup>2(3"+v("x")+"+1)</sup> = 5<sup>4("+v("x")+"&minus;3)</sup>")),
 dict(t="Iguala exponentes",
  d=para("Con bases iguales, los exponentes deben ser iguales:")+
    disp("6"+v("x")+" + 2 = 4"+v("x")+" &minus; 12")),
 dict(t="Despeja",
  d=disp("2"+v("x")+" = &minus;14"+IMPL+hl(v("x")+" = &minus;7"))+
    para("CS = {&minus;7}.")),
 dict(t="Verifica",
  d=para("Exponente izquierdo: 2(3·(&minus;7)+1) = &minus;40. Exponente derecho: 4(&minus;7&minus;3) = &minus;40 &#10003;.")),
],
idea="Ecuación exponencial: expresa ambos lados en la misma base y pasa a igualar exponentes."),

# ─────────────────────────────── P19 ──────────────────────────────
dict(n=19, tema="Álgebra", sub="Ecuaciones exponenciales", dif=3,
enun="Halle el valor de "+v("x")+" en la siguiente ecuación:"+
     disp(rt("4", fr("2"+CDOT+sq("4")+"<sup>23</sup> + 4<sup>"+v("x")+"</sup>", "4<sup>"+v("x")+"+4</sup> + 1"))+" = 4"),
opts=["16", "8", "4", "2"], ans=2,
steps=[
 dict(t="Ordena el numerador",
  d=para("Primero simplifica 2"+CDOT+"("+sq("4")+")<sup>23</sup> = 2"+CDOT+"2<sup>23</sup> = 2<sup>24</sup>. "
     "Y como 2<sup>24</sup> = (2²)<sup>12</sup>, esto es "+hl("4<sup>12</sup>")+". Todo queda en base 4.")),
 dict(t="Elimina la raíz cuarta",
  d=para("Elevamos ambos lados a la cuarta potencia:")+
    disp(fr("4<sup>12</sup> + 4<sup>"+v("x")+"</sup>", "4<sup>"+v("x")+"+4</sup> + 1")+" = 4⁴")),
 dict(t="Multiplica en cruz",
  d=disp("4<sup>12</sup> + 4<sup>"+v("x")+"</sup> = 4⁴"+CDOT+"4<sup>"+v("x")+"+4</sup> + 4⁴ = 4<sup>"+v("x")+"+8</sup> + 4⁴")),
 dict(t="Compara término a término",
  d=para("Busca que los dos lados tengan la misma forma. Si "+v("x")+" = 4:")+
    disp("4<sup>12</sup> + 4⁴ = 4<sup>12</sup> + 4⁴ &#10003;")+
    para("Los términos se emparejan exactamente (4<sup>x+8</sup> = 4<sup>12</sup> y 4<sup>x</sup> = 4⁴), así que "+hl(v("x")+" = 4")+".")),
],
idea="Unifica la base (aquí, todo a base 4), elimina la raíz elevando, y busca que ambos lados queden con la misma estructura."),

# ─────────────────────────────── P20 ──────────────────────────────
dict(n=20, tema="Álgebra", sub="Racionalización", dif=3,
enun="Si se cumple que:"+
     disp(fr("3", rt("3","4")+" &minus; 1")+" = "+rt("3",v("a"))+" + "+rt("3",v("b"))+" + "+rt("3",v("c")))+
     "halle "+v("a")+" + "+v("b")+" + "+v("c")+".",
opts=["4", "16", "20", "21"], ans=3,
steps=[
 dict(t="Reconoce la identidad útil",
  d=para("Para racionalizar denominadores con raíces cúbicas se usa la diferencia de cubos:")+
    disp(v("t")+"³ &minus; 1 = ("+v("t")+" &minus; 1)("+v("t")+"² + "+v("t")+" + 1)")+
    para("Aquí conviene llamar "+v("t")+" = "+rt("3","4")+", de modo que "+v("t")+"³ = 4.")),
 dict(t="Multiplica por el factor racionalizante",
  d=disp(fr("3", v("t")+" &minus; 1")+CDOT+fr(v("t")+"² + "+v("t")+" + 1", v("t")+"² + "+v("t")+" + 1")+
         " = "+fr("3("+v("t")+"² + "+v("t")+" + 1)", v("t")+"³ &minus; 1")+" = "+fr("3("+v("t")+"² + "+v("t")+" + 1)", "4 &minus; 1"))),
 dict(t="Simplifica",
  d=disp("= "+v("t")+"² + "+v("t")+" + 1 = "+rt("3","16")+" + "+rt("3","4")+" + "+rt("3","1"))+
    para("Porque "+v("t")+"² = ("+rt("3","4")+")² = "+rt("3","16")+" y 1 = "+rt("3","1")+".")),
 dict(t="Identifica y suma",
  d=disp(v("a")+" + "+v("b")+" + "+v("c")+" = 16 + 4 + 1 = "+hl("21"))),
],
idea="Denominador t − 1 con t = raíz cúbica: multiplica por (t² + t + 1) y usa t³ − 1. El denominador se vuelve racional de inmediato."),

# ─────────────────────────────── P21 ──────────────────────────────
dict(n=21, tema="Álgebra", sub="División de polinomios", dif=2,
enun="Halle el resto de:"+disp(fr("("+v("x")+" &minus; 1)⁴ + 1", v("x")+"² &minus; 1")),
opts=["8"+v("x")+" &minus; 9", "&minus;8"+v("x")+" + 9", "8"+v("x")+" + 9", "&minus;8"+v("x")+" &minus; 9"], ans=1,
steps=[
 dict(t="Define la forma del resto",
  d=para("El divisor "+v("x")+"² &minus; 1 tiene grado 2, así que el resto tiene grado a lo más 1:")+
    disp(v("R")+"("+v("x")+") = "+v("a")+v("x")+" + "+v("b"))+
    para("Además "+v("x")+"² &minus; 1 = ("+v("x")+"&minus;1)("+v("x")+"+1): sus raíces son 1 y &minus;1. "
     "El truco: evaluar el dividendo en esas raíces, donde el término del cociente se anula.")),
 dict(t="Evalúa en x = 1",
  d=disp("(1 &minus; 1)⁴ + 1 = 1"+IMPL+v("a")+" + "+v("b")+" = 1")),
 dict(t="Evalúa en x = −1",
  d=disp("(&minus;1 &minus; 1)⁴ + 1 = 16 + 1 = 17"+IMPL+"&minus;"+v("a")+" + "+v("b")+" = 17")),
 dict(t="Resuelve el sistema",
  d=para("Sumando ambas ecuaciones: 2"+v("b")+" = 18 "+IMPL+" "+v("b")+" = 9, y entonces "+v("a")+" = &minus;8.")+
    disp(v("R")+"("+v("x")+") = "+hl("&minus;8"+v("x")+" + 9"))),
],
idea="Teorema del resto generalizado: D(x) = d(x)·q(x) + R(x). Evalúa en las raíces del divisor y q(x) desaparece; queda un sistema para R."),

# ─────────────────────────────── P22 ──────────────────────────────
dict(n=22, tema="Álgebra", sub="Polinomios", dif=3,
enun="Los polinomios "+v("P")+"("+v("x")+") y "+v("Q")+"("+v("x")+") satisfacen: tienen grados 2 y 1 "
     "respectivamente; tienen como factor común a ("+v("x")+" &minus; 1); "+v("P")+"(0) = 2 y "+
     fr(v("P")+"("+v("x")+")", v("Q")+"("+v("x")+")")+" = 2"+v("x")+" + 2. Halle "+v("P")+"("+v("x")+") &minus; "+v("Q")+"("+v("x")+").",
opts=["2"+v("x")+"² &minus; "+v("x")+" + 1", "&minus;2"+v("x")+"² + "+v("x")+" + 1",
      "&minus;2"+v("x")+"² + "+v("x")+" &minus; 1", "2"+v("x")+"² &minus; "+v("x")+" &minus; 1"], ans=1,
steps=[
 dict(t="Modela Q con el factor común",
  d=para(v("Q")+" es de grado 1 y contiene al factor ("+v("x")+" &minus; 1); entonces es un múltiplo escalar:")+
    disp(v("Q")+"("+v("x")+") = "+v("k")+"("+v("x")+" &minus; 1)")),
 dict(t="Construye P desde la división",
  d=para("Si "+v("P")+"/"+v("Q")+" = 2"+v("x")+" + 2, entonces:")+
    disp(v("P")+"("+v("x")+") = "+v("Q")+"("+v("x")+")"+CDOT+"(2"+v("x")+" + 2) = 2"+v("k")+"("+v("x")+" &minus; 1)("+v("x")+" + 1)")+
    para("Grado 2 &#10003; y también contiene a ("+v("x")+" &minus; 1) &#10003;.")),
 dict(t="Usa P(0) = 2 para hallar k",
  d=disp(v("P")+"(0) = 2"+v("k")+"(&minus;1)(1) = &minus;2"+v("k")+" = 2"+IMPL+hl(v("k")+" = &minus;1"))+
    para("Entonces "+v("P")+"("+v("x")+") = &minus;2("+v("x")+"² &minus; 1) = &minus;2"+v("x")+"² + 2 y "+
     v("Q")+"("+v("x")+") = &minus;("+v("x")+" &minus; 1) = 1 &minus; "+v("x")+".")),
 dict(t="Resta",
  d=disp(v("P")+" &minus; "+v("Q")+" = (&minus;2"+v("x")+"² + 2) &minus; (1 &minus; "+v("x")+") = "+hl("&minus;2"+v("x")+"² + "+v("x")+" + 1"))),
 dict(t="Verifica",
  d=para(v("P")+"(0) = 2 &#10003;; "+v("P")+"/"+v("Q")+" = &minus;2("+v("x")+"&minus;1)("+v("x")+"+1)/[&minus;("+v("x")+"&minus;1)] = 2("+v("x")+"+1) = 2"+v("x")+"+2 &#10003;.")),
],
idea="Cuando P/Q es un polinomio, escribe P = Q·cociente. Las condiciones restantes (grado, factor, un valor numérico) fijan la constante."),

# ─────────────────────────────── P23 ──────────────────────────────
dict(n=23, tema="Álgebra", sub="Ecuaciones con radicales", dif=2,
enun="Resuelva: "+sq("6")+CDOT+v("x")+" &minus; "+sq("8")+" = "+sq("2")+CDOT+v("x")+" &minus; "+sq("24"),
opts=["C.S. = {2}", "C.S. = {&minus;2}", "C.S. = {"+sq("3")+"}", "C.S. = {"+sq("2")+"}"], ans=1,
steps=[
 dict(t="Agrupa x a un lado",
  d=disp(sq("6")+v("x")+" &minus; "+sq("2")+v("x")+" = "+sq("8")+" &minus; "+sq("24"))+
    disp(v("x")+"("+sq("6")+" &minus; "+sq("2")+") = "+sq("8")+" &minus; "+sq("24"))),
 dict(t="Simplifica los radicales",
  d=disp(sq("8")+" = 2"+sq("2")+"&nbsp;&nbsp;&nbsp;&nbsp;"+sq("24")+" = 2"+sq("6"))+
    para("Entonces el lado derecho es 2"+sq("2")+" &minus; 2"+sq("6")+" = &minus;2("+sq("6")+" &minus; "+sq("2")+").")),
 dict(t="Despeja x",
  d=para("El factor ("+sq("6")+" &minus; "+sq("2")+") aparece en ambos lados y no es cero, así que se cancela:")+
    disp(v("x")+" = "+fr("&minus;2("+sq("6")+" &minus; "+sq("2")+")", sq("6")+" &minus; "+sq("2"))+" = "+hl("&minus;2"))+
    para("C.S. = {&minus;2}.")),
],
idea="Simplifica cada radical (√8 = 2√2, √24 = 2√6) y busca el factor común: la ecuación es lineal en x."),

# ─────────────────────────────── P24 ──────────────────────────────
dict(n=24, tema="Álgebra", sub="Ecuación cuadrática", dif=1,
enun="Si "+v("r")+" y "+v("s")+" son las raíces de la ecuación 2"+v("x")+"² &minus; 16"+v("x")+" &minus; 130 = 0, "
     "halle "+fr(v("r")+" + "+v("s"), v("r")+v("s"))+".",
opts=["&minus;"+fr("8","65"), fr("8","65"), "&minus;"+fr("8","130"), "&minus;"+fr("8","130")], ans=0,
steps=[
 dict(t="No resuelvas: usa Cardano–Vieta",
  d=para("Para "+v("a")+v("x")+"² + "+v("b")+v("x")+" + "+v("c")+" = 0, la suma de raíces es &minus;"+v("b")+"/"+v("a")+
     " y el producto es "+v("c")+"/"+v("a")+". No hace falta hallar las raíces.")),
 dict(t="Calcula suma y producto",
  d=disp(v("r")+" + "+v("s")+" = "+fr("16","2")+" = 8&nbsp;&nbsp;&nbsp;&nbsp;"+
         v("r")+v("s")+" = "+fr("&minus;130","2")+" = &minus;65")),
 dict(t="Divide",
  d=disp(fr(v("r")+" + "+v("s"), v("r")+v("s"))+" = "+fr("8","&minus;65")+" = "+hl("&minus;"+fr("8","65")))),
],
idea="Suma = −b/a, producto = c/a. Divide primero entre el coeficiente principal (aquí 2) y evita arrastrar el −130.",
nota="En el examen reconstruido las alternativas C y D aparecen repetidas (−8/130); es una errata de la reconstrucción. La correcta es A: −8/65."),

# ─────────────────────────────── P25 ──────────────────────────────
dict(n=25, tema="Álgebra", sub="Planteo con áreas", dif=2,
enun="Un terreno tiene forma rectangular. Si tuviera 5 m más de largo y 5 m más de ancho, su área "
     "se duplicaría. Si tuviera 2 m menos de largo y 2 m menos de ancho, su área disminuiría en 46 m². "
     "Halle la longitud del mayor lado del terreno original.",
opts=["15 m", "10 m", "12 m", "8 m"], ans=0,
steps=[
 dict(t="Plantea las dos condiciones",
  d=para("Sean "+v("L")+" y "+v("W")+" los lados. Las condiciones son:")+
    disp("("+v("L")+"+5)("+v("W")+"+5) = 2"+v("L")+v("W")+"&nbsp;&nbsp;&nbsp;&nbsp;("+v("L")+"&minus;2)("+v("W")+"&minus;2) = "+v("L")+v("W")+" &minus; 46")),
 dict(t="Desarrolla la segunda (es la fácil)",
  d=disp(v("L")+v("W")+" &minus; 2"+v("L")+" &minus; 2"+v("W")+" + 4 = "+v("L")+v("W")+" &minus; 46"+IMPL+
         hl(v("L")+" + "+v("W")+" = 25"))),
 dict(t="Desarrolla la primera",
  d=disp(v("L")+v("W")+" + 5("+v("L")+"+"+v("W")+") + 25 = 2"+v("L")+v("W")+IMPL+
         v("L")+v("W")+" = 5(25) + 25 = "+hl("150"))),
 dict(t="Encuentra los lados",
  d=para("Dos números que suman 25 y multiplican 150: son las raíces de "+v("t")+"² &minus; 25"+v("t")+" + 150 = 0, "
     "que factoriza como ("+v("t")+"&minus;10)("+v("t")+"&minus;15) = 0. Lados: 10 y 15.")+
    disp("Mayor lado = "+hl("15 m"))),
 dict(t="Verifica",
  d=para("Original: 150 m². Con +5: 20"+TIMES+"15 = 300 = 2·150 &#10003;. Con &minus;2: 13"+TIMES+"8 = 104 = 150 &minus; 46 &#10003;.")),
],
idea="Desarrolla y simplifica: los productos LW se cancelan y quedan la suma (L+W) y el producto (LW) — de ahí, ecuación de segundo grado."),

# ─────────────────────────────── P26 ──────────────────────────────
dict(n=26, tema="Álgebra", sub="Planteo de ecuaciones", dif=2,
enun="El peso de una barra de hierro es de 36 kg. Si se la estira hasta hacerla 1 m más larga, cada "
     "metro pesará 0,5 kg menos. Si "+v("x")+" es la longitud inicial de la barra, la ecuación que "
     "permite resolver este problema es:",
opts=[v("x")+"² + "+v("x")+" &minus; 72 = 0", v("x")+"² &minus; 2"+v("x")+" &minus; 36 = 0",
      v("x")+"² &minus; "+v("x")+" &minus; 72 = 0", v("x")+"² + "+v("x")+" + 72 = 0"], ans=0,
steps=[
 dict(t="Expresa el peso por metro",
  d=para("La barra pesa 36 kg en total (estirarla no cambia su masa).")+
    para("&bull; Antes: "+fr("36",v("x"))+" kg por metro.<br>&bull; Después (mide "+v("x")+"+1): "+
     fr("36",v("x")+"+1")+" kg por metro.")),
 dict(t="Traduce «0,5 kg menos»",
  d=disp(fr("36",v("x"))+" &minus; "+fr("36",v("x")+"+1")+" = "+fr("1","2"))),
 dict(t="Elimina denominadores",
  d=para("Multiplicamos por 2"+v("x")+"("+v("x")+"+1):")+
    disp("72("+v("x")+"+1) &minus; 72"+v("x")+" = "+v("x")+"("+v("x")+"+1)"+IMPL+"72 = "+v("x")+"² + "+v("x"))+
    disp(hl(v("x")+"² + "+v("x")+" &minus; 72 = 0"))),
 dict(t="Chequeo rápido",
  d=para("Esa cuadrática factoriza como ("+v("x")+"+9)("+v("x")+"&minus;8) = 0 "+ARROW+" "+v("x")+" = 8 m. "
     "Peso por metro: 4,5 kg antes y 4 kg después: exactamente 0,5 menos &#10003;. "
     "(El problema solo pedía la ecuación).")),
],
idea="Densidad lineal = peso total ÷ longitud. La comparación «pesará 0,5 menos por metro» da la ecuación racional que se vuelve cuadrática."),

# ─────────────────────────────── P27 ──────────────────────────────
dict(n=27, tema="Álgebra", sub="Geometría analítica", dif=2,
enun="Se sabe que la ecuación de una recta es "+v("p")+v("x")+" + "+v("q")+v("y")+" + "+v("r")+" = 0. "
     "Además "+v("p")+" + "+v("q")+" + "+v("r")+" = 6 y la pendiente de dicha recta es 3. "
     "Si el punto (0; &minus;5) pertenece a la recta, calcule "+v("p")+CDOT+v("q")+CDOT+v("r")+".",
opts=["120", "&minus;60", "60", "&minus;120"], ans=3,
steps=[
 dict(t="Usa el punto conocido",
  d=para("Sustituye (0; &minus;5) en la ecuación:")+
    disp(v("p")+"(0) + "+v("q")+"(&minus;5) + "+v("r")+" = 0"+IMPL+hl(v("r")+" = 5"+v("q")))),
 dict(t="Usa la pendiente",
  d=para("De "+v("p")+v("x")+" + "+v("q")+v("y")+" + "+v("r")+" = 0, la pendiente es &minus;"+v("p")+"/"+v("q")+":")+
    disp("&minus;"+fr(v("p"),v("q"))+" = 3"+IMPL+hl(v("p")+" = &minus;3"+v("q")))),
 dict(t="Usa la suma",
  d=disp(v("p")+" + "+v("q")+" + "+v("r")+" = &minus;3"+v("q")+" + "+v("q")+" + 5"+v("q")+" = 3"+v("q")+" = 6"+IMPL+
         hl(v("q")+" = 2"))+
    para("Entonces "+v("p")+" = &minus;6 y "+v("r")+" = 10.")),
 dict(t="Multiplica",
  d=disp(v("p")+CDOT+v("q")+CDOT+v("r")+" = (&minus;6)(2)(10) = "+hl("&minus;120"))+
    para("Verificación: la recta &minus;6"+v("x")+" + 2"+v("y")+" + 10 = 0 equivale a "+v("y")+" = 3"+v("x")+" &minus; 5: "
     "pendiente 3 &#10003; y pasa por (0; &minus;5) &#10003;.")),
],
idea="En px + qy + r = 0 la pendiente es −p/q y el punto (0, y₀) da r directamente. Tres datos, tres incógnitas."),

# ─────────────────────────────── P28 ──────────────────────────────
dict(n=28, tema="Álgebra", sub="Fracciones algebraicas", dif=2,
enun="Simplifique la expresión (donde "+v("x")+" "+NEQ+" 0 e "+v("y")+" "+NEQ+" 0):"+
     disp(v("P")+" = "+mrow("(", fr(v("x")+"<sup>&minus;1</sup> + "+v("y")+"<sup>&minus;1</sup>",
                                    v("x")+"<sup>&minus;1</sup> &minus; "+v("y")+"<sup>&minus;1</sup>"), ")<sup>&minus;1</sup>")),
opts=["&minus;1", fr(v("y")+" &minus; "+v("x"), v("y")+" + "+v("x")),
      fr(v("x")+"² + "+v("y")+"²", v("x")+"²"+v("y")+"²"), "0"], ans=1,
steps=[
 dict(t="Convierte los exponentes negativos",
  d=para(v("x")+"<sup>&minus;1</sup> = "+fr("1",v("x"))+". Sumamos y restamos con denominador común "+v("x")+v("y")+":")+
    disp(fr("1",v("x"))+" + "+fr("1",v("y"))+" = "+fr(v("y")+" + "+v("x"), v("x")+v("y"))+
         "&nbsp;&nbsp;&nbsp;&nbsp;"+fr("1",v("x"))+" &minus; "+fr("1",v("y"))+" = "+fr(v("y")+" &minus; "+v("x"), v("x")+v("y")))),
 dict(t="Divide las fracciones",
  d=disp(fr(v("x")+"<sup>&minus;1</sup> + "+v("y")+"<sup>&minus;1</sup>", v("x")+"<sup>&minus;1</sup> &minus; "+v("y")+"<sup>&minus;1</sup>")+
         " = "+fr(v("y")+" + "+v("x"), v("y")+" &minus; "+v("x")))+
    para("Los "+v("x")+v("y")+" se cancelan al dividir.")),
 dict(t="Aplica el exponente −1 exterior",
  d=para("Elevar a &minus;1 es invertir la fracción:")+
    disp(v("P")+" = "+hl(fr(v("y")+" &minus; "+v("x"), v("y")+" + "+v("x"))))),
],
idea="x⁻¹ = 1/x y elevar a −1 invierte. Trabaja por capas: primero el paréntesis, al final la inversión exterior."),

# ─────────────────────────────── P29 ──────────────────────────────
dict(n=29, tema="Álgebra", sub="Radicales y exponentes", dif=2,
enun="Resuelve la ecuación:"+disp(sq("3"+CDOT+rt("3","9"+sq("27")))+" = 3<sup>"+v("x")+"</sup>"),
opts=[fr("11","12"), fr("13","12"), fr("12","13"), fr("17","12")], ans=1,
steps=[
 dict(t="Convierte todo a potencias de 3",
  d=disp("27 = 3³"+IMPL+sq("27")+" = 3<sup>3/2</sup>&nbsp;&nbsp;&nbsp;&nbsp;9 = 3²")),
 dict(t="Trabaja de adentro hacia afuera",
  d=disp("9"+CDOT+sq("27")+" = 3²"+CDOT+"3<sup>3/2</sup> = 3<sup>7/2</sup>")+
    disp(rt("3","3<sup>7/2</sup>")+" = 3<sup>7/6</sup>")+
    para("(la raíz cúbica divide el exponente entre 3).")),
 dict(t="Sigue con la capa exterior",
  d=disp("3"+CDOT+"3<sup>7/6</sup> = 3<sup>13/6</sup>"+IMPL+sq("3<sup>13/6</sup>")+" = 3<sup>13/12</sup>")),
 dict(t="Iguala exponentes",
  d=disp("3<sup>"+v("x")+"</sup> = 3<sup>13/12</sup>"+IMPL+hl(v("x")+" = "+fr("13","12")))),
],
idea="Raíces anidadas: convierte todo a la misma base y opera exponentes de adentro hacia afuera (multiplicar suma, raíz divide)."),

# ─────────────────────────────── P30 ──────────────────────────────
dict(n=30, tema="Álgebra", sub="Ecuación cuadrática", dif=1,
enun="Calcula el producto de raíces de la ecuación: ("+v("x")+" + 2)("+v("x")+" &minus; 1) = 4",
opts=["&minus;2", "1", "&minus;6", "4"], ans=2,
steps=[
 dict(t="Cuidado con el error clásico",
  d=para("No puedes leer las raíces de ("+v("x")+"+2)("+v("x")+"&minus;1) = 4 directamente: eso solo vale "
     "cuando el producto es <b>cero</b>. Primero hay que pasar todo a un lado.")),
 dict(t="Desarrolla y ordena",
  d=disp(v("x")+"² + "+v("x")+" &minus; 2 = 4"+IMPL+v("x")+"² + "+v("x")+" &minus; 6 = 0")),
 dict(t="Producto de raíces",
  d=para("Por Cardano–Vieta, el producto es "+v("c")+"/"+v("a")+":")+
    disp(v("x")+"<sub>1</sub>"+CDOT+v("x")+"<sub>2</sub> = "+fr("&minus;6","1")+" = "+hl("&minus;6"))+
    para("De hecho la ecuación factoriza como ("+v("x")+"+3)("+v("x")+"&minus;2) = 0: raíces &minus;3 y 2, producto &minus;6 &#10003;.")),
],
idea="Iguala a cero antes de usar cualquier propiedad de raíces. Luego, producto = c/a sin resolver."),

# ─────────────────────────────── P31 ──────────────────────────────
dict(n=31, tema="Álgebra", sub="Sistemas no lineales", dif=3,
enun="Resuelve el sistema e indica un valor de "+v("x")+" + "+v("y")+":"+
     disp("2"+v("x")+"² + 32"+v("y")+" + 56 = 0&nbsp;&nbsp;&nbsp;&nbsp;"+v("x")+"² + "+v("x")+" &minus; 3"+v("y")+" &minus; 54 = 0"),
opts=["&minus;4", "&minus;6", "2", "6"], ans=2,
steps=[
 dict(t="Despeja x² de la primera",
  d=disp("2"+v("x")+"² = &minus;32"+v("y")+" &minus; 56"+IMPL+hl(v("x")+"² = &minus;16"+v("y")+" &minus; 28"))),
 dict(t="Sustituye en la segunda",
  d=disp("(&minus;16"+v("y")+" &minus; 28) + "+v("x")+" &minus; 3"+v("y")+" &minus; 54 = 0"+IMPL+
         hl(v("x")+" = 19"+v("y")+" + 82"))+
    para("La segunda ecuación se volvió lineal: ahora "+v("x")+" está en función de "+v("y")+".")),
 dict(t="Vuelve a la primera",
  d=para("Sustituimos "+v("x")+" = 19"+v("y")+" + 82 en "+v("x")+"² = &minus;16"+v("y")+" &minus; 28:")+
    disp("(19"+v("y")+" + 82)² = &minus;16"+v("y")+" &minus; 28")+
    para("Desarrollando: 361"+v("y")+"² + 3132"+v("y")+" + 6752 = 0. Se ve dura, pero prueba "+v("y")+" = &minus;4: "
     "361(16) &minus; 3132(4) + 6752 = 5776 &minus; 12528 + 6752 = 0 &#10003;.")),
 dict(t="Halla x y responde",
  d=disp(v("y")+" = &minus;4"+IMPL+v("x")+" = 19(&minus;4) + 82 = 6"+IMPL+
         v("x")+" + "+v("y")+" = 6 &minus; 4 = "+hl("2"))+
    para("Comprobación en las originales: 2(36) + 32(&minus;4) + 56 = 0 &#10003; y 36 + 6 + 12 &minus; 54 = 0 &#10003;.")),
],
idea="En sistemas con x² en ambas ecuaciones, elimina x² primero: una ecuación se vuelve lineal y el sistema cae por sustitución."),

# ─────────────────────────────── P32 ──────────────────────────────
dict(n=32, tema="Aritmética", sub="Fracciones", dif=2,
enun="Calcula:"+disp(v("E")+" = "+mrow("(",fr("1",fr("1","3")),")³ + (",fr("1",fr("2","5")),")² + (",fr("1",fr("4","11")),")")),
opts=["18", "27", "36", "54"], ans=2, dup=14,
steps=[
 dict(t="Es la misma expresión del problema 14",
  d=para("El examen repite la expresión; aquí piden directamente su valor "+v("E")+" (en el problema 14 pedían "+sq(v("A"))+").")),
 dict(t="Invierte y opera",
  d=disp(fr("1",fr("1","3"))+" = 3"+IMPL+"3³ = 27&nbsp;&nbsp;&nbsp;&nbsp;"+
         fr("1",fr("2","5"))+" = "+fr("5","2")+IMPL+mrow("(",fr("5","2"),")² = ",fr("25","4"))+
         "&nbsp;&nbsp;&nbsp;&nbsp;"+fr("1",fr("4","11"))+" = "+fr("11","4"))),
 dict(t="Suma",
  d=disp(v("E")+" = 27 + "+fr("25","4")+" + "+fr("11","4")+" = 27 + 9 = "+hl("36"))),
],
idea="1 ÷ (a/b) = b/a. Las fracciones de igual denominador (25/4 y 11/4) suman un entero exacto: 9."),

# ─────────────────────────────── P33 ──────────────────────────────
dict(n=33, tema="Álgebra", sub="Intervalos", dif=2,
enun="Dados los intervalos "+v("A")+" = [&minus;2; 1], "+v("B")+" = [&minus;1; +"+INF+"[ y "+
     v("C")+" = ]&minus;"+INF+"; 2[, determine ("+v("B")+" &cap; "+v("C")+") &minus; "+v("A")+".",
opts=["[&minus;2; 2[", "[1; 2[", "]1; &minus;1[", "]1; 2["], ans=3, fig="fig33",
steps=[
 dict(t="Primero la intersección B ∩ C",
  d=para(v("B")+" pide "+v("x")+" "+GEQ+" &minus;1 y "+v("C")+" pide "+v("x")+" &lt; 2. Juntas:")+
    disp(v("B")+" &cap; "+v("C")+" = [&minus;1; 2[")),
 dict(t="Ahora quita A",
  d=para("La diferencia «&minus; "+v("A")+"» elimina de [&minus;1; 2[ todo lo que esté en [&minus;2; 1]. "
     "Lo que sobrevive es lo que está <b>después de 1</b> (el 1 incluido se va, porque 1 &isin; "+v("A")+"):")+
    disp("[&minus;1; 2[ &minus; [&minus;2; 1] = "+hl("]1; 2["))),
 dict(t="Revisa los extremos",
  d=para("&bull; ¿Entra 1? No: 1 está en "+v("A")+", queda excluido "+ARROW+" paréntesis abierto en 1.<br>"
     "&bull; ¿Entra 2? No: "+v("C")+" ya lo excluía "+ARROW+" abierto en 2. Resultado: ]1; 2[.")),
],
idea="Dibuja la recta numérica: intersecar = zona común; restar = borrar la zona del otro conjunto y vigilar si cada extremo entra o no."),

# ─────────────────────────────── P34 ──────────────────────────────
dict(n=34, tema="Álgebra", sub="Ecuaciones polinómicas", dif=3,
enun="Luego de resolver la ecuación ("+v("x")+"² &minus; "+v("x")+")³ &minus; 2"+v("x")+"²("+v("x")+" &minus; 1)² = 0, "
     "halla la suma del menor y el mayor valor que puede tomar "+v("x")+".",
opts=["&minus;1", "0", "1", "2"], ans=2,
steps=[
 dict(t="Factoriza la base común",
  d=para("Observa que "+v("x")+"² &minus; "+v("x")+" = "+v("x")+"("+v("x")+" &minus; 1). Entonces:")+
    disp("("+v("x")+"² &minus; "+v("x")+")³ = "+v("x")+"³("+v("x")+" &minus; 1)³")+
    para("Ambos términos comparten el factor "+v("x")+"²("+v("x")+" &minus; 1)².")),
 dict(t="Extrae el factor común",
  d=disp(v("x")+"²("+v("x")+" &minus; 1)²"+CDOT+"["+v("x")+"("+v("x")+" &minus; 1) &minus; 2] = 0")),
 dict(t="Anula cada factor",
  d=para("&bull; "+v("x")+"² = 0 "+ARROW+" "+v("x")+" = 0<br>"
     "&bull; ("+v("x")+" &minus; 1)² = 0 "+ARROW+" "+v("x")+" = 1<br>"
     "&bull; "+v("x")+"² &minus; "+v("x")+" &minus; 2 = 0 "+ARROW+" ("+v("x")+" &minus; 2)("+v("x")+" + 1) = 0 "+ARROW+" "+v("x")+" = 2 o "+v("x")+" = &minus;1")),
 dict(t="Suma extremos",
  d=para("Soluciones: {&minus;1, 0, 1, 2}. Menor: &minus;1. Mayor: 2.")+
    disp("&minus;1 + 2 = "+hl("1"))),
],
idea="Antes de expandir, busca la base repetida: x² − x = x(x − 1). Factorizar el bloque común convierte un grado 6 en una cuadrática."),
]
