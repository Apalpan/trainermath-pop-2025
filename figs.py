# -*- coding: utf-8 -*-
"""Figuras SVG de los problemas — líneas en tinta muted, acento teal solo en lo relevante."""
import math

def _pt(cx, cy, r, adeg):
    a = math.radians(adeg)
    return (cx + r*math.cos(a), cy - r*math.sin(a))

def arc(cx, cy, r, a1, a2, cls="ar"):
    """Arco de a1 a a2 en grados (convención matemática, y hacia arriba)."""
    x1, y1 = _pt(cx, cy, r, a1)
    x2, y2 = _pt(cx, cy, r, a2)
    large = 1 if abs(a2 - a1) > 180 else 0
    return f'<path class="{cls}" d="M {x1:.1f} {y1:.1f} A {r} {r} 0 {large} 0 {x2:.1f} {y2:.1f}"/>'

def line(x1, y1, x2, y2, cls="ln"):
    return f'<line class="{cls}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>'

def txt(x, y, s, cls="lb", anchor="middle"):
    return f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}">{s}</text>'

def poly(pts, cls="ln", closed=True):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    tag = "polygon" if closed else "polyline"
    return f'<{tag} class="{cls}" points="{d}"/>'

def svg(w, h, inner, label=""):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" '
            f'preserveAspectRatio="xMidYMid meet">{inner}</svg>')

def _ext(p, q, t0, t1):
    """Puntos extendidos de la recta p->q entre parámetros t0..t1."""
    return ((p[0]+(q[0]-p[0])*t0, p[1]+(q[1]-p[1])*t0),
            (p[0]+(q[0]-p[0])*t1, p[1]+(q[1]-p[1])*t1))

# ── P3: terreno con parcelas ──────────────────────────────────────
def fig3():
    x0, y0, w, h = 46, 26, 288, 180   # 1.5 px por metro
    cell = 12                          # 8 m
    g = [f'<rect class="ln" x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none"/>']
    for i in range(1, 24):
        g.append(line(x0+i*cell, y0, x0+i*cell, y0+h, "lngrid"))
    for j in range(1, 15):
        g.append(line(x0, y0+j*cell, x0+w, y0+j*cell, "lngrid"))
    g.append(f'<rect class="cellA" x="{x0}" y="{y0+h-cell}" width="{cell}" height="{cell}"/>')
    g.append(txt(x0+w/2, y0+h+22, "192 m"))
    g.append(txt(x0-24, y0+h/2+4, "120 m"))
    g.append(txt(x0+52, y0+h-18, "8 × 8", "lbA", "start"))
    return svg(380, 236, "".join(g), "Terreno de 120 por 192 dividido en parcelas cuadradas de 8 metros")

# ── P33: recta numérica ───────────────────────────────────────────
def fig33():
    def X(t): return 240 + t*58
    g = [line(30, 178, 452, 178), txt(456, 182, "&#8477;", "lb", "start")]
    for t in range(-3, 4):
        g.append(line(X(t), 173, X(t), 183))
        g.append(txt(X(t), 202, str(t), "lbdim"))
    def bar(t1, t2, y, cls, o1, o2, lab):
        p = [line(X(t1), y, X(t2), y, cls)]
        r = 4.5
        p.append(f'<circle class="{cls} {"dotO" if o1 else "dotC"}" cx="{X(t1):.1f}" cy="{y}" r="{r}"/>')
        p.append(f'<circle class="{cls} {"dotO" if o2 else "dotC"}" cx="{X(t2):.1f}" cy="{y}" r="{r}"/>')
        p.append(txt(X(t1)-16, y+4, lab, "lbdim", "end"))
        return "".join(p)
    g.append(bar(-2, 1, 46, "lnB", False, False, "A = [&#8722;2; 1]"))
    g.append(bar(-1, 3.4, 78, "lnB", False, True, "B = [&#8722;1; +&#8734;&#10217;"))
    g.append(bar(-3.4, 2, 110, "lnB", True, True, "C = &#10216;&#8722;&#8734;; 2&#10217;"))
    g.append(bar(1, 2, 145, "lnA", True, True, "(B&#8745;C) &#8722; A"))
    return svg(500, 214, "".join(g), "Recta numérica con los intervalos A, B, C y el resultado ]1;2[")

