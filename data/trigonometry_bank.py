"""48 ejercicios originales de trigonometría CEPRE, sin lectura o escritura al importar."""
from fractions import Fraction
from random import Random

TRIG_INDEX={"file":"Informacion/TRIGONOMETRÍA - PRISMA 2025 (1).pdf","page":5,"concept":"razones, cofunciones, identidades y ángulos compuestos del temario visual"}
TRIG_STYLE={"file":"Informacion/TRIGONOMETRÍA - PRISMA 2025 (1).pdf","page":6,"concept":"ejercicios visuales de triángulos rectángulos, tangente y simplificación"}
TRIPLES=((3,4,5),(5,12,13),(8,15,17),(7,24,25),(20,21,29),(12,35,37),(9,40,41),(28,45,53))
TRIG_APPLIED={**TRIG_STYLE,'page':10,'concept':'aplicaciones, elevación y depresión'}
TRIG_IDENTITIES={**TRIG_INDEX,'page':7,'concept':'razones e identidades en ángulos agudos'}
TRIG_COMPOUND={**TRIG_INDEX,'page':16,'concept':'ángulos compuestos y doble ángulo'}

def shown(v): return str(v).replace("-","−")
def steps(*xs): return [{"t":t,"d":d} for t,d in xs]
def options(answer, seed):
    if isinstance(answer,Fraction):
        d=Fraction(1,max(2,answer.denominator)); vals=[answer,answer+d,answer-d,answer+2*d]
    else: vals=[answer,answer+1,answer-1,answer+2]
    out=[]
    for v in vals:
        if shown(v) not in out: out.append(shown(v))
    while len(out)<4: out.append(str(len(out)+3))
    Random(seed).shuffle(out)
    return out,out.index(shown(answer))
def make(n,sub,family,dif,target,enun,answer,work,idea,hint,trap,source,kind,params):
    opts,ans=options(answer,n*73)
    bounded = (kind=='ratio' and params['ask']!='tan') or kind in ('complement','double_angle')
    if bounded:
        low = Fraction(-1) if kind=='double_angle' else Fraction(0)
        delta=Fraction(1,max(2,answer.denominator))
        candidates=[answer,1-answer,answer-delta,answer+delta,answer-2*delta,answer+2*delta,Fraction(0),Fraction(1,2),Fraction(1)]
        values=list(dict.fromkeys(x for x in candidates if low<=x<=1))[:4]
        opts=[shown(x) for x in values]; Random(n*73).shuffle(opts);ans=opts.index(shown(answer))
    return {"n":n,"id":str(n),"tema":"Trigonometría","sub":sub,"family":family,"dif":dif,"target":target,
      "enun":enun,"opts":opts,"ans":ans,"steps":work,"idea":idea,"hint":hint,"trap":trap,"origin":"generated","source":source,
      "params":params|{"kind":kind,"expected":shown(answer)}}

def ratios(n,i):
    op,adj,hyp=TRIPLES[i]; ask=("sen","cos","tan")[i%3]
    answer={"sen":Fraction(op,hyp),"cos":Fraction(adj,hyp),"tan":Fraction(op,adj)}[ask]
    return make(n,"Razones trigonométricas","trig_razones_pitagoricos",1,40,
      f"En un triángulo rectángulo, respecto del ángulo θ, el cateto opuesto mide {op}, el adyacente {adj} y la hipotenusa {hyp}. Halla {ask} θ.",answer,
      steps(("Ubica los lados",f"Para θ: opuesto={op}, adyacente={adj}, hipotenusa={hyp}."),("Aplica razón",f"{ask} θ = {shown(answer)}.")),
      "Nombra los lados respecto del ángulo marcado antes de elegir la razón.","Escribe O/A/H junto al ángulo θ.","No intercambies cateto opuesto y adyacente.",TRIG_STYLE,"ratio",{"op":op,"adj":adj,"hyp":hyp,"ask":ask})
def shadow(n,i):
    rise,run=((3,4),(4,3),(5,12),(8,15))[i%4]; shadow=run*(2+i); height=rise*(2+i)
    return make(n,"Tangente en triángulo rectángulo","trig_altura_sombra",2,65,
      f"Un poste proyecta una sombra horizontal de {shadow} m. El ángulo de elevación al extremo superior tiene tan θ={rise}/{run}. ¿Cuál es la altura del poste?",height,
      steps(("Relaciona altura y sombra",f"tan θ = altura/{shadow}."),("Despeja",f"altura = {shadow}×{rise}/{run} = {height} m.")),
      "La tangente conecta altura vertical con distancia horizontal.","Usa altura/sombra, no hipotenusa.","No uses seno si no conoces la hipotenusa.",TRIG_APPLIED,"shadow",{"rise":rise,"run":run,"shadow":shadow})
