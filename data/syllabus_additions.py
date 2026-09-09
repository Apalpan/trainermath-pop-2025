"""Ninety-six original, parameterized practice problems for uncovered Prisma units.

Eight deterministic variants are produced for each of the twelve units.  The
temario is a route reference only: none of its exercises or wording is copied.
"""
from __future__ import annotations

from fractions import Fraction
from math import gcd
from random import Random

from data.generated_bank import _html, _p, _steps

SOURCE_FILE = "TEMARIO PUCP - EVALUACIÓN DEL TALENTO 2026-2.pdf"


def source(unit: str) -> dict[str, object]:
    return {"file": SOURCE_FILE, "page": 4, "concept": unit}


def set_options(problem: dict, answer: object, choices: list[object]) -> dict:
    rendered = [_html(value) for value in choices]
    expected = _html(answer)
    if len(rendered) != 4 or len(set(rendered)) != 4 or expected not in rendered:
        raise ValueError(f"Invalid alternatives for {problem['id']}")
    Random(int(problem["id"]) * 101).shuffle(rendered)
    problem["opts"] = rendered
    problem["ans"] = rendered.index(expected)
    return problem


def decimal_operaciones(n: int, i: int) -> dict:
    a, b = 125 + 17 * i, 70 + 9 * i  # hundredths: exact decimal arithmetic
    sign = "+" if i % 2 == 0 else "−"
    total = a + b if sign == "+" else a - b
    text = f"Calcula {a // 100},{a % 100:02d} {sign} {b // 100},{b % 100:02d}."
    answer = f"{total // 100},{abs(total) % 100:02d}"
    p = _p(n, "Números y Operaciones", "Número decimal", "decimal_operaciones", 1, 35, text, answer,
      _steps(("Alinea centésimos", f"Trabaja {a} y {b} centésimos."), ("Opera", f"El resultado es {answer}.")),
      "Alinea las comas; los centésimos son enteros disfrazados.", "Convierte ambos números a centésimos.", "Mover una posición la coma multiplica o divide el valor por 10.", source("Número decimal"), "decimal_cents", {"a": a, "b": b, "sign": sign})
    return set_options(p, answer, [answer, f"{(total + 10) // 100},{abs(total + 10) % 100:02d}", f"{(total - 10) // 100},{abs(total - 10) % 100:02d}", f"{(total + 100) // 100},{abs(total + 100) % 100:02d}"])


def valor_posicional(n: int, i: int) -> dict:
    digit = 2 + (i % 7); place = (10, 100, 1000, 10000)[i % 4]
    tail = 7 + (i % 3); number = digit * place + tail
    answer = digit * place
    return _p(n, "Números y Operaciones", "Sistema decimal", "valor_posicional", 1, 30,
      f"En el número {number}, ¿cuál es el valor posicional del dígito {digit}?", answer,
      _steps(("Ubica el dígito", f"El {digit} está en la posición de {place}."), ("Multiplica", f"{digit}×{place}={answer}.")),
      "El valor depende de la posición, no solo del dígito.", "Cuenta las posiciones a la derecha del dígito.", "Responder solo el dígito ignora su posición.", source("Sistema decimal"), "place_value", {"digit": digit, "place": place, "tail": tail})


def factorizacion_evaluada(n: int, i: int) -> dict:
    r1, r2 = 2 + i, 6 + (i % 3)
    s, prod = r1 + r2, r1 * r2
    answer = max(r1, r2)
    return _p(n, "Álgebra", "Factorización", "factorizacion_evaluada", 2, 55,
      f"Factoriza x²−{s}x+{prod}=0 y halla su raíz mayor.", answer,
      _steps(("Busca factores", f"Dos números suman {s} y multiplican {prod}: {r1} y {r2}."), ("Iguala factores", f"(x−{r1})(x−{r2})=0; la mayor raíz es {answer}.")),
      "En un trinomio monico, suma y producto revelan los binomios.", f"Busca un par de factores de {prod}.", "No cambies el signo: las raíces son positivas aquí.", source("Factorización"), "factor_root", {"sum": s, "product": prod})


def funcion_aplicada(n: int, i: int) -> dict:
    fixed, rate, units = 8 + i, 3 + (i % 4), 4 + i
    answer = fixed + rate * units
    return _p(n, "Álgebra", "Aplicaciones de funciones", "funcion_aplicada", 1, 40,
      f"Un servicio cobra S/ {fixed} fijos más S/ {rate} por cada hora. ¿Cuánto cuestan {units} horas?", answer,
      _steps(("Modela", f"C(h)={fixed}+{rate}h."), ("Evalúa", f"C({units})={fixed}+{rate}×{units}={answer}.")),
      "Una tarifa fija se suma una vez; la variable se multiplica.", "Separa cuota fija y tarifa por hora.", "No multipliques la cuota fija por las horas.", source("Aplicaciones de funciones"), "affine_cost", {"fixed": fixed, "rate": rate, "units": units})