# ── P35: paralelas y poligonal ────────────────────────────────────
def fig35():
    L1y, L2y = 88, 292
    P1 = (156.9, L1y); P2 = (282.4, L1y)          # cruces con L1
    V3 = (329.4, 179.8); V2 = (292.0, 261.4)      # vértices
    P3 = (204.5, L2y)                              # cruce con L2
    s1a, s1b = _ext(P3, V2, -0.55, 1.55)           # tramo con θ
    s2a, s2b = _ext(V2, V3, -0.1, 1.75)            # tramo con 2θ
    s3a, s3b = _ext(V3, (258.0, 40.4), 0, 1.0)     # tramo con 3θ/12θ
    s4a, s4b = _ext(P1, V3, -0.35, 1.0)            # tramo con x/80°
    g = [line(25, L1y, 500, L1y), line(25, L2y, 500, L2y),
         txt(506, L1y+4, "L&#8321;", "lb", "start"), txt(506, L2y+4, "L&#8322;", "lb", "start"),
         line(*s1a, *s1b), line(*s2a, *s2b), line(*s3a, *s3b), line(*s4a, *s4b)]
    g += [arc(*P3, 30, 0, 18, "arA"), txt(248, 286, "&#952;", "lbA"),
          arc(*V2, 26, 18, 66, "arA"), txt(322, 238, "2&#952;", "lbA"),
          arc(*V3, 26, 66, 117, "arA"), txt(350, 148, "3&#952;", "lbA"),
          arc(*V3, 34, 117, 152, "ar"), txt(288, 152, "80&#176;", "lb"),
          arc(*P2, 26, 117, 180, "arA"), txt(240, 74, "12&#952;", "lbA"),
          arc(*P1, 26, -28, 0, "arX"), txt(196, 112, "x", "lbX")]
    return svg(540, 330, "".join(g), "Poligonal entre las paralelas L1 y L2 con ángulos θ, 2θ, 3θ, 80°, x y 12θ")

# ── P36: dos casos del isósceles ──────────────────────────────────
def fig36():
    g = []
    # Caso imposible 15-15-32
    bx1, bx2, by = 34, 208, 168
    g += [line(bx1, by, bx2, by),
          arc(bx1, by, 62, 10, 80, "lnB"), arc(bx2, by, 62, 100, 170, "lnB"),
          txt((bx1+bx2)/2, by+22, "32"), txt(66, 118, "15", "lbdim"), txt(178, 118, "15", "lbdim"),
          txt((bx1+bx2)/2, 66, "&#10007;", "lbX"),
          txt((bx1+bx2)/2, 206, "15 + 15 = 30 &lt; 32", "lbX")]
    # Caso válido 32-32-15
    cx1, cx2 = 330, 400.5; apx, apy = 365.25, 26
    g += [poly([(cx1, by), (cx2, by), (apx, apy)], "ln", True),
          txt((cx1+cx2)/2, by+22, "15"), txt(332, 96, "32", "lbdim"), txt(400, 96, "32", "lbdim"),
          txt(437, 108, "&#10003;", "lbA", "start"),
          txt(365, 206, "per&#237;metro = 79", "lbA")]
    return svg(500, 220, "".join(g), "Caso 15-15-32 imposible y caso 32-32-15 válido")

# ── P37: altura y bisectriz desde B ──────────────────────────────
def fig37():
    A, B, C = (36, 240), (176, 62), (400, 240)
    H = (176, 240)
    D = (216, 240)
    g = [poly([A, B, C], "ln"),
         line(*B, *H, "lnB"), line(*B, *D, "lnB"),
         f'<rect class="ra" x="{H[0]-11}" y="{H[1]-11}" width="11" height="11"/>',
         arc(*A, 34, 0, 45, "ar"), txt(84, 228, "45&#176;", "lbdim"),
         arc(*C, 40, 135, 180, "ar"), txt(346, 226, "75&#176;", "lbdim"),
         arc(*B, 44, 262, 297, "arA"), txt(198, 130, "15&#176;", "lbA"),
         txt(A[0]-10, A[1]+16, "A"), txt(B[0], B[1]-10, "B"), txt(C[0]+10, C[1]+16, "C"),
         txt(H[0]-14, 226, "H", "lbdim"), txt(D[0]+13, 226, "D", "lbdim"),
         txt(150, 158, "altura", "lbdim", "end"), txt(238, 168, "bisectriz", "lbdim", "start")]
    return svg(440, 268, "".join(g), "Triángulo con la altura y la bisectriz trazadas desde B")

