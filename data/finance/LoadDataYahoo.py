'''
Created on 16.2.2017
Sharpe ratio, Asset classification, income statement, operation ration

James Chistopher

@author: Markus.Walden
'''
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import sqlalchemy as sqla
from yahoo_finance import Share
import re
import sys
import seaborn as sns

from data.finance import engineString, retrieve_company_data, retrieve_company_IDs 
from data.finance import companyStatistics, companyStatisticsWithClass, missing_records, companyDetails

style.use('ggplot')

class LoadDataFromSQL(object):
    '''
    classdocs
    Main queries
        retrieve_company_IDs = id query
        retrieve_company_data = data query
        missing_records = records not working
        
    Main goal is to load Id and data to pandas objects from SQL datasource
    
    visualize
        Correlation 
        Covariance 
    
    Linking 
        retrieve_company_IDs = self._df_symbols (dataFrame)
        retrieve_company_data = self.ts_Stockdata (timeSeries)
        companyStatistics = self.df_company (dataFrame)
         
    on the stocks data
    '''
    sql = sqla.create_engine(engineString)

    def __init__(self, df_symbols = pd.DataFrame(), ts_Stockdata = [], df_company = pd.DataFrame(), params=[]):
        '''
        Constructor
        '''
        self._df_symbols = df_symbols
        self.ts_Stockdata = ts_Stockdata
        self.df_company = df_company
        
    def to_dict(self):
        return {
            "symbols":self._df_symbols,
        }
    
    def __repr__(self):
        '''
        eval to turn back to dictionary
        '''
        return str(self.to_dict())    
    
    @classmethod
    def retrieve_ALLCompanyData (cls, readClassifier = False, runList = True):
        '''
        Loading company data - returning data 
        for specific id, type symbol - for all, type %
        
        Make stocksData to 
        '''
        print ("loading stocks to shared dataframe, recordset based on query:\n", cls.retrieve_company_IDs)
        
        query = retrieve_company_IDs
        df_companyIds = pd.read_sql_query(query, cls.sql)
        
        listStocks=[]
        query = sqla.text(retrieve_company_data)
        
        if runList:    
            for count ,item in enumerate(df_companyIds['symbol']):
                df_companyStock = pd.read_sql_query(query, cls.sql,  params={'symbol': item})
                ts = df_companyStock.set_index('Date')
                listStocks.append(ts)
                
                if count % 10 == 0:    
                    print ("Stocks loaded: ", count)
       
        if readClassifier:
            query = companyStatisticsWithClass
        else:
            query = companyStatistics
        
        df_companyStat = pd.read_sql_query(query, cls.sql)
        print ("\nstatistics loaded")
        
        return df_companyIds, listStocks, df_companyStat
    
    @classmethod
    def retrieveInSingleDataFrame_ALLCompanyData (cls, recordCount = 10, queryUsingGigs = False, classifierID = 1):
        
        print ("loading stocks to shared dataframe, recordset will contain {0} records".format(recordCount))
        '''
        cls.retrieve_company_data with symbol:
        SELECT S_data.[symbol], [Date], [Open], [High], [Low], [Close], [Volume], [Adj Close], [100ma] 
                            FROM [dbo].[SandP500_index_data] as S_data 
                                    inner join [dbo].[SandP500Index] as S  on S_data.symbol = S.symbol 
                            where S_data.symbol like :symbol order by S_data.[symbol], [Date]   
        '''
        if queryUsingGigs:
            ids = ''' SELECT class.[symbol], class.[GICS_Sector], class.[GICS_subIndustry], [classifierId], [CIK], [security] 
                      FROM [dbo].[SandP500GigsClassifier] as class inner join 
                          [dbo].[SandP500Index] c_index on c_index.symbol = class.symbol 
                      where [classifierId] = :id
                      order by [index] '''
            query = sqla.text(ids)
            df_companyIds = pd.read_sql_query(query, cls.sql, params={'id': str(classifierID)})
        else:    
            ids = ''' SELECT top {0} [symbol], [dateAdded], [CIK], [security] FROM [dbo].[SandP500Index] '''.format(recordCount)
            query = sqla.text(ids)
            df_companyIds = pd.read_sql_query(query, cls.sql)
        
        data = ''' SELECT S_data.[symbol], [Date], [Open], [High], [Low], [Close], [Volume], [Adj Close], [100ma] 
                            FROM [dbo].[SandP500_index_data] as S_data 
                                    inner join [dbo].[SandP500Index] as S  on S_data.symbol = S.symbol 
                            where S_data.symbol like :symbol order by S_data.[symbol], [Date] '''.format(recordCount)
        query = sqla.text(data)
        
        main_df = pd.DataFrame()
        for count ,item in enumerate(df_companyIds['symbol']):
            df_companyStock = pd.read_sql_query(query, cls.sql,  params={'symbol': item})
            if count == 0:
                main_df = df_companyStock
            else:
                main_df = main_df.merge(df_companyStock, how ='outer')
            
            if count % 10 == 0:    
                print ("Stocks loaded: ", count) 
        return main_df    
        