def programacion_lineal(n: int, i: int) -> dict:
    total, cap_x, px, py = 10 + i, 3 + (i % 4), 9 + i, 3 + (i % 3)
    x, y = cap_x, total - cap_x
    answer = px * x + py * y
    return _p(n, "Álgebra", "Programación lineal", "programacion_lineal", 3, 90,
      f"Una feria vende x e y. Se cumple x+y≤{total}, x≤{cap_x}, x,y≥0. Cada x deja S/ {px} y cada y S/ {py}. ¿Cuál es la ganancia máxima?", answer,
      _steps(("Compara aportes", f"Como {px}>{py}, conviene llevar x al máximo: x={cap_x}."), ("Completa capacidad", f"y={total-cap_x}; ganancia={px}×{x}+{py}×{y}={answer}.")),
      "Con coeficiente mayor, llena primero esa variable si las restricciones lo permiten.", "Prueba el vértice x máximo y la capacidad total.", "No uses x=total: viola x≤límite.", source("Programación lineal"), "linear_program", {"total": total, "cap_x": cap_x, "px": px, "py": py})


def inecuacion_cuadratica(n: int, i: int) -> dict:
    a, b = 1 + i, 5 + i + (i % 3)
    answer = b - a + 1
    return _p(n, "Álgebra", "Inecuaciones de segundo grado", "inecuacion_cuadratica", 3, 80,
      f"¿Cuántos enteros x satisfacen (x−{a})(x−{b})≤0?", answer,
      _steps(("Ubica ceros", f"Las raíces son {a} y {b}."), ("Lee el intervalo", f"Entre ellas, inclusive, hay {b}−{a}+1={answer} enteros.")),
      "Una parábola con coeficiente positivo es no positiva entre sus raíces.", "Incluye ambos extremos por el signo ≤.", "Excluir las raíces cambia el conteo.", source("Inecuaciones de segundo grado"), "quadratic_inequality_count", {"a": a, "b": b})


def valor_absoluto(n: int, i: int) -> dict:
    center, distance = 4 + i, 2 + (i % 4)
    answer = 2 * center
    return _p(n, "Álgebra", "Valor absoluto", "valor_absoluto", 2, 50,
      f"Si |x−{center}|={distance}, halla la suma de las dos soluciones.", answer,
      _steps(("Abre dos casos", f"x={center}+{distance} o x={center}−{distance}."), ("Suma", f"Las dos soluciones suman {answer}.")),
      "La distancia a un centro genera dos puntos simétricos.", "Escribe centro más y menos distancia.", "Resolver solo el caso positivo pierde una solución.", source("Valor absoluto"), "absolute_sum", {"center": center, "distance": distance})


def triangulo_notable(n: int, i: int) -> dict:
    k = 2 + i
    if i % 2 == 0:
        answer = f"{2*k}√2"
        prompt = f"En un triángulo 45°-45°-90° cada cateto mide {2*k}. ¿Cuál es su hipotenusa?"
        kind, params = "notable_45_hyp", {"leg": 2 * k}
    else:
        answer = str(2 * k)
        prompt = f"En un triángulo 30°-60°-90° el cateto menor mide {k}. ¿Cuál es la hipotenusa?"
        kind, params = "notable_30_hyp", {"short": k}
    p = _p(n, "Geometría", "Triángulos rectángulos notables", "triangulo_notable", 2, 55, prompt, answer,
      _steps(("Reconoce la razón", "45-45-90 usa 1:1:√2; 30-60-90 usa 1:√3:2."), ("Escala", f"La longitud solicitada es {answer}.")),
      "Memoriza razones, no dibujes Pitágoras desde cero.", "Identifica primero el ángulo especial.", "Confundir cateto menor con mayor intercambia √3 y 2.", source("Triángulos rectángulos notables"), kind, params)
    return set_options(p, answer, [answer, f"{2*k}√3", str(k), f"{k}√2"])


def grados_radianes(n: int, i: int) -> dict:
    degree, fraction = ((30,"π/6"),(45,"π/4"),(60,"π/3"),(90,"π/2"),(120,"2π/3"),(135,"3π/4"),(150,"5π/6"),(180,"π"))[i]
    p = _p(n, "Trigonometría", "Sistemas de medidas angulares", "grados_radianes", 1, 35,
      f"Expresa {degree}° en radianes.", fraction,
      _steps(("Usa equivalencia", "180° equivale a π radianes."), ("Convierte", f"{degree}°={fraction}.")),
      "Convierte grados multiplicando por π/180.", f"Simplifica {degree}/180.", "Usar π/360 deja la mitad del valor.", source("Sistemas de medidas angulares"), "degree_radian", {"degree": degree, "answer": fraction})
    alternatives = ["π/6","π/4","π/3","π/2","2π/3","3π/4","5π/6","π"]
    return set_options(p, fraction, [fraction] + [value for value in alternatives if value != fraction][:3])