# ── P38: triángulo ley de cosenos ────────────────────────────────
def fig38():
    A, B, C = (44, 196), (208, 60), (330, 196)
    g = [poly([A, B, C], "ln"),
         arc(*A, 40, 0, 40, "arA"), txt(102, 186, "30&#176;", "lbA"),
         txt(110, 118, "6", "lb"), txt(284, 118, "x", "lbX"),
         txt(187, 222, "4&#8730;3", "lb")]
    return svg(380, 240, "".join(g), "Triángulo con lados 6 y 4 raíz de 3 con ángulo 30 grados")

# ── P39: alturas AM y CN ─────────────────────────────────────────
def fig39():
    B, C, A = (60, 224), (336, 224), (144, 60)
    M = (144, 224)
    # pie de la perpendicular desde C a AB
    t = ((C[0]-B[0])*(A[0]-B[0]) + (C[1]-B[1])*(A[1]-B[1])) / ((A[0]-B[0])**2 + (A[1]-B[1])**2)
    N = (B[0]+t*(A[0]-B[0]), B[1]+t*(A[1]-B[1]))
    g = [poly([A, B, C], "ln"),
         line(*A, *M, "lnB"), line(*C, *N, "lnB"),
         f'<rect class="ra" x="{M[0]-11}" y="{M[1]-11}" width="11" height="11"/>',
         txt(A[0], A[1]-10, "A"), txt(B[0]-13, B[1]+14, "B"), txt(C[0]+13, C[1]+14, "C"),
         txt(N[0]-13, N[1]-4, "N"), txt(M[0]+4, M[1]+18, "M", "lbdim"),
         txt(86, 128, "5", "lb"), txt(122, 180, "3", "lbdim"),
         txt(240, 246, "6", "lb"), txt(102, 246, "BM = ?", "lbX")]
    return svg(390, 268, "".join(g), "Triángulo acutángulo con las alturas AM y CN")

# ── P40: trapecio isósceles ──────────────────────────────────────
def fig40():
    A, D = (50, 196), (358, 196)
    B, C = (138, 44), (270, 44)
    g = [poly([A, B, C, D], "ln"),
         line(B[0], B[1], B[0], 196, "lnB"), line(C[0], C[1], C[0], 196, "lnB"),
         arc(*A, 36, 0, 60, "arA"), txt(102, 186, "60&#176;", "lbA"),
         txt((B[0]+C[0])/2, 32, "6"), txt(74, 112, "8", "lb"),
         txt((A[0]+B[0])/2, 214, "4", "lbA"), txt((C[0]+D[0])/2, 214, "4", "lbA"),
         txt((B[0]+C[0])/2, 214, "6", "lbdim"),
         txt(A[0]-12, A[1]+16, "A"), txt(B[0]-12, B[1]-8, "B"), txt(C[0]+12, C[1]-8, "C"), txt(D[0]+12, D[1]+16, "D"),
         txt((A[0]+D[0])/2, 240, "AD = 4 + 6 + 4 = 14", "lbX")]
    return svg(410, 252, "".join(g), "Trapecio isósceles con base menor 6, laterales 8 y ángulo 60 grados")

# ── P42: prolongaciones desde B ──────────────────────────────────
def fig42():
    B, A, C = (52, 244), (102, 194), (122, 244)
    M = (A[0]+3*(A[0]-B[0]), A[1]+3*(A[1]-B[1]))   # (252, 44)
    P = (C[0]+3*(C[0]-B[0]), C[1])                  # (332, 244)
    g = [poly([A, C, P, M], "fillA"), poly([B, A, C], "fillB"),
         line(*B, *M), line(*B, *P), line(*A, *C, "lnB"), line(*M, *P, "lnB"),
         txt(B[0]-12, B[1]+6, "B"), txt(A[0]-14, A[1], "A"), txt(C[0]+2, C[1]+20, "C"),
         txt(M[0], M[1]-10, "M"), txt(P[0]+14, P[1]+6, "P"),
         txt(62, 212, "AB", "lbdim"), txt(190, 108, "AM = 3AB", "lbdim", "start"),
         txt(86, 262, "BC", "lbdim"), txt(225, 262, "CP = 3BC", "lbdim"),
         txt(82, 236, "30", "lbB"), txt(205, 180, "&#191;ACPM?", "lbX")]
    return svg(400, 290, "".join(g), "Triángulo ABC con prolongaciones hasta M y P; cuadrilátero ACPM sombreado")

