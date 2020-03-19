# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:23:17 2020

@author: Datalab
"""
import gdal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
#%%

def predict_NWB(file):
  Image = gdal.Open(file)
  rgb = np.dstack([Image.GetRasterBand(1).ReadAsArray()])
  a = np.count_nonzero(rgb==1) #telt alle pixels met kleurcode 1 in de afbeelding
  if a>0:
      score_NWB=1
  else:
      score_NWB=0

  return score_NWB
 
#%%    
    
# def predict_NWB(file):
#   Image = gdal.Open(file)
#   rgb = np.dstack([Image.GetRasterBand(1).ReadAsArray()])
#   a = np.count_nonzero(rgb==1) #telt alle pixels met kleurcode 1 in de afbeelding
#   if a>0:
#       score_NWB=1
      
#   else:
#       score_NWB=0

#   img = image.imread(file)
#   plt.rcParams["figure.figsize"] = (7,7)
#   plt.figure()
#   plt.imshow(img,cmap="gray", vmin=0, vmax=255)
#   plt.xlabel("Predicted score: "+ str(score_NWB))
#   plt.show()
  
#   return score_NWB
 


