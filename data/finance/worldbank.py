'''
Created on 18.8.2017

- https://datahelpdesk.worldbank.org/knowledgebase/articles/889464-wbopendata-stata-module-to-access-world-bank-data
- https://datahelpdesk.worldbank.org/knowledgebase/topics/19286-world-development-indicators-wdi
- https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information
- https://datahelpdesk.worldbank.org/knowledgebase/articles/902061-climate-data-api
- https://datahelpdesk.worldbank.org/knowledgebase/articles/898614-api-aggregates-regions-and-income-levels

@author: Markus.Walden
'''

import wbdata
import pandas as pd
import sqlalchemy as sqla
import csv
import datetime
import sys

from data.finance import countryCodes, worldbankConfFile, engineString, countryStatistics

class WorldBankDataReader(object):
    '''
    classdocs
    used factors: GNI, GDP, Employment, income, consumption, Nominal, and debt
    
    metrics (symbol - meaning):
        CPTOTNSXN  -             CPI Price, nominal
        GC.DOD.TOTL.GD.ZS  -     Central government debt, total (percentage of GDP)
        GC.DOD.TOTL.CN  -        Central government debt, total (current LCU)
        GFDD.DM.10  -            Gross portfolio debt liabilities to GDP (percentage)
        GFDD.DM.07  -            International debt issues to GDP (percentage)
        NY.GNP.PCAP.PP.CD  -     GNI per capita, PPP (current international $)
        NY.GNP.PCAP.CD  -        GNI per capita, Atlas method (current US$)
        NY.GNP.PCAP.KD.ZG  -     GNI per capita growth (annual percentage)
        NY.GDP.PCAP.CD  -        GDP per capita (current US$)
        NY.GDP.PCAP.KD.ZG  -     GDP per capita growth (annual percentage)
        NY.ADJ.NNTY.PC.CD  -     Adjusted net national income per capita (current US$)
        NY.ADJ.NNTY.PC.KD.ZG  -  Adjusted net national income per capita (annual percentage growth)
        SL.UEM.TOTL.ZS  -        Unemployment, total (percentage of total labor force) (modeled ILO estimate)
        SL.UEM.TOTL.NE.ZS  -     Unemployment, total (percentage of total labor force) (national estimate)
    '''  
    
    def __init__(self, fileName):
        '''
        Constructor
        ''' 
        try:
            with open(fileName) as f:
                self.configurationParams = dict(filter(None, csv.reader(f, delimiter=';')))
                print (self.configurationParams)
        except:
            print ('Exception type:', sys.exc_info()[0])
            print ('Exception value:', sys.exc_info()[1])
                
        self.sql = sqla.create_engine(engineString)
            
    def setDateFilter (self, dateFilter):
        '''
        dateFilter = (datetime.datetime(1995, 1, 1), datetime.datetime(2015, 1, 1))
        '''
        self.data_date = dateFilter
        
    def setCountries(self, countries):
        '''
        countries = ["FI"]
        '''
        self.countries = countries
    
    def getAllCountryCodes(self):
        query = countryCodes
        df_countries = pd.read_sql_query(query, self.sql)
        countries = df_countries['iso_a3'].tolist()
        
        print (countries) 
        return countries
        
    def storeStatisticsToSQL(self, dfToStore, tableName = '[geographicNEStat]', reload = False ):

        if reload:
            conn = self.sql.connect()
            trans = conn.begin()
            conn.execute("truncate table [dbo]." + tableName )
            trans.commit()
            conn.close()
            print ('Truncate done, reloading table:')       
        try:
            dfToStore.to_sql(tableName , self.sql, if_exists='append')  
        except:
            print ('Exception type:', sys.exc_info()[0])
            print ('Exception value:', sys.exc_info()[1])

    @classmethod            
    def setDataFrame(cls, countries = ["FIN"],  data_date = (datetime.datetime(1995, 1, 1), datetime.datetime(2015, 1, 1))):    
        '''
        set up the indicator - {'NY.GNP.PCAP.CD':'GNI per Capita'}
        df = df.dropna()
        '''
        cls.setCountries(countries)
        cls.setDateFilter(dateFilter = data_date)
        countries = cls.getAllCountryCodes()
        
        indicators =  cls.configurationParams
         
        #grab indicators above for countires above and load into data frame
        for country in countries :
            df = wbdata.get_dataframe(indicators, country=cls.countries, convert_date=True, data_date = cls.data_date)
            df_describe = df.describe()
            df['country_code'] = country
            cls.storeStatisticsToSQL(dfToStore = df, tableName = 'geographicNE_Stat')
    
            
def main():
    '''
    setDataFrame() - available parameters
        countries = ["FI"] - List of countries
        fileName = 'mainConf.csv' - config file for ID attributes from the World Bank 
        data_date = (datetime.datetime(1995, 1, 1), datetime.datetime(2015, 1, 1)) - Date filter to limit the records
    

    get countrycodes to list
    load dataframe to SQL database - use test case.
        use date + countryId as key
    '''
    fileName = 'mainConf.csv'
    
    reader = WorldBankDataReader(fileName = fileName)
    reader.setDateFilter(dateFilter = (datetime.datetime(1995, 1, 1), datetime.datetime(2015, 1, 1)))    
    
    countries = reader.getAllCountryCodes()
    reader.setCountries(countries = countries)
    
    df_main, df_stat = reader.setDataFrame(reader = reader)    

    
if __name__ == '__main__':
    main()