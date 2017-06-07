'''
Created on 30.5.2017

@author: Markus.Walden
- https://developers.arcgis.com/authentication/accessing-arcgis-online-services/
'''
import requests  
import pandas as pd
import numpy as np


def main():
    return None
    
def getStockData():
#    df = df.sample(n = 20) # , frac, replace, weights, random_state, axis
#    result.fillna(method='ffill')

    df_stock = pd.read_csv('./data/stockFull.csv', sep = ';', encoding='latin-1', decimal=",")   
    df_symbol = pd.read_csv('./data/symbolLatLong.csv', sep = ';', encoding='latin-1', decimal=",", index_col = 'symbol')   

#    print (df_stock) 
    columnN = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    columnsNames = ['100ma', 'Adj Close', 'City', 'Latitude', 'Longitude', 'Volume', '﻿Date']
    grouped = df_stock.groupby("symbol")

    count = 0 
    result = pd.DataFrame()

    for key, value in df_stock.groupby("symbol").groups.items():
        print (key)
        df = grouped.get_group(key)
        df = df.reset_index()

        df_adj    = df[['Adj Close']].rename(columns={'Adj Close': key})
        df_volume = df[['Volume']].rename(columns={'Volume': key})
        df_100ma  = df[['100ma']].rename(columns={'100ma': key})
        
        if count == 0:
            result = df_adj.T
            count = 1
        elif count == 1:
            result = result.append (df_adj.T)
            
    result = result.dropna(axis=1, how='any')
    result.rename(columns={1 : 'a', 2 : 'b', 3 : 'c',4 :  'd',5 :  'e',6 :  'f',7 :  'g',8 :  'h',9 :  'i',10 :  'j'}, inplace=True)
    result.index.name = 'symbol'
    result.sort_index(inplace = True)
#    print (result)

    df_combined = result.merge(df_symbol, how='inner', left_index=True, right_index=True)
    print (df_combined)
    df_combined.to_csv('./data/StockDetail.csv')
    

def token(token, url):    
    '''
    - https://utility.arcgis.com/usrsvcs/appservices/PaxuIDwgHm34KeUH/rest/services/World/GeoenrichmentServer/GeoEnrichment/enrich
    '''
    params = {
    'f': 'json',
    'token': token,
    'studyAreas': '[{"geometry":{"x":-117.1956,"y":34.0572}}]'
    }
    
    url = 'https://utility.arcgis.com/usrsvcs/appservices/PaxuIDwgHm34KeUH/rest/services/World/GeoenrichmentServer/GeoEnrichment/enrich'
    data = requests.post(url, params=params)
    
    return data.json()


def get_token():
    params = {
        'client_id': "3hEOA0ytHFO2XH3w",
        'client_secret': "f3721c85ba2d4c919a792f6cf427ca8e",
        'grant_type': "client_credentials"
    }

    request = requests.get('https://www.arcgis.com/sharing/oauth2/token',
                           params=params)
    response = request.json()
    token = response["access_token"]
    return token

if __name__ == "__main__":
    main()