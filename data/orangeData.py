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
import datetime as dt
import sqlalchemy as sqla

from sympy.plotting import (
    plot )

from Orange.data import (
    Table, 
    Domain, 
    ContinuousVariable, 
    DiscreteVariable 
    )
from sympy import (
    Rational, sqrt,
    Symbol, symbols, lambdify,
    dsolve,  Eq,  Function,
    sin, limit,  oo,
    log, exp, Limit
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
   
def sympyExpression():
    x, a, b, c = symbols('x a b c')
    em = Expression(expr = a * x**2 + b*sqrt(3)*x - c * Rational(1,3), x = x) 
    print (em.expr)

    substituteValues_1 = em.makeEquationUsingScalarDict(x = x, result = {a:29.39, b:12.39, c:2.39})
    substituteValues_2, lambda_x = em.makeEquationUsingNumpyVector(x_vals = np.linspace(0, 10, 100), x = x)
    print (substituteValues_2)
    return em.expr, substituteValues_1, substituteValues_2

def produceDictionary(dataFrame):
    return dataFrame.tail(1).T.to_dict()  

def produceNumpyVector(dataFrame, fieldName):
    numpyArray=dataFrame[[fieldName]].as_matrix()
    return numpyArray

def mapSymbolsIntoDataframe(dataframe):
    '''
    CPI Price, nominal' : a }, inplace=True)
    Central government debt, total (percentage of GDP) : b,
    Central government debt, total (current LCU) : c,
    Gross portfolio debt liabilities to GDP (percentage) : d,
    International debt issues to GDP (percentage) : e,
    GNI per capita, PPP (current international $) : f,
    GNI per capita, Atlas method (current US$) : g,
    GNI per capita growth (annual percentage) : h,
    GDP per capita (current US$) : aa,
    GDP per capita growth (annual percentage) : ab,
    Adjusted net national income per capita (current US$): ac,
    Adjusted net national income per capita (annual percentage growth) : ad,
    Unemployment, total (percentage of total labor force) (modeled ILO estimate) : ae,
    Unemployment, total (percentage of total labor force) (national estimate) : af
    '''
    a,b,c,d,e,f,g,h,aa,ab,ac,ad,ae,af = symbols('a b c d e f g h aa ab ac ad ae af') 
    columnNames = dataframe.columns.values.tolist()
    newColumnNames = [a,b,c,d,e,f,g,h,aa,ab,ac,ad,ae,af]
    dict_columns = dict(zip(columnNames, newColumnNames))
    
    dataframe.rename(columns=dict_columns, inplace=True)
    return dataframe, dict_columns  

def storeToSQL(dataFrame, engineString):
    reload = False
    databaseTable = 'results_27_09_17' 
    sql = sqla.create_engine(engineString)
    def loadAllCompanyDetailsToSQL(dataFrame,reload = False, databaseTable = 'companyStatistics'):
        try:
            if reload:
                conn = sql.connect()
                trans = conn.begin()
                conn.execute("truncate table [dbo].[" + databaseTable + "]")
                trans.commit()
                conn.close()
            dataFrame.to_sql(databaseTable, sql, if_exists='append')
            return True
        except:
            return False
    if loadAllCompanyDetailsToSQL(dataFrame,reload = reload, databaseTable = databaseTable):
        print ("done")
    else:
        print ("failed")
    
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

class OrangeTable(ProcessOrange):  
    '''
    Class structure 
    
    - https://stackoverflow.com/questions/26320638/converting-pandas-dataframe-to-orange-table
    '''
    def __init__(self):
        self.t = 0
    
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

class Expression(object):
    '''
    classdocs
    '''
    def __init__(self, expr, x = Symbol('x')):
        '''
        Constructor
        expr = x**2 + sqrt(3)*x - Rational(1,3) - sympolic expression
        '''
        self.expr = expr
        try:
            self.negativeLimit = Limit(expr, x , oo, dir = '-')
            self.positivveLimit = Limit(expr, x , oo, dir = '+')   
        except:
            print ('producing limit failed')
    
    def sympy_expr(self, x_val, x = Symbol('x')):
        return self.expr.subs(x, x_val)  
 
    def makeEquationUsingNumpyVector(self, x_vals, x):
        '''
        t = symbols('t')
        x = 0.05*t + 0.2/((t - 5)**2 + 2)
        x_vals = np.linspace(0, 10, 100), 
        y_vals = lam_x(x_vals)
        
        returns: y as output and lambda function
        '''
        lam_x = lambdify(x, self.expr, modules=['numpy'])
        y_vals = lam_x(x_vals)
               
        plt.plot(x_vals, y_vals)
        plt.ylabel("Speed")
        plt.show()
        return y_vals, lam_x

    def makeEquationUsingScalarDict(self, x, result = {"b1":29.3930964972769,"b2":0.327159886574049}):
        '''
        x, b1, b2 = symbols("i b1 b2") - defined for the expression
        result defined as variables to match the symbols defined for the expression
        f = x/(x+exp(b1-b2*x)) is an example statement, in which b1 and b2 are provided as results for the substituted values
        '''
        f = self.expr        
        substituteValues = f.subs(result)
        
        plot(substituteValues, (x, 0, 100))
        return substituteValues

def main():
    x, a, b, c = symbols('x a b c')
    em = Expression(expr = a * x**2 + b*sqrt(3)*x - c * Rational(1,3), x = x) 
    
    print ("for Original statement: ", em.expr)
    
    substituteValues_1 = em.makeEquationUsingScalarDict(x = x, result = {a:29.39, b:12.39, c:2.39})
    em.expr = substituteValues_1
    
    substituteValues_2, lambda_x = em.makeEquationUsingNumpyVector(x_vals = np.linspace(0, 10, 100), x = x)
    
    print ("For Algorithm: ", substituteValues_2, "\n\nWith Labda function", lambda_x)
    
    testNumpy()
    testScalar()
    testDiff()
    testLimit()
    
def testNumpy():
    t = symbols('t')
    x = 0.05*t + 0.2/((t - 5)**2 + 2)
    lam_x = lambdify(t, x, modules=['numpy'])
        
    x_vals = np.linspace(0, 10, 100)
    y_vals = lam_x(x_vals)
        
    plt.plot(x_vals, y_vals)
    plt.ylabel("Speed")
    plt.show()
    
def testScalar():
    x, b1, b2 = symbols("i b1 b2")

    f = x/(x+exp(b1-b2*x))
    res = {b1:29.3930964972769,b2:0.327159886574049}
    
    plot(f.subs(res), (x, 0, 100))

def testDiff():
    x = Symbol("x")
    f = Function("f")

    eq_1 = Eq(f(x).diff(x), f(x))
    print("Solution for ", eq_1, " : ", dsolve(eq_1, f(x)))

    eq_2 = Eq(f(x).diff(x, 2), -f(x))
    print("Solution for ", eq_2, " : ", dsolve(eq_2, f(x)))

    eq_3 = Eq(x**2*f(x).diff(x), -3*x*f(x) + sin(x)/x)
    print("Solution for ", eq_3, " : ", dsolve(eq_3, f(x)))
    
    t = dsolve(eq_1, hint='1st_exact')
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

if __name__ == '__main__':
    main()
    
    in_data = pd.DataFrame() 
    in_learner = pd.DataFrame() 
    in_classifier = pd.DataFrame() 
    in_object = pd.DataFrame()
    engineString = ""
    
    df_data, df_series = initialize(in_data, in_learner, in_classifier, in_object)
    storeToSQL(df_series, engineString)

    a,b,c,d,e,f,g,h,aa,ab,ac,ad,ae,af = symbols('a b c d e f g h aa ab ac ad ae af') 
    df_symbols, dict_columns = mapSymbolsIntoDataframe(df_data)
    #print (dict_columns)
    
    dict_scalar = produceDictionary(df_symbols)
    print (dict_scalar)
    
    np_vector = produceNumpyVector(df_symbols, fieldName = a)
    #print (np_vector)
    
    table = makeOutput(df_data)
    
    print(type(table)) 
    out_data = table
    