class LoadDataFromYahoo(LoadDataFromSQL):
    '''
    main metrics 
        Start time
        End time
        List to transfer (ID)
    Main goal is to update data in the SQL datasource
    
    SELECT distinct year =  DATEPART (yyyy,DATEADD(day,1 , max([Date]))),
                     month =  DATEPART (mm,DATEADD(day,1 , max([Date]))),
                     day =  DATEPART (dd,DATEADD(day,1 , max([Date]))),
                     date = DATEADD(day,1 , max([Date]))
                     FROM [finance].[dbo].[SandP500_index_data] where symbol like '%'
    '''
    
    latestUpload = '''SELECT distinct date = DATEADD(day,1 , max([Date]))
                     FROM [finance].[dbo].[SandP500_index_data] where symbol like '%'  '''
    
    symbols = pd.DataFrame() 
    start = dt.datetime(2000,1,1) 
    end = dt.datetime(2016,12,31)   
        
    def __init__(self, symbol ='', marketCap = 0.0, bookValue = 0.0, ebitda = 0.0, dividentShare = 0.0, dividentYield = 0.0, earningShare = 0.0,
                 bookPrice = 0.0, salesPrice = 0.0, earningsGrowth = 0.0, earningRatio = 0.0, date = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), params=[]): 
        '''
        Constructor
        '''
        super().__init__()
        self.symbol = symbol
        self.marketCap = marketCap
        self.bookValue = bookValue
        self.ebitda = ebitda
        self.dividentShare = dividentShare
        self.dividentYield = dividentYield
        self.earningShare = earningShare
        self.bookPrice = bookPrice
        self.salesPrice = salesPrice
        self.earningGrowth = earningsGrowth
        self.earningRation = earningRatio
        self.date = date

    def to_dict(self):
        '''
        Returns dictionary object
        '''
        return {
            'marketCapital': self.markeCap,        
            'bookValue': self.bookValue,
            'ebitda': self.ebitda,                                                                      # yahoo.get_ebitda(),
            'dividentShare': self.dividentShare,
            'DividentYield': self.dividentYield,
            'earningShare': self.earningsShare,
            'BookPrice': self.bookPrice,
            'SalesPrice': self.salesPrice,
            'earningsGrowth': self.earningGrowth,
            'earningsRatio': self.earningRatio,
            'symbol': self.symbol,
            'date': self.date,
        }
    
    def __repr__(self):
        '''
        eval to turn back to dictionary
        '''
        return str(self.to_dict())    
    
    @classmethod
    def getDataFromYahoo(cls, load_csv = False, reload = False, tableNameA = "SandP500_index_data", 
                         start = dt.datetime(2000,1,1), end = dt.datetime.today()):
        ''' 
            * read symbols from SQL 
            * Create a virtual table using sql alchemy
            * form into class
        '''
        cls.start = start
        cls.end = end
        
        if load_csv :
            df_smp = pd.read_csv('sAndP500.csv', sep = ';', encoding='latin-1') # (df_smp['symbol']  
        else:
            df_smp = cls.retrieveCompanyIds()
        
        if reload:
            conn = cls.sql.connect()
            trans = conn.begin()
            conn.execute("truncate table [dbo].[SandP500_index_data]")
            trans.commit()
            conn.close()
            print ('Truncate done, reloading table:')
         
        for item in df_smp['symbol']:
            df = web.DataReader(item, 'yahoo', cls.start, cls.end)
            df ['100ma'] = df['Adj Close'].rolling(window = 100, min_periods = 0).mean()
            df ['symbol'] = item
            df.to_sql(tableNameA, cls.sql, if_exists='append')   
            print (item)         
        print ('done - stocks data loaded')  

    @classmethod
    def retrieveCompanyIds (cls, getUnloadedCompanies = False ):
        '''
        Load company Id:s
        Runs a query: 'SELECT [symbol],[dateAdded], [CIK] FROM [dbo].[SandP500Index]' to pandas dataFrame
        
        remaining fields: [security], [GICS_Sector], [GICS_subIndustry], [address], 
        '''
        if getUnloadedCompanies == False:
            query = retrieve_company_IDs
        else:
            query = missing_records
        df_company = pd.read_sql_query(query, cls.sql)
        return df_company
    
    @classmethod        
    def loadAllCompanyDetailsToSQL(cls, reload = False, databaseTable = 'companyStatistics', errorTable = 'errorStatistics', getUnloadedCompanies = False):
        df = cls.retrieveCompanyIds(getUnloadedCompanies)
        
        companies = []
        df_errorCompanies = {}
        for item in df['symbol']:
            c, df_error, e = cls.loadKeyStatistics(companyID = item)
            if e == None:
                companies.append(c)
            else:
                df_errorCompanies.update({item: df_error})
            print ('Symbol: ' + item)
        print ('done')
        
        if reload:
            conn = cls.sql.connect()
            trans = conn.begin()
            conn.execute("truncate table [dbo].[" + databaseTable + "]")
            trans.commit()
            conn.close()
        
        df_c = pd.DataFrame.from_records([l.to_dict() for l in companies])
        df_c.to_sql(databaseTable, cls.sql, if_exists='append')
        
        return df_errorCompanies
    
    @classmethod
    def loadKeyStatistics (cls, companyID = 'A'):
        '''
        dataset 
        df= pd.DataFrame(columns=['marketCapital','bookValue','ebitda','dividentShare','DividentYield','earningShare',
                                  'BookPrice','SalesPrice','earningsGrowth','earningsRatio', 'symbol', 'date'])
        '''
        yahoo = Share(companyID)
        print (type (yahoo))
        yahoo.refresh()
       
        try:    
            a = re.search('[a-zA-Z]+', yahoo.get_market_cap())
            b = re.search('[a-zA-Z]+', yahoo.get_ebitda())
    
            if a.group(0) is not None:
                p = re.split('[a-zA-Z]+', yahoo.get_market_cap())
                if a.group(0) in 'B':
                    marketCap = float(p[0]) * 10 ** 9
                elif a.group(0) in 'M':
                    marketCap = float(p[0]) * 10 ** 6
                else: 
                    marketCap = -1
                print ('Market cap: ' + yahoo.get_market_cap())
            else:
                marketCap = yahoo.get_market_cap()
        
            if b.group(0) is not None:    
                p = re.split('[a-zA-Z]+', yahoo.get_ebitda())
                if b.group(0) in 'B':
                    ebitda = float(p[0]) * 10 ** 9
                elif b.group(0) in 'M':
                    ebitda = float(p[0]) * 10 ** 6
                else: 
                    ebitda = -1
                
                print ('Ebitda: ' +yahoo.get_ebitda())
            else:
                ebitda =  yahoo.get_ebitda()
    
        except (TypeError, AttributeError):
            print ('Missing :' + companyID)
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )
            ebitda = -1.0
            marketCap = -1.0
        
        try:
            company = LoadDataFromYahoo(symbol = companyID, marketCap = marketCap, bookValue = float(yahoo.get_book_value()), ebitda = ebitda, 
                                   dividentShare = float(yahoo.get_dividend_share()), dividentYield = float(yahoo.get_dividend_yield()), earningShare = float(yahoo.get_earnings_share()),
                                   bookPrice = float(yahoo.get_price_book()), salesPrice = float(yahoo.get_price_sales()), earningsGrowth = float(yahoo.get_price_earnings_growth_ratio()),
                                   earningRatio = float(yahoo.get_price_earnings_ratio()))
            
            return company, yahoo, None
        except :
            print ('Missing :' + companyID)
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )
            return None, yahoo, e
      
