"""Read-only independent mathematical audit for the 96 syllabus additions.

This intentionally does not import or call validate_syllabus_additions.py and never
uses params['expected'].  It recalculates selected keys from the displayed model and
checks semantic domains that a formula-only validator can miss.
"""
from __future__ import annotations

from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
OUTPUT = ROOT / "output" / "audit-syllabus-independent.md"

from data.syllabus_additions import PROBLEMS_SYLLABUS


def shown(value: object) -> str:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    return str(value).replace("-", "−")


def radians(degrees: int) -> str:
    numerator, denominator = degrees, 180
    divisor = gcd(numerator, denominator)
    numerator //= divisor
    denominator //= divisor
    if denominator == 1:
        return "π" if numerator == 1 else f"{numerator}π"
    return f"π/{denominator}" if numerator == 1 else f"{numerator}π/{denominator}"


def unit_value(func: str, angle: int) -> str:
    """Exact elementary unit-circle values, independent from the author validator."""
    table = {
        ("sen", 30): "1/2", ("sen", 45): "√2/2", ("sen", 60): "√3/2",
        ("sen", 120): "√3/2", ("sen", 135): "√2/2", ("sen", 150): "1/2",
        ("sen", 210): "−1/2", ("sen", 225): "−√2/2", ("sen", 240): "−√3/2",
        ("sen", 300): "−√3/2", ("sen", 315): "−√2/2", ("sen", 330): "−1/2",
        ("cos", 30): "√3/2", ("cos", 45): "√2/2", ("cos", 60): "1/2",
        ("cos", 120): "−1/2", ("cos", 135): "−√2/2", ("cos", 150): "−√3/2",
        ("cos", 210): "−√3/2", ("cos", 225): "−√2/2", ("cos", 240): "−1/2",
        ("cos", 300): "1/2", ("cos", 315): "√2/2", ("cos", 330): "√3/2",
    }
    return table[(func, angle)]


def solve(params: dict[str, object]) -> object:
    q, kind = params, params["kind"]
    if kind == "decimal_cents":
        cents = q["a"] + q["b"] if q["sign"] == "+" else q["a"] - q["b"]
        return f"{cents // 100},{abs(cents) % 100:02d}"
    if kind == "place_value":
        return q["digit"] * q["place"]
    if kind == "factor_root":
        discriminant = q["sum"] ** 2 - 4 * q["product"]
        root = isqrt(discriminant)
        if root * root != discriminant:
            raise ValueError("non-square discriminant")
        return (q["sum"] + root) // 2
    if kind == "affine_cost":
        return q["fixed"] + q["rate"] * q["units"]
    if kind == "linear_program":
        # py>0 fills x+y=total; px>py then selects the greatest feasible x.
        return q["py"] * q["total"] + (q["px"] - q["py"]) * q["cap_x"]
    if kind == "quadratic_inequality_count":
        return q["b"] - q["a"] + 1
    if kind == "absolute_sum":
        return 2 * q["center"]
    if kind == "notable_45_hyp":
        return f"{q['leg']}√2"
    if kind == "notable_30_hyp":
        return 2 * q["short"]
    if kind == "degree_radian":
        return radians(q["degree"])
    if kind == "quadrant_reduction":
        return unit_value(q["func"], q["angle"])
    if kind == "trig_equation_sum":
        angles = [angle for angle in range(360) if (q["func"], angle) in {
            ("sen", 30), ("sen", 45), ("sen", 60), ("sen", 120), ("sen", 135), ("sen", 150),
            ("sen", 210), ("sen", 225), ("sen", 240), ("sen", 300), ("sen", 315), ("sen", 330),
            ("cos", 30), ("cos", 45), ("cos", 60), ("cos", 120), ("cos", 135), ("cos", 150),
            ("cos", 210), ("cos", 225), ("cos", 240), ("cos", 300), ("cos", 315), ("cos", 330),
        } and unit_value(q["func"], angle) == q["value"]]
        return sum(angles)
    if kind == "trig_function_feature":
        return 360 // q["coefficient"] if q["ask_period"] else abs(q["amplitude"])
    raise ValueError(f"Unhandled kind: {kind}")


