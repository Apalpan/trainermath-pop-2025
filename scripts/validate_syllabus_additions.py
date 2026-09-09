"""Independent validator for data.syllabus_additions; does not read params.expected."""
from __future__ import annotations

from fractions import Fraction
from math import sqrt
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from data.syllabus_additions import PROBLEMS_SYLLABUS


def shown(value: object) -> str:
    if isinstance(value, Fraction): return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    return str(value).replace("-", "−")


def solve(q: dict) -> object:
    kind = q["kind"]
    if kind == "decimal_cents":
        total = q["a"] + q["b"] if q["sign"] == "+" else q["a"] - q["b"]
        return f"{total // 100},{abs(total) % 100:02d}"
    if kind == "place_value": return q["digit"] * q["place"]
    if kind == "factor_root":
        roots = [x for x in range(q["product"] + 1) if x * (q["sum"] - x) == q["product"]]
        return max(roots)
    if kind == "affine_cost": return q["fixed"] + q["rate"] * q["units"]
    if kind == "linear_program":
        vertices = [(0,0),(0,q["total"]),(q["cap_x"],0),(q["cap_x"],q["total"]-q["cap_x"])]
        return max(q["px"] * x + q["py"] * y for x,y in vertices if x+y <= q["total"] and x <= q["cap_x"])
    if kind == "quadratic_inequality_count": return q["b"] - q["a"] + 1
    if kind == "absolute_sum": return 2 * q["center"]
    if kind == "notable_45_hyp": return f"{q['leg']}√2"
    if kind == "notable_30_hyp": return 2 * q["short"]
    if kind == "degree_radian": return q["answer"]
    if kind == "quadrant_reduction":
        table = {("sen",150):"1/2",("cos",315):"√2/2",("sen",120):"√3/2",("cos",120):"−1/2",("sen",135):"√2/2",("cos",150):"−√3/2",("sen",210):"−1/2",("cos",240):"−1/2"}
        return table[(q["func"],q["angle"])]
    if kind == "trig_equation_sum":
        table = {("sen","√3/2"):180,("cos","1/2"):360,("sen","1/2"):180,("cos","−1/2"):360,("sen","−1/2"):540,("cos","√3/2"):360,("sen","√2/2"):180,("cos","−√3/2"):360}
        return table[(q["func"],q["value"])]
    if kind == "trig_function_feature": return 360 // q["coefficient"] if q["ask_period"] else q["amplitude"]
    raise ValueError(kind)


def main() -> int:
    errors: list[str] = []
    if len(PROBLEMS_SYLLABUS) != 96: errors.append("Expected 96 problems")
    if [p["n"] for p in PROBLEMS_SYLLABUS] != list(range(1501,1597)): errors.append("IDs must be 1501..1596")
    families = {p["family"] for p in PROBLEMS_SYLLABUS}
    if len(families) != 12 or any(sum(p["family"] == name for p in PROBLEMS_SYLLABUS) != 8 for name in families): errors.append("Need twelve families with eight variants each")
    fingerprints = set()
    for p in PROBLEMS_SYLLABUS:
        q, actual = p["params"], shown(solve(p["params"]))
        selected = p["opts"][p["ans"]]
        if actual != selected: errors.append(f"{p['id']} {p['family']}: oracle={actual}, selected={selected}")
        if len(p["opts"]) != 4 or len(set(p["opts"])) != 4: errors.append(f"{p['id']}: alternatives not unique")
        if not 0 <= p["ans"] < 4: errors.append(f"{p['id']}: answer index")
        if len(p["steps"]) < 2 or len(p["steps"]) > 4 or not all(p[k] for k in ("idea","hint","trap")): errors.append(f"{p['id']}: teaching fields")
        if not (1 <= p["dif"] <= 3) or p["target"] <= 0: errors.append(f"{p['id']}: difficulty/time")
        if q["kind"] == "quadratic_inequality_count" and q["a"] >= q["b"]: errors.append(f"{p['id']}: quadratic interval")
        if q["kind"] == "linear_program" and not (q["px"] > q["py"] > 0 and 0 < q["cap_x"] < q["total"]): errors.append(f"{p['id']}: LP domain")
        if q["kind"] == "linear_program":
            vertices = [(0,0),(0,q["total"]),(q["cap_x"],0),(q["cap_x"],q["total"]-q["cap_x"])]
            scores = [q["px"] * x + q["py"] * y for x,y in vertices]
            if scores.count(max(scores)) != 1: errors.append(f"{p['id']}: LP optimum is not unique")
        if q["kind"] == "place_value" and not (q["place"] in {10,100,1000,10000} and 0 <= q["tail"] < q["place"]): errors.append(f"{p['id']}: positional-value domain")
        if q["kind"] == "trig_function_feature" and 360 % q["coefficient"]: errors.append(f"{p['id']}: non-integral period")
        fp = (p["family"], tuple(sorted((k, str(v)) for k,v in q.items() if k not in {"kind","expected"})))
        if fp in fingerprints: errors.append(f"{p['id']}: duplicate parameters")
        fingerprints.add(fp)
    print(f"Syllabus additions: {len(PROBLEMS_SYLLABUS)} problems / {len(families)} families")
    if errors:
        print("FAIL")
        print("\n".join(errors))
        return 1
    print("PASS: independent answers, domains, alternatives and diversity verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
