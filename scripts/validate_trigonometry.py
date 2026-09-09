"""Independent calculation audit for the generated trigonometry bank."""
from fractions import Fraction
from pathlib import Path
import sys
import json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from data.trigonometry_bank import PROBLEMS_TRIGONOMETRY

def solve(p):
    q=p["params"]; k=q["kind"]
    if k=="ratio":
        return {"sen":Fraction(q["op"],q["hyp"]),"cos":Fraction(q["adj"],q["hyp"]),"tan":Fraction(q["op"],q["adj"])}[q["ask"]]
    if k=="shadow": return Fraction(q["shadow"]*q["rise"],q["run"])
    if k=="fundamental": return 1+Fraction(q["op"]**2,q["adj"]**2)
    if k=="complement": return Fraction(q["op"],q["hyp"])
    if k=="double_angle":
        s,c=Fraction(q["op"],q["hyp"]),Fraction(q["adj"],q["hyp"])
        return 2*s*c if q["choice"]=="sen" else c*c-s*s
    if k=="angle_sum": return (q["a"]+q["b"])/(1-q["a"]*q["b"])
    raise ValueError(k)
def validate():
    errors=[]; required={"n","id","tema","sub","family","dif","target","enun","opts","ans","steps","idea","hint","trap","origin","source","params"}
    canonical=[json.dumps({k:v for k,v in p['params'].items() if k!='expected'},sort_keys=True,default=str) for p in PROBLEMS_TRIGONOMETRY]
    if len(set(canonical))!=len(canonical): errors.append('Repeated mathematical parameters')
    for p in PROBLEMS_TRIGONOMETRY:
        if required-set(p): errors.append(f"{p['id']}: schema")
        if len(p["opts"])!=4 or len(set(p["opts"]))!=4: errors.append(f"{p['id']}: options")
        if not 0<=p["ans"]<4 or p["opts"][p["ans"]]!=p["params"]["expected"]: errors.append(f"{p['id']}: answer index")
        if str(solve(p))!=p["params"]["expected"]: errors.append(f"{p['id']}: math")
        if not 2<=len(p["steps"])<=4 or not 30<=p["target"]<=150: errors.append(f"{p['id']}: teaching metadata")
        if p["source"]["file"]!="Informacion/TRIGONOMETRÍA - PRISMA 2025 (1).pdf" or p["source"]["page"] not in (5,6,7,10,16): errors.append(f"{p['id']}: source")
    if errors: raise AssertionError("\n".join(errors))
    print(f"OK: {len(PROBLEMS_TRIGONOMETRY)} trigonometry exercises; 6 families")
if __name__=="__main__": validate()
