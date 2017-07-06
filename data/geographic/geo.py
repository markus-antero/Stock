'''
Created on 2.5.2017

@author: Markus.Walden

- https://media.readthedocs.org/pdf/geopy/latest/geopy.pdf
- https://freegisdata.rtwilson.com/
- https://www.ncbi.nlm.nih.gov/gds/
- http://www.gis.usu.edu/~chrisg/python/2009/

gdal
- http://www.gdal.org/
- https://pypi.python.org/pypi/GDAL
- http://desktop.arcgis.com/en/analytics/python-in-arcgis/iii-python.htm

shapefile - loaded world map 
- https://github.com/GeospatialPython/pyshp

arcgis manuals
- https://github.com/Esri/arcgis-python-api/tree/master/samples/04_gis_analysts_data_scientists
- https://developers.arcgis.com/python/
- https://developers.arcgis.com/python/sample-notebooks/chennai-floods-analysis/
- https://developers.arcgis.com/documentation/

-web service
- http://resources.arcgis.com/en/help/runtime-wpf/concepts/index.html#/Welcome_to_the_help_for_developing_Operations_Dashboard_for_ArcGIS_add_ins/0170000000np000000/

python cource
- https://www.e-education.psu.edu/geog485/book/export/html/

publish data arcgis
- https://github.com/Esri/arcgis-python-api/tree/master/samples/05_content_publishers/data

aggregate
- https://developers.arcgis.com/python/guide/summarizing-feature-data/

'''
import arcgis 
from arcgis.gis import GIS

from arcgis.features import find_locations
from arcgis.features.analyze_patterns import interpolate_points
from arcgis.features import use_proximity

import pandas as pd
import json

from data.geographic import gisPass, gisUser


class AddInformationUsingDataFrame(object):
    '''
    classdocs
    Templates:
        item_properties = {
            "title": "Worldwide gun ownership",
            "tags" : "guns,violence",
            "snippet": " GSR Worldwide gun ownership",
            "description": "test description",
            "text": json.dumps({"featureCollection": {"layers": [dict(fc.layer)]}}),
            "type": "Feature Collection",
            "typeKeywords": "Data, Feature Collection, Singlelayer",
            "extent" : "-102.5272,-41.7886,172.5967,64.984"
        }
    '''
    def __init__(self, conn = "https://www.arcgis.com"):
        '''
        Constructor
        Initiate gis instance
        '''
        self.gis = GIS(conn, gisUser, gisPass) 
        
    def addGisItem(self, item_properties):
        item = self.gis.content.add(item_properties)
        return item
    
    def createDir(self, dir = 'packages'):
        try:
            self.gis.content.create_folder(dir)
            return True
        except:
            return False
    
    def addContent(self, source, destinationDir):
        try:
            self.gis.content.add({}, data=source, folder=destinationDir)
            return True
        except:
            return False

    @staticmethod    
    def postMapUseWikipedia(item_properties, gis, fc):
      
        map1 = gis.map('UK')
        map1.add_layer(fc, {"renderer":"ClassedSizeRenderer",
                   "field_name": "Guns_per_100_Residents"})
        
        item = gis.content.add(item_properties)
        return map1, item

class GisMapUpdate(AddInformationUsingDataFrame):

    def __init__(self):
        super.__init__()
        
    def addSDFile(self, sd_file = "./data/Ebola_Treatment_Units.sd"):
        item = self.gis.content.add({},sd_file)
        new_item = item.publish()
        return new_item
    
    def readJSONFile(self, jsonFile):
        with open(jsonFile,"r") as file_handle:
            self.web_map_json = json.load(file_handle)
    
    @staticmethod
    def printOperationalLayer(web_scene_obj):
        for layer in web_scene_obj['operationalLayers']:
            print(layer['title'] + " :: " + layer['layerType'])
            if layer['layerType'] == 'GroupLayer':
                for sub_layer in layer['layers']:
                    print("\t" + sub_layer['title'] + " :: "+ sub_layer['url'])
    
    @staticmethod
    def makeMapLayer(df_toInterpolate, gis, map, featureCollection):       
        # 1. Create an arcgis.features.FeatureCollection object by importing the pandas dataframe with an address field
        rainfall = gis.content.import_data(df_toInterpolate, {"Address" : "LOCATION"})       
        
        # 2. add dataframe to arcgis map using method add_layer
        map.add_layer(rainfall, { "renderer":"ClassedSizeRenderer", "field_name":"RAINFALL" })
        
        # 3. using the interpolate_point 
        interpolated_rf = interpolate_points(rainfall, field='RAINFALL')
        
        # 4. using find location and use
        floodprone_buffer = use_proximity.create_buffers(find_locations.trace_downstream(featureCollection), [ 1 ], units='Miles')
        
        return interpolated_rf, floodprone_buffer
    
        