# ── P43: mediana y ceviana ───────────────────────────────────────
def fig43():
    A, B, C = (94, 46), (40, 244), (372, 244)
    D = (B[0]+0.4*(C[0]-B[0]), 244)
    Mm = ((A[0]+C[0])/2, (A[1]+C[1])/2)
    # intersección P de AD con BM
    ax, ay = A; dx, dy = D[0]-ax, D[1]-ay
    bx, by = B; mx, my = Mm[0]-bx, Mm[1]-by
    det = dx*(-my) - (-mx)*dy
    tt = ((bx-ax)*(-my) - (-mx)*(by-ay)) / det
    Pp = (ax+tt*dx, ay+tt*dy)
    g = [poly([(B[0], B[1]), (D[0], D[1]), (Pp[0], Pp[1])], "fillA"),
         poly([A, B, C], "ln"),
         line(*A, *D, "lnB"), line(*B, *Mm, "lnB"),
         txt(A[0], A[1]-10, "A"), txt(B[0]-13, B[1]+14, "B"), txt(C[0]+13, C[1]+14, "C"),
         txt(D[0], D[1]+20, "D", "lbdim"), txt(Mm[0]+16, Mm[1]-2, "M", "lbdim"),
         txt(Pp[0]-4, Pp[1]-10, "P", "lb"),
         txt((B[0]+D[0])/2, 266, "2u", "lbdim"), txt((D[0]+C[0])/2, 266, "3u", "lbdim"),
         txt(118, 226, "8", "lbA")]
    return svg(420, 286, "".join(g), "Triángulo con mediana BM y ceviana AD; región BPD de 8 cm²")

# ── P44: rectángulo + semicírculo + diagonales ───────────────────
def fig44():
    x0, y0, x1, y1 = 30, 25, 370, 195
    cx, cy, r = 200, 195, 170
    semi = f'M {x0} {y1} A {r} {r} 0 0 1 {x1} {y1} Z'
    g = [f'<path class="fillA" d="{semi}"/>',
         poly([(x0, y1), (x1, y1), (cx, 110)], "fillCut"),
         f'<path class="ln" fill="none" d="M {x0} {y1} A {r} {r} 0 0 1 {x1} {y1}"/>',
         f'<rect class="ln" x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none"/>',
         line(x0, y0, x1, y1, "lnB"), line(x1, y0, x0, y1, "lnB"),
         txt(200, 90, "&#193;rea = 200", "lbdim")]
    return svg(400, 224, "".join(g), "Rectángulo con semicírculo inscrito y diagonales; semicírculo sombreado salvo el triángulo inferior")

# ── P45: dos cilindros ───────────────────────────────────────────
def _cyl(cx, top, rx, ry, h, cls="ln"):
    bot = top + h
    return (f'<ellipse class="{cls}" cx="{cx}" cy="{top}" rx="{rx}" ry="{ry}" fill="none"/>'
            f'<path class="{cls}" fill="none" d="M {cx-rx} {top} V {bot} A {rx} {ry} 0 0 0 {cx+rx} {bot} V {top}"/>'
            f'<path class="lndash" fill="none" d="M {cx-rx} {bot} A {rx} {ry} 0 0 1 {cx+rx} {bot}"/>')

def fig45():
    g = [_cyl(120, 78, 88, 20, 66), _cyl(330, 62, 66, 15, 88),
         line(120, 78, 120, 144, "lndashA"), line(330, 62, 330, 150, "lndashA"),
         line(120, 78, 208, 78, "lnB"), txt(164, 70, "r = 4", "lbdim"),
         txt(104, 118, "h = 3", "lbdim", "end"),
         line(330, 62, 396, 62, "lnB"), txt(363, 54, "r = 3", "lbdim"),
         txt(316, 112, "h = 4", "lbdim", "end"),
         txt(120, 196, "V&#8321; = 48&#960;", "lbA"), txt(330, 196, "V&#8322; = 36&#960;", "lb"),
         txt(120, 30, "gira sobre el lado 3", "lbdim"), txt(330, 30, "gira sobre el lado 4", "lbdim")]
    return svg(450, 212, "".join(g), "Dos cilindros generados al girar el rectángulo de 3 por 4")

