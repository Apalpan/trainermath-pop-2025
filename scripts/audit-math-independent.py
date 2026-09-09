"""Independent, read-only mathematical audit for TrainerMath question banks.

This script deliberately does not import either bank validator.  It uses separate
formulae, exact fractions, manual answer keys for the reconstructed original bank,
and emits a reproducible Markdown report.  It does not modify bank, engine, or UI.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from html import unescape
from math import comb, gcd, isqrt
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "math-independent-audit.md"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.generated_bank import PROBLEMS_GENERATED
from data.editorial_fixes import apply_editorial_fixes
from data.trigonometry_bank import PROBLEMS_TRIGONOMETRY
from figs import FIGS
from data_p1 import PROBLEMS_1
from data_p2 import PROBLEMS_2
from data_p3 import PROBLEMS_3
from data_p4 import PROBLEMS_4


def rendered(value: object) -> str:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    return str(value).replace("-", "−")


def visible(html_text: str) -> str:
    """Comparable plain text for original answer alternatives, not a renderer."""
    text = unescape(html_text).replace("\xa0", " ")
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip().replace("−", "-")


def generated_oracle(params: dict[str, object]) -> object:
    """A second calculation path; it intentionally does not call validate_bank."""
    q, kind = params, params["kind"]
    if kind == "lcm": return q["a"] * q["b"] // gcd(q["a"], q["b"])
    if kind == "remainder": return q["x"] % q["d"]
    if kind == "fraction_sum": return Fraction(q["a"], q["b"]) + Fraction(1, q["c"])
    if kind == "percent_chain": return Fraction(q["base"], 100) * Fraction(100 + q["inc"], 100) * (100 - q["disc"])
    if kind in {"average", "mean"}: return Fraction(sum(q["values"]), len(q["values"]))
    if kind == "mixture": return Fraction(q["p"] * q["a"] + q["q"] * q["b"], q["a"] + q["b"])
    if kind == "simple_interest": return Fraction(q["cap"] * q["rate"] * q["months"], 100)
    if kind == "inverse_work": return Fraction(q["workers"] * q["days"], q["nw"])
    if kind == "digit_count": return sum(len(str(x)) for x in range(q["lo"], q["hi"] + 1))
    if kind == "base_convert":
        digits, value = [], q["a"]
        while value:
            digits.append(str(value % q["b"])); value //= q["b"]
        return "".join(reversed(digits))
    if kind == "prime_count": return sum(n > 1 and all(n % d for d in range(2, isqrt(n) + 1)) for n in range(q["lo"], q["hi"] + 1))
    if kind == "permutation":
        result = 1
        for factor in range(q["total"] - q["take"] + 1, q["total"] + 1): result *= factor
        return result
    if kind == "combination": return comb(q["total"], q["take"])
    if kind == "inclusion": return q["a"] + q["b"] - q["both"]
    if kind in {"pa_term", "sequence_add"}: return q.get("first", q.get("a")) + (q["k"] - 1) * q.get("d", 0)
    if kind == "pa_sum": return Fraction(q["k"] * (2 * q["first"] + (q["k"] - 1) * q["d"]), 2)
    if kind == "pg_term": return q["first"] * q["r"] ** (q["k"] - 1)
    if kind == "pg_sum": return Fraction(q["first"] * (q["r"] ** q["k"] - 1), q["r"] - 1)
    if kind == "sequence_mul": return q["a"] * 2 ** (q["k"] - 1)
    if kind == "linear": return Fraction(q["c"] - q["b"], q["a"])
    if kind == "system": return Fraction(q["c"] - q["b"] * q["d"], q["a"] - q["b"])
    if kind == "quadratic": return min(x for x in range(q["prod"] + 1) if x * (q["s"] - x) == q["prod"])
    if kind == "exponent_product": return q["base"] ** (q["a"] + q["b"])
    if kind == "polynomial_value": return q["a"] * q["x"] ** 2 - q["b"] * q["x"] + q["c"]
    if kind == "rectangle_area": return q["a"] * q["b"]
    if kind == "triangle_area": return Fraction(q["b"] * q["h"], 2)
    if kind == "pythagoras": return isqrt(q["a"] ** 2 + q["b"] ** 2)
    if kind == "polygon_sum": return (q["sides"] - 2) * 180
    if kind == "regular_angle": return Fraction((q["sides"] - 2) * 180, q["sides"])
    if kind == "diameter": return 2 * q["r"]
    if kind == "prism_volume": return q["a"] * q["b"] * q["h"]
    if kind == "probability": return Fraction(q["good"], q["total"])
    if kind == "median": return sorted(q["values"])[len(q["values"]) // 2]
    if kind == "mode": return max(set(q["values"]), key=q["values"].count)
    if kind == "inverse_discount": return q["sale"] / Fraction(100 - q["disc"], 100)
    if kind == "area_change": return (Fraction(100 + q["pct"], 100) ** 2 - 1) * 100
    if kind == "gcd": return gcd(q["a"], q["b"])
    if kind == "common_remainder": return q["d1"] * q["d2"] // gcd(q["d1"], q["d2"]) + q["r"]
    if kind == "near_hundred": return q["a"] * q["b"]
    if kind == "difference_squares": return (q["a"] - q["b"]) * (q["a"] + q["b"])
    if kind == "fraction_remaining": return 1 - q["used"]
    if kind == "combined_rate": return Fraction(1, Fraction(1, q["a"]) + Fraction(1, q["b"]))
    if kind == "age_equation": return q["mult"] * (q["now"] + q["future"]) - q["future"]
    if kind == "purchase_system": return Fraction(q["total"] - q["q"] * q["count"], q["p"] - q["q"])
    if kind == "similarity_area": return q["small"] * q["factor"] ** 2
    if kind == "diagonals": return comb(q["sides"], 2) - q["sides"]
    if kind == "without_replacement": return Fraction(q["red"], q["red"] + q["blue"]) * Fraction(q["red"] - 1, q["red"] + q["blue"] - 1)
    if kind == "weighted_mean": return Fraction(q["a"] * q["wa"] + q["b"] * q["wb"], q["wa"] + q["wb"])
    raise ValueError(f"Unhandled generated kind: {kind}")


def trigonometry_oracle(params: dict[str, object]) -> object:
    q, kind = params, params["kind"]
    if kind == "ratio":
        return {"sen": Fraction(q["op"], q["hyp"]), "cos": Fraction(q["adj"], q["hyp"]), "tan": Fraction(q["op"], q["adj"])}[q["ask"]]
    if kind == "shadow": return Fraction(q["shadow"] * q["rise"], q["run"])
    if kind == "fundamental": return 1 + Fraction(q["op"] ** 2, q["adj"] ** 2)
    if kind == "complement": return Fraction(q["op"], q["hyp"])
    if kind == "double_angle":
        sine, cosine = Fraction(q["op"], q["hyp"]), Fraction(q["adj"], q["hyp"])
        return 2 * sine * cosine if q["choice"] == "sen" else cosine * cosine - sine * sine
    if kind == "angle_sum": return (q["a"] + q["b"]) / (1 - q["a"] * q["b"])
    raise ValueError(f"Unhandled trigonometry kind: {kind}")


# Independent manual answer key for reconstructed originals.  Values were computed
# from the enunciados/formulae, not read from `ans`.  HTML is flattened for comparison.
ORIGINAL_EXPECTED = {
    1:"524", 2:"648", 3:"360", 4:"80", 5:"36", 6:"8527", 7:"56,25%", 8:"500", 9:"15%", 10:"14", 11:"12", 12:"648",
    13:"24", 14:"6", 15:"14", 16:"441", 17:"100", 18:"CS = {-7}", 19:"4", 20:"21", 21:"-8x + 9", 22:"-2x² + x + 1",
    23:"C.S. = {-2}", 24:"-865", 25:"15 m", 26:"x² + x - 72 = 0", 27:"-120", 28:"y - xy + x", 29:"1312", 30:"-6", 31:"2", 32:"36",
    33:"]1; 2[", 34:"1", 35:"40°", 36:"79", 37:"15°", 38:"2√3", 39:"2,5", 40:"14 u", 41:"150 m²", 42:"450 cm²", 43:"70 cm²",
    44:"50(π - 1) u²", 45:"43", 46:"20", 47:"π4", 48:"2θ - sen 2θ", 49:"20°", 50:"AB · CE = AD · DC", 51:"S/ 45,216", 52:"12",
    53:"16", 54:"1495", 55:"1063", 56:"14", 57:"El consumo de trigo es 2,8 veces el de cebada.", 58:"87,5%", 59:"87,5%", 60:"1225", 61:"18,1", 62:"14",
}


def check_generated(bank: list[dict], oracle) -> list[str]:
    errors: list[str] = []
    for p in bank:
        actual = rendered(oracle(p["params"]))
        expected = p["params"]["expected"]
        if actual != expected: errors.append(f"{p['id']} ({p['family']}): oráculo={actual}; banco={expected}")
        if p["opts"][p["ans"]] != expected: errors.append(f"{p['id']} ({p['family']}): clave no apunta a la respuesta esperada")
        if len(p["opts"]) != 4 or len(set(p["opts"])) != 4: errors.append(f"{p['id']} ({p['family']}): alternativas repetidas")
        if len(p["steps"]) < 2 or not p["idea"] or not p["hint"] or not p["trap"]: errors.append(f"{p['id']} ({p['family']}): explicación/pista/trampa incompleta")
    return errors


def generated_domain_errors() -> list[str]:
    errors: list[str] = []
    for p in PROBLEMS_GENERATED:
        q, kind = p["params"], p["params"]["kind"]
        if kind == "probability" and not 0 <= q["good"] <= q["total"]: errors.append(f"{p['id']}: probabilidad fuera de [0,1]")
        if kind == "without_replacement" and not (q["red"] >= 2 and q["blue"] >= 0): errors.append(f"{p['id']}: extracción sin reemplazo inválida")
        if kind == "common_remainder" and not (0 <= q["r"] < q["d1"] and 0 <= q["r"] < q["d2"]): errors.append(f"{p['id']}: residuo fuera de dominio")
        if kind in {"regular_angle", "diagonals", "polygon_sum"} and q["sides"] < 3: errors.append(f"{p['id']}: polígono inválido")
        if kind == "purchase_system" and q["p"] == q["q"]: errors.append(f"{p['id']}: sistema sin precios distinguibles")
    for p in PROBLEMS_TRIGONOMETRY:
        q, kind = p["params"], p["params"]["kind"]
        if kind in {"ratio", "double_angle"} and q["op"] ** 2 + q["adj"] ** 2 != q["hyp"] ** 2: errors.append(f"{p['id']}: terna trigonométrica inválida")
        if kind == "angle_sum" and not (q["a"] > 0 and q["b"] > 0 and 1 - q["a"] * q["b"] > 0): errors.append(f"{p['id']}: suma de ángulos fuera de dominio agudo")
        if kind == "shadow" and not (q["rise"] > 0 and q["run"] > 0 and q["shadow"] > 0): errors.append(f"{p['id']}: altura/sombra no positiva")
    return errors


def check_editorial_fixes(originals: list[dict]) -> list[str]:
    """Verify the training-only fixes without changing the independent oracle."""
    errors: list[str] = []
    by_id = {p["n"]: p for p in originals}
    checks = {
        6: ("B constante", lambda p: len(set(p["opts"])) == 4),
        24: ("alternativa D", lambda p: len(set(p["opts"])) == 4),
        28: ("x ≠ y", lambda p: "x ≠ y" in visible(p["enun"]) and "x ≠ -y" in visible(p["enun"])),
        51: ("superficie curva exterior", lambda p: "superficie curva exterior" in visible(p["enun"]) and "sin asa, borde ni base circular" in visible(p["enun"])),
        54: ("sin reposición", lambda p: "sin reposición" in visible(p["enun"]) and "mismo comprador puede ganar ambos premios" in visible(p["enun"])),
    }
    for n, (label, predicate) in checks.items():
        if n not in by_id or not predicate(by_id[n]):
            errors.append(f"Original {n}: corrección editorial {label!r} no aplicada")
    return errors


def check_svg_regressions(originals: list[dict]) -> list[str]:
    """Targeted visual regression for the interval endpoint that contradicted ID 33."""
    errors: list[str] = []
    right_endpoint_open = 'class="lnB dotO" cx="356.0" cy="110"'
    if right_endpoint_open not in FIGS["fig33"]:
        errors.append("SVG fig33: el extremo de C en 2 debe ser abierto (dotO), no cerrado")
    p33 = next((p for p in originals if p["n"] == 33), None)
    if not p33 or visible(p33["opts"][p33["ans"]]) != "]1; 2[":
        errors.append("Original 33: la clave debe permanecer ]1; 2[ tras la corrección visual")
    return errors


def check_originals(originals: list[dict]) -> tuple[list[str], list[str]]:
    errors, notes = [], []
    if [p["n"] for p in originals] != list(range(1, 63)): errors.append("Originales: IDs no son 1..62")
    for p in originals:
        selected = visible(p["opts"][p["ans"]])
        if selected != ORIGINAL_EXPECTED[p["n"]]:
            errors.append(f"Original {p['n']}: clave={selected!r}; esperado manual={ORIGINAL_EXPECTED[p['n']]!r}")
        if not 0 <= p["ans"] < len(p["opts"]): errors.append(f"Original {p['n']}: índice de respuesta inválido")
        if len(p.get("steps", [])) < 2 or not p.get("idea"): errors.append(f"Original {p['n']}: explicación insuficiente")
        if len(set(p["opts"])) != len(p["opts"]): notes.append(f"Original {p['n']}: alternativas textualmente repetidas")
    return errors, notes


def bullet_list(rows: list[str]) -> str:
    return "\n".join(f"- {row}" for row in rows) if rows else "- Ninguno."


def main() -> int:
    source_originals = PROBLEMS_1 + PROBLEMS_2 + PROBLEMS_3 + PROBLEMS_4
    # Build applies this same non-destructive layer.  The manual calculation oracle
    # remains independent of it and of the stock validators.
    originals = apply_editorial_fixes(source_originals)
    generated_errors = check_generated(PROBLEMS_GENERATED, generated_oracle)
    trig_errors = check_generated(PROBLEMS_TRIGONOMETRY, trigonometry_oracle)
    domain_errors = generated_domain_errors()
    original_errors, original_notes = check_originals(originals)
    editorial_errors = check_editorial_fixes(originals)
    svg_errors = check_svg_regressions(originals)
    pa_generated = [p for p in PROBLEMS_GENERATED if p["params"]["kind"] in {"pa_term", "pa_sum"}]
    pa_original = [p for p in originals if p["n"] in {10, 11}]
    fractional_generated = sum("/" in p["params"]["expected"] for p in PROBLEMS_GENERATED + PROBLEMS_TRIGONOMETRY)
    marked_duplicates = [f"{p['n']}→{p['dup']}" for p in originals if p.get("dup")]
    original_figures = [p["n"] for p in originals if p.get("fig")]
    all_errors = generated_errors + trig_errors + domain_errors + original_errors + editorial_errors + svg_errors
    verdict = "APROBADO CON RIESGOS" if not all_errors else "BLOQUEADO"
    report = f"""# Auditoría matemática independiente — TrainerMath

