# -*- coding: utf-8 -*-
"""POP 2025 Reconstruido PUCP — Problemas 35 a 51 (Geometría)."""
from mh import *

PROBLEMS_3 = [

# ─────────────────────────────── P35 ──────────────────────────────
dict(n=35, tema="Geometría", sub="Ángulos entre paralelas", dif=3,
enun="En la figura mostrada, "+v("L")+"<sub>1</sub> // "+v("L")+"<sub>2</sub> son paralelas. Hallar "+v("x")+".",
opts=["30"+DEG, "40"+DEG, "50"+DEG, "60"+DEG], ans=1, fig="fig35",
steps=[
 dict(t="Sigue la poligonal desde L₂ hacia L₁",
  d=para("La línea quebrada sube de "+v("L")+"<sub>2</sub> a "+v("L")+"<sub>1</sub> y en cada vértice "
     "gira un poco más. Midamos la <b>inclinación</b> de cada tramo respecto de la horizontal "
     "(las paralelas son horizontales).")),
 dict(t="Acumula las inclinaciones",
  d=para("&bull; El primer tramo corta a "+v("L")+"<sub>2</sub> formando "+THETA+": inclinación = "+THETA+".<br>"
     "&bull; En el siguiente vértice el tramo gira 2"+THETA+" más: inclinación = "+THETA+" + 2"+THETA+" = 3"+THETA+".<br>"
     "&bull; En el vértice superior gira 3"+THETA+" más: inclinación = 3"+THETA+" + 3"+THETA+" = 6"+THETA+".")),
 dict(t="Cierra el circuito en L₁",
  d=para("Ese último tramo corta a "+v("L")+"<sub>1</sub> formando el ángulo 12"+THETA+" medido al otro lado. "
     "Ángulos suplementarios sobre la misma recta:")+
    disp("6"+THETA+" + 12"+THETA+" = 180"+DEG+IMPL+hl(THETA+" = 10"+DEG))),
 dict(t="Usa el triángulo pequeño para hallar x",
  d=para("En el vértice superior, la recta de 80"+DEG+" y la transversal forman un triángulo con "+v("L")+"<sub>1</sub>. "
     "La inclinación de la transversal que baja con ángulo "+v("x")+" y la que sube con 12"+THETA+" difieren "
     "exactamente en el ángulo de 80"+DEG+":")+
    disp("12"+THETA+" = "+v("x")+" + 80"+DEG+IMPL+v("x")+" = 120"+DEG+" &minus; 80"+DEG+" = "+hl("40"+DEG))),
 dict(t="Verifica la coherencia",
  d=para("Con "+THETA+" = 10"+DEG+": los ángulos de la figura valen "+THETA+"=10"+DEG+", 2"+THETA+"=20"+DEG+", "
     "3"+THETA+"=30"+DEG+", 12"+THETA+"=120"+DEG+" y "+v("x")+"=40"+DEG+". Todo suma y encaja con las paralelas &#10003;.")),
],
idea="Entre paralelas, la inclinación de una poligonal se va acumulando vértice a vértice; al llegar a la otra paralela debe cerrar 180°."),

# ─────────────────────────────── P36 ──────────────────────────────
dict(n=36, tema="Geometría", sub="Desigualdad triangular", dif=2,
enun="Las longitudes de dos de los lados de un triángulo isósceles son 15 cm y 32 cm. "
     "¿Cuál(es) es (son) el (los) posible(s) valor(es) del perímetro en cm?",
opts=["62 y 69", "62", "62 y 79", "79"], ans=3, fig="fig36",
steps=[
 dict(t="Plantea los dos casos posibles",
  d=para("Isósceles = dos lados iguales. El tercero repite 15 o repite 32:")+
    para("&bull; Caso 1: lados 15, 15, 32 "+ARROW+" perímetro 62.<br>"
     "&bull; Caso 2: lados 32, 32, 15 "+ARROW+" perímetro 79.")),
 dict(t="Filtra con la desigualdad triangular",
  d=para("En todo triángulo, la suma de dos lados debe <b>superar</b> al tercero.")+
    disp("Caso 1: 15 + 15 = 30 &lt; 32 &nbsp;&#10007;&nbsp; ¡no existe ese triángulo!")+
    disp("Caso 2: 32 + 32 = 64 &gt; 15 &nbsp;&#10003;&nbsp; y 32 + 15 &gt; 32 &#10003;")),
 dict(t="Concluye",
  d=para("Solo sobrevive el caso 32, 32, 15:")+
    disp("Perímetro = 32 + 32 + 15 = "+hl("79 cm"))),
],
idea="En los isósceles con dos datos, siempre hay dos candidatos — pero la desigualdad triangular suele eliminar uno. Verifica antes de responder «ambos»."),

# ─────────────────────────────── P37 ──────────────────────────────
dict(n=37, tema="Geometría", sub="Triángulos: alturas y bisectrices", dif=2,
enun="En un triángulo ABC cuyos ángulos están en proporción de 3, 4 y 5 respectivamente, "
     "calcular el ángulo formado por la altura y la bisectriz trazadas desde el ángulo B.",
opts=["30"+DEG, "15"+DEG, "45"+DEG, "18"+DEG], ans=1, fig="fig37",
steps=[
 dict(t="Halla los ángulos del triángulo",
  d=para("Si son 3"+v("k")+", 4"+v("k")+" y 5"+v("k")+": 3"+v("k")+" + 4"+v("k")+" + 5"+v("k")+" = 180"+DEG+
     " "+IMPL+" "+v("k")+" = 15"+DEG+".")+
    disp(v("A")+" = 45"+DEG+"&nbsp;&nbsp;&nbsp;"+v("B")+" = 60"+DEG+"&nbsp;&nbsp;&nbsp;"+v("C")+" = 75"+DEG)),
 dict(t="Usa la fórmula del ángulo entre altura y bisectriz",
  d=para("Desde un mismo vértice, la bisectriz parte el ángulo en dos mitades y la altura cae "
     "perpendicular al lado opuesto. El ángulo entre ambas es:")+
    disp(v("&delta;")+" = "+fr("|"+v("A")+" &minus; "+v("C")+"|","2"))+
    para("(La demostración sale de comparar el ángulo de la altura, 90"+DEG+" &minus; "+v("A")+", con la mitad de "+v("B")+".)")),
 dict(t="Calcula",
  d=disp(v("&delta;")+" = "+fr("|45"+DEG+" &minus; 75"+DEG+"|","2")+" = "+fr("30"+DEG,"2")+" = "+hl("15"+DEG))),
 dict(t="Camino alternativo (sin fórmula)",
  d=para("La altura desde B forma con AB un ángulo de 90"+DEG+" &minus; 45"+DEG+" = 45"+DEG+". "
     "La bisectriz forma 60"+DEG+"/2 = 30"+DEG+" con AB. Diferencia: 45"+DEG+" &minus; 30"+DEG+" = 15"+DEG+" &#10003;.")),
],
idea="Ángulo entre la altura y la bisectriz desde un vértice = |diferencia de los otros dos ángulos| ÷ 2."),

# ─────────────────────────────── P38 ──────────────────────────────
dict(n=38, tema="Geometría", sub="Ley de cosenos", dif=2,
enun="En el triángulo mostrado, el valor de "+v("x")+" es:",
opts=["2"+sq("3"), "5"+sq("3"), "3"+sq("3"), "4"+sq("3")], ans=0, fig="fig38",
steps=[
 dict(t="Identifica qué tienes",
  d=para("Dos lados (6 y 4"+sq("3")+") y el ángulo <b>entre ellos</b> (30"+DEG+"). "
     "Eso pide directamente la ley de cosenos para el lado opuesto "+v("x")+".")),
 dict(t="Aplica la ley de cosenos",
  d=disp(v("x")+"² = 6² + (4"+sq("3")+")² &minus; 2"+CDOT+"6"+CDOT+"4"+sq("3")+CDOT+"cos 30"+DEG)),
 dict(t="Evalúa cada pieza",
  d=disp("6² = 36&nbsp;&nbsp;&nbsp;(4"+sq("3")+")² = 16"+CDOT+"3 = 48&nbsp;&nbsp;&nbsp;cos 30"+DEG+" = "+fr(sq("3"),"2"))+
    disp("2"+CDOT+"6"+CDOT+"4"+sq("3")+CDOT+fr(sq("3"),"2")+" = 24"+CDOT+sq("3")+CDOT+sq("3")+" = 72")+
    para("Aquí está la gracia del problema: "+sq("3")+CDOT+sq("3")+" = 3 y todo se vuelve entero.")),
 dict(t="Resuelve",
  d=disp(v("x")+"² = 36 + 48 &minus; 72 = 12"+IMPL+v("x")+" = "+sq("12")+" = "+hl("2"+sq("3")))),
],
idea="Dos lados y el ángulo incluido ⇒ ley de cosenos. Los radicales del enunciado (4√3, cos 30°) están puestos para que el producto se racionalice."),

# ─────────────────────────────── P39 ──────────────────────────────
dict(n=39, tema="Geometría", sub="Triángulos: alturas", dif=2,
enun="En un triángulo acutángulo ABC se trazan las alturas AM y CN, de modo que AB = 5, NB = 3 y "
     "BC = 6. Halle BM.",
opts=["2,4", "3,6", "2,5", "3,5"], ans=2, fig="fig39",
steps=[
 dict(t="Mira los triángulos rectángulos en B",
  d=para("La altura CN es perpendicular a AB, así que el triángulo CNB es rectángulo en N. "
     "En él, el cateto NB es la <b>proyección</b> de BC sobre AB:")+
    disp("NB = BC"+CDOT+"cos "+v("B")+IMPL+"3 = 6"+CDOT+"cos "+v("B")+IMPL+hl("cos "+v("B")+" = "+fr("1","2")))),
 dict(t="Aplica lo mismo con la otra altura",
  d=para("La altura AM es perpendicular a BC, así que AMB es rectángulo en M y BM es la proyección "
     "de AB sobre BC:")+
    disp("BM = AB"+CDOT+"cos "+v("B")+" = 5"+CDOT+fr("1","2")+" = "+hl("2,5"))),
 dict(t="Nota elegante",
  d=para("De paso, cos "+v("B")+" = 1/2 significa que "+v("B")+" = 60"+DEG+". Y BM·BC = BN·BA = 15 "
     "(los triángulos BNC y BMA son semejantes por compartir el ángulo B): otra forma de llegar a BM = 15/6 = 2,5.")),
],
idea="Cada altura crea un triángulo rectángulo donde el segmento sobre el lado es «lado · cos B». El ángulo B es compartido: dos ecuaciones, una incógnita."),

# ─────────────────────────────── P40 ──────────────────────────────
dict(n=40, tema="Geometría", sub="Trapecios", dif=2,
enun="En un trapecio isósceles ABCD (BC // AD), la base menor mide 6 u y el lado no paralelo 8 u. "
     "Si m"+ANG+"BAD = 60"+DEG+", calcular la longitud de la base mayor.",
opts=["16 u", "18 u", "14 u", "20 u"], ans=2, fig="fig40",
steps=[
 dict(t="Baja las alturas",
  d=para("Desde B y C trazamos alturas hasta AD. La base mayor queda partida en tres pedazos: "
     "un pie izquierdo "+v("p")+", el centro igual a la base menor (6) y un pie derecho igual a "+v("p")+
     " (por ser isósceles).")),
 dict(t="Calcula el pie con el ángulo de 60°",
  d=para("En el triángulo rectángulo del extremo izquierdo, la hipotenusa es el lado no paralelo (8) "
     "y el cateto adyacente al ángulo de 60"+DEG+" es "+v("p")+":")+
    disp(v("p")+" = 8"+CDOT+"cos 60"+DEG+" = 8"+CDOT+fr("1","2")+" = "+hl("4 u"))),
 dict(t="Arma la base mayor",
  d=disp("AD = "+v("p")+" + 6 + "+v("p")+" = 4 + 6 + 4 = "+hl("14 u"))),
],
idea="Trapecio isósceles: bajar las dos alturas siempre parte la base mayor en «pie + base menor + pie», y el pie sale con cos del ángulo de la base."),

# ─────────────────────────────── P41 ──────────────────────────────
dict(n=41, tema="Geometría", sub="Planteo con áreas", dif=2,
enun="Se tiene un rectángulo. Si a cada lado se le agrega 5 m, el área se duplica; y si se le quita "
     "2 m a cada lado, el área disminuye en 46 m². ¿Cuál es el área original?",
opts=["100 m²", "125 m²", "150 m²", "175 m²"], ans=2, dup=25,
steps=[
 dict(t="Es el mismo modelo del problema 25",
  d=para("Idéntico planteo (allí pedían el lado mayor; aquí, el área). Sean "+v("L")+" y "+v("W")+" los lados:")+
    disp("("+v("L")+"+5)("+v("W")+"+5) = 2"+v("L")+v("W")+"&nbsp;&nbsp;&nbsp;&nbsp;("+v("L")+"&minus;2)("+v("W")+"&minus;2) = "+v("L")+v("W")+" &minus; 46")),
 dict(t="La segunda condición da la suma",
  d=disp(v("L")+v("W")+" &minus; 2("+v("L")+"+"+v("W")+") + 4 = "+v("L")+v("W")+" &minus; 46"+IMPL+hl(v("L")+" + "+v("W")+" = 25"))),
 dict(t="La primera da el área",
  d=disp(v("L")+v("W")+" + 5("+v("L")+"+"+v("W")+") + 25 = 2"+v("L")+v("W")+IMPL+
         v("L")+v("W")+" = 5(25) + 25 = "+hl("150 m²"))+
    para("(Los lados son 15 y 10, como en el problema 25.)")),
],
idea="El desarrollo cancela los LW: una condición entrega L + W y la otra convierte esa suma en el área LW."),

# ─────────────────────────────── P42 ──────────────────────────────
dict(n=42, tema="Geometría", sub="Áreas y proporcionalidad", dif=3,
enun="En un triángulo ABC de área 30 cm², se prolonga BA hasta un punto M, de tal manera que "
     "3AB = AM (A entre B y M). Se prolonga BC hasta el punto P, donde 3BC = CP (C entre B y P). "
     "Hallar el área del cuadrilátero ACPM.",
opts=["60 cm²", "90 cm²", "300 cm²", "450 cm²"], ans=3, fig="fig42",
steps=[
 dict(t="Mide los lados del triángulo grande",
  d=para("Todo pasa por el vértice B. Con las prolongaciones:")+
    para("&bull; BM = BA + AM = AB + 3AB = <b>4·AB</b><br>"
         "&bull; BP = BC + CP = BC + 3BC = <b>4·BC</b>")),
 dict(t="Compara áreas con el ángulo común",
  d=para("Los triángulos ABC y MBP comparten el ángulo en B. Cuando dos triángulos comparten un ángulo, "
     "sus áreas están en proporción al producto de los lados que lo forman:")+
    disp(fr("[MBP]","[ABC]")+" = "+fr("BM"+CDOT+"BP","BA"+CDOT+"BC")+" = "+fr("4"+CDOT+"4","1"+CDOT+"1")+" = 16")+
    disp("[MBP] = 16"+CDOT+"30 = 480 cm²")),
 dict(t="Resta el triángulo original",
  d=para("El cuadrilátero ACPM es el triángulo grande sin el pequeño:")+
    disp("[ACPM] = [MBP] &minus; [ABC] = 480 &minus; 30 = "+hl("450 cm²"))),
],
idea="Triángulos con un ángulo común: [②]/[①] = producto de lados que abrazan el ángulo. El cuadrilátero pedido es «grande − pequeño»."),

# ─────────────────────────────── P43 ──────────────────────────────
dict(n=43, tema="Geometría", sub="Cevianas y áreas", dif=3,
enun="En el triángulo ABC se trazan la mediana BM y la ceviana AD, que divide al segmento BC en la "
     "relación de 2 a 3. Si el área del triángulo BPD es 8 cm², siendo P el punto de corte de AD y BM, "
     "calcular el área de ABC.",
opts=["20 cm²", "30 cm²", "50 cm²", "70 cm²"], ans=3, fig="fig43",
steps=[
 dict(t="Ubica los datos",
  d=para("D está en BC con BD : DC = 2 : 3 (tomemos BD = 2"+v("u")+", DC = 3"+v("u")+"). "
     "M es punto medio de AC. P es el cruce de AD con BM.")),
 dict(t="Encuentra en qué razón P corta a AD",
  d=para("Usamos masas (o Menelao). Asignamos masa 3 en B y masa 2 en C para que D los equilibre "
     "(3·BD = 2·DC &#10003;). Para que M sea punto medio de AC, la masa de A debe igualar la de C: masa 2 en A.")+
    para("Sobre la ceviana AD: A tiene masa 2 y D carga la masa de B + C = 5. El punto de equilibrio P cumple:")+
    disp("AP : PD = 5 : 2")),
 dict(t="Escala del triángulo BPD al triángulo BAD",
  d=para("BPD y BAD comparten la base sobre la recta AD... mejor dicho: comparten el vértice B, y sus bases "
     "PD y AD están sobre la misma recta. Sus áreas van como sus bases:")+
    disp(fr("[BPD]","[BAD]")+" = "+fr("PD","AD")+" = "+fr("2","7")+IMPL+"[BAD] = "+fr("7","2")+CDOT+"8 = 28 cm²")),
 dict(t="Escala del triángulo BAD al ABC",
  d=para("BAD y BAC comparten el vértice A y sus bases BD y BC están sobre BC:")+
    disp(fr("[BAD]","[ABC]")+" = "+fr("BD","BC")+" = "+fr("2","5")+IMPL+
         "[ABC] = "+fr("5","2")+CDOT+"28 = "+hl("70 cm²"))),
],
idea="Cadena de razones de áreas: triángulos con el mismo vértice tienen áreas proporcionales a sus bases. El punto de cruce se resuelve con masas: AP:PD = 5:2."),

# ─────────────────────────────── P44 ──────────────────────────────
dict(n=44, tema="Geometría", sub="Áreas sombreadas", dif=3,
enun="En el gráfico, el área de la región rectangular es 200. Calcula el área de la región sombreada.",
opts=["50("+PI+" &minus; 1) u²", "25("+PI+" &minus; 1) u²", "50("+PI+" &minus; 2) u²", "25("+PI+" &minus; 2) u²"], ans=0, fig="fig44",
steps=[
 dict(t="Ponle medidas al rectángulo",
  d=para("El semicírculo tiene su diámetro en la base y toca el lado superior: si su radio es "+v("r")+", "
     "el rectángulo mide 2"+v("r")+" de base y "+v("r")+" de alto.")+
    disp("2"+v("r")+CDOT+v("r")+" = 200"+IMPL+hl(v("r")+"² = 100")),
 ),
 dict(t="Identifica la región sombreada",
  d=para("Lo sombreado es el semicírculo <b>menos</b> el triángulo blanco de abajo, formado por las dos "
     "diagonales del rectángulo y la base. Las diagonales se cruzan en el centro del rectángulo, "
     "a altura "+v("r")+"/2.")),
 dict(t="Área del semicírculo",
  d=disp(fr(PI+v("r")+"²","2")+" = "+fr(PI+CDOT+"100","2")+" = 50"+PI)),
 dict(t="Área del triángulo blanco",
  d=para("Base 2"+v("r")+" y altura "+v("r")+"/2 (el punto de cruce de las diagonales):")+
    disp(fr("1","2")+CDOT+"2"+v("r")+CDOT+fr(v("r"),"2")+" = "+fr(v("r")+"²","2")+" = 50")),
 dict(t="Resta",
  d=disp("Sombreada = 50"+PI+" &minus; 50 = "+hl("50("+PI+" &minus; 1) u²"))),
],
idea="Semicírculo inscrito en rectángulo ⇒ base = 2r, altura = r. Las diagonales se cortan en el centro (altura r/2): el triángulo blanco vale r²/2."),

# ─────────────────────────────── P45 ──────────────────────────────
dict(n=45, tema="Geometría", sub="Sólidos de revolución", dif=2,
enun="Dos lados de un rectángulo miden 3 m y 4 m. Al girar el rectángulo alrededor de cada uno de "
     "dichos lados se obtienen dos cilindros. Determine la relación entre los volúmenes de dichos cilindros.",
opts=[fr("7","6"), fr("4","3"), "2", fr("16","9")], ans=1, fig="fig45",
steps=[
 dict(t="Visualiza cada giro",
  d=para("Al girar alrededor de un lado, ese lado se vuelve el <b>eje</b> (la altura) y el otro lado barre "
     "el <b>radio</b>.")+
    para("&bull; Giro alrededor del lado 3: altura 3, radio 4.<br>&bull; Giro alrededor del lado 4: altura 4, radio 3.")),
 dict(t="Calcula ambos volúmenes",
  d=disp(v("V")+"<sub>1</sub> = "+PI+CDOT+"4²"+CDOT+"3 = 48"+PI+"&nbsp;&nbsp;&nbsp;&nbsp;"+
         v("V")+"<sub>2</sub> = "+PI+CDOT+"3²"+CDOT+"4 = 36"+PI)),
 dict(t="Divide",
  d=disp(fr(v("V")+"<sub>1</sub>", v("V")+"<sub>2</sub>")+" = "+fr("48"+PI,"36"+PI)+" = "+hl(fr("4","3")))+
    para("El radio pesa más que la altura (va al cuadrado): por eso gana el cilindro «echado» sobre el lado corto.")),
],
idea="V = πr²h: el lado que hace de radio entra al cuadrado. La razón de volúmenes queda (lado mayor)/(lado menor) = 4/3."),

# ─────────────────────────────── P46 ──────────────────────────────
dict(n=46, tema="Geometría", sub="Volúmenes", dif=3,
enun="Un envase cilíndrico lleno de agua tiene radio 6 cm y altura 30 cm. Se desea vaciar el contenido "
     "en vasos con forma de tronco de cono de altura 8 cm, radio menor 2 cm y radio mayor 4 cm, de tal "
     "manera que el agua no ocupe más de las tres cuartas partes del volumen del vaso. Halle la cantidad "
     "mínima de vasos para que el envase quede completamente vacío.",
opts=["18", "19", "20", "21"], ans=2, fig="fig46",
steps=[
 dict(t="Volumen de agua disponible",
  d=disp(v("V")+"<sub>cil</sub> = "+PI+v("r")+"²"+v("h")+" = "+PI+CDOT+"6²"+CDOT+"30 = 1080"+PI+" cm³")),
 dict(t="Capacidad de cada vaso (tronco de cono)",
  d=disp(v("V")+"<sub>tronco</sub> = "+fr(PI+v("h"),"3")+"("+v("R")+"² + "+v("R")+v("r")+" + "+v("r")+"²) = "+
         fr(PI+CDOT+"8","3")+"(16 + 8 + 4) = "+fr("8"+PI,"3")+CDOT+"28 = "+fr("224"+PI,"3")+" cm³")),
 dict(t="Aplica la restricción de los ¾",
  d=para("Cada vaso solo puede recibir el 75% de su capacidad:")+
    disp(fr("3","4")+CDOT+fr("224"+PI,"3")+" = 56"+PI+" cm³ por vaso")),
 dict(t="Divide y redondea hacia arriba",
  d=disp(fr("1080"+PI,"56"+PI)+" = "+fr("1080","56")+" &asymp; 19,29")+
    para("Con 19 vasos no alcanza (queda agua); se necesita empezar un vaso más:")+
    disp("mínimo = "+hl("20 vasos"))),
],
idea="Tronco de cono: V = πh(R² + Rr + r²)/3. En problemas de «cuántos recipientes», la división casi nunca es exacta: redondea SIEMPRE hacia arriba."),

# ─────────────────────────────── P47 ──────────────────────────────
dict(n=47, tema="Geometría", sub="Sólidos inscritos", dif=1,
enun="Se inscribe un cilindro en un cubo de arista 3 cm. Hallar la relación entre el volumen del "
     "cilindro y el volumen del cubo.",
opts=[fr(PI,"4"), fr("4",PI), fr(PI,"3"), fr("3",PI)], ans=0, fig="fig47",
steps=[
 dict(t="Dimensiona el cilindro inscrito",
  d=para("El cilindro toca las cuatro caras laterales: su diámetro es la arista (3), o sea radio 3/2. "
     "Su altura es la misma arista: 3.")),
 dict(t="Calcula ambos volúmenes",
  d=disp(v("V")+"<sub>cil</sub> = "+PI+mrow("(",fr("3","2"),")²")+CDOT+"3 = "+fr("27"+PI,"4")+
         "&nbsp;&nbsp;&nbsp;&nbsp;"+v("V")+"<sub>cubo</sub> = 3³ = 27")),
 dict(t="Divide",
  d=disp(fr(v("V")+"<sub>cil</sub>", v("V")+"<sub>cubo</sub>")+" = "+fr("27"+PI+"/4","27")+" = "+hl(fr(PI,"4")))+
    para("Dato para recordar: un cilindro inscrito en cualquier cubo ocupa siempre "+PI+"/4 &asymp; 78,5% del volumen.")),
],
idea="Cilindro inscrito en cubo de arista a: radio a/2, altura a ⇒ V = πa³/4. La razón π/4 no depende de la arista."),

# ─────────────────────────────── P48 ──────────────────────────────
dict(n=48, tema="Geometría", sub="Áreas con trigonometría", dif=3,
enun="En el gráfico mostrado, calcular el área sombreada en función del radio 2 cm de la "
     "semicircunferencia y el ángulo "+THETA+" en radianes.",
opts=["2"+THETA+" &minus; tg 2"+THETA, "2"+THETA+" &minus; cos 2"+THETA,
      "2"+THETA+" &minus; sen 2"+THETA, THETA+" &minus; sen 2"+THETA], ans=2, fig="fig48",
steps=[
 dict(t="Describe la región",
  d=para("La zona rayada está entre el lado CD del rectángulo, el arco y el diámetro: es el "
     "<b>sector circular</b> de ángulo "+THETA+" al que se le quita el <b>triángulo</b> ODC.")),
 dict(t="Área del sector",
  d=para("Con "+THETA+" en radianes y radio 2:")+
    disp(v("A")+"<sub>sector</sub> = "+fr("1","2")+v("r")+"²"+THETA+" = "+fr("1","2")+CDOT+"4"+CDOT+THETA+" = 2"+THETA)),
 dict(t="Área del triángulo ODC",
  d=para("El triángulo tiene catetos OD = 2 cos "+THETA+" y DC = 2 sen "+THETA+" (proyecciones del radio OC):")+
    disp(v("A")+"<sub>&#9651;</sub> = "+fr("1","2")+CDOT+"2 cos "+THETA+CDOT+"2 sen "+THETA+" = 2 sen "+THETA+" cos "+THETA+" = sen 2"+THETA)+
    para("Usamos la identidad del ángulo doble: 2 sen "+THETA+" cos "+THETA+" = sen 2"+THETA+".")),
 dict(t="Resta",
  d=disp("Sombreada = 2"+THETA+" &minus; sen 2"+THETA+" "+hl("&#10003;"))),
],
idea="Área de sector = ½r²θ (θ en radianes). El triángulo de proyecciones aporta ½(2cosθ)(2senθ) = sen 2θ. Sombreado = sector − triángulo."),

# ─────────────────────────────── P49 ──────────────────────────────
dict(n=49, tema="Geometría", sub="Ángulos y bisectrices", dif=2,
enun="Se tienen los ángulos consecutivos AOB, BOC y COD que forman un ángulo llano. Halle la "
     "m"+ANG+"BOC si las bisectrices de los ángulos AOB y COD determinan un ángulo de 100"+DEG+".",
opts=["40"+DEG, "20"+DEG, "30"+DEG, "25"+DEG], ans=1, fig="fig49",
steps=[
 dict(t="Nombra las mitades",
  d=para("Sea m"+ANG+"AOB = 2"+v("a")+", m"+ANG+"BOC = "+v("x")+" y m"+ANG+"COD = 2"+v("c")+". "
     "Como forman un ángulo llano:")+
    disp("2"+v("a")+" + "+v("x")+" + 2"+v("c")+" = 180"+DEG)),
 dict(t="Expresa el ángulo entre bisectrices",
  d=para("La bisectriz de AOB deja "+v("a")+" a cada lado, y la de COD deja "+v("c")+". El ángulo entre "
     "las dos bisectrices atraviesa: la mitad "+v("a")+", todo "+v("x")+" y la mitad "+v("c")+":")+
    disp(v("a")+" + "+v("x")+" + "+v("c")+" = 100"+DEG)),
 dict(t="Resuelve el sistema",
  d=para("De la segunda: "+v("a")+" + "+v("c")+" = 100"+DEG+" &minus; "+v("x")+". Sustituye en la primera:")+
    disp("2(100"+DEG+" &minus; "+v("x")+") + "+v("x")+" = 180"+DEG+IMPL+"200"+DEG+" &minus; "+v("x")+" = 180"+DEG+IMPL+
         hl(v("x")+" = 20"+DEG))),
 dict(t="Verifica",
  d=para("Si "+v("x")+" = 20"+DEG+", entonces "+v("a")+" + "+v("c")+" = 80"+DEG+" y los tres ángulos suman "
     "160"+DEG+" + 20"+DEG+" = 180"+DEG+" &#10003;. Entre bisectrices: 80"+DEG+" + 20"+DEG+" = 100"+DEG+" &#10003;.")),
],
idea="Ángulo entre bisectrices de los extremos = (a + c) + x, y el llano da 2(a + c) + x. Restando: x = 2·100° − 180°.",
nota="El PDF reconstruido dice «ángulo lleno» (360°), pero con 360° no existe solución entre las alternativas; el enunciado original es con ángulo llano (180°)."),

# ─────────────────────────────── P50 ──────────────────────────────
dict(n=50, tema="Geometría", sub="Congruencia", dif=2,
enun="En un triángulo ABC se trazan las cevianas AD y BE de tal manera que AB = CD, AD = CE y "
     "m"+ANG+"BAD = m"+ANG+"DCE. Señale cuál de las siguientes afirmaciones es verdadera.",
opts=["AB + DC = AD + CE", "AB"+CDOT+"DC = AD"+CDOT+"CE", "AE + CE = BD + CD", "AB"+CDOT+"CE = AD"+CDOT+"DC"], ans=3, fig="fig50",
steps=[
 dict(t="Anota las igualdades dadas",
  d=para("Tenemos dos parejas de segmentos iguales: AB = CD y AD = CE (y un par de ángulos iguales, "
     "que garantiza que la configuración existe — triángulos ABD y CDE congruentes por LAL).")),
 dict(t="Prueba cada alternativa sustituyendo",
  d=para("La estrategia ganadora aquí es sustituir las igualdades en cada opción:")+
    para("&bull; <b>A:</b> AB + DC = AD + CE "+ARROW+" 2·AB = 2·AD ⇔ AB = AD: no tiene por qué cumplirse &#10007;<br>"
     "&bull; <b>B:</b> AB·DC = AD·CE "+ARROW+" AB² = AD² ⇔ AB = AD: tampoco &#10007;<br>"
     "&bull; <b>C:</b> AE + CE = BD + CD "+ARROW+" involucra AE y BD, que no están controlados por los datos &#10007;")),
 dict(t="Confirma la alternativa D",
  d=disp("AB"+CDOT+"CE = AB"+CDOT+"AD&nbsp;&nbsp;(porque CE = AD)")+
    disp("AD"+CDOT+"DC = AD"+CDOT+"AB&nbsp;&nbsp;(porque DC = AB)")+
    para("Ambos productos valen AB"+CDOT+"AD: son iguales <b>siempre</b>, con los datos dados. "+hl("D es verdadera")+".")),
],
idea="Cuando las alternativas son igualdades entre segmentos, sustituye los datos (AB = CD, AD = CE): la verdadera se vuelve una identidad."),

# ─────────────────────────────── P51 ──────────────────────────────
dict(n=51, tema="Geometría", sub="Superficies", dif=2,
enun="Se tiene una taza de forma semiesférica de radio 6 cm. Calcular el costo de pintar dicha taza "
     "si el cm² cuesta S/ 0,2. (Considere "+PI+" = 3,14).",
opts=["S/ 45,216", "S/ 46,116", "S/ 40,216", "S/ 48,116"], ans=0, fig="fig51",
steps=[
 dict(t="Superficie de la semiesfera",
  d=para("La superficie curva de media esfera es la mitad de 4"+PI+v("r")+"²:")+
    disp(v("S")+" = 2"+PI+v("r")+"² = 2"+CDOT+"3,14"+CDOT+"6² = 2"+CDOT+"3,14"+CDOT+"36 = 226,08 cm²")),
 dict(t="Multiplica por el precio",
  d=disp("Costo = 226,08"+TIMES+"0,2 = "+hl("S/ 45,216"))),
 dict(t="Chequeo de coherencia",
  d=para("Las alternativas están alrededor de S/ 45, consistente con pintar solo la cara curva "
     "(2"+PI+v("r")+"²). El enunciado dice «m²» por errata; con el precio por cm² el resultado "
     "coincide exactamente con la alternativa A.")),
],
idea="Semiesfera: superficie curva = 2πr². Con π = 3,14 y r = 6: 226,08 cm², y el costo sale multiplicando por la tarifa."),
]