def place_value_domain_error(problem: dict) -> str | None:
    q = problem["params"]
    if q["kind"] != "place_value":
        return None
    number = q["digit"] * q["place"] + q["tail"]
    matches = []
    for index, char in enumerate(reversed(str(number))):
        if char == str(q["digit"]):
            matches.append(10 ** index)
    if not matches:
        return f"{problem['id']} ({problem['family']}): el dígito {q['digit']} no aparece en {number}"
    if len(matches) != 1:
        return f"{problem['id']} ({problem['family']}): el dígito {q['digit']} aparece en posiciones {matches}; el enunciado es ambiguo"
    if matches[0] != q["place"]:
        return f"{problem['id']} ({problem['family']}): el dígito aparece en {matches[0]}, no en la posición declarada {q['place']}"
    return None


def domain_errors(problem: dict) -> list[str]:
    q, kind, errors = problem["params"], problem["params"]["kind"], []
    if kind == "linear_program" and not (q["total"] > q["cap_x"] > 0 and q["px"] > q["py"] > 0):
        errors.append(f"{problem['id']} ({problem['family']}): dominio de programación lineal inválido")
    if kind == "quadratic_inequality_count" and not q["a"] < q["b"]:
        errors.append(f"{problem['id']} ({problem['family']}): raíces de inecuación sin orden estricto")
    if kind == "absolute_sum" and q["distance"] <= 0:
        errors.append(f"{problem['id']} ({problem['family']}): valor absoluto debe tener dos soluciones distintas")
    if kind == "degree_radian" and not 0 < q["degree"] <= 360:
        errors.append(f"{problem['id']} ({problem['family']}): grados fuera de dominio de conversión")
    if kind == "quadrant_reduction" and not (q["func"] in {"sen", "cos"} and 0 < q["angle"] < 360):
        errors.append(f"{problem['id']} ({problem['family']}): función/ángulo trigonométrico inválido")
    if kind == "trig_equation_sum" and q["func"] not in {"sen", "cos"}:
        errors.append(f"{problem['id']} ({problem['family']}): función trigonométrica inválida")
    if kind == "trig_function_feature" and (q["coefficient"] <= 0 or 360 % q["coefficient"]):
        errors.append(f"{problem['id']} ({problem['family']}): período en grados no entero o coeficiente inválido")
    place_error = place_value_domain_error(problem)
    if place_error:
        errors.append(place_error)
    return errors


def reference_angle(angle: int) -> int:
    reduced = angle % 360
    if reduced <= 90:
        return reduced
    if reduced <= 180:
        return 180 - reduced
    if reduced <= 270:
        return reduced - 180
    return 360 - reduced


def explanation_errors(problem: dict) -> list[str]:
    """Check displayed trig reasoning, rather than merely its answer key."""
    q, kind = problem["params"], problem["params"]["kind"]
    if kind == "quadrant_reduction":
        text = problem["steps"][0]["d"]
        found = re.search(r"referencia es (\d+)°", text)
        correct = reference_angle(q["angle"])
        if not found or int(found.group(1)) != correct:
            return [f"{problem['id']} ({problem['family']}): paso de referencia debe declarar {correct}°, no una referencia incompatible"]
        return []
    if kind == "trig_equation_sum":
        roots = [angle for angle in range(360) if (q["func"], angle) in {
            ("sen", 30), ("sen", 45), ("sen", 60), ("sen", 120), ("sen", 135), ("sen", 150),
            ("sen", 210), ("sen", 225), ("sen", 240), ("sen", 300), ("sen", 315), ("sen", 330),
            ("cos", 30), ("cos", 45), ("cos", 60), ("cos", 120), ("cos", 135), ("cos", 150),
            ("cos", 210), ("cos", 225), ("cos", 240), ("cos", 300), ("cos", 315), ("cos", 330),
        } and unit_value(q["func"], angle) == q["value"]]
        solution_step = next((step["d"] for step in problem["steps"] if step["t"] == "Escribe ambas soluciones"), "")
        found = re.search(r"x=(\d+)° o x=(\d+)°", solution_step)
        if not found or {int(found.group(1)), int(found.group(2))} != set(roots):
            return [f"{problem['id']} ({problem['family']}): paso debe declarar las soluciones {roots[0]}° y {roots[1]}°"]
        sum_step = next((step["d"] for step in problem["steps"] if step["t"] == "Suma soluciones"), "")
        summed = re.search(r"(\d+)°\+(\d+)°=(\d+)°", sum_step)
        if not summed or {int(summed.group(1)), int(summed.group(2))} != set(roots) or int(summed.group(3)) != sum(roots):
            return [f"{problem['id']} ({problem['family']}): paso de suma debe conservar {roots[0]}°+{roots[1]}°={sum(roots)}°"]
    return []