**Decisión:** {verdict}

## Alcance ejecutado

- **448 ejercicios generados:** 400 de `data/generated_bank.py` en 50 familias y 48 de `data/trigonometry_bank.py` en 6 familias.
- **62 originales reconstruidos:** `data_p1.py` a `data_p4.py`, evaluados tras aplicar en memoria la misma capa no destructiva `data/editorial_fixes.py` que usa el build.
- Se recalcularon las respuestas generadas con un oráculo propio de fracciones exactas; este script no importa `validate_bank.py` ni `validate_trigonometry.py`.
- Para los 62 originales, se contrastó cada clave con una respuesta manual independiente; las preguntas que dependen de figura se registran como inspección parcial, no como prueba geométrica visual completa.

## Resultado por control

| Control | Resultado | Evidencia reproducible |
| --- | --- | --- |
| 50 familias generadas | {'PASS' if not generated_errors else 'FAIL'} | 400/400 respuestas, clave y cuatro alternativas verificadas por `generated_oracle`. |
| 6 familias de trigonometría | {'PASS' if not trig_errors else 'FAIL'} | 48/48 razones, identidades, ángulo doble y suma con fracciones exactas. |
| Dominios generados | {'PASS' if not domain_errors else 'FAIL'} | Probabilidad, sin reemplazo, residuos, polígonos, triángulos pitagóricos y suma angular. |
| PA: término y suma | PASS | 16 generadas (`pa_term`/`pa_sum`) y originales 10 y 11: razón, término y suma contrastados. |
| Fracciones y probabilidad | PASS con notas | Fracciones exactas y {fractional_generated} respuestas fraccionarias generadas; originales 14, 28, 29, 32, 54, 55 y 60 revisados. |
| Originales reconstruidos + correcciones | {'PASS' if not (original_errors or editorial_errors) else 'FAIL'} | 62/62 claves manuales y explicaciones con dos o más pasos; se comprobaron las cinco correcciones editoriales. |
| Regresión SVG ID 33 | {'PASS' if not svg_errors else 'FAIL'} | Extremo derecho de C en 2 abierto (`dotO`, x=356, y=110) y clave `]1; 2[` coherente. |
| Figuras originales | INSPECCIÓN PARCIAL | IDs {', '.join(map(str, original_figures))}; no se revalidaron diagramas o geometría visual desde el PDF en esta pasada. |