def main():
# Test adding Data to gis
    useMyAccount = False    
    myGis = AddInformationUsingDataFrame()
    
    if useMyAccount:
        gis = GIS(myGis.gis)
    else:
        gis = GIS()
        
    fc = gis.content.import_data(readWiki(), {"CountryCode":"Country"})
    item_properties = {
            "title": "Worldwide gun ownership",
            "tags" : "guns,violence",
            "snippet": " GSR Worldwide gun ownership",
            "description": "test description",
            "text": json.dumps({"featureCollection": {"layers": [dict(fc.layer)]}}),
            "type": "Feature Collection",
            "typeKeywords": "Data, Feature Collection, Singlelayer",
            "extent" : "-102.5272,-41.7886,172.5967,64.984"
    }
    map1, item, gis = AddInformationUsingDataFrame.postMapUseWikipedia(item_properties = item_properties, gis = gis)

# Test webMap using 
    testWebMapScene()


def readWiki():
    df = pd.read_html("https://en.wikipedia.org/wiki/Number_of_guns_per_capita_by_country")[1]
    df.columns = df.iloc[0]
    df = df.reindex(df.index.drop(0))
    
    # change number + index to number    
    df.iloc[0,2] = 112.6
    
    # change column format    
    converted_column = pd.to_numeric(df["Guns per 100 Residents"], errors = 'coerce')
    df['Guns per 100 Residents'] = converted_column
    return df



def testArcgisWeb():
    '''
    creates 3d object layer on buildings in montreal, canada
    '''
    myGis = GisMapUpdate()
    myGis.readJSONFile(jsonFile = "./data/arcgis_map.json")
    json1 = myGis.web_map_json
    
    myGis.readJSONFile(jsonFile = "./data/arcgis_map_scene.json")
    json2 = myGis.web_map_json
    
    search_result = myGis.gis.content.search("title:2012 USA Median Age AND owner:esri", 
                                   item_type = "Map Service", outside_org = True)
    
    median_age_weblayer = search_result[1]
    
    json2['operationalLayers'][0]['itemId'] = median_age_weblayer.itemid
    json2['operationalLayers'][0]['layerType'] = "ArcGISMapServiceLayer"
    json2['operationalLayers'][0]['title'] = median_age_weblayer.title
    json2['operationalLayers'][0]['url'] = median_age_weblayer.url
    
    web_map_properties = {'title':'USA median age map',
                     'type':'Web Map',
                     'snippet':'This map service shows the median age of people' +\
                     'in the United States as of 2012 census. The Median Age for' +\
                      'the U.S. is 37 years of age.',
                     'tags':'ArcGIS Python API',
                     'text':json.dumps(json2)}

    web_map_item = myGis.gis.content.add(web_map_properties)
    
    search_result = myGis.gis.content.search("title:Montreal, Canada Buildings AND owner:esri_3d", 
                                   item_type="scene service", outside_org = True)
    
    buildings_layer = search_result[0]
    json1['operationalLayers'][0]['itemId'] = buildings_layer.itemid
    json1['operationalLayers'][0]['layerType'] = "ArcGISSceneServiceLayer"
    json1['operationalLayers'][0]['title'] = buildings_layer.title
    json1['operationalLayers'][0]['url'] = buildings_layer.url

    web_scene_item_properties = {'title':'Web scene with photo realistic buildings',
                            'type':'Web Scene',
                            'snippet':'This scene highlights buildings of Montreal, Canada',
                            'tags':'ArcGIS Python API',
                            'text': json.dumps(json1)}

# Use the add() method to publish a new web scenej
    web_scene_item = myGis.gis.content.add(web_scene_item_properties)
    web_scene_item.share(True)
    web_scene_obj = arcgis.mapping.WebScene(web_scene_item)
    return web_scene_obj

def testWebMapScene():    
    '''
    - Test JSON load to 
    - publish a web map
    '''
    myGis = GisMapUpdate()
    myGis.readJSONFile(jsonFile = "./data/map_ebola.json")
    
    web_map_item_properties = {'title':'Ebola treatment locations',
                           'type':'Web Map',
                           'snippet':'This map shows locations of Ebola treatment centers in Africa',
                           'tags':'ArcGIS Python API',
                           'text':json.dumps(myGis.web_map_json)}
    
    web_map_item = myGis.addGisItem(item_properties = web_map_item_properties)
    
    # create a web map object out of the item
    web_map_obj = arcgis.mapping.WebMap(web_map_item)
    layer_list = web_map_obj['operationalLayers']

    search_result = myGis.gis.content.search('title:Ebola', item_type='Feature Layer')
    ebola = search_result[0]
    
# set the url to feature service item's url
    layer_list[0]['url'] = ebola.layers[1].url
    layer_list[0]['itemId'] = search_result[0].id

# update the web map object's operationalLayers dictionary
    web_map_obj['operationalLayers'] = layer_list
    search_result = myGis.gis.content.search('title:Western Pacific Typhoons (2005) AND owner:esri_3d', 
                                   item_type = 'Web Scene', outside_org = True)

    web_scene_item = search_result[0]
    web_scene_obj = arcgis.mapping.WebScene(web_scene_item)
    return web_scene_obj
    
if __name__ == "__main__":
    main()      