def bullet(rows: list[str]) -> str:
    return "\n".join(f"- {row}" for row in rows) if rows else "- Ninguno."


def main() -> int:
    errors: list[str] = []
    bank = PROBLEMS_SYLLABUS
    if len(bank) != 96 or [p["n"] for p in bank] != list(range(1501, 1597)):
        errors.append("Banco: se esperaban IDs consecutivos 1501..1596")
    family_counts = {family: sum(p["family"] == family for p in bank) for family in {p["family"] for p in bank}}
    if len(family_counts) != 12 or set(family_counts.values()) != {8}:
        errors.append(f"Familias: distribución inválida {family_counts}")
    fingerprints: set[tuple] = set()
    for p in bank:
        q = p["params"]
        try:
            expected = shown(solve(q))
        except Exception as exc:
            errors.append(f"{p['id']} ({p['family']}): oráculo no pudo calcular: {exc}")
            continue
        if not 0 <= p["ans"] < len(p["opts"]):
            errors.append(f"{p['id']} ({p['family']}): índice de clave inválido")
        elif p["opts"][p["ans"]] != expected:
            errors.append(f"{p['id']} ({p['family']}): clave={p['opts'][p['ans']]}; oráculo={expected}")
        if len(p["opts"]) != 4 or len(set(p["opts"])) != 4:
            errors.append(f"{p['id']} ({p['family']}): alternativas no son cuatro valores únicos")
        if len(p["steps"]) < 2 or not all(p.get(k) for k in ("idea", "hint", "trap")):
            errors.append(f"{p['id']} ({p['family']}): explicación/pista/trampa incompleta")
        errors.extend(domain_errors(p))
        errors.extend(explanation_errors(p))
        fingerprint = (p["family"], tuple(sorted((key, str(value)) for key, value in q.items() if key not in {"kind", "expected"})))
        if fingerprint in fingerprints:
            errors.append(f"{p['id']} ({p['family']}): parámetros repetidos")
        fingerprints.add(fingerprint)

    verdict = "APROBADO" if not errors else "BLOQUEADO"
    report = f"""# Auditoría matemática independiente — adiciones de temario

**Decisión:** {verdict}

## Alcance ejecutado

- 96 problemas, IDs 1501–1596: 12 familias con 8 variantes cada una.
- Recalculé cada clave a partir de parámetros, sin llamar `validate_syllabus_additions.py` ni leer `params.expected`.
- Se revisaron cuatro alternativas distintas, la posición de la clave, los campos de enseñanza, diversidad de parámetros y dominios.
- Controles reforzados: programación lineal, inecuaciones cuadráticas, valor absoluto, medidas angulares, signos por cuadrante, ecuaciones trigonométricas y período/amplitud.

## Resultado por control

| Control | Resultado | Evidencia |
| --- | --- | --- |
| Claves y alternativas | {'PASS' if not [e for e in errors if 'clave=' in e or 'alternativas' in e] else 'FAIL'} | Oráculo matemático propio sobre 96/96 claves. |
| Programación lineal | {'PASS' if not [e for e in errors if 'programación lineal' in e] else 'FAIL'} | Restricciones, vértice x máximo y capacidad completa. |
| Inecuaciones cuadráticas | {'PASS' if not [e for e in errors if 'inecuación' in e] else 'FAIL'} | Conteo entero inclusivo entre raíces ordenadas. |
| Trigonometría | {'PASS' if not [e for e in errors if 'trigonométr' in e or 'período' in e or 'referencia' in e or 'soluciones' in e] else 'FAIL'} | Círculo unitario exacto, referencias declaradas, pares de soluciones y período. |
| Dominio semántico de valor posicional | {'PASS' if not [e for e in errors if 'dígito' in e] else 'FAIL'} | El dígito debe aparecer una sola vez y en la posición preguntada. |

## Defectos

{bullet(errors)}

## Limitaciones

- Esta revisión valida cálculo, dominio y estructura del banco; no reemplaza la validación de clasificación contra la fuente temática ni una prueba con estudiantes de la calidad pedagógica de cada distractor.

## Reproducir

```powershell
python scripts/audit-syllabus-independent.py
```

El comando genera este informe y termina con código distinto de cero ante errores de clave, dominio, alternativas o estructura.
"""
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(report, encoding="utf-8")
    print(f"Syllabus independent audit: {len(bank)} problems / {len(family_counts)} families")
    print(f"Failures: {len(errors)}")
    for error in errors:
        print(error.encode("ascii", "backslashreplace").decode())
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