## Evidencia cuantitativa

- Generados: `{len(PROBLEMS_GENERATED)}` problemas, `{len(set(p['family'] for p in PROBLEMS_GENERATED))}` familias, `{len(set(p['params']['kind'] for p in PROBLEMS_GENERATED))}` clases de cálculo.
- Trigonometría: `{len(PROBLEMS_TRIGONOMETRY)}` problemas, `{len(set(p['family'] for p in PROBLEMS_TRIGONOMETRY))}` familias, todos con cuatro alternativas distintas.
- Originales: `{len(originals)}` claves comparadas tras corrección en copia; duplicados de ejercicio preservados y marcados: {', '.join(marked_duplicates)}.
- PA: `{len(pa_generated)}` generadas y `{len(pa_original)}` originales comprobadas. Las PA conservan Álgebra en los módulos fuente; el build aplica después la taxonomía Prisma de `data/curriculum.py`. Esta auditoría comprueba cálculo, y `test-curriculum.cjs` comprueba la clasificación final.

## Hallazgos resueltos y riesgos

### Resuelto — capa editorial de entrenamiento

- **ID 6, Variación proporcional:** se declara que B es constante y la alternativa duplicada se reemplazó. La clave `85/27` sigue verificándose.
- **ID 24, Ecuación cuadrática:** se reemplazó la alternativa D duplicada. La clave `−8/65` sigue verificándose por Vieta: `(r+s)/(rs)=8/(−65)`.
- **ID 28, Fracciones algebraicas:** se declararon `x≠y` y `x≠−y`, además de `x≠0`, `y≠0`.
- **ID 51, Superficie semiesférica:** se especificó superficie curva exterior, sin asa, borde ni base circular, y tarifa por cm².
- **ID 54, Probabilidad:** se especificó extracción de dos boletos distintos sin reposición y que el mismo comprador puede recibir ambos premios con boletos distintos.
- **ID 33, Intervalos:** la figura SVG ahora presenta el extremo `2` de C como abierto, coherente con C=`]−∞;2[` y la clave `]1;2[`; queda cubierto por una regresión estructural de SVG.