class ClassificationStocks(LoadDataFromSQL):
    
    gigsClassifier = ''' SELECT distinct [GICS_Sector] FROM [finance].[dbo].[SandP500Index] '''         # 11
    gigsSubClassifier = ''' SELECT distinct [GICS_subIndustry] FROM [finance].[dbo].[SandP500Index] ''' # 124
    category = "S&P"
    
    def __init__(self, classifier= {}, region = category):
        self.classifier  = classifier
        
    @classmethod    
    def loadGigsClassifier (cls, classifier = 'gigs'):
        print ("loading stocks to shared dataframe, recordset based on query:\n", cls.gigsClassifier)        
        query = cls.gigsClassifier
        df_classifier = pd.read_sql_query(query, cls.sql)
        return df_classifier
    
    @classmethod
    def createDataSetsBasedOnGigs(cls):
        df_classifier = cls.loadGigsClassifier(classifier = 'gigs')
        query = sqla.text(companyDetails)
        classCompanies = {}
        for _ ,item in enumerate(df_classifier['GICS_Sector']):
            df_companyStock = pd.read_sql_query(query, cls.sql,  params={'gigs': item})
            classCompanies.update({item: df_companyStock})
        return classCompanies
    
    @classmethod
    def storeGigsClassifier(cls, reload = False, tableName = "SandP500GigsClassifier"):
        if reload:
            conn = cls.sql.connect()
            trans = conn.begin()
            conn.execute("truncate table [dbo].[" + tableName + "]")
            trans.commit()
            conn.close()
        
        companyDetails = '''SELECT c_index.[symbol],[GICS_Sector], [GICS_subIndustry]
                        FROM [finance].[dbo].[SandP500Index] as c_index
                                inner join [finance].[dbo].[companyStatistics] as stat on c_index.symbol = stat.symbol
                        where [GICS_Sector] like :gigs '''

        df_classifier = cls.loadGigsClassifier(classifier = 'gigs')
        query = sqla.text(companyDetails)
        for count ,item in enumerate(df_classifier['GICS_Sector']):
            df_companyStock = pd.read_sql_query(query, cls.sql,  params={'gigs': item})
            df_companyStock['classifierId'] = str(count + 1)
            df_companyStock.to_sql(tableName, cls.sql, if_exists='append')
        
      
