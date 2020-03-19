#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:43:01 2020

@author: datalab
"""
#%%
import os 
import shutil
import requests
from requests.auth import HTTPBasicAuth

from func_satellite import Download_zip, extract_zip, cut_tif, remove_black, predict_image

in_path = 'downloaded_tiles/'
out_path = 'tiles/'
dest_dir = 'welrotonde_satelliet/'
os.makedirs(dest_dir, exist_ok=True)

#%%
def FromDownloadtoPredict(geo, coordinates, startdate, enddate):
    """
    Download one zipfile from api satellietdataportaal for the Netherlands in the given timeframe at the same time, 
    then extract, cut, remove black and predict the tiles. The files that do not contain detected rotondes are removed.
    
    Make a list with download links:
    first 1: number of features, total links = 190
    second 2: sort data, we need to download 8bit_RGB
    """
    results_json = open("downloadlink.json", "w")
  
    response = Download_zip(geo="Polygon", coordinates=[[ [7.19, 53.23], [6.04, 50.76], [3.40, 51.36],[4.73, 52.96], [7.19, 53.23] ]], startdate="2019-12-19" , enddate="2020-03-03") 
        
    for i in range(len(response.json()["features"])):
        results = response.json()["features"][i]["properties"]["downloads"][2]["href"]
        print(results)
        
        print("downloading: ", results)
        r = requests.get(results, auth=HTTPBasicAuth('satelliet.datalab.rws@gmail.com', 'RWS4121312'), stream=True)
        zip_filename = os.path.join(in_path, 'downloaded_'+ str(i) + '.zip')
        with open(zip_filename, 'wb') as f:
            f.write(r.content)
        tif_filename = extract_zip(zip_filename)
        os.remove(zip_filename)
        
        print("cutting tiffs...")
        cut_tif(tif_filename)
        os.remove(tif_filename)
        print("Done cutting tiffs")
        
        print("removing black images..")
        for tile in os.listdir(out_path):
            if tile.startswith('tile_'):
                print(tile)
                remove_black(tile)
        print("Done removing black images") 
    
        
        print("Predicting score..")
        file = open("detected_rotondes_satelliet.txt","w")
        for tile in os.listdir(out_path):
            if tile.startswith('tile_'):
                print(tile)
                source_file = os.path.join(out_path, tile)
                predicted_score = predict_image(source_file)
                print(predicted_score)
                if predicted_score > 0.7:
                    dest_file = os.path.join(dest_dir, tile + '_detected' + '.tif')
                    shutil.copy2(source_file, dest_file)
                    file.write(tile + '_detected' + '.tif') 
                    file.write("\n")
                    print("Image saved in folder: %s, Rotonde is detected in satellite image: %.2f" %(dest_dir, predicted_score))
                os.remove(source_file)
        file.close()
        
    results_json.close()
    
FromDownloadtoPredict(geo="Polygon", coordinates=[[ [7.19, 53.23], [6.04, 50.76], [3.40, 51.36],[4.73, 52.96], [7.19, 53.23] ]], startdate="2019-12-19" , enddate="2020-03-10") 