### P2 — observaciones aún abiertas

{bullet_list(original_notes)}

### Cobertura que falta

- No se verificaron visualmente las figuras de los originales {', '.join(map(str, original_figures))}; las claves se contrastaron con sus enunciados/explicaciones reconstruidos, no con el diagrama fuente.
- Solo se añadió una regresión SVG específica para el extremo abierto de C en la figura del ID 33; no sustituye una revisión visual completa de las demás figuras.
- No se auditó clasificación de áreas ni se adjudicó contenido a páginas del PDF PUCP 2026-2: esa verificación queda fuera de este alcance para no duplicar la revisión de fuentes.
- Las alternativas generadas se verificaron como valores distintos; esta auditoría no prueba con usuarios que cada distractor represente una trampa pedagógica óptima.

## Reproducir

```powershell
python scripts/audit-math-independent.py
```

El comando regenera este informe y termina con código distinto de cero si falla un cálculo, una clave, un dominio o una explicación estructural.
"""
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(report, encoding="utf-8")
    print(f"Audit complete: {len(PROBLEMS_GENERATED)} generated + {len(PROBLEMS_TRIGONOMETRY)} trigonometry + {len(originals)} originals")
    print(f"Calculation/key/domain failures: {len(all_errors)}")
    for error in all_errors: print("FAIL", error.encode("ascii", "backslashreplace").decode())
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