# ── P46: cilindro y vaso tronco de cono ──────────────────────────
def fig46():
    g = [_cyl(110, 42, 54, 12, 178),
         f'<path class="fillA" d="M 56 60 V 220 A 54 12 0 0 0 164 220 V 60 A 54 12 0 0 1 56 60 Z"/>',
         txt(110, 34, "r = 6", "lbdim"), txt(42, 130, "30", "lbdim", "end"),
         # vaso tronco de cono
         f'<ellipse class="ln" cx="330" cy="120" rx="42" ry="10" fill="none"/>',
         f'<path class="ln" fill="none" d="M 288 120 L 309 192 A 21 5 0 0 0 351 192 L 372 120"/>',
         line(330, 120, 372, 120, "lnB"), txt(352, 112, "R = 4", "lbdim"),
         line(330, 192, 351, 192, "lnB"), txt(346, 210, "r = 2", "lbdim"),
         txt(386, 158, "h = 8", "lbdim", "start"),
         line(296, 146, 364, 146, "lndashA"), txt(374, 150, "&#190;", "lbA", "start"),
         txt(330, 240, "m&#225;x. 56&#960; por vaso", "lbA"), txt(110, 240, "1080&#960; cm&#179;", "lb")]
    return svg(460, 256, "".join(g), "Cilindro de agua y vaso en forma de tronco de cono llenado a tres cuartos")

# ── P47: cilindro inscrito en cubo ───────────────────────────────
def fig47():
    F = [(70, 90), (230, 90), (230, 250), (70, 250)]     # cara frontal
    o = (44, -44)
    Bk = [(x+o[0], y+o[1]) for x, y in F]
    g = [poly(F, "ln"), line(*F[0], *Bk[0], "ln"), line(*F[1], *Bk[1], "ln"), line(*F[2], *Bk[2], "ln"),
         line(*Bk[0], *Bk[1], "ln"), line(*Bk[1], *Bk[2], "ln"),
         line(*F[3], *Bk[3], "lndash"), line(*Bk[3], *Bk[0], "lndash"), line(*Bk[3], *Bk[2], "lndash"),
         f'<ellipse class="lnA" cx="172" cy="68" rx="80" ry="20" fill="none"/>',
         f'<path class="lnA" fill="none" d="M 92 68 V 228"/>',
         f'<path class="lnA" fill="none" d="M 252 68 V 228"/>',
         f'<path class="lnA" fill="none" d="M 92 228 A 80 20 0 0 0 252 228"/>',
         f'<path class="lndashA" fill="none" d="M 92 228 A 80 20 0 0 1 252 228"/>',
         txt(150, 274, "arista = 3", "lbdim"), txt(292, 160, "r = 3/2", "lbA", "start")]
    return svg(400, 292, "".join(g), "Cilindro inscrito en un cubo de arista 3")

# ── P48: semicírculo, rectángulo inscrito y segmento ─────────────
def fig48():
    O = (200, 190); r = 150; th = 48
    Cx, Cy = _pt(*O, r, th)
    Ax = 2*O[0] - Cx
    g = [f'<path class="fillA" d="M {Cx:.1f} {190} L {Cx:.1f} {Cy:.1f} A {r} {r} 0 0 1 {O[0]+r} 190 Z"/>',
         f'<path class="ln" fill="none" d="M {O[0]-r} 190 A {r} {r} 0 0 1 {O[0]+r} 190"/>',
         line(O[0]-r-14, 190, O[0]+r+14, 190),
         f'<rect class="ln" x="{Ax:.1f}" y="{Cy:.1f}" width="{Cx-Ax:.1f}" height="{190-Cy:.1f}" fill="none"/>',
         line(*O, Cx, Cy, "lnB"),
         arc(*O, 34, 0, th, "arA"), txt(O[0]+52, 178, "&#952;", "lbA"),
         txt((O[0]+Cx)/2+12, (190+Cy)/2-6, "2", "lb"),
         f'<circle class="dotC lb" cx="{O[0]}" cy="190" r="3"/>',
         txt(Ax-12, Cy+2, "B"), txt(Cx+13, Cy+2, "C"),
         txt(Ax-10, 210, "A"), txt(O[0], 212, "O"), txt(Cx+4, 212, "D"),
         f'<rect class="ra" x="{Ax:.1f}" y="{Cy:.1f}" width="10" height="10"/>',
         f'<rect class="ra" x="{Cx-10:.1f}" y="{Cy:.1f}" width="10" height="10"/>',
         f'<rect class="ra" x="{Cx-10:.1f}" y="180" width="10" height="10"/>'],
    return svg(410, 232, "".join(g[0]), "Semicircunferencia de radio 2 con rectángulo inscrito y región sombreada entre C y D")

