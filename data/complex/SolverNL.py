'''
Created on 8.4.2017

@author: Markus.Walden
'''
from sklearn.preprocessing import StandardScaler
import scipy.optimize as opt
from numpy import cosh, zeros_like, mgrid, zeros
import matplotlib.pyplot as plt


from sympy import (
     symbols,   # define symbols for symbolic math
     diff,      # differentiate expressions
     integrate, # integrate expressions
     Rational,  # define rational numbers
     lambdify,  # turn symbolic expr. into Python functions
     solve,
     exp, 
     sin, 
     cos,
     latex
     )

class SolverDiff(object):
    '''
    classdocs
    http://hplgit.github.io/primer.html/doc/pub/formulas/._formulas-bootstrap007.html#sec:formula:sympy
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        
    @staticmethod
    def solverUsingDiff():
        '''
        Test method for sympy, test equation roots:
        - y = v0 * t - Rational(1,2) * g * t ** 2
            
        :return: symbolic equation for root(s)
        :rtype: symbolic
        '''
        t, v0, g = symbols('t v0 g')
        y = v0 * t - Rational(1,2) * g * t ** 2
        
        roots = solve(y,t)
        print (y.subs(t, roots[0]))
        return roots
    
    @staticmethod
    def taylorSeries():
        '''
        Test method for sympy, test equation taylor series:
        - y = v0 * t - Rational(1,2) * g * t ** 2
            
        :return: symbolic equation for taylor series(s)
        :rtype: symbolic
        '''
        t, v0, g = symbols('t v0 g')
        y = v0 * t - Rational(1,2) * g * t ** 2
        
        f = exp(t)
        o = f.series(t, 0, 3)
        print (latex(o))
        
        f = exp(sin(t))
        o = f.series(t, 0, 8)
        print (latex(o))
        
        return f        
    
    @staticmethod
    def symbolicMathTest():
        '''
        ValueError:  
            specify dummy variables for -g*t + v0. 
            If the integrand contains more than one free symbol, an integration variable should be supplied explicitly e.g., 
            integrate(f(x, y), x)

        :return: t, v0, g, dydt
        :rtype: time, initial, internal variable, time differential
        '''
        t, v0, g = symbols('t v0 g')
        y = v0 * t - Rational(1,2) * g * t ** 2
        try:
            dydt = diff(y,t)
            dydt2 = diff(y, t, t)  # 2nd derivative
            y2 = integrate(y, t)
            print ('y: ', y)
            print ('derivative of: dy/dt: ', dydt)
            print ('second derivative: ', dydt2)
            print ('y integral: ', y2)
        except ValueError: 
            print ('bugi')
        return t, v0, g, dydt

def main ():
    '''
    newton_krylov
    '''
    t, v0, g, dydt = SolverDiff.symbolicMathTest()
    v = lambdify([t, v0, g], dydt)
    
    roots = SolverDiff.solverUsingDiff()
    f = SolverDiff.taylorSeries()
    
    print (roots)

#    solver()
#    pq = PredictSVMOnQuandl()
#    pq.populateCompanyData(readClassifier = True, runList = False)
#    pq.df_main
#    pq.df_classifier
    
    return None
    #X_std = StandardScaler().fit_transform(X)
            
def solver():
    nx, ny = 75, 75
    hx, hy = 1./(nx-1), 1./(ny-1)

    P_left, P_right = 0, 0
    P_top, P_bottom = 1, 0
    
    def residual(P):
        d2x = zeros_like(P)
        d2y = zeros_like(P)
    
        d2x[1:-1] = (P[2:]   - 2*P[1:-1] + P[:-2]) / hx/hx
        d2x[0]    = (P[1]    - 2*P[0]    + P_left)/hx/hx
        d2x[-1]   = (P_right - 2*P[-1]   + P[-2])/hx/hx
    
        d2y[:,1:-1] = (P[:,2:] - 2*P[:,1:-1] + P[:,:-2])/hy/hy
        d2y[:,0]    = (P[:,1]  - 2*P[:,0]    + P_bottom)/hy/hy
        d2y[:,-1]   = (P_top   - 2*P[:,-1]   + P[:,-2])/hy/hy
    
        return d2x + d2y - 10*cosh(P).mean()**2
    
    guess = zeros((nx, ny), float)
    sol = opt.newton_krylov(residual, guess, method='lgmres', verbose=1)
    print('Residual: %g' % abs(residual(sol)).max())
    
    x, y = mgrid[0:1:(nx*1j), 0:1:(ny*1j)]
    plt.pcolor(x, y, sol)
    plt.colorbar()
    plt.show()
    
if __name__ == '__main__':
    main() 