"""Independent mathematical verification for data.generated_bank."""
from math import comb, gcd, isqrt
from fractions import Fraction
from pathlib import Path
import sys
import json
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data.generated_bank import PROBLEMS_GENERATED

def result(p):
    q=p["params"]; k=q["kind"]
    if k=="lcm": return q["a"]*q["b"]//gcd(q["a"],q["b"])
    if k=="remainder": return q["x"]%q["d"]
    if k=="fraction_sum":
        f=Fraction(q["a"],q["b"])+Fraction(1,q["c"]); return f"{f.numerator}/{f.denominator}"
    if k=="percent_chain": return Fraction(q["base"]*(100+q["inc"])*(100-q["disc"]),10000)
    if k=="average" or k=="mean": return sum(q["values"])//len(q["values"])
    if k=="mixture": return Fraction(q["p"]*q["a"]+q["q"]*q["b"],q["a"]+q["b"])
    if k=="simple_interest": return q["cap"]*q["rate"]*q["months"]//100
    if k=="inverse_work": return Fraction(q["workers"]*q["days"],q["nw"])
    if k=="digit_count": return sum(len(str(x)) for x in range(q["lo"],q["hi"]+1))
    if k=="base_convert":
        x=q["a"]; ds=[]
        while x: ds.append(str(x%q["b"])); x//=q["b"]
        return "".join(ds[::-1])
    if k=="prime_count": return sum(x>1 and all(x%d for d in range(2,isqrt(x)+1)) for x in range(q["lo"],q["hi"]+1))
    if k=="permutation":
        out=1
        for x in range(q["total"]-q["take"]+1,q["total"]+1): out*=x
        return out
    if k=="combination": return comb(q["total"],q["take"])
    if k=="inclusion": return q["a"]+q["b"]-q["both"]
    if k=="pa_term" or k=="sequence_add": return q.get("first",q.get("a"))+(q["k"]-1)*q.get("d",0)
    if k=="pa_sum":
        last=q["first"]+(q["k"]-1)*q["d"]; return q["k"]*(q["first"]+last)//2
    if k=="pg_term": return q["first"]*q["r"]**(q["k"]-1)
    if k=="pg_sum": return q["first"]*(q["r"]**q["k"]-1)//(q["r"]-1)
    if k=="sequence_mul": return q["a"]*2**(q["k"]-1)
    if k=="linear": return (q["c"]-q["b"])//q["a"]
    if k=="system": return (q["c"]-q["b"]*q["d"])//(q["a"]-q["b"])
    if k=="quadratic":
        s,pd=q["s"],q["prod"]; return min(x for x in range(0,pd+1) if x*(s-x)==pd)
    if k=="exponent_product": return q["base"]**(q["a"]+q["b"])
    if k=="polynomial_value": return q["a"]*q["x"]**2-q["b"]*q["x"]+q["c"]
    if k=="rectangle_area": return q["a"]*q["b"]
    if k=="triangle_area": return q["b"]*q["h"]//2
    if k=="pythagoras": return isqrt(q["a"]**2+q["b"]**2)
    if k=="polygon_sum": return (q["sides"]-2)*180
    if k=="regular_angle": return Fraction((q["sides"]-2)*180,q["sides"])
    if k=="diameter": return 2*q["r"]
    if k=="prism_volume": return q["a"]*q["b"]*q["h"]
    if k=="probability":
        f=Fraction(q["good"],q["total"]); return f"{f.numerator}/{f.denominator}"
    if k=="median": return sorted(q["values"])[len(q["values"])//2]
    if k=="mode": return max(set(q["values"]),key=q["values"].count)
    if k=="inverse_discount": return q["sale"]*100/Fraction(100-q["disc"])
    if k=="area_change": return Fraction((100+q["pct"])**2-100**2,100)
    if k=="gcd": return gcd(q["a"],q["b"])
    if k=="common_remainder": return q["d1"]*q["d2"]//gcd(q["d1"],q["d2"])+q["r"]
    if k=="near_hundred": return q["a"]*q["b"]
    if k=="difference_squares": return q["a"]**2-q["b"]**2
    if k=="fraction_remaining": return 1-q["used"]
    if k=="combined_rate": return Fraction(q["a"]*q["b"],q["a"]+q["b"])
    if k=="age_equation": return q["mult"]*(q["now"]+q["future"])-q["future"]
    if k=="purchase_system": return Fraction(q["total"]-q["q"]*q["count"],q["p"]-q["q"])
    if k=="similarity_area": return q["small"]*q["factor"]**2
    if k=="diagonals": return q["sides"]*(q["sides"]-3)//2
    if k=="without_replacement": return Fraction(q["red"],q["red"]+q["blue"])*Fraction(q["red"]-1,q["red"]+q["blue"]-1)
    if k=="weighted_mean": return Fraction(q["a"]*q["wa"]+q["b"]*q["wb"],q["wa"]+q["wb"])
    raise ValueError(k)

def validate():
    required={"n","id","tema","sub","family","dif","target","enun","opts","ans","steps","idea","hint","trap","origin","source","params"}
    errors=[]
    canonical = [json.dumps({k:v for k,v in p['params'].items() if k!='expected'},sort_keys=True,default=str) for p in PROBLEMS_GENERATED]
    if len(set(canonical))!=len(canonical): errors.append('Repeated mathematical parameters')
    if len({p['enun'] for p in PROBLEMS_GENERATED})!=len(PROBLEMS_GENERATED): errors.append('Repeated statements')
    for p in PROBLEMS_GENERATED:
        if required-set(p): errors.append(f"{p.get('id')}: schema")
        if len(p["opts"])!=4 or len(set(p["opts"]))!=4: errors.append(f"{p['id']}: options")
        if not 0<=p["ans"]<4 or p["opts"][p["ans"]]!=p["params"]["expected"]: errors.append(f"{p['id']}: answer index")
        if not 2<=len(p["steps"])<=4: errors.append(f"{p['id']}: steps")
        computed=str(result(p)).replace("-", "−")
        if computed!=p["params"]["expected"]: errors.append(f"{p['id']}: math {result(p)}")
        if not 30<=p["target"]<=150 or p["dif"] not in (1,2,3): errors.append(f"{p['id']}: metadata")
    assert len(PROBLEMS_GENERATED)>=400
    if errors: raise AssertionError("\n".join(errors))
    print(f"OK: {len(PROBLEMS_GENERATED)} exercises; {len(set(p['family'] for p in PROBLEMS_GENERATED))} labelled families")
if __name__=="__main__": validate()