# ── P49: ángulo llano y bisectrices ──────────────────────────────
def fig49():
    O = (210, 200); R = 168
    ang = dict(B=130, C=110, X=155, Y=55)
    Bp = _pt(*O, R, ang["B"]); Cp = _pt(*O, R, ang["C"])
    Xp = _pt(*O, R*0.98, ang["X"]); Yp = _pt(*O, R*0.98, ang["Y"])
    g = [line(30, 200, 396, 200),
         txt(22, 206, "A", "lb", "end"), txt(404, 206, "D", "lb", "start"), txt(O[0], 220, "O"),
         line(*O, *Bp, "ln"), line(*O, *Cp, "ln"),
         line(*O, *Xp, "lndashA"), line(*O, *Yp, "lndashA"),
         txt(Bp[0]-6, Bp[1]-8, "B"), txt(Cp[0], Cp[1]-8, "C"),
         arc(*O, 58, ang["Y"], ang["X"], "arA"), txt(198, 118, "100&#176;", "lbA"),
         arc(*O, 96, ang["C"], ang["B"], "arX"), txt(160, 92, "x", "lbX"),
         arc(*O, 26, ang["B"], 180, "ar"), arc(*O, 32, ang["X"], 180, "ar"),
         arc(*O, 26, 0, ang["C"], "ar"), arc(*O, 32, 0, ang["Y"], "ar"),
         txt(146, 178, "&#945;", "lbdim"), txt(122, 148, "&#945;", "lbdim"),
         txt(286, 178, "&#946;", "lbdim"), txt(272, 136, "&#946;", "lbdim")]
    return svg(430, 236, "".join(g), "Ángulos consecutivos sobre un ángulo llano con las bisectrices formando 100 grados")

# ── P50: cevianas AD y BE ────────────────────────────────────────
def fig50():
    A, B, C = (44, 226), (196, 44), (396, 226)
    D = (B[0]+0.55*(C[0]-B[0]), B[1]+0.55*(C[1]-B[1]))
    E = (A[0]+0.58*(C[0]-A[0]), 226)
    def tick(p, q, n=1):
        mx, my = (p[0]+q[0])/2, (p[1]+q[1])/2
        dx, dy = q[0]-p[0], q[1]-p[1]
        L = math.hypot(dx, dy); ux, uy = -dy/L, dx/L
        out = []
        for i in range(n):
            off = (i - (n-1)/2) * 7
            cxx, cyy = mx + dx/L*off, my + dy/L*off
            out.append(line(cxx-6*ux, cyy-6*uy, cxx+6*ux, cyy+6*uy, "lnB"))
        return "".join(out)
    g = [poly([A, B, C], "ln"), line(*A, *D, "lnB"), line(*B, *E, "lnB"),
         tick(A, B, 1), tick(D, C, 1), tick(A, D, 2), tick(C, E, 2),
         arc(*A, 36, 22, 50, "arA"), arc(*C, 36, 148, 176, "arA"),
         txt(A[0]-12, A[1]+14, "A"), txt(B[0], B[1]-10, "B"), txt(C[0]+13, C[1]+14, "C"),
         txt(D[0]+14, D[1]-4, "D"), txt(E[0], E[1]+20, "E", "lbdim")]
    return svg(440, 258, "".join(g), "Triángulo ABC con cevianas AD y BE, marcas de segmentos iguales")

