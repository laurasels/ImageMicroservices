#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 12:46:58 2020

@author: datalab
"""
#%%

import gdal
import os 
import numpy as np 
import requests
import json
import zipfile

in_path = 'downloaded_tiles/'
out_path = 'tiles/'

#%%
"""
Download one zipfile from api satellietdataportaal for the Netherlands in the given timeframe at the same time, 
then extract, cut, remove black and predict the tiles. The files that do not contain detected rotondes are removed.
"""    

def Download_zip(geo, coordinates, startdate, enddate):
    """
    geo: define Point or Polygon
    coordinates: lat, lon for example [5.92,52.67]
    startdate: startdate of data you would like to download
    enddate: enddate of data you would like to download
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

    return response
#%%
    
def extract_zip(zip_filename):
    print("extracting file:", zip_filename)
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(in_path)
        tif_filelist = zip_ref.namelist()[0]
        tif_filename = os.path.join(in_path, tif_filelist)
        print(tif_filename)
    return tif_filename 
        
#%%

"""
Cut tiles in smaller tiles and save in folder: tiles
"""

def cut_tif(file):
    tile_size_x = 1000 #aantal pixels breedte
    tile_size_y = 1000 #aantal pixels lengte

    ds = gdal.Open(file)
    band = ds.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize

    for i in range(0, xsize, tile_size_x):
        for j in range(0, ysize, tile_size_y):
            gdal.Translate(out_path + "/tile_" + str(i) + "_" + str(j), file, srcWin=[str(i), str(j), tile_size_x, tile_size_y])

#%%
"""
Remove the black tiles
"""
def remove_black(file):
    ds = gdal.Open(os.path.join(out_path+file))
    band = ds.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize

    rgb = np.stack([ds.GetRasterBand(b).ReadAsArray() for b in (1,2,3)])
    rgb = np.reshape(rgb,(xsize,ysize,3))

    if rgb.max()==0:
        print("delete black picture ", file)
        ds = None
        os.remove(os.path.join(out_path+file))

#%%
"""
Predict if the smaller tiles consists of a roundabout, if that's true: tile is save in: welrotonde_satelliet. 
The predicted tiles are also saved in a txt file: detected_rotondes_satelliet.txt
"""

from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
from keras.applications.vgg16 import preprocess_input

def predict_image(file):
  model = load_model('finalmodel2.h5', compile=False)
  model.summary()
  x = load_img(file, target_size=(1000,1000))
  x = img_to_array(x)
  x = np.expand_dims(x, axis=0)
  x = preprocess_input(x)
  score = model.predict(x)[0][0]  
  return score

#%%