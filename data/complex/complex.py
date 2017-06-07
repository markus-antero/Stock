'''
Created on 27.4.2017

@author: Markus.Walden

Link
----
example library

- http://hplgit.github.io/primer.html/doc/pub/formulas/._formulas-bootstrap000.html#table_of_contents
- http://www2.clarku.edu/~djoyce/trig/ - trigonometri
- https://www2.clarku.edu/~djoyce/complex/ - complex numbers
- http://www.tigerjython.ch/engl/index.php?inhalt_links=navigation.inc.php&inhalt_mitte=simulationen/komplexezahlen.inc.php


TODO
    print (simplify (r1))
    print (expand (r1))
'''
import cmath 
import matplotlib.pyplot as plt
import numpy as np

from sympy import (
     symbols,
     solve,
     latex, 
     simplify, 
     expand,
     Eq,
     exp,
     plot)

def main ():
    examples()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    circ = plt.Circle((0.5, 0.5), radius=0.5, edgecolor='b', facecolor='None')
    ax.add_patch(circ)
    plt.show()
    polynomial()
    plotSymbolicEq()
    
    a = np.arange(5) + 1j*np.arange(6,11)
    plotInComplexNumbers(a)
    
    f = np.logspace(-2,4,10)
    y = makeToComplexForm(f)
        
def polynomial():
    a, b, c, x = symbols('a b c x')
    y = a*x**2 + b*x + c
    print (y)
    r1 = (-b + (b**2 - 4 * a*c)**0.5) / (2 * a)
    r2 = (-b - (b**2 - 4 * a*c)**0.5) / (2 * a)

    print (latex(r1))
    return r1, r2

def plotSymbolicEq():
    b1, b2, x = symbols('b1 b2 x')
    def calculateRoots():
        roots = solve([Eq(90*0.05+90*exp(b1-(b2*90))-90, 0.0), Eq(99*0.95+99*exp(b1-(b2*99))-99, 0.0)], [b1, b2])
        return roots
    roots = calculateRoots()
    f = x/(x+exp(b1-b2*x))
    res = {b1:roots.get(b1),b2:roots.get(b2)}
    plot(f.subs(res), (x, 0, 100))

def plotInComplexNumbers(a):
    for x in range(len(a)):
        plt.plot([0,a[x].real],[0,a[x].imag],'ro-',label='python')
        plt.polar([0,np.angle(x)],[0,abs(x)],marker='o')
    limit=np.max(np.ceil(np.absolute(a))) # set limits for axis
    plt.xlim((-limit,limit))
    plt.ylim((-limit,limit))
    plt.ylabel('Imaginary')
    plt.xlabel('Real')
    plt.show()
    
def makeToComplexForm(f = np.logspace(-2,4,10)):
    print(f)
    tau=1.0
    omega=2*np.pi*f
    y=np.vectorize(complex)(1,omega*tau)
    print (y)
    return y
    
def examples():
    y = complex(2,3) 
    print ("real part: ", y.real) 
    print ("imag part: ", y.imag)
    print ("Squar: ", pow(y,2))
    print ("Distance: ", abs(y))
    print ("cmath sin: ", cmath.sin(y) )
    #six_DeMoivre(y)
    
if __name__ == '__main__':
    main()