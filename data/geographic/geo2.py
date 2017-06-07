'''
Created on 29.5.2017

@author: Markus.Walden

arcgis manuals
- https://github.com/Esri/arcgis-python-api/tree/master/samples/04_gis_analysts_data_scientists
- https://developers.arcgis.com/python/
- https://developers.arcgis.com/python/sample-notebooks/chennai-floods-analysis/
- https://developers.arcgis.com/documentation/

web service
- http://resources.arcgis.com/en/help/runtime-wpf/concepts/index.html#/Welcome_to_the_help_for_developing_Operations_Dashboard_for_ArcGIS_add_ins/0170000000np000000/

python cource
- https://www.e-education.psu.edu/geog485/book/export/html/

publish data arcgis
- https://github.com/Esri/arcgis-python-api/tree/master/samples/05_content_publishers/data

aggregate
- https://developers.arcgis.com/python/guide/summarizing-feature-data/
'''

from arcgis.features import find_locations
from arcgis.features.analyze_patterns import interpolate_points
from arcgis.features import use_proximity
from arcgis.features import summarize_data

from arcgis.geocoding import geocode
from arcgis.gis import GIS
import pandas as pd

class MyClass(object):

    
    def __init__(self, params):
        '''
        Constructor
        '''  
        self.i = 0
           
def main():
    df = pd.read_csv('data/chennai-rainfall.csv')
    print (df)

def testGis():    
    help(GIS)
    
    gis = GIS()
    map = gis.map('Palm Springs')

    items = gis.content.search('Palm Springs Trails')
    for item in items:
        print (item)
    
    map.add_layer(items[9])
    
def makeMapLayer():
    # 1. make pandas dataframe
    df = pd.read_csv('data/chennai-rainfall.csv')
    
    # 2. Create an arcgis.features.FeatureCollection object by importing the pandas dataframe with an address field
    gis = GIS()
    rainfall = gis.content.import_data(df, {"Address" : "LOCATION"})
    intmap = gis.map("Tamil Nadu", zoomlevel=7)
    lakemap = gis.map("Chennai", zoomlevel=11)
    chennai_lakes = gis.content.search("Chennai Lakes", "feature collection", outside_org=True)[0]
    
    # 3. add dataframe to arcgis map using method add_layer
    map.add_layer(rainfall, { "renderer":"ClassedSizeRenderer", "field_name":"RAINFALL" })
    
    # 3. using the interpolate_point 
    interpolated_rf = interpolate_points(rainfall, field='RAINFALL')
    intmap.add_layer(interpolated_rf['result_layer'])
    
    # 4. using find location and use
    floodprone_buffer = use_proximity.create_buffers(find_locations.trace_downstream(chennai_lakes), [ 1 ], units='Miles')
    lakemap.add_layer(floodprone_buffer)
    
if __name__ == "__main__":
    main()