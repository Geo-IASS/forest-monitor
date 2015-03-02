# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Applying the Catenary Equation

# <headingcell level=2>

# Solving for known $T_h$

# <markdowncell>

# The equation for our cable from (0,z_1) to (w,z_2) will be of the form
# 
# $$
# z = z_c + a \cosh{ \frac{x + x_c}{a} } 
# $$
# 
# Increasing z_c and x_c shifts the curve up and to the right respectively.
# 
# a is simply the ratio between the horizontal component of cable tension and the weight per unit length of that cable.
# 
# $$
# a = \frac{f_t}{f_g}
# $$
# 
# We need to find xc so that the difference between 
# 
# $$
# a \cosh{ \frac{0 + x_c}{a} } 
# $$
# 
# and
# 
# $$
# a \cosh{ \frac{w + x_c}{a} } 
# $$
# 
# is 
# $$
# z_1 - z_2
# $$
# 
# 
# $$
# a \cosh{ \frac{0 + x_c}{a} } - z_1 = a \cosh{ \frac{w + x_c}{a} }  - z_2
# $$
# 
# If we define z_2 - z_1 as z_d
# 
# $$
# a \cosh{ \frac{0 + x_c}{a} } = a \cosh{ \frac{w + x_c}{a} }  - z_d
# $$
# 
# 
# To solve this we'll use Sympy

# <codecell>

from IPython.display import display

from sympy.interactive import printing
printing.init_printing(use_latex='mathjax')

from __future__ import division
import sympy as sym

# <codecell>

# define our variables
xc, z1, z2, zc, zd, w, a = sym.symbols("xc z1, z2, zc zd w a")

# <codecell>

e = sym.Eq(a * sym.cosh((0 + xc)/a), a * sym.cosh((w + xc) / a) - zd)
e

# <codecell>

# Determine value of xc that statifies this...  
q = solve(e,xc)
q

# <markdowncell>

# Which would have been fun to derive manually.  Now convert this equation to Python, noting that we are dealing with real numbers and so we can only take the log of positive numbers.

# <codecell>

str = python(q)
print(str)

# <markdowncell>

# Cleaning this up we get:

# <codecell>

import numpy as np

class Cable:
    
    def __init__(self, a, w, z1, z2):
        zd = z2 - z1
        e2wa = np.exp(2 * w / a)
        ewa = np.exp(w / a)
        a2 = a ** 2

        q1 = (a2 * e2wa - 2 * a2 * ewa + a2 + zd ** 2 * ewa) * ewa
        q2 = (-2 * a * e2wa + 2 * a * ewa)
        q3 = zd / (a * (ewa - 1))
        self.xc = a * np.log(2 * np.abs(np.sqrt(q1) / q2) + q3)
        self.zc = z1 - a * np.cosh(self.xc / a)
        self.a = a
        
    def z(self, x):
        return self.zc + self.a * np.cosh((x + self.xc) / self.a)
    
    

# <codecell>

c = Cable(a=1, w=10, z1=5, z2=10)
print(c.z(0), c.z(10))

c = Cable(a=1, w=10, z1=5, z2=5)
print(c.z(0), c.z(10))

c = Cable(a=1, w=10, z1=10, z2=5)
print(c.z(0), c.z(10))


# <codecell>

%matplotlib inline
import matplotlib.pyplot as plt

plt.figure(figsize=(12,8))


z1 = 0
z2 = 5
w = 10
x = np.linspace(0,w)
for a in np.linspace(2, 15.0, num=15):
    c = Cable(a=a, w=w, z1=z1, z2=z2)
    z = c.z(x)
    plt.plot(x, z, 'b-')
    plt.plot(-c.xc, c.z(-c.xc), 'k*')
plt.plot([0, w],[z1, z2], 'ro')
plt.title('Cable under different tensions: minima marked')
    

# <markdowncell>

# As the cable is tensioned, it droops less and the low point shifts towards the lower anchor point.

# <headingcell level=2>

# Solving for Known $T_{total}$

# <codecell>

# define our variables
x, xc, zc, w, a = sym.symbols("x xc zc w a")

# <codecell>

e = a * sym.cosh((x + xc)/a) + zc
e

# <codecell>

sym.diff(e, x)

# <markdowncell>

# The vertical component of tension is given by:
# $$
# T_v = T_h \frac{\mathrm d z}{\mathrm d x}
# $$
# 
# and the total would be:
# 
# $$
# T_{total} = T_h \sqrt{ 1 + \Big( \frac{\mathrm d z}{\mathrm d x} \Big) ^2 }
# $$
# 
# So:
# 
# $$
# T_h = \frac{ T_{total} } { \sqrt{ 1 + \Big( \sinh{ \frac{x_c}{a} } \Big) ^2 } }
# $$

# <markdowncell>

# solve numerically so that 

# <codecell>

import cableStatics as cs

# <codecell>

reload(cs)
c = cs.Cable(z1=10, z2=5, w=10, unitWeight=0.35)
c.setHorizForce(10)
print(c.tension(0))
print(c.tension(5))
print(c.tension(10))

# <codecell>

reload(cs)
c = cs.Cable(z1=10, z2=5, w=10, unitWeight=0.35)
c.setTension(ten=12.21545251, x=0)
print(c.th)
c.setTension(ten=10.4654525134, x=10)
print(c.th)

# <codecell>


