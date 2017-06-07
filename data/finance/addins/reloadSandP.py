'''
Created on 18.1.2017
@author: Markus.Walden
'''
from datetime import datetime
import datetime as dt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import sqlalchemy as sqla
from yahoo_finance import Share
import re
import sys
from data.finance import engineString, retrieve_company_data, retrieve_company_IDs

style.use('ggplot')

class LoadYahooFinance(object):
    
    start = dt.datetime(2000,1,1) 
    end = dt.datetime(2016,12,31)
    
    engine = sqla.create_engine(engineString)

    def __init__(self, symbol ='', marketCap = 0.0, bookValue = 0.0, ebitda = 0.0, dividentShare = 0.0, dividentYield = 0.0, earningShare = 0.0,
                 bookPrice = 0.0, salesPrice = 0.0, earningsGrowth = 0.0, earningRatio = 0.0, date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')): 
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

    def getInstanceDictionary(self):
        '''
        for loadKeyStatistics
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
        
    @classmethod
    def retrieveCompanyIds (cls ):
        '''
        Load company Id:s
        Runs a query: 'SELECT [symbol],[dateAdded], [CIK] FROM [dbo].[SandP500Index]' to pandas dataFrame
        
        remaining fields: [security], [GICS_Sector], [GICS_subIndustry], [address], 
        '''
        query = retrieve_company_IDs
        df_company = pd.read_sql_query(query, cls.engine)
        return df_company
    
    @classmethod
    def retrieve_ALLCompanyData (cls):
        '''
        Loading company data - returning data 
        for specific id, type symbol - for all, type %
        '''
        query = retrieve_company_data
        df_company = pd.read_sql_query(query, cls.engine)
        return df_company
    
    @classmethod
    def loadKeyStatistics (cls, companyID = 'A'):
        '''
        dataset 
        df= pd.DataFrame(columns=['marketCapital','bookValue','ebitda','dividentShare','DividentYield','earningShare',
                                  'BookPrice','SalesPrice','earningsGrowth','earningsRatio', 'symbol', 'date'])
        '''
        yahoo = Share(companyID)
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
            company = LoadYahooFinance(symbol = companyID, marketCap = marketCap, bookValue = float(yahoo.get_book_value()), ebitda = ebitda, 
                                   dividentShare = float(yahoo.get_dividend_share()), dividentYield = float(yahoo.get_dividend_yield()), earningShare = float(yahoo.get_earnings_share()),
                                   bookPrice = float(yahoo.get_price_book()), salesPrice = float(yahoo.get_price_sales()), earningsGrowth = float(yahoo.get_price_earnings_growth_ratio()),
                                   earningRatio = float(yahoo.get_price_earnings_ratio()))
            
            return company
        except TypeError:
            print ('Missing :' + companyID)
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )
        
    @classmethod        
    def loadAllCompanyDetailsToSQL(cls, reload = False, databaseTable = 'companyStatistics'):
        df = cls.retrieveCompanyIds()
        
        companies = []
        for item in df['symbol']:
            c = cls.loadKeyStatistics(companyID = item)
            companies.append(c)
            print ('Symbol: ' + item)
        print ('done')
        
        if reload:
            conn = cls.engine.connect()
            trans = conn.begin()
            conn.execute("truncate table [dbo].[" + databaseTable + "]")
            trans.commit()
            conn.close()
        
        df_c = pd.DataFrame.from_records([l.to_dict() for l in companies])
        df_c.to_sql(databaseTable, cls.engine, if_exists='append')  

class CompanyHistory (LoadYahooFinance):    
    '''
    stock data, derived 
    '''
    
    def __init__(self,  ):
        super().__init__()
        
    @classmethod
    def getDataFromYahoo(cls, load_csv = False, reload = False, tableNameA = "SandP500_index_data", 
                         start = dt.datetime(2000,1,1), end = dt.datetime(2016,12,31)):
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
            conn = cls.engine.connect()
            trans = conn.begin()
            conn.execute("truncate table [dbo].[SandP500_index_data]")
            trans.commit()
            conn.close()
            print ('Truncate done, reloading table:')
         
        for item in df_smp['symbol']:
            df = web.DataReader(item, 'yahoo', cls.start, cls.end)
            df ['100ma'] = df['Adj Close'].rolling(window = 100, min_periods = 0).mean()
            df ['symbol'] = item
            df.to_sql(tableNameA, cls.engine, if_exists='append')   
            print (item)         
        print ('done')  

def main():
    #visualize_All_data()
    
    df_ids = LoadYahooFinance.retrieveCompanyIds()
    print ('Symbols:\n', df_ids)
    
    companyDetails = []
    
    for item in df_ids['symbol']:
        c = LoadYahooFinance.loadKeyStatistics(companyID = item)
        companyDetails.append(c)        
        print ('Symbol: ' + item)
    print ('done')
    
    df_companyStock = LoadYahooFinance.retrieve_ALLCompanyData()
    print (df_companyStock)
    CompanyHistory.getDataFromYahoo(reload = True)
    
    LoadYahooFinance.loadAllCompanyDetailsToSQL(reload = True, databaseTable = 'companyStatistics')

if __name__ == '__main__':
    main()