'''
Created on 8.5.2017
TODO - packages not loaded but applicable
- geojson 
- shapely
- seaborn as sns
- shapely.wkt, wkt = http://www.geoapi.org/3.0/javadoc/org/opengis/referencing/doc-files/WKT.html

@author: Markus.Walden
'''
#Array
from datetime import datetime
import shapefile
import geopandas as gp
from geopandas import datasets
import pandas as pd
from shapely.geometry import Point


#SQL
import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker

#computer
import sys
from geographic import engineString

#map
import matplotlib.pyplot as plt

plt.style.use('bmh')
Base = declarative_base()

class GeographicNE(Base):
    '''
    classdocs
    '''
    __tablename__ = 'GeographicNE'
    index =  sqla.Column(sqla.Integer)
    continent =  sqla.Column(sqla.NVARCHAR(50))
    gdp_md_est = sqla.Column(sqla.Float)
    iso_a3 = sqla.Column(sqla.NVARCHAR(50), primary_key=True)
    name = sqla.Column(sqla.NVARCHAR(50))
    pop_est = sqla.Column(sqla.Float)
    geometry = sqla.Column(Geometry("POLYGON"))
    
    def __init__(self, params):
        '''
        Constructor
        '''
    def __repr__(self):
        #"(id='%s', Date='%s', Type='%s', Value='%s')" % (self.id, self.Date, self.Type, self.Value)
        return ""

class Cities(Base):
    __tablename__ = 'cities'
    name = sqla.Column(sqla.NVARCHAR(50), primary_key=True)
    geometry = sqla.Column(Geometry("POINT"))    

class Lake(Base):
    __tablename__ = 'lakes'
#    id = sqla.Column(sqla.Integer)
    name = sqla.Column(sqla.NVARCHAR(50), primary_key=True)
    depth = sqla.Column(sqla.Integer, default = 0)
    created = sqla.Column(sqla.DateTime, default=datetime.now())
    geom = sqla.Column(Geometry("POLYGON"))
                
def main():
    '''
    shapefileTest()
    ---------------
    - test to print shapefile content 
    - divided to two files dbf and shp
    - uses dictionaries as resultsets to contain data related to location and the location as polycon
    
    Using datasets geopandas for country and city statistics OR Using the gadm28 dataset  
    - http://stackoverflow.com/questions/31997859/bulk-insert-a-pandas-dataframe-using-sqlalchemy
    
    crs (coordinate system )
    
    http://stackoverflow.com/questions/3845006/database-of-countries-and-their-cities
    ''' 
    naturalEarthToCSV = False
    esriShapefileToGeopandas = False
    loadShapefileData = False
    combineDataForCities = True
    
    if naturalEarthToCSV:
        gp_world, gp_cities = generateWorldToDB(loadCSV = True)  
        print ('Countries: ', gp_world)
        print ('Cities: ', gp_cities)
        
    if esriShapefileToGeopandas:
        '''
         'OBJECTID', 'geometry', 'UID', 'ID_0', 'ISO', 'NAME_0', 
         'REGION', 'VARREGION', 'Shape_Leng', 'Shape_Area'
         
         'ID_1', 'NAME_1', 
         'ID_2', 'NAME_2', 
         'ID_3', 'NAME_3', 
         'ID_4', 'NAME_4', 
         'ID_5', 'NAME_5', 
        '''
        shp = gp.GeoDataFrame.from_file('./gadm28/gadm28.shp')
        shp_1 = shp[['OBJECTID', 'geometry']]
        shp = shp[['OBJECTID', 'UID', 'ID_0', 'ISO', 'NAME_0', 'REGION', 
                   'VARREGION', 'Shape_Leng', 'Shape_Area', 'ID_1', 'NAME_1','ID_2', 'NAME_2',
                   'ID_3', 'NAME_3', 'ID_4', 'NAME_4', 'ID_5', 'NAME_5']]
 
        #save X,Y into csv file
        shp.to_csv("./data/allData.csv",header=True,index=False,sep="\t")
        shp_1.to_csv("./data/allData_geom.csv",header=True,index=False,sep="\t")
        print (shp)
        
    if loadShapefileData:
        shapefileTest(i = 0, i_max = 50)
        
    if combineDataForCities: 
        '''
        cities: Country,City,AccentCity,Region,Population,Latitude,Longitude
            - Country, City, Population,Latitude,Longitude - link to add iso3 
        
        countrycodes: euname,modified,linked_country,iso3,iso2,grc,isonum,country,imperitive
            - country, iso3, iso2
            
        - define datasets
        - merge with country
        - add geometry  
        - store to csv  
        '''  
        df_cities = pd.read_csv("./data/worldcitiespop.csv", sep = ',', encoding = "ISO-8859-1", header = 0,  
                                names=['Country','City','AccentCity','Region','Population','Latitude','Longitude'])
        df_cities = df_cities[['Country','City','Region','Population','Latitude','Longitude']]
        df_cities.columns = ['iso2', 'City','Region','Population','Latitude','Longitude']
        df_cities['iso2'] = df_cities['iso2'].str.upper()
        df_cities = df_cities[df_cities['Population'] > 50000]
        
        df_countryCodes = pd.read_csv("./data/countryISO2, 3.csv", sep = ',', header = 0,
                                      names=['euname','modified','linked_country','iso3','iso2','grc','isonum','country','imperitive'])
        df_countryCodes = df_countryCodes[['country', 'iso3', 'iso2']]
        
        df_main = pd.merge(df_cities, df_countryCodes, on='iso2', how='inner')
        

        geometry = [Point(xy) for xy in zip(df_main.Longitude, df_main.Latitude)]
        crs = {'init': 'epsg:4326'}
        df_geo = gp.GeoDataFrame(df_main, crs=crs, geometry=geometry)
        
        print (df_geo)
        df_geo.to_csv("./data/allDataCities.csv",header=True,index=False,sep=",")

