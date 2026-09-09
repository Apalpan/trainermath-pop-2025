"""Banco original parametrizado para práctica CEPRE.

No lee archivos ni escribe al importarse. Las 50 familias producen ocho
variantes deterministas cada una: 400 problemas con datos y verificador
recalculables. Los PDF se usan como mapa temático, nunca se copian.
"""
from __future__ import annotations

from math import comb, gcd, isqrt
from fractions import Fraction
from random import Random

AR = {"file": "Informacion/ARITMÉTICA - PRISMA 2025 (1).pdf", "page": 2, "concept": "temario visual: divisibilidad, fracciones, conteo, sucesiones y porcentajes"}
AL = {"file": "Informacion/CIENCIAS PRACTICAS/Practiquemos Semana 1 CC.pdf", "page": 4, "concept": "ecuaciones y sistemas"}
ALS = {"file": "Informacion/CIENCIAS PRACTICAS/Practiquemos semana 5 cc.pdf", "page": 2, "concept": "progresiones y sumas"}
GE = {"file": "Informacion/GEOMETRÍA - PRISMA 2025 (1).pdf", "page": 2, "concept": "temario visual de geometría plana y espacial"}
GEX = {"file": "Informacion/CIENCIAS PRACTICAS/Practiquemos semana 4 cc.pdf", "page": 9, "concept": "polígonos, ángulos, apotema y perímetros"}
PR = {"file": "Informacion/CIENCIAS PRACTICAS/CRP Hora 1 Semana 4 2026.7 LL.pdf", "page": 2, "concept": "conjuntos, preferencias y conteo"}

def _html(x):
    if isinstance(x, Fraction): return str(x)
    return str(x).replace("-", "−")
