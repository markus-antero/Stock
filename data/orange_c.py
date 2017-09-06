'''
Created on 2.5.2017

@author: Markus.Walden

in_data (Orange.data.Table)                    - Input data set bound to in_data variable in the script’s local namespace.
in_distance (Orange.core.SymMatrix)            - Input symmetric matrix bound to in_distance variable in the script’s local namespace.
in_learner (Orange.classification.Learner)     - Input learner bound to in_learner variable in the script’s local namespace.
in_classifier (Orange.classification.Learner)  - Input classifier bound to in_classifier variable in the script’s local namespace.
in_object (object)                             - Input python object bound to in_object variable in the script’s local namespace.
'''
import cmath 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Orange.data import (
    Table, 
    Domain, 
    ContinuousVariable, 
    DiscreteVariable 
    )
from sympy import (
    Rational,
    sqrt,
    Symbol,
    dsolve, 
    Eq, 
    Function,
    sin,
    limit,
    oo,
    log,
    exp,
    )
    
def initialize(in_data, in_learner, in_classifier, in_object):
    ora = ProcessOrange(in_data, in_learner, in_classifier, in_object)
    df_data = ora.makeOrangeTableToDataFrame()
    df_time = pd.DataFrame(pd.to_datetime(in_data.X [:, 0], unit='s'))
    df_data['Country Code'] = str(in_data[0]['country_code'])
    df_data['datetime'] = df_time[0]
    df_series = df_data.set_index(keys =['Country Code', 'datetime'], inplace = False)
    
    print (df_series)
    return df_data, df_series

def makeOutput(df):
    ot = OrangeTable()
    table = ot.df2table(df)
    return table
    
df_data, df_series = initialize(in_data, in_learner, in_classifier, in_object)
table = makeOutput(df_data)

print(type(table)) 
out_data = table
#print ("hello")

class ProcessOrange(object):
    '''
    classdocs
    '''
    def __init__(self, in_data, in_learner, in_classifier, in_object):
        '''
        Constructor
        '''
        self.in_data = in_data 
        self.in_learner = in_learner 
        self.in_classifier = in_classifier 
        self.in_object = in_object
        
    def makeOrangeTableToDataFrame(self):
        '''
        :param x: input.
        :type state: int.
        :returns:
        :raises: 
        '''
        object_names = self.in_object[1:]
        data = self.in_data.X
        
        print (type(object_names))
        print (type(data))
        
        df = pd.DataFrame(data[:, 2:], columns = object_names[1:])
        print (df)
        print (self.in_data[:, 0])
        return df

    def makeDfToOrangeTable(self, df):
        self.out_data = Table(df.as_matrix())

    def storeToSQL (self, df):
        return None


class Expression(object):
    '''
    classdocs
    '''
    def __init__(self, expr):
        '''
        Constructor
        expr = x**2 + sqrt(3)*x - Rational(1,3) - sympolic expression
        '''
        self.expr = expr
    
    
    def sympy_expr(self, x_val, x = Symbol('x')):
        return self.expr.subs(x, x_val)  


def main():
    testDiff()
    testLimit()

def testDiff():
    x = Symbol("x")
    f = Function("f")

    eq = Eq(f(x).diff(x), f(x))
    print("Solution for ", eq, " : ", dsolve(eq, f(x)))

    eq = Eq(f(x).diff(x, 2), -f(x))
    print("Solution for ", eq, " : ", dsolve(eq, f(x)))

    eq = Eq(x**2*f(x).diff(x), -3*x*f(x) + sin(x)/x)
    print("Solution for ", eq, " : ", dsolve(eq, f(x)))
    
    t = dsolve(eq, hint='1st_exact')
    print (t)
    
def testLimit():
    x = Symbol("x")

    print( limit(sqrt(x**2 - 5*x + 6) - x, x, oo), -Rational(5)/2 )
    print( limit(x*(sqrt(x**2 + 1) - x), x, oo), Rational(1)/2 )
    print( limit(x - sqrt(x**3 - 1), x, oo), Rational(0) )
    print( limit(log(1 + exp(x))/x, x, -oo), Rational(0) )
    print( limit(log(1 + exp(x))/x, x, oo), Rational(1) )
    print( limit(sin(3*x)/x, x, 0), Rational(3) )
    print( limit(sin(5*x)/sin(2*x), x, 0), Rational(5)/2 )
    print( limit(((x - 1)/(x + 1))**x, x, oo), exp(-2))

def testSolver():
    
    
    return None    

class OrangeTable(object):  
    '''
    Class structure 
    
    - https://stackoverflow.com/questions/26320638/converting-pandas-dataframe-to-orange-table
    '''
    
    def __init__(self):
        self.t = 0
#        super().__init__()
    
    def series2descriptor(self, d):
        if d.dtype is np.dtype("float") or d.dtype is np.dtype("int"):
            return ContinuousVariable(str(d.name))
        else:
            t = d.unique()
            t.sort()
            return DiscreteVariable(str(d.name), list(t.astype("str")))

    def df2domain(self,df):
        featurelist = [self.series2descriptor(df.iloc[:,col]) for col in range(len(df.columns))]
        return Domain(featurelist)
    
    def df2table(self, df):
        tdomain = self.df2domain(df)
        ttables = [self.series2table(df.iloc[:,i], tdomain[i]) for i in range(len(df.columns))]
        ttables = np.array(ttables).reshape((len(df.columns),-1)).transpose()
        return Table(tdomain , ttables)
    
    def series2table(self, series, variable):
        if series.dtype is np.dtype("int") or series.dtype is np.dtype("float"):
            series = series.values[:, np.newaxis]
            return Table(series)
        else:
            series = series.astype('category').cat.codes.reshape((-1,1))
            return Table(series)

if __name__ == '__main__':
    main()