def generateWorldToDB(loadCSV = False, getAsPandasDataFrame = False):
    '''
    - Main test method, contains two cases and main body
    - The main issue is with handling geographic data. Since the available python libraries have no support for MSSQL. 
        Storing the data as csv maybe the best bet.
    - With conventional data the transformation works
    - The geometry type in SQL is image data with convert methods to coordinates or geometric shapes like polycon
    
    returns: datasets for countries, cities
    '''
    world = gp.read_file(datasets.get_path('naturalearth_lowres'))
    cities = gp.read_file(datasets.get_path('naturalearth_cities'))
    
    if loadCSV:
        world.to_csv('./data/countries.csv', sep='\t')
        cities.to_csv('./data/cities.csv', sep='\t')
        return world, cities
        
    if getAsPandasDataFrame:
        df_countries = pd.read_csv('./data/countries.csv',sep='\t',  
                               index_col='iso_a3', names=['iso_a3', 'name','continent', 'gdp_md_est', 'geometry', 'pop_est'])
        df_cities = pd.read_csv('./data/cities.csv',  
                               index_col='name', names=['name', 'geometry'])
        return df_countries, df_cities
    
    else:   
        dbData = world.to_dict(orient = 'records')
        dbData_1 = cities.to_dict(orient = 'records')
        print ("original dataframe - countries: ", world)
        print ("original dataframe - cities: ", cities)

        tableNameA = 'GeographicNE'
        print (GeographicNE.__table__)
        
    # process for SQL    
        sql = sqla.create_engine(engineString)
        conn = sql.connect()
        
        metadata = sqla.schema.MetaData(bind=sql,reflect=True)
        table = sqla.Table(tableNameA, metadata, autoload=True)
        print (table)
        # Open the session
    
        Session= sessionmaker(bind=sql)
        session = Session()
        
        try:
            conn.execute(table.insert(), dbData) 
            world.to_sql(tableNameA, sql, if_exists='append')
        except:
            print ('Exception type:', sys.exc_info()[0])
            print ('Exception value:', sys.exc_info()[1])
            
        session.commit()
        session.close()
        return dbData, dbData_1

def shapefileTest(i = 0, i_max = 50):
    '''
    Loads gadm28 shapefile, containing geographical 
    - files: gadm28.shp, gadm28.dbf 
    - fields:  ['OBJECTID', 'UID', 'ID_0', 'ISO', 'NAME_0', 'ID_1', 'NAME_1', 'VARNAME_1', 
                'NL_NAME_1', 'HASC_1', 'CCN_1', 'CCA_1', 'TYPE_1', 'ENGTYPE_1', 'VALIDFR_1', 'VALIDTO_1', 
                'REMARKS_1', 'ID_2', 'NAME_2', 'VARNAME_2', 'NL_NAME_2', 'HASC_2', 'CCN_2', 'CCA_2', 'TYPE_2', 
                'ENGTYPE_2', 'VALIDFR_2', 'VALIDTO_2', 'REMARKS_2', 'ID_3', 'NAME_3', 'VARNAME_3', 'NL_NAME_3', 
                'HASC_3', 'CCN_3', 'CCA_3', 'TYPE_3', 'ENGTYPE_3', 'VALIDFR_3', 'VALIDTO_3', 'REMARKS_3', 'ID_4', 
                'NAME_4', 'VARNAME_4', 'CCN_4', 'CCA_4', 'TYPE_4', 'ENGTYPE_4', 'VALIDFR_4', 'VALIDTO_4', 'REMARKS_4', 
                'ID_5', 'NAME_5', 'CCN_5', 'CCA_5', 'TYPE_5', 'ENGTYPE_5', 'REGION', 'VARREGION', 'Shape_Leng', 
                'Shape_Area']
    
    location 
    - geometric
    - polygon + coordinates marking 
    '''        
    myshp = open("./gadm28/gadm28.shp", "rb")
    mydbf = open("./gadm28/gadm28.dbf", "rb")
    r = shapefile.Reader(shp=myshp, dbf=mydbf)
    
    fields = [field[0] for field in r.fields[1:]]
    print ('fields: ', fields)

    for feature in r.shapeRecords():
        try:
            geom = feature.shape.__geo_interface__
            atr = dict(zip(fields, feature.record))
            print ("geo_interface: ", geom)
            print ('feature record: ', atr)
        except:
            print ('Exception type:', sys.exc_info()[0])
            print ('Exception value:', sys.exc_info()[1])
        i = i + 1
        if i == 50:
            break
    return r 

def testSQLAlchemyORM():    
    '''
    - Use dumy example, lake class to test commit to database using native geometry type.
    - DOES not work with MSSQL, current implementation covers postgreSQL with postGIS
    '''
    print (Lake.__table__)
#    lake = Lake(name='Majeur')
    lake = Lake(name='Majeur', geom='POLYGON((0 0,1 0,1 1,0 1,0 0))')
#    print (lake.geom)
    
    sql = sqla.create_engine(engineString)
    conn = sql.connect()
    
    Session= sessionmaker(bind=sql)
    session = Session()
    try:
        session.add(lake)
        session.commit()
    except:
        print ('Exception type:', sys.exc_info()[0])
        print ('Exception value:', sys.exc_info()[1])
    session.close()
   
        
if __name__ == "__main__":
    main()      