def fundamental(n,i):
    op,adj,hyp=TRIPLES[i]; answer=Fraction(hyp*hyp,adj*adj)
    return make(n,"Identidades fundamentales","trig_identidad_fundamental",2,65,
      f"Para un ángulo agudo θ se sabe que tan θ={op}/{adj}. Halla sec² θ.",answer,
      steps(("Usa identidad",f"1+tan²θ=sec²θ."),("Sustituye",f"1+({op}/{adj})² = {shown(answer)}.")),
      "La identidad convierte una razón conocida en otra sin dibujar de nuevo.","Eleva al cuadrado numerador y denominador.","No olvides el 1 de la identidad.",TRIG_IDENTITIES,"fundamental",{"op":op,"adj":adj})
def complementary(n,i):
    op,adj,hyp=TRIPLES[i]; answer=Fraction(op,hyp)
    return make(n,"Cofunciones","trig_complementarios",2,55,
      f"θ es agudo y sen θ={op}/{hyp}. Halla cos(90°−θ).",answer,
      steps(("Reconoce cofunción",f"cos(90°−θ)=sen θ."),("Sustituye",f"cos(90°−θ)={op}/{hyp}.")),
      "Los ángulos complementarios intercambian seno y coseno.","Observa que 90°−θ es complementario de θ.","No cambies el valor por cos θ: la cofunción conserva sen θ.",TRIG_INDEX,"complement",{"op":op,"hyp":hyp})
def double_angle(n,i):
    op,adj,hyp=TRIPLES[i]; choice=("sen","cos")[i%2]
    answer=Fraction(2*op*adj,hyp*hyp) if choice=="sen" else Fraction(adj*adj-op*op,hyp*hyp)
    formula="sen 2θ=2 senθ cosθ" if choice=="sen" else "cos 2θ=cos²θ−sen²θ"
    return make(n,"Ángulo doble","trig_angulo_doble",3,90,
      f"θ es agudo, sen θ={op}/{hyp} y cos θ={adj}/{hyp}. Halla {choice} 2θ.",answer,
      steps(("Elige identidad",formula+"."),("Sustituye",(f"2×{op}×{adj}/{hyp}²" if choice=='sen' else f"({adj}²−{op}²)/{hyp}²") + f" = {shown(answer)}.")),
      "Para doble ángulo, conserva seno y coseno como fracciones exactas.","No aproximes: los denominadores quedan al cuadrado.","No uses la fórmula de suma sin duplicar ambos ángulos.",TRIG_COMPOUND,"double_angle",{"op":op,"adj":adj,"hyp":hyp,"choice":choice})
def angle_sum(n,i):
    pairs=[(Fraction(1,3),Fraction(1,4)),(Fraction(1,2),Fraction(1,3)),(Fraction(2,5),Fraction(1,4)),(Fraction(3,5),Fraction(1,5)),(Fraction(1,5),Fraction(1,2)),(Fraction(2,3),Fraction(1,4)),(Fraction(3,4),Fraction(1,3)),(Fraction(2,5),Fraction(2,3))]
    a,b=pairs[i]; answer=(a+b)/(1-a*b)
    return make(n,"Suma de ángulos","trig_suma_angulos",3,90,
      f"α y β son agudos, tan α={shown(a)} y tan β={shown(b)}. Si α+β<90°, halla tan(α+β).",answer,
      steps(("Formula",f"tan(α+β)=(tanα+tanβ)/(1−tanα·tanβ)."),("Sustituye",f"({shown(a)}+{shown(b)})/(1−{shown(a)}·{shown(b)}) = {shown(answer)}.")),
      "La condición α+β<90° fija el dominio y evita una tangente indefinida.","Calcula primero el producto del denominador.","No sumes tangentes directamente.",TRIG_COMPOUND,"angle_sum",{"a":a,"b":b})

BUILDERS=[ratios,shadow,fundamental,complementary,double_angle,angle_sum]
PROBLEMS_TRIGONOMETRY=[builder(1401+8*f+v,v) for f,builder in enumerate(BUILDERS) for v in range(8)]
assert len(PROBLEMS_TRIGONOMETRY)==48 and len({p["id"] for p in PROBLEMS_TRIGONOMETRY})==48
