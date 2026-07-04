# -*- coding: utf-8 -*-
"""Helpers de tipografía matemática (HTML/CSS puro, sin librerías)."""

def fr(num, den):
    """Fracción vertical inline."""
    return f'<span class="fr"><span class="fn">{num}</span><span class="fd">{den}</span></span>'

def sq(x):
    """Raíz cuadrada con vínculo."""
    return f'<span class="sqrt"><span class="rad">&#8730;</span><span class="vin">{x}</span></span>'

def rt(idx, x):
    """Raíz n-ésima con índice."""
    return f'<span class="sqrt"><sup class="ridx">{idx}</sup><span class="rad">&#8730;</span><span class="vin">{x}</span></span>'

def v(x):
    """Variable en cursiva matemática."""
    return f'<i class="mv">{x}</i>'

def disp(x):
    """Bloque de ecuación destacada (display math)."""
    return f'<div class="disp">{x}</div>'

def mrow(*parts):
    return '<span class="mrow">' + ''.join(parts) + '</span>'

def hl(x):
    """Resaltado teal para el resultado clave dentro de una ecuación."""
    return f'<span class="hlm">{x}</span>'

def para(x):
    return f'<p>{x}</p>'

TIMES = '&nbsp;&times;&nbsp;'
CDOT = '&nbsp;&middot;&nbsp;'
ARROW = '&nbsp;&rarr;&nbsp;'
IMPL = '&nbsp;&rArr;&nbsp;'
PM = '&plusmn;'
NEQ = '&ne;'
LEQ = '&le;'
GEQ = '&ge;'
INF = '&infin;'
PI = '&pi;'
THETA = '&theta;'
DEG = '&deg;'
ANG = '&#8737;'   # ∡
TRIG = '&#9651;'  # △