def _steps(*rows): return [{"t": t, "d": d} for t, d in rows]
def _opts(answer, seed):
    # options as strings avoid HTML math coupling; deterministic position rotates.
    ans = _html(answer)
    if isinstance(answer, Fraction):
        delta=Fraction(1, max(2, answer.denominator))
        raw=[answer, answer+delta, max(Fraction(0),answer-delta), answer+2*delta]
    elif isinstance(answer, int):
        spread=max(2, abs(answer)//7+1); raw=[answer,answer+spread,answer-spread,answer+2*spread]
    else: raw=[answer, "0", "1", "2"]
    out = []
    for v in raw:
        s = _html(v)
        if s not in out: out.append(s)
    bump = 3
    while len(out) < 4:
        s = _html(answer + bump * spread) if isinstance(answer, int) else str(bump)
        if s not in out: out.append(s)
        bump += 1
    Random(seed).shuffle(out)
    return out, out.index(ans)

def _p(n, tema, sub, family, dif, target, text, answer, steps, idea, hint, trap, source, kind, params):
    opts, ans = _opts(answer, n * 7919 + len(family))
    return {"n": n, "id": str(n), "tema": tema, "sub": sub, "family": family,
            "dif": dif, "target": target, "enun": text, "opts": opts, "ans": ans,
            "steps": steps, "idea": idea, "hint": hint, "trap": trap,
            "origin": "generated", "source": source, "params": params | {"kind": kind, "expected": _html(answer)}}

# Each builder uses an independent number pattern.  The corresponding validator
# recomputes the answer solely from params and kind.
def divisibility(n, i):
    a, b = 12+i, 18+2*i; l = a*b//gcd(a,b)
    return _p(n,"Aritmética","MCD y MCM","mcm_ciclos",1,35,
      f"Dos alarmas suenan cada {a} y {b} minutos. Si coinciden ahora, ¿en cuántos minutos volverán a coincidir?",l,
      _steps(("Busca el MCM",f"MCM({a},{b}) = {l}."),("Interpreta",f"La siguiente coincidencia ocurre a los {l} minutos.")),
      "Los ciclos coinciden en el mínimo común múltiplo.","Factoriza solo si no ves un múltiplo rápido.","Sumar los periodos da una coincidencia falsa.",AR,"lcm",{"a":a,"b":b})
def remainder(n,i):
    d=5+i; q=7+i; r=(2*i+1)%d; x=d*q+r
    return _p(n,"Aritmética","Divisibilidad","division_residuo",1,30,f"Al dividir {x} entre {d}, ¿cuál es el residuo?",r,_steps(("Separa múltiplos",f"{x} = {d}×{q} + {r}."),("Lee el residuo",f"El número que sobra es {r}.")),"Escribe dividendo = divisor·cociente + residuo.",f"Busca el múltiplo de {d} más cercano.","El cociente no es el residuo.",AR,"remainder",{"x":x,"d":d})
def fraction_sum(n,i):
    a,b,c=2+i,3+i,5+i; val=Fraction(a,b)+Fraction(1,c)
    return _p(n,"Aritmética","Fracciones","suma_fracciones",2,55,f"Calcula {a}/{b} + 1/{c}.",val,_steps(("Usa denominador común",f"{a}/{b} + 1/{c} = ({a}×{c}+{b})/({b}×{c})."),("Simplifica",f"El resultado es {_html(val)}.")),"Multiplica cruzado; no sumes denominadores.",f"El denominador común es {b}×{c}.","a/b + 1/c nunca es (a+1)/(b+c).",AR,"fraction_sum",{"a":a,"b":b,"c":c})
def percentage(n,i):
    base=400*(1+i); inc=10+(i%4)*5; disc=5+(i%3)*5; ans=Fraction(base*(100+inc)*(100-disc),10000)
    return _p(n,"Aritmética","Porcentajes","aumento_descuento",2,55,f"Un artículo cuesta S/ {base}. Aumenta {inc}% y luego se descuenta {disc}%. ¿Precio final?",ans,_steps(("Aplica el aumento",f"{base}×{100+inc}/100."),("Aplica el descuento",f"Multiplica luego por {100-disc}/100: S/ {ans}.")),"Los porcentajes sucesivos se multiplican.","Convierte cada cambio en factor.","No restes los porcentajes entre sí.",AR,"percent_chain",{"base":base,"inc":inc,"disc":disc})
def average(n,i):
    vals=[8+i,12+i,16+i,20+i]; ans=sum(vals)//4
    return _p(n,"Aritmética","Promedios","media_datos",1,35,f"Halla el promedio de {', '.join(map(str,vals))}.",ans,_steps(("Suma",f"{'+'.join(map(str,vals))} = {sum(vals)}."),("Divide",f"{sum(vals)}/4 = {ans}.")),"Promedio = suma entre cantidad.","Suma primero en parejas.","Dividir entre el mayor dato es un error común.",AR,"average",{"values":vals})
def mixture(n,i):
    p=20+5*(i%5); q=50+5*(i%4); a=2+i; b=3+i; ans=Fraction(p*a+q*b,a+b)
    return _p(n,"Aritmética","Promedios y mezclas","precio_ponderado",2,65,f"Se mezclan {a} kg a S/ {p} por kg con {b} kg a S/ {q} por kg. ¿Precio medio por kg?",ans,_steps(("Costo total",f"{a}×{p}+{b}×{q} = {a*p+b*q}."),("Peso total",f"Divide entre {a+b}: {ans}.")),"En mezclas, pondera cada precio por su cantidad.","Calcula costos, luego divide por kilos.","No promedies precios sin considerar cantidades.",AR,"mixture",{"p":p,"q":q,"a":a,"b":b})
def simple_interest(n,i):
    cap=500+100*i; rate=2+i%4; months=3+i; ans=cap*rate*months//100
    return _p(n,"Aritmética","Interés simple","interes_mensual",2,60,f"Se presta S/ {cap} al {rate}% mensual simple durante {months} meses. ¿Interés generado?",ans,_steps(("Formula",f"I=C·r·t/100."),("Sustituye",f"I={cap}×{rate}×{months}/100 = {ans}.")),"En interés simple no capitalizas el interés.","Identifica que la tasa es mensual.","No uses interés compuesto si no lo indican.",AR,"simple_interest",{"cap":cap,"rate":rate,"months":months})
def rule_three(n,i):
    workers=3+i; nw=workers+2; days=nw*(2+i); ans=Fraction(workers*days,nw)
    return _p(n,"Aritmética","Regla de tres","trabajo_inverso",2,60,f"{workers} operarios terminan una tarea en {days} días. Al trabajar {nw} operarios al mismo ritmo, ¿en cuántos días la terminan?",ans,_steps(("Reconoce relación inversa",f"operarios×días = {workers}×{days}."),("Despeja",f"días = {workers*days}/{nw} = {ans}.")),"Para la misma obra, más operarios implica menos días.","Conserva constante operarios·días.","No hagas proporción directa.",AR,"inverse_work",{"workers":workers,"days":days,"nw":nw})
def digits(n,i):
    lo=100+i*10; hi=lo+49; ans=sum(len(str(k)) for k in range(lo,hi+1))
    return _p(n,"Aritmética","Numeración","conteo_cifras",1,45,f"¿Cuántas cifras se escriben al numerar del {lo} al {hi}?",ans,_steps(("Cuenta números",f"Hay {hi-lo+1} números."),("Cada uno tiene 3 cifras",f"{hi-lo+1}×3 = {ans}.")),"Clasifica por cantidad de cifras antes de contar.","Todos están entre 100 y 999.","No cuentes los extremos dos veces.",AR,"digit_count",{"lo":lo,"hi":hi})
def base_conversion(n,i):
    a=20+3*i; b=3+i%4; digits=[]; x=a
    while x: digits.append(x%b); x//=b
    ans="".join(str(d) for d in digits[::-1])
    p = _p(n,"Aritmética","Sistemas de numeración","decimal_a_base",2,70,f"Escribe {a} en base {b}.",ans,_steps(("Divide sucesivamente",f"Divide por {b} y guarda residuos."),("Lee al revés",f"Los residuos producen {ans}<sub>{b}</sub>.")),"Los residuos se leen desde el último al primero.","Haz divisiones sucesivas.","Leer residuos en orden directo invierte el número.",AR,"base_convert",{"a":a,"b":b})
    choices=[]
    for number in (a,a-1,a+1,a+b):
        ds=[]
        while number:
            ds.append(str(number%b)); number//=b
        choices.append(''.join(reversed(ds)))
    Random(n).shuffle(choices); p['opts']=choices; p['ans']=choices.index(ans)
    return p
def prime_count(n,i):
    lo=10+i; hi=lo+18
    def prime(x): return x>1 and all(x%d for d in range(2,isqrt(x)+1))
    ans=sum(prime(x) for x in range(lo,hi+1))
    return _p(n,"Aritmética","Números primos","conteo_primos",2,75,f"¿Cuántos números primos hay desde {lo} hasta {hi}, inclusive?",ans,_steps(("Descarta compuestos",f"Revisa divisibilidad por primos hasta √{hi}."),("Cuenta",f"En el intervalo aparecen {ans} primos.")),"Para probar primalidad basta revisar hasta la raíz.","Tacha múltiplos de 2, 3 y 5 primero.","El 1 no es primo.",AR,"prime_count",{"lo":lo,"hi":hi})
def permutations(n,i):
    total=5+i; take=2+i%2; ans=1
    for x in range(total-take+1,total+1): ans*=x
    return _p(n,"Aritmética","Análisis combinatorio","ordenamientos",2,75,f"¿De cuántas formas se puede ordenar una fila de {take} estudiantes elegidos entre {total}, sin repetición?",ans,_steps(("Elige por posiciones",f"{total} opciones para la primera, luego {total-1}, …"),("Multiplica",f"P({total},{take}) = {ans}.")),"Si importa el orden, usa permutaciones.","Cuenta una posición a la vez.","No uses combinaciones: aquí el orden cambia la fila.",AR,"permutation",{"total":total,"take":take})
def combinations(n,i):
    total=6+i; take=2+i%2; ans=comb(total,take)
    return _p(n,"Aritmética","Análisis combinatorio","comites",2,80,f"De {total} postulantes se forma un comité de {take}. ¿Cuántos comités distintos hay?",ans,_steps(("No importa el orden",f"Se usa C({total},{take})."),("Calcula",f"C({total},{take}) = {ans}.")),"Un comité no cambia si intercambias personas.","Decide primero si el orden importa.","Contar filas sobrecuenta cada comité.",AR,"combination",{"total":total,"take":take})
def inclusion(n,i):
    a=18+i; b=14+i; both=5+i%4; ans=a+b-both
    return _p(n,"Aritmética","Conjuntos","union_dos_conjuntos",2,65,f"En un aula, {a} prefieren A, {b} prefieren B y {both} prefieren ambos. ¿Cuántos prefieren al menos uno?",ans,_steps(("Suma inicial",f"{a}+{b} cuenta a los de ambos dos veces."),("Corrige",f"{a}+{b}−{both} = {ans}.")),"En la unión, resta la intersección una vez.","Dibuja dos círculos si dudas.","Sumar sin restar duplica a quienes están en ambos.",PR,"inclusion",{"a":a,"b":b,"both":both})
def pa_term(n,i):
    first=4+i; d=2+i%4; k=8+i; ans=first+(k-1)*d
    return _p(n,"Álgebra","Progresión aritmética","pa_termino",1,40,f"En la PA {first}, {first+d}, …, halla el término {k}.",ans,_steps(("Formula",f"a<sub>n</sub>=a<sub>1</sub>+(n−1)d."),("Sustituye",f"{first}+({k}−1)×{d} = {ans}.")),"En PA se avanza por diferencias iguales.","Cuenta n−1 saltos.","Usar n saltos agrega una razón de más.",ALS,"pa_term",{"first":first,"d":d,"k":k})
def pa_sum(n,i):
    first=3+i; d=2+i%3; k=6+i; last=first+(k-1)*d; ans=k*(first+last)//2
    return _p(n,"Álgebra","Progresión aritmética","pa_suma",2,70,f"Calcula la suma de los primeros {k} términos de la PA {first}, {first+d}, ….",ans,_steps(("Obtén el último",f"a<sub>{k}</sub> = {last}."),("Promedio de extremos",f"S={k}({first}+{last})/2 = {ans}.")),"Suma de PA = cantidad × promedio de extremos.","Halla el último antes de sumar.","No multipliques el primer término por n.",ALS,"pa_sum",{"first":first,"d":d,"k":k})
def pg_term(n,i):
    first=2+i%3; r=2; k=5+i%4; ans=first*r**(k-1)
    return _p(n,"Álgebra","Progresión geométrica","pg_termino",1,40,f"En la PG {first}, {first*r}, …, halla el término {k}.",ans,_steps(("Formula",f"a<sub>n</sub>=a<sub>1</sub>r<sup>n−1</sup>."),("Sustituye",f"{first}×2<sup>{k-1}</sup> = {ans}.")),"En PG se multiplica siempre por la razón.","Cuenta los exponentes desde cero.","No sumes la razón como en PA.",ALS,"pg_term",{"first":first,"r":r,"k":k})
def pg_sum(n,i):
    first=1+i; r=2; k=5+i%3; ans=first*(r**k-1)//(r-1)
    return _p(n,"Álgebra","Progresión geométrica","pg_suma",2,75,f"Calcula la suma de los primeros {k} términos de la PG {first}, {first*r}, ….",ans,_steps(("Formula",f"S=a(r<sup>n</sup>−1)/(r−1)."),("Sustituye",f"{first}(2<sup>{k}</sup>−1) = {ans}.")),"Memoriza la suma de una PG de razón 2.","Evalúa primero la potencia.","No uses la fórmula de PA.",ALS,"pg_sum",{"first":first,"r":r,"k":k})
def linear(n,i):
    a=2+i%5; x=3+i; b=5+i%4; ans=x; c=a*x+b
    return _p(n,"Álgebra","Ecuaciones","ecuacion_lineal",1,35,f"Resuelve {a}x + {b} = {c}.",ans,_steps(("Aísla",f"{a}x = {c}−{b} = {c-b}."),("Divide",f"x = {c-b}/{a} = {ans}.")),"Deshaz suma y multiplicación en orden inverso.","Pasa primero la constante.","Cambiar signo sin ambos lados desequilibra la ecuación.",AL,"linear",{"a":a,"b":b,"c":c})
def system(n,i):
    x=2+i; y=3+i%4; a=1+i%3; b=2+i%3; c=a*x+b*y; d=x+y
    return _p(n,"Álgebra","Sistemas","sistema_suma",2,70,f"Si x+y={d} y {a}x+{b}y={c}, halla x.",x,_steps(("Sustituye",f"y={d}−x."),("Resuelve",f"{a}x+{b}({d}−x)={c}, por tanto x={x}.")),"Una ecuación simple permite sustitución inmediata.","Despeja la variable con coeficiente 1.","No olvides distribuir b en el paréntesis.",AL,"system",{"a":a,"b":b,"d":d,"c":c})
def quadratic(n,i):
    r1=2+i%4; r2=5+i%3; s=r1+r2; prod=r1*r2
    return _p(n,"Álgebra","Ecuaciones cuadráticas","factorizacion_raiz",2,70,f"Resuelve x² − {s}x + {prod}=0. Da la raíz menor.",min(r1,r2),_steps(("Busca dos números",f"Suman {s} y multiplican {prod}: {r1} y {r2}."),("Factoriza",f"(x−{r1})(x−{r2})=0; la menor es {min(r1,r2)}.")),"En x²−Sx+P busca suma S y producto P.","Prueba pares de factores de P.","No cambies el signo de las raíces.",AL,"quadratic",{"s":s,"prod":prod})
def exponent(n,i):
    base,a,b=((2,3,2),(3,2,1),(5,2,1),(2,4,2),(3,3,2),(2,5,3),(5,2,2),(3,2,2))[i%8]; ans=base**(a+b)
    return _p(n,"Álgebra","Potenciación","producto_potencias",1,35,f"Calcula {base}<sup>{a}</sup> · {base}<sup>{b}</sup>.",ans,_steps(("Misma base",f"Se suman exponentes: {a}+{b}={a+b}."),("Evalúa",f"{base}<sup>{a+b}</sup>={ans}.")),"Al multiplicar potencias de igual base, suma exponentes.","Conserva la base.","No multipliques los exponentes.",AL,"exponent_product",{"base":base,"a":a,"b":b})
def polynomial_value(n,i):
    x=2+i%4; a=2+i%3; b=3+i; c=4+i%3; ans=a*x*x-b*x+c
    return _p(n,"Álgebra","Polinomios","evaluacion_polinomio",1,45,f"Evalúa P(x)={a}x²−{b}x+{c} para x={x}.",ans,_steps(("Sustituye",f"P({x})={a}({x})²−{b}({x})+{c}."),("Opera",f"P({x})={ans}.")),"Sustituye con paréntesis para proteger signos.","Calcula la potencia antes de multiplicar.","No olvides que −b·x es negativo.",AL,"polynomial_value",{"x":x,"a":a,"b":b,"c":c})
def rectangle(n,i):
    a=6+i; b=4+i%5; ans=a*b
    return _p(n,"Geometría","Áreas","area_rectangulo",1,30,f"Un rectángulo mide {a} cm por {b} cm. ¿Cuál es su área?",ans,_steps(("Formula",f"A=base×altura."),("Calcula",f"A={a}×{b}={ans} cm².")),"Área de rectángulo: base por altura.","Identifica las dos dimensiones perpendiculares.","No sumes lados: eso sería perímetro.",GE,"rectangle_area",{"a":a,"b":b})
def triangle(n,i):
    b=8+2*i; h=5+i; ans=b*h//2
    return _p(n,"Geometría","Áreas","area_triangulo",1,35,f"Un triángulo tiene base {b} cm y altura {h} cm. Halla su área.",ans,_steps(("Formula",f"A=base×altura/2."),("Calcula",f"{b}×{h}/2={ans} cm².")),"Todo triángulo es la mitad del paralelogramo de igual base y altura.","Multiplica y divide entre dos.","No olvides el /2.",GE,"triangle_area",{"b":b,"h":h})
def pythagoras(n,i):
    a=3+i; b=4+i; ans=isqrt(a*a+b*b)
    # choose triples only? this may not sqrt. use scale classic
    k=1+i; a,b,ans=3*k,4*k,5*k
    return _p(n,"Geometría","Triángulos rectángulos","pitagoras",2,55,f"Los catetos de un triángulo rectángulo miden {a} y {b} cm. Halla la hipotenusa.",ans,_steps(("Teorema",f"c²={a}²+{b}²."),("Raíz",f"c²={ans*ans}; c={ans}.")),"Reconoce triples 3-4-5 y sus múltiplos.","Cuadra los catetos antes de sumar.","No sumes catetos directamente.",GE,"pythagoras",{"a":a,"b":b})
def polygon_angles(n,i):
    sides=5+i; ans=(sides-2)*180
    return _p(n,"Geometría","Polígonos","suma_angulos",1,40,f"¿Cuánto suman los ángulos internos de un polígono de {sides} lados?",ans,_steps(("Triangula",f"Desde un vértice se forman {sides-2} triángulos."),("Suma",f"{sides-2}×180°={ans}°.")),"Un n-gono se divide en n−2 triángulos.","Resta 2 al número de lados.","No uses 360°, que es la suma de exteriores.",GEX,"polygon_sum",{"sides":sides})
def regular_polygon(n,i):
    sides=(5,6,8,9,10,12,15,18)[i%8]; ans=Fraction((sides-2)*180,sides)
    return _p(n,"Geometría","Polígonos","angulo_regular",2,60,f"Halla cada ángulo interno de un polígono regular de {sides} lados.",ans,_steps(("Suma interna",f"({sides}−2)×180°={((sides-2)*180)}°."),("Reparte",f"Divide entre {sides}: {ans}°.")),"En un polígono regular todos los ángulos son iguales.","Obtén suma total y divide por n.","No confundas interno con exterior.",GEX,"regular_angle",{"sides":sides})
def circle(n,i):
    r=3+i; ans=2*r
    return _p(n,"Geometría","Circunferencia","diametro_radio",1,30,f"Una circunferencia tiene radio {r} cm. ¿Cuál es su diámetro?",ans,_steps(("Relación",f"d=2r."),("Calcula",f"d=2×{r}={ans} cm.")),"El diámetro contiene dos radios.","Duplica el radio.","No uses π: no piden longitud.",GE,"diameter",{"r":r})
def prism(n,i):
    a=3+i; b=4+i%4; h=5+i%3; ans=a*b*h
    return _p(n,"Geometría","Sólidos","volumen_prisma",2,60,f"Un prisma rectangular mide {a} cm, {b} cm y {h} cm. Halla su volumen.",ans,_steps(("Área de base",f"{a}×{b}={a*b}."),("Multiplica altura",f"V={a*b}×{h}={ans} cm³.")),"Volumen de prisma = área de base por altura.","Primero halla el área rectangular de la base.","No respondas con cm²: el volumen usa cm³.",GE,"prism_volume",{"a":a,"b":b,"h":h})
def probability(n,i):
    good=2+i%5; total=8+i; from fractions import Fraction as F
    val=F(good,total); ans=f"{val.numerator}/{val.denominator}"
    values=list(dict.fromkeys([val,F(total-good,total),F(good-1,total),F(good,total+1),F(good+1,total)]))[:4]
    opts=[str(v) for v in values]; ans=str(val); Random(n).shuffle(opts)
    p=_p(n,"Probabilidad","Probabilidad simple","casos_favorables",1,45,f"Una bolsa tiene {good} fichas verdes y {total-good} azules. Se extrae una al azar. ¿P(verde)?",ans,_steps(("Casos favorables",f"Hay {good} verdes de {total} fichas."),("Forma razón",f"P={good}/{total}={ans}.")),"Probabilidad simple = favorables / posibles.","Cuenta total incluyendo ambos colores.","No uses solo las fichas que no sirven.",PR,"probability",{"good":good,"total":total})
    p["opts"],p["ans"]=opts,opts.index(ans); return p
def mean_dataset(n,i):
    vals=[4+i,6+i,8+i,10+i,12+i]; ans=sum(vals)//len(vals)
    return _p(n,"Estadística","Media","media_tabla",1,40,f"Calcula la media de los datos: {', '.join(map(str,vals))}.",ans,_steps(("Suma datos",f"La suma es {sum(vals)}."),("Divide entre 5",f"Media={sum(vals)}/5={ans}.")),"La media usa todos los datos por igual.","Agrupa extremos para sumar mentalmente.","No tomes el valor central: eso sería mediana.",PR,"mean",{"values":vals})
def median(n,i):
    vals=[3+i,9+i,5+i,1+i,7+i]; ans=5+i
    return _p(n,"Estadística","Mediana","mediana_ordenada",1,40,f"Halla la mediana de: {', '.join(map(str,vals))}.",ans,_steps(("Ordena",f"{sorted(vals)}."),("Ubica centro",f"El tercer dato es {ans}.")),"La mediana exige ordenar antes.","Con 5 datos, busca el tercero ordenado.","No promedies si hay cantidad impar.",PR,"median",{"values":vals})
def mode(n,i):
    a=2+i; vals=[a,a,a, a+1,a+1,a+2]; ans=a
    return _p(n,"Estadística","Moda","moda_frecuencia",1,30,f"Halla la moda de: {', '.join(map(str,vals))}.",ans,_steps(("Cuenta frecuencias",f"{a} aparece 3 veces."),("Elige mayor frecuencia",f"La moda es {ans}.")),"Moda es el valor más repetido.","Haz marcas rápidas por cada repetición.","No confundas moda con promedio.",PR,"mode",{"values":vals})
def arithmetic_sequence(n,i):
    a=5+i; d=3+i%3; k=7+i%3; ans=a+(k-1)*d
    return _p(n,"Aritmética","Razonamiento numérico","patron_aditivo",1,35,f"Completa la sucesión {a}, {a+d}, {a+2*d}, …: ¿cuál es el término {k}?",ans,_steps(("Detecta patrón",f"Se suma {d} cada vez."),("Avanza",f"Tras {k-1} saltos: {ans}.")),"Una diferencia constante señala patrón aditivo.","Mira la resta entre términos consecutivos.","No multipliques si la diferencia es constante.",AR,"sequence_add",{"a":a,"d":d,"k":k})
def geometric_sequence(n,i):
    a=2+i; k=6+i%3; ans=a*2**(k-1)
    return _p(n,"Aritmética","Razonamiento numérico","patron_multiplicativo",2,50,f"Completa la sucesión {a}, {a*2}, {a*4}, …: ¿cuál es el término {k}?",ans,_steps(("Detecta razón",f"Cada término se duplica."),("Aplica potencia",f"{a}×2<sup>{k-1}</sup>={ans}.")),"Una razón constante señala patrón multiplicativo.","Divide términos consecutivos.","No sumes 2; aquí se multiplica por 2.",AR,"sequence_mul",{"a":a,"k":k})

def inverse_discount(n,i):
    original=200+100*i; disc=(10,20,25,40)[i%4]; sale=Fraction(original*(100-disc),100)
    return _p(n,"Aritmética","Porcentajes","precio_antes_descuento",2,65,f"Tras un descuento de {disc}%, un producto cuesta S/ {_html(sale)}. ¿Cuál era su precio original?",original,_steps(("Factor de descuento",f"El precio final representa {100-disc}% del original."),("Invierte",f"Original = {_html(sale)}×100/{100-disc} = {original}.")),"Para deshacer un descuento, divide entre el factor restante.",f"El {disc}% se aplica al precio inicial.",f"Sumar {disc}% al precio final no recupera el original.",AR,"inverse_discount",{"sale":sale,"disc":disc})
def area_percentage(n,i):
    side=10+2*i; pct=(5,10,15,20,25,30,40,50)[i%8]; new=Fraction(side*(100+pct),100); ratio=Fraction(new*new-side*side,side*side)*100
    return _p(n,"Geometría","Áreas y porcentajes","cambio_area_cuadrado",3,90,f"El lado de un cuadrado aumenta {pct}%. ¿En qué porcentaje aumenta su área?",ratio,_steps(("Cambia el lado",f"El factor lineal es {100+pct}/100."),("Cuadra el factor",f"El área cambia en ({100+pct}/100)²−1 = {_html(ratio)}%.")),"El área depende del cuadrado del lado.","Convierte primero el aumento en factor.","El área no aumenta el mismo porcentaje que el lado.",ALS,"area_change",{"pct":pct})
def gcd_groups(n,i):
    g=4+i; a=g*5; b=g*7
    return _p(n,"Aritmética","MCD","agrupacion_maxima",2,55,f"Se tienen {a} lápices rojos y {b} azules. Se arman el máximo número de grupos idénticos sin sobrantes. ¿Cuántos grupos?",g,_steps(("Traduce",f"El número de grupos debe dividir a {a} y a {b}."),("Calcula MCD",f"MCD({a},{b}) = {g}.")),"Máximos grupos iguales sin sobra significa MCD.","Busca el mayor divisor común.","El MCM sirve para coincidencias, no para agrupación.",AR,"gcd",{"a":a,"b":b})
def congruent_remainders(n,i):
    d1=3+i%3; d2=5+i%4; r=1+i%min(d1-1,3); x=d1*d2//gcd(d1,d2)+r
    return _p(n,"Aritmética","Divisibilidad","resto_comun",3,90,f"¿Cuál es el menor número mayor que {r} que deja residuo {r} al dividirse entre {d1} y entre {d2}?",x,_steps(("Resta el residuo",f"N−{r} debe ser múltiplo de {d1} y {d2}."),("Usa MCM",f"MCM({d1},{d2})+{r} = {x}.")),"Si el residuo es igual, réstalo antes de usar MCM.",f"Trabaja con N−{r}.","Usar el MCD no garantiza ambos residuos.",AR,"common_remainder",{"d1":d1,"d2":d2,"r":r})
def near_hundred(n,i):
    a=100-(3+i); b=100+(4+i); ans=a*b
    return _p(n,"Aritmética","Cálculo rápido","producto_cerca_100",2,35,f"Calcula mentalmente {a}×{b}.",ans,_steps(("Descompón alrededor de 100",f"({100-(3+i)})({100+(4+i)}) = 10000+100−({3+i}×{4+i})."),("Opera",f"El producto es {ans}.")),"Cerca de 100, reescribe como (100−a)(100+b).","Multiplica las desviaciones pequeñas.","No supongas que las desviaciones son iguales.",AR,"near_hundred",{"a":a,"b":b})
def difference_squares(n,i):
    a=12+i; b=5+i%4; ans=a*a-b*b
    return _p(n,"Álgebra","Productos notables","diferencia_cuadrados",2,40,f"Calcula {a}²−{b}² sin desarrollar ambos cuadrados.",ans,_steps(("Factoriza",f"a²−b²=(a−b)(a+b)."),("Aplica",f"({a}−{b})({a}+{b}) = {ans}.")),"La diferencia de cuadrados se convierte en producto de suma por diferencia.","Resta y suma los números primero.","No confundas a²−b² con (a−b)².",AL,"difference_squares",{"a":a,"b":b})
def fraction_remaining(n,i):
    used=(Fraction(1,3),Fraction(2,5),Fraction(3,8),Fraction(5,12),Fraction(7,10),Fraction(4,7),Fraction(5,9),Fraction(7,12))[i%8]; ans=1-used
    return _p(n,"Aritmética","Fracciones","parte_restante",2,55,f"Brenda resolvió {_html(used)} de una práctica. ¿Qué fracción falta resolver?",ans,_steps(("Representa el total",f"El total es 1."),("Resta",f"1−{_html(used)} = {_html(ans)}.")),"La parte restante es total menos parte usada.","Escribe 1 con el mismo denominador.","No restes numeradores sin ajustar denominador.",AR,"fraction_remaining",{"used":used})
def tank_combined(n,i):
    a=6+i; b=12+2*i; ans=Fraction(a*b,a+b)
    return _p(n,"Aritmética","Razones y trabajo","tanque_dos_llaves",3,90,f"Una llave llena un tanque en {a} h y otra en {b} h. Abiertas juntas, ¿en cuántas horas se llena?",ans,_steps(("Suma tasas",f"Tasa conjunta = 1/{a}+1/{b}."),("Invierte",f"Tiempo = 1/(1/{a}+1/{b}) = {_html(ans)} h.")),"En trabajo conjunto se suman tasas, no tiempos.","Piensa en fracción de tanque por hora.",f"El tiempo conjunto debe ser menor que {a} h.",AR,"combined_rate",{"a":a,"b":b})
def age_equation(n,i):
    now=12+i; future=4+i%3; mult=2+i%2; parent=mult*(now+future)-future
    return _p(n,"Álgebra","Ecuaciones","edades_futuro",2,70,f"Dentro de {future} años, la edad de Ana será la {mult}ª parte de la edad de su madre. Ana tiene {now} años hoy. ¿Edad actual de la madre?",parent,_steps(("Lleva ambas edades al futuro",f"Ana: {now}+{future}; madre: M+{future}."),("Plantea",f"M+{future}={mult}({now}+{future}); M={parent}.")),"Alinea las edades en el mismo momento temporal.","Usa M para la edad actual desconocida.","No multipliques la edad actual de Ana si la relación es futura.",AL,"age_equation",{"now":now,"future":future,"mult":mult})
def purchase_system(n,i):
    x=2+i%4; y=3+i%3; p=4+i%3; q=7+i%4; total=x*p+y*q; count=x+y
    return _p(n,"Álgebra","Sistemas","compras_dos_precios",2,75,f"En una compra hay {count} artículos: unos cuestan S/ {p} y otros S/ {q}. Se paga S/ {total}. ¿Cuántos cuestan S/ {p}?",x,_steps(("Define",f"u+v={count}; {p}u+{q}v={total}."),("Sustituye",f"v={count}−u; al resolver, u={x}.")),"Usa cantidad total y costo total como dos ecuaciones.","Despeja una variable de la ecuación simple.","No divides el total entre un único precio.",AL,"purchase_system",{"count":count,"p":p,"q":q,"total":total})
def similarity_area(n,i):
    small=20+5*i; factor=2+i%3; ans=small*factor*factor
    return _p(n,"Geometría","Semejanza","areas_semejantes",3,85,f"Dos triángulos semejantes tienen razón de semejanza {factor}. Si el menor tiene área {small} cm², ¿área del mayor?",ans,_steps(("Cuadra la razón",f"Las áreas cambian por {factor}²."),("Multiplica",f"{small}×{factor}² = {ans} cm².")),"En figuras semejantes, áreas usan el cuadrado de la razón.","Distingue longitud de área.",f"Multiplicar el área solo por {factor} es insuficiente.",GE,"similarity_area",{"small":small,"factor":factor})
def diagonals(n,i):
    sides=5+i; ans=sides*(sides-3)//2
    return _p(n,"Geometría","Polígonos","diagonales_poligono",2,60,f"¿Cuántas diagonales tiene un polígono de {sides} lados?",ans,_steps(("Desde cada vértice",f"Salen {sides-3} diagonales."),("Corrige duplicación",f"{sides}({sides-3})/2 = {ans}.")),"Cada diagonal se cuenta desde dos vértices; divide entre 2.","No conectes un vértice consigo mismo ni con vecinos.","No olvides dividir entre 2.",GEX,"diagonals",{"sides":sides})
def without_replacement(n,i):
    red=3+i%4; blue=4+i%3; ans=Fraction(red,red+blue)*Fraction(red-1,red+blue-1)
    return _p(n,"Probabilidad","Sin reemplazo","dos_fichas_rojas",3,85,f"Una bolsa tiene {red} rojas y {blue} azules. Se extraen dos sin reemplazo. ¿P(ambas rojas)?",ans,_steps(("Primera extracción",f"P(roja)={red}/{red+blue}."),("Actualiza",f"Luego quedan {red-1} rojas de {red+blue-1}; producto = {_html(ans)}.")),"Sin reemplazo cambia el total de la segunda extracción.","Actualiza numerador y denominador.","No repitas la primera fracción en la segunda extracción.",PR,"without_replacement",{"red":red,"blue":blue})
def weighted_mean(n,i):
    a=12+i; b=18+i; wa=2+i%3; wb=3+i%3; ans=Fraction(a*wa+b*wb,wa+wb)
    return _p(n,"Estadística","Media ponderada","promedio_ponderado",3,80,f"Una evaluación vale {wa} partes y se obtiene {a}; otra vale {wb} partes y se obtiene {b}. ¿Promedio ponderado?",ans,_steps(("Pondera",f"Suma {a}×{wa}+{b}×{wb}."),("Divide pesos",f"({a*wa}+{b*wb})/({wa+wb}) = {_html(ans)}.")),"Cada nota pesa según sus partes, no por igual.","Multiplica nota por peso antes de sumar.","El promedio simple ignora pesos distintos.",PR,"weighted_mean",{"a":a,"b":b,"wa":wa,"wb":wb})

# 50 labelled practice families: several use a formulation variant of an
# underlying calculation so Brenda can train recognition as well as mechanics.
BUILDERS=[divisibility,remainder,fraction_sum,percentage,average,mixture,simple_interest,rule_three,digits,base_conversion,prime_count,permutations,combinations,inclusion,arithmetic_sequence,geometric_sequence,pa_term,pa_sum,pg_term,pg_sum,linear,system,quadratic,exponent,polynomial_value,rectangle,triangle,pythagoras,polygon_angles,regular_polygon,circle,prism,probability,mean_dataset,median,mode,
          inverse_discount,area_percentage,gcd_groups,congruent_remainders,near_hundred,difference_squares,fraction_remaining,tank_combined,age_equation,purchase_system,similarity_area,diagonals,without_replacement,weighted_mean]

PROBLEMS_GENERATED=[]
for family_index, builder in enumerate(BUILDERS):
    for variant in range(8):
        n=1001+family_index*8+variant
        problem=builder(n,variant)
        PROBLEMS_GENERATED.append(problem)

assert len(PROBLEMS_GENERATED)==400 and len({p["id"] for p in PROBLEMS_GENERATED})==400
