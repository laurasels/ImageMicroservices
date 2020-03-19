#%%
"""
Created on Mon Jan 20 11:14:00 2020
@author: Datalab
"""
import requests
from requests.auth import HTTPBasicAuth
import json

def DownloadTiles(geo, coordinates, startdate, enddate):
    """
    geo: define Point or Polygon
    coordinates: lat, lon for example [5.92,52.67]
    startdate: startdate of data you would like to download
    enddate: enddate of data you would like to download
    Example_1: searchAvailableTiles(geo="Point",coordinates=[5.92,52.67], startdate="2018-06-14" , enddate="2018-09-16") 
    #sensorname = TripleSat, coordinates = Steenwijk
    Example_2: searchAvailableTiles(geo="Point",coordinates=[5.12,52.09], startdate="2019-09-19" , enddate="2019-10-26") 
    #sensorname = SuperView-1, coordinates = Utrecht
    """
    
    data = {
            "type": "Feature",
            "geometry": {
                "type": geo,
                "coordinates": coordinates
            },
            "properties": {
                "fields":{
                    "geometry": False
                },
                "filters" : {
                    "datefilter": {
                        "startdate": startdate,
                        "enddate" : enddate
                    },
                    "resolutionfilter": {
                        "maxres" : 0.5, 
                        "minres" : 0 
                    }
                } 
            }
        }
         
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
  
    response = requests.post('https://api.satellietdataportaal.nl/v1/search', data=json.dumps(data), headers=headers, 
                             auth=('satelliet.datalab.rws@gmail.com', 'RWS4121312'))
  
    """
    Make a list with download links
    first 1: number of features, total links = 190
    second 2: sort data, we need to download 8bit_RGB
    """
    results_json = open("downloadlink.json", "w")
    
    #for i in range(len(response.json()["features"])):
    for i in range(7,10):
        results = response.json()["features"][i]["properties"]["downloads"][2]["href"]
        results_json.write(results) 
        results_json.write("\n") 
        print("download: ", results)
        r = requests.get(results, auth=HTTPBasicAuth('satelliet.datalab.rws@gmail.com', 'RWS4121312'), stream=True)
        with open('downloaded_tiles/downloaded_'+ str(i) + '.zip', 'wb') as f:
            f.write(r.content)
    results_json.close()
    
DownloadTiles(geo="Polygon",coordinates=[[ [7.19, 53.23], [6.04, 50.76], [3.40, 51.36],[4.73, 52.96], [7.19, 53.23] ]], 
              startdate="2019-12-19" , enddate="2020-03-03") 
      



    