def reduccion_cuadrante(n: int, i: int) -> dict:
    theta, answer = ((30,"1/2"),(45,"√2/2"),(60,"√3/2"),(30,"√3/2"),(45,"√2/2"),(60,"1/2"),(30,"−1/2"),(60,"−√3/2"))[i]
    angle = 180-theta if i < 3 else 90+theta if i < 6 else 180+theta
    func = "sen" if i % 2 == 0 else "cos"
    # selected pairs are chosen only where the stated exact result is valid
    if i == 3: func, angle, answer = "cos", 120, "−1/2"
    if i == 1: func, angle, answer = "cos", 315, "√2/2"
    if i == 4: func, angle, answer = "sen", 135, "√2/2"
    if i == 5: func, angle, answer = "cos", 150, "−√3/2"
    if i == 6: func, angle, answer = "sen", 210, "−1/2"
    if i == 7: func, angle, answer = "cos", 240, "−1/2"
    reference = min(angle % 180, 180 - (angle % 180))
    p = _p(n, "Trigonometría", "Reducción al primer cuadrante", "reduccion_cuadrante", 2, 45,
      f"Calcula {func} {angle}°.", answer,
      _steps(("Reduce", f"El ángulo de referencia es {reference}° y determina el signo por cuadrante."), ("Evalúa", f"{func} {angle}°={answer}.")),
      "Referencia primero, signo después.", "Ubica el cuadrante antes de recordar la razón.", "El valor notable sin signo no basta.", source("Reducción al primer cuadrante"), "quadrant_reduction", {"func": func, "angle": angle})
    pool = ["1/2", "−1/2", "√2/2", "−√2/2", "√3/2", "−√3/2"]
    return set_options(p, answer, [answer] + [value for value in pool if value != answer][:3])


def ecuacion_trigonometrica(n: int, i: int) -> dict:
    cases = [("sen","√3/2",(60,120)),("cos","1/2",(60,300)),("sen","1/2",(30,150)),("cos","−1/2",(120,240)),("sen","−1/2",(210,330)),("cos","√3/2",(30,330)),("sen","√2/2",(45,135)),("cos","−√3/2",(150,210))]
    func, value, roots = cases[i]
    answer = sum(roots)
    p = _p(n, "Trigonometría", "Ecuaciones trigonométricas", "ecuacion_trigonometrica", 3, 75,
      f"En [0°,360°), resuelve {func} x={value}. Halla la suma de sus soluciones.", answer,
      _steps(("Busca ángulo de referencia", f"Usa el valor notable {value} y los cuadrantes con ese signo."), ("Escribe ambas soluciones", f"En [0°,360°): x={roots[0]}° o x={roots[1]}°."), ("Suma soluciones", f"{roots[0]}°+{roots[1]}°={answer}°.")),
      "No resuelvas con calculadora: usa referencia y cuadrantes.", "Lista ambas soluciones antes de sumarlas.", "Olvidar el segundo cuadrante o el cuarto deja una solución fuera.", source("Ecuaciones trigonométricas"), "trig_equation_sum", {"func": func, "value": value})
    return p


def funcion_trigonometrica(n: int, i: int) -> dict:
    amplitude, coefficient = 2 + (i % 5), (1,2,3,4,6,2,3,4)[i]
    ask_period = i % 2 == 1
    answer = 360 // coefficient if ask_period else amplitude
    asked = "período en grados" if ask_period else "amplitud"
    p = _p(n, "Trigonometría", "Funciones trigonométricas", "funcion_trigonometrica", 2, 55,
      f"Para f(x)={amplitude}·sen({coefficient}x), ¿cuál es su {asked}?", answer,
      _steps(("Lee parámetros", f"La amplitud es |{amplitude}| y el coeficiente angular es {coefficient}."), ("Aplica", f"El valor pedido es {answer}{'°' if ask_period else ''}.")),
      "En A·sen(Bx), amplitud=|A| y período=360°/B.", "Mira si piden altura o repetición.", "No confundas el coeficiente externo con el interno.", source("Funciones trigonométricas"), "trig_function_feature", {"amplitude": amplitude, "coefficient": coefficient, "ask_period": ask_period})
    return p


BUILDERS = [decimal_operaciones, valor_posicional, factorizacion_evaluada, funcion_aplicada, programacion_lineal, inecuacion_cuadratica, valor_absoluto, triangulo_notable, grados_radianes, reduccion_cuadrante, ecuacion_trigonometrica, funcion_trigonometrica]
PROBLEMS_SYLLABUS = [builder(1501 + family * 8 + variant, variant) for family, builder in enumerate(BUILDERS) for variant in range(8)]

if len(PROBLEMS_SYLLABUS) != 96 or [problem["n"] for problem in PROBLEMS_SYLLABUS] != list(range(1501, 1597)):
    raise RuntimeError("Syllabus additions must remain IDs 1501..1596")