class StocksStatistics(object):
    '''
    Add visualization for candlestic
    '''
    
    index_performance = ''' SELECT [year] ,[indexChange]  ,[totalAnnualReturn] FROM [finance].[dbo].[SandP500history] '''

    def __init__(self):
        print ("No instance variables or methods")

    @classmethod    
    def correlationDf(cls, df, index = 'Date', columns = 'symbol', values = 'Adj Close'):
        print (df.head())
        df_pivot = df.pivot(index=index, columns=columns, values=values)
        df_corr = df_pivot.corr()
        return df_corr
    
    @classmethod    
    def covarianceDf(cls, df, index = 'Date', columns = 'symbol', values = 'Adj Close'):
        print (df.head())
        df_pivot = df.pivot(index=index, columns=columns, values=values)
        df_cov = df_pivot.cov()
        return df_cov
        
    @classmethod    
    def visualize_heatmap(cls, df, useRange = True, rangeMin = -1, rangeMax = 1):   
        plt.clf()
        sns.set(font_scale=1.2)
        sns.set_style({"savefig.dpi": 100})
        column_labels = df.columns
        row_labels = df.index
        print ("\nColumn labels: {0} \n\nRow labels: {1}".format(column_labels, row_labels))
        data = df.values
        
        if useRange:
            ax = sns.heatmap(df, cmap=plt.cm.get_cmap('rainbow'), linewidths=.1, vmin = rangeMin, vmax = rangeMax) #  cmap=plt.cm.Blues
        else:
            ax = sns.heatmap(df, cmap=plt.cm.get_cmap('rainbow'), linewidths=.1) 
               
        ax.xaxis.tick_top()
        plt.xticks(rotation=90)
        plt.yticks(rotation=0)
        #ax.invert_yaxis()
        
        fig = ax.get_figure()
        return fig, data
        
def main ():
    '''
    Update S&p index
    
    update stocks data: 
        query latestUpload, add one day, store to datetime object, provide as start Date,
        set end date as current date 

    update company statistics, add date
    
    Load information into dataFrame and timeseries
    
    Make correlation and comparison
    '''
    runStockData = False
    runCompanyStat = False
    runGigsClassifier = False
    
    engine = LoadDataFromSQL.sql
    conn = engine.connect()
    start = conn.execute(LoadDataFromYahoo.latestUpload).fetchone()
    conn.close()
    
    yahoo = LoadDataFromYahoo()
    if runStockData:
        yahoo.getDataFromYahoo(load_csv = False, reload = False, tableNameA = "SandP500_index_data", start = start)
        print ("company data laoded")
    
    if runCompanyStat:
        '''
        handle error records
        '''
        errorRecords = yahoo.loadAllCompanyDetailsToSQL()
        print (errorRecords) 
        print ("company Stocks laoded")
        
    if runGigsClassifier:
        ClassificationStocks.storeGigsClassifier(reload = True)
        print ("Gigs classifier reinitiated")

    testClassifier()  
    
def testClassifier():
    companies = ClassificationStocks.createDataSetsBasedOnGigs()
    for count, item in enumerate(companies):
        df = companies.get(item)
        print ("dataset for {0}".format(item), df)
    print ("done")    
     
if __name__ == '__main__':
    main()