# ── P51: taza semiesférica ───────────────────────────────────────
def fig51():
    cx, cy, rx, ry = 160, 66, 112, 26
    g = [f'<ellipse class="ln" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none"/>',
         f'<path class="fillA" d="M {cx-rx} {cy} A {rx} {rx} 0 0 0 {cx+rx} {cy} A {rx} {ry} 0 0 1 {cx-rx} {cy} Z"/>',
         f'<path class="ln" fill="none" d="M {cx-rx} {cy} A {rx} {rx} 0 0 0 {cx+rx} {cy}"/>',
         line(cx, cy, cx+rx, cy, "lnB"), txt(cx+54, cy-8, "r = 6", "lbdim"),
         f'<circle class="dotC lb" cx="{cx}" cy="{cy}" r="3"/>',
         txt(cx, 216, "S = 2&#960;r&#178;", "lbA")]
    return svg(330, 232, "".join(g), "Taza semiesférica de radio 6")

# ── P57: tabla de cereales (HTML) ────────────────────────────────
def fig57():
    return ('<table class="dtab"><caption>Consumo de cereales (kg)</caption>'
            '<tr><th>Trigo</th><td>25 200</td></tr>'
            '<tr><th>Cebada</th><td>9 000</td></tr>'
            '<tr><th>Arroz</th><td>15 800</td></tr>'
            '<tr class="tot"><th>Total</th><td>50 000</td></tr></table>')

# ── P58: histograma ──────────────────────────────────────────────
def fig58():
    x0, y0 = 70, 212          # origen
    bw, sc = 60, 7.5          # ancho de bin, px por alumno
    heights = [10, 20, 10, 16, 8]
    g = [line(x0, y0, x0, 34), line(x0, y0, x0+5*bw+26, y0)]
    for i, hh in enumerate(heights):
        x = x0 + i*bw
        g.append(f'<rect class="bar" x="{x+2}" y="{y0-hh*sc:.1f}" width="{bw-4}" height="{hh*sc:.1f}" rx="3">'
                 f'<title>[{50+10*i}; {60+10*i}&#10217; : {hh} alumnos</title></rect>')
        g.append(txt(x+bw/2, y0-hh*sc-8, str(hh), "lb"))
    for tv in range(8, 22, 2):
        g.append(line(x0-5, y0-tv*sc, x0, y0-tv*sc))
        g.append(txt(x0-10, y0-tv*sc+4, str(tv), "lbdim", "end"))
    for i in range(6):
        g.append(txt(x0+i*bw, y0+20, str(50+10*i), "lbdim"))
    g.append(line(x0, y0-20*sc, x0+bw+56, y0-20*sc, "lndash"))
    g.append(line(x0, y0-16*sc, x0+3*bw+56, y0-16*sc, "lndash"))
    g.append(txt(x0+2, 24, "# alumnos", "lbdim", "start"))
    g.append(txt(x0+5*bw+30, y0+20, "Notas", "lbdim", "start"))
    return svg(450, 252, "".join(g), "Histograma de notas: 10, 20, 10, 16 y 8 alumnos por rango de 50 a 100")

# ── P60: diagrama de árbol ───────────────────────────────────────
def fig60():
    g = [txt(56, 124, "100", "lb"),
         line(84, 114, 168, 66, "ln"), line(84, 130, 168, 182, "ln"),
         txt(206, 62, "ceviche: 60", "lb"), txt(214, 186, "no ceviche: 40", "lb"),
         line(268, 54, 330, 32, "ln"), line(268, 66, 330, 90, "ln"),
         line(286, 178, 330, 152, "ln"), line(286, 190, 330, 212, "ln"),
         txt(340, 36, "mujeres 40% &#8594; 24", "lbA", "start"),
         txt(340, 96, "hombres 60% &#8594; 36", "lbdim", "start"),
         txt(340, 154, "mujeres 60% &#8594; 24", "lbA", "start"),
         txt(340, 218, "hombres 40% &#8594; 16", "lbdim", "start"),
         txt(414, 124, "24 + 24 = 48 mujeres", "lbX", "middle")]
    return svg(560, 240, "".join(g), "Árbol: 60 con ceviche (24 mujeres) y 40 sin ceviche (24 mujeres)")

FIGS = dict(fig3=fig3(), fig33=fig33(), fig35=fig35(), fig36=fig36(), fig37=fig37(),
            fig38=fig38(), fig39=fig39(), fig40=fig40(), fig42=fig42(), fig43=fig43(),
            fig44=fig44(), fig45=fig45(), fig46=fig46(), fig47=fig47(), fig48=fig48(),
            fig49=fig49(), fig50=fig50(), fig51=fig51(), fig57=fig57(), fig58=fig58(),
            fig60=fig60())
