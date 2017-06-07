'''
Created on 12.4.2017

@author: Markus.Walden
'''

from data.finance.LoadDataYahoo import LoadDataFromSQL, StocksStatistics
from data.finance.addins.mlToFinance1 import LinkQuandl
from data.finance.addins.neuralNetTestModified import NeuralNetForward, plotSleepStudy, generateSampleData

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def main():
    '''
    Test utility for various 
    
    :returns:  None.
    :raises: AttributeError, KeyError
    '''
# load data from yahoo and use it
    testVisualization ()
    
# machine learning to finance
    lq = LinkQuandl()
    df = lq.createQuandlDataFrame(ticker = 'GOOGL', database = 'WIKI')
    X, X_lately, y = lq.produceForecast(df = df)
    forecast_set, clf, accurary = lq.forecastLinear(X = X, X_lately = X_lately, y = y)
    lq.visualizeForecast(clf = clf, accuracy = accurary, forecast_set = forecast_set, df = df)
    testLogic(lq)
    
# Neural network    
    x = NeuralNetForward.x/np.amax(NeuralNetForward.x, axis = 0)
    y = NeuralNetForward.y/100
    testX = NeuralNetForward.testX/np.amax(NeuralNetForward.testX, axis = 0)
    testY = NeuralNetForward.testY/100   
    plotSleepStudy(x, y)
    plotSleepStudy(testX, testY)
    
    allInputs, hoursSleep, hoursStudy = generateSampleData (sampleSize = 100, max = 10, min = 0)
    nn = NeuralNetForward(x = x, y = y)
    testNeuralNetForward(nn, x, y)
    
#principle coordinate analysis
    Utils.correlation(X)
    Utils.covariance(X)
    
    return None

def testVisualization ():  
    '''
    Visualization for stock data
    '''      
    for count in range(11):  
        df_main = LoadDataFromSQL.retrieveInSingleDataFrame_ALLCompanyData( queryUsingGigs = True, classifierID = count+1)   
        df_corr = StocksStatistics.correlationDf(df_main)
        fig, data = StocksStatistics.visualize_heatmap(df_corr, useRange = True, rangeMin = -1, rangeMax = 1 )
        fig.savefig("nba_corr{}.png".format(count))  
    
#    df_main = LoadDataFromSQL.retrieveInSingleDataFrame_ALLCompanyData(recordCount = 50)  
#    df_cov = StocksStatistics.covarianceDf(df_main)
#    fig, data = StocksStatistics.visualize_heatmap(df_cov, useRange = False)
#    fig.savefig("nba_cov.png")
    
    df_companyIds, ts_companyStock, df_companyStat = LoadDataFromSQL.retrieve_ALLCompanyData()
    data = LoadDataFromSQL(df_symbols = df_companyIds, ts_Stockdata = ts_companyStock, df_company = df_companyStat)
    
    for count, i in enumerate(ts_companyStock):
        rolmean = pd.rolling_mean(i, window=12)
        rolstd = pd.rolling_std(i, window=12)
        
       # orig = plt.plot(i, color='blue')
        mean = plt.plot(rolmean, color='red')
        std = plt.plot(rolstd, color='black')
        
        plt.legend(loc='best')
        plt.title('Rolling Mean & Standard Deviation')
        plt.show()
        
        if count == 10:
            break
        print (count)
        
def testLogic(lq):  
    '''
    Generate statistics needed for neural network
    
    Args:
        lq (LinkQuandl): object.
    
    '''
    xs, ys = lq.createDatabase(hm = 40, variance = 60, step = 2, correlation = 'pos')
    m,b = lq.bestFitSlope(xs, ys)
    
    regressionLine = [(m*x) + b for x in xs]
    
    predict_x = 10
    print ('predict y: ', (m * predict_x)+b)
    
    r_squared = lq.coefficientOfDetermination(ys_orig = ys, ys_line = regressionLine)
    print ("Coefficience: ", r_squared)
    
    plt.scatter(xs, ys)
    plt.plot(xs, regressionLine)
    plt.show()

