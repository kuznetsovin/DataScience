# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from IPython.display import display, Latex

from sympy.interactive import printing
printing.init_printing(use_latex=True)

from __future__ import division
from sympy import *

# <codecell>

def answer(fu):
    answer = []
    last = fu
    prev = 1
    answer.append(fu.expand())
    while len(last.args) > 2:    
        first, last = last.as_two_terms()
        prev = Mul(prev,first)
        answer.append(Mul(prev, last.expand()))
        next
    answer.append(fu)
    for i in reversed(answer):
        print i

# <codecell>

x = symbols('x')
f = (x-3)*(x**2+3)*(x+7)
answer(f)

# <codecell>


