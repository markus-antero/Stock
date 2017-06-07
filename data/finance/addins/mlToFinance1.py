
from data.finance.LoadDataYahoo import LoadDataFromSQL, ClassificationStocks
import quandl, math
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, cross_validation, svm
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt
import statistics as st
import random

style.use('ggplot')

'''
Quandl
API Key Management
API Key: 2suZ1gv-896LK2WvuzaD

Manual
    https://www.quandl.com/docs/api#overview

Request 
    https://www.quandl.com/api/v3/datasets/WIKI/AAPL.csv?api_key=YOURAPIKEY
    
Key databases
    EOD: End-of-Day US Stock Prices
    SGE: Global Economic Indicators
    SF1: Core US Stock Fundamentals
    ZFC: Extended US Stock Fundamentals

Available databases
    https://www.quandl.com/browse?idx=database-browser_stock-data
'''

class LinkQuandl(object):
    '''
    classdocs
    use Stock - load statistics,
        mydata = quandl.get("FRED/GDP")
        mydata = quandl.get("FRED/GDP", start_date="2001-12-31", end_date="2005-12-31")
        mydata = quandl.get("EIA/PET_RWTC_D", collapse="monthly")
        mydata = quandl.get("FRED/GDP", transformation="rdiff")
        mydata = quandl.get_table('ZACKS/FC', paginate=True, ticker='AAPL', qopts={'columns': ['ticker', 'per_end_date']})              
        mydata = quandl.get('NSE/OIL', start_date='2010-01-01', end_date='2014-01-01',
                      collapse='annual', transformation='rdiff',
                      rows=4)
    File save    
        quandl.bulkdownload('EOD', filename='/my/path/EOD_DB.zip')
    
    '''

    def __init__(self, key = '2suZ1gv-896LK2WvuzaD'):
        '''
        Constructor
        API config
        '''
        self.key = key
        
    def createDatabase (self, hm, variance, step, correlation):
        val = 1
        ys = []
        
        for _ in range (hm):
            y = val + random.randrange(-variance, variance)
            ys.append(y)
            if correlation and correlation == 'pos':
                val += step
            elif correlation and correlation == 'neg':
                val -= step
        
        xs = [i for i in range (len (ys))]
        xs = np.array(xs, dtype = np.float)
        ys = np.array(ys, dtype = np.float)
        
        print ("x array: ", xs, "\ny array", ys)
        return xs, ys
    
    def bestFitSlope (self, xs, ys):
        m = ((st.mean(xs)) * st.mean(ys) - st.mean(xs*ys)) / ((st.mean(xs) ** 2 ) - st.mean(xs**2))
        b = st.mean(ys) - m*st.mean(xs)    
        return m, b
    
    def squaredError (self, ys_orig, ys_line):
        sum_y = sum((ys_line - ys_orig)**2)
        return sum_y
    
    def coefficientOfDetermination (self, ys_orig, ys_line):
        y_meanLine = [st.mean(ys_orig) for y in ys_orig]
        squarredErrorRegr = self.squaredError(ys_orig = ys_orig, ys_line = ys_line)
        squarredError_yMean = self.squaredError(ys_orig = ys_orig, ys_line = y_meanLine)
        coefficientDet = 1 - squarredErrorRegr / squarredError_yMean
        
        print ('coefficientDet: ', coefficientDet)
        return coefficientDet
    
    def createQuandlDataFrame (self, ticker = 'GOOGL', database = 'WIKI'):
        df = quandl.get(database + '/' + ticker)
        
        df = df [['Adj. Open', 'Adj. High', 'Adj. Close', 'Adj. Volume',]]
        df['HL_PCT'] = (df ['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100
        df['PCT_change'] = (df ['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100
        
        df = df[['Adj. Close', 'HL_PCT' , 'PCT_change', 'Adj. Volume']]
        return df
    
    def produceForecast (self, df, distance = 0.01, forecast_col = 'Adj. Close'):
        '''
        make df using createQuandlDataFrame
        returns regretion and accuracy
        Returns factor and label
        '''
        df.fillna(-9999, inplace = True)
        forecast_out = int(math.ceil(distance*len(df)))
        
        df['label'] = df[forecast_col].shift(-forecast_out)
        print(df.head(n = 10))
        
        X = np.array(df.drop(['label'], 1))
        X = preprocessing.scale(X)
        X_lately = X[-forecast_out:]
        X = X[:-forecast_out]
        
        df.dropna(inplace = True )
        y = np.array(df['label'])
        
        return X, X_lately, y
    
    def forecastLinear(self, X, X_lately, y, test_size = 0.2,  technique = 'linear'):
        '''
        make X, X_lately and y using produceForecast
        available techniques are linear and svm (support vector machnine)
        '''
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = test_size)
        
        if technique == 'linear':
            print ("Linear")
            clf = LinearRegression(n_jobs = -1)
        elif technique == 'svn':
            print ("Support Vector Machines")
            clf = svm.SVR()
        else: 
            print ("Not implemented, returning")
            return None
            
        clf.fit(X_train, y_train)
        accurary = clf.score(X_test, y_test)
        
        forecast_set = clf.predict(X_lately)
        print ("forecast: \n", forecast_set)
        print ("\nconfidence: ", accurary)
        
        return forecast_set, clf, accurary
    
    def visualizeForecast (self, clf, accuracy, forecast_set, df):
        '''
        df = ['Adj. Close', 'HL_PCT' , 'PCT_change', 'Adj. Volume']
        '''
        df['Forecast'] = np.nan
        last_date = df.iloc[-1].name
        last_unix = last_date.timestamp()
        one_day = 86400
        next_unix = last_unix + one_day
        
        for i in forecast_set:
            next_date = dt.datetime.fromtimestamp(next_unix)
            next_unix += one_day
            df.loc[next_date] = [np.nan for _ in range (len (df.columns) -1)] + [i]
        
        df['Adj. Close'].plot()
        df['Forecast'].plot()
        plt.legend(loc = 4)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()
        
        return df

class PredictSVMOnQuandl(LinkQuandl): 
    '''
    retrieve_ALLCompanyData
    '''
    
    def __init__(self):
        super().__init__()
        self.df_classifier = ClassificationStocks.loadGigsClassifier()
        
    def populateStockData(self, classificationCount = 3):
        '''
        Loads dataset on the daily interactions of companies in the stock market
        Available Classifiers:     symbol       Date    gigs
        Available features:        Open       High        Low      Close  Volume  Adj Close      100ma  
        '''
        for count in range(classificationCount):  
            if count == 0:
                self.df_main = LoadDataFromSQL.retrieveInSingleDataFrame_ALLCompanyData( queryUsingGigs = True, classifierID = count+1)
            else:
                self.df_main = self.df_main.merge(
                    LoadDataFromSQL.retrieveInSingleDataFrame_ALLCompanyData( queryUsingGigs = True, classifierID = count+1), how ='outer')
            print (count)
        print ("done")
    
    def populateCompanyData(self, readClassifier = True, runList = False):
        '''
        LoadDataFromSQL.retrieve_ALLCompanyData()
        :returns: df_companyIds: self.df_IDs - Id fields
                  listStocks: self.df_features - timeseries dataframe
                  df_companyStat: df_main - complete dataframe with features and classifiers
        '''      
        self.df_IDs, self.df_features, self.df_main = LoadDataFromSQL.retrieve_ALLCompanyData(readClassifier, runList)
                
    def SupportVectorMachineAsAutomated(self, test_size = 0.2):
        #print (self.df_classifier)
        #print (self.df_main)
        
        #df = self.df_main[['marketCapital', 'dividentShare', 'DividentYield' ,'earningsGrowth',  'earningsRatio', ]]
        df = self.df_main[[ 'earningsGrowth',  'earningsRatio','dividentShare']]
        
        X = np.array(df)
        y = np.array(self.df_main['classifierId'])
        
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = test_size)
        clf = svm.SVR()
        
        clf.fit(X_train, y_train)
        accurary = clf.score(X_test, y_test)
        
        #forecast_set = clf.predict(X_lately)
        #print ("forecast: \n", forecast_set)
        print ("\nconfidence: ", accurary)
        return  clf, accurary 

def main():
    pq = PredictSVMOnQuandl()
    pq.populateCompanyData(readClassifier = True, runList = False)
    pq.SupportVectorMachineAsAutomated()
    
if __name__ == '__main__':
    main()      