def testNeuralNetForward(nn, x, y):
    '''
    Generate statistics needed for neural network
    
    Args:
        nn (NeuralNetForward): object.
        x :input
        y :output
        
    '''
    yHat = nn.forward(x)

    cost, time = nn.bruteforceCost(nn,y, x, iteration = 1500)
    print ("cost: {0} \nTime elapsed: {1}".format(cost, time))

    djdw1, djdw2, delta3, delta2 = nn.costFunctionPrime(x, y)
    print ("djdw1: {0} \ndjdw2: {1}".format(djdw1, djdw2))
    
    def f(x):
        return x**2

    epsilon = 1e-4
    xz = 1.5

    numericalGradient = (f(xz+epsilon)- f(xz-epsilon))/(2*epsilon)
    print ("numericalGradient: {0} \nxz: {1}".format (numericalGradient, 2*xz))

    numgrad = nn.computeNumericalGradient(x, y)
    print ("numericalGradient: {0}".format(numgrad))

def testPCA():
    '''
    Generate test array for Anomaly detection course
    
    :returns: list with instances for x1, x2.
    :raises: 
    '''
    x1 = [2.5, 0.5, 2.2, 1.9, 3.1, 2.3, 2, 1, 1.5, 1.1] 
    x2 = [2.4, 0.7, 2.9, 2.2, 3.0, 2.7, 1.6, 1.1, 1.6, 0.9]
    x = pd.DataFrame()
    x['x1'] = x1
    x['x2'] = x2
    x.plot()
    plt.show()
    print ('Current data:\n', x)   
    return x


def visualize_All_data(type = 'corr'):
    '''
    Visualize all Company data
        
    Kwargs:
        type (str): corr - correlation OR cov - covariance 
    '''
    _, _, df = LoadDataFromSQL.retrieve_ALLCompanyData()
    print (df.head())
        
    if type == 'corr':
        df_corr = df.corr()
        print (df_corr.head())
    else: 
        print ('not implemented')
        return
        
    data = df_corr.values
    fig = plt.Figure()
    ax = fig.add_subplot(1,1,1)
        
    heatmap = ax.pcolor(data, cmap=plt.cm.get_cmap('rainbow'))
    fig.colorbar(heatmap)
        
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)    
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
        
    column_labels = df_corr.columns
    row_labels = df_corr.index
        
    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1, 1)
    plt.show()

def testMain(companyID = 'TSLA'):
    '''
    Visualize Company stock data
        
    Kwargs:
        companyID (str): Ticker (symbol - TSLA) for company 
    '''
    
    #getDataFromYahoo()
    _, _, df = LoadDataFromSQL.retrieve_ALLCompanyData()
    print(df)
        
    #read company symbols
    df_smp = pd.read_csv('sAndP500.csv', sep = ';', encoding='latin-1') # (df_smp['symbol'] 
    
    #df_ohlc.reset_index(inplace = True)
    #df_ohlc['Date'] = df_ohlc['Date'].map(mdates, date2num)
    
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan = 1, colspan = 1, sharex = ax1)
    
    #candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup = 'g')
    #ax2.fill_between(df_volume.index.map(mdates, date2num), df_volume.values, 0)
    
    ax1.plot(df.index, df['Adj Close'])
    ax1.plot(df.index, df['100ma'])
    ax2.bar(df.index, df['Volume'])
    
    df.plot()
    plt.show()

class Utils(object):
    
    def __init__(self, foo, bar='baz'):
        '''
        This function does something
        
        Args:
            foo (str): We all know what foo does.
    
        Kwargs:
            bar (str): Really, same as foo.
        '''
    
    @staticmethod
    def covariance (X):
        '''
        :param state: Input.
        :type state: Array.
        :returns:  covariance matrix, standard deviation.
        :raises: 
        '''
        def std():
            X_std = StandardScaler().fit_transform(X)
            return X_std
        mean_vec = np.mean(std(), axis=0)
        cov_mat = (std() - mean_vec).T.dot((std() - mean_vec)) / (std().shape[0]-1)
        print('Covariance matrix \n%s' %cov_mat)
        return cov_mat, std()
    
    @staticmethod
    def correlation (X):
        '''
        :param state: Input.
        :type state: Array.
        :returns:  correlation matrix, standard deviation.
        :raises: 
        '''
        def std():
            X_std = StandardScaler().fit_transform(X)
            return X_std        
        cor_mat1 = np.corrcoef(std().T)
        print('Correlation matrix \n%s' %cor_mat1)
        return cor_mat1

if __name__ == '__main__':
    main()