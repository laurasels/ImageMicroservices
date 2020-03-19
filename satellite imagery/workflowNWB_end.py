#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 13:59:10 2020
@author: datalab
"""
"""
NWB
Nu we de satellietbeelden hebben opgeknipt, willen we aan elk satelliet tegeltje het NWB linken.
Dit doen we door voor elke geknipte tegel, de tegel 'leeg' te openen en hierover het NWB te openen. De wegen printen we in lichtgrijs (kleurcode 200) en de rotondes in zwart (kleurcode 1), zodat er geen verwarring kan ontstaan over wat een rotonde is. Het resultaat slaan we vervolgens op als .tif bestand.
We definiëren de volgende functie die dit proces voor ons zal doen.
"""
#%%

import os
import shutil

input_dir = "welrotonde_satelliet"
output_dir = "NWB/"
dest_dir = "welrotonde_NWB/"
os.makedirs("welrotonde_NWB/", exist_ok=True)

#%%

"""
Nu kunnen we de functie aanroepen om satelliet tegels om te zetten in NWB tegels.
De functie heeft 4 argumenten die we eerst moeten definiëren.
"""
from RasterizeNWB import rasterize

InputVector = r"NWB/Nederland/Wegvakken.shp" # pad naar het NWB van heel Nederland
InputVectorRB = r"NWB/Nederland/Wegvakken_RB.shp"

for subdir, dirs, files in os.walk(input_dir):
    for name in files:
        RefImage = os.path.join(subdir, name)
        OutputImage = os.path.join(output_dir + "/NWB_"+RefImage.rsplit('/')[-1])
        rasterize(InputVector,InputVectorRB,RefImage,OutputImage)
print("Rasterizing done.")


#%%
"""
Nu kunnen we de functie aanroepen om te voorspellen of er een rotonde op het NWB plaatje staat
"""

from predictNWB import predict_NWB

#define size of tif image
xsize = 1000
ysize = 1000
tile_size_x = 1000
tile_size_y = 1000


print("Predicting NWB...")
for subdir, dirs, files in os.walk(output_dir):
    for name in files:
        if name.startswith("NWB_") and name.endswith("tif"):
            source_file = os.path.join(output_dir, name)
            predict_score = predict_NWB(output_dir + name)
            print(name,"predicted score is:", predict_score)
            if predict_score == 1:
                dest_file = os.path.join(dest_dir, name)
                shutil.copy2(source_file, dest_file)
                print("Image saved in folder: welrotonde_NWB, rotonde is detected in satellite image")

# Wegschrijven van detected rotondes naar txt file:
file = open("NWB/NWB_detected_rotondes.txt", "w")

for tile in os.listdir(dest_dir):
    print(file)
    file.write(tile)
    file.write("\n")
file.close()

#%%
"""
Compare detected files in satellite and NWB folder:
"""
d1 = set(os.listdir(input_dir))
d2 = []
for file in os.listdir(dest_dir):
    d2.append(file.rsplit('NWB_')[-1])
d2 = set(d2)

common = list(d1 & d2)
print("common files:", common)

#%%
file_sat = open("verschillijst_welsatelliet_geenNWB.txt", "w")
file_sat.write("Op deze satelliettiles zijn wel rotondes gedetecteerd, maar staat niet in NWB")
file_sat.write("\n")

weld1_nietd2 = []
for z in d1:
    if z not in d2:
        weld1_nietd2.append(z)
        file_sat.write(z)
        file_sat.write("\n")
print("files wel in satellietmap, niet in NWB:", weld1_nietd2)

file_sat.close()
#%%

file_NWB = open("verschillijst_welNWB_geensatelliet.txt", "w")
file_NWB.write("Op deze satelliettiles zijn geen rotondes gedetecteerd, maar staat wel in NWB (dit zou leeg moeten zijn of niet veel)")
file_NWB.write("\n")

weld2_nietd1 = []
for z in d2:
    if z not in d1:
        weld2_nietd1.append(z)
        file_NWB.write(z)
        file_NWB.write("\n")
print("files wel in NWB, niet in satellietmap:", weld2_nietd1)

file_NWB.close()

#%%
