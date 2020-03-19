# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 11:30:23 2020

@author: Datalab
"""

#%%
# Importeren Libraries
from osgeo import ogr, gdal
import subprocess
import numpy as np

#%%
# A script to rasterise a shapefile to the same projection & pixel resolution as a reference image.
#shp_naar_tif.py maar dan als een functie op te roepen door rasterize(-,-,-,-)
def rasterize(InputVector, InputVectorRB, RefImage, OutputImage):   
    gdalformat = 'GTiff'
    datatype = gdal.GDT_Byte
    #burnVal = 1 #value for the output image pixels
	##########################################################
	# Get projection info from reference image
    Image = gdal.Open(RefImage, gdal.GA_ReadOnly)
  # Get RGB array of reference image
    band = Image.GetRasterBand(1)
    print(band)
    xsize = band.XSize
    ysize = band.YSize
    rgb = np.dstack([Image.GetRasterBand(b).ReadAsArray() 
        for b in (1,2,3)])
    x,y,z = rgb.shape    
	# Open Shapefile
    Shapefile = ogr.Open(InputVector)
    Shapefile_layer = Shapefile.GetLayer()
    burnVal = 200 #value for the output image size
  # Open RB Shapefile
    ShapefileRB = ogr.Open(InputVectorRB)
    ShapefileRB_layer = ShapefileRB.GetLayer()
    burnValRB = 1 #value for the output image size
	# Rasterise
    print("Rasterising shapefile...")
    Output = gdal.GetDriverByName(gdalformat).Create(OutputImage, Image.RasterXSize, Image.RasterYSize, 1, datatype)#, options=['COMPRESS=DEFLATE'])
    Output.SetProjection(Image.GetProjectionRef())
    Output.SetGeoTransform(Image.GetGeoTransform()) 
	# Write data to band 1
    Band = Output.GetRasterBand(1)
    Band.SetNoDataValue(255)
    gdal.RasterizeLayer(Output, [1], Shapefile_layer, burn_values=[burnVal])
    gdal.RasterizeLayer(Output, [1], ShapefileRB_layer, burn_values=[burnValRB])
	# Prints black part on the new output image if the reference image is partially black (border image)
    a = np.count_nonzero(rgb==0)
    if a >= (rgb.size*0.07):
        bw = Output.GetRasterBand(1).ReadAsArray()
    	#compare
        for i in range(x):
            for j in range(y):
                if max(rgb[i,j,:])==0:
                    bw[i,j]=0       
        Output.GetRasterBand(1).WriteArray(bw)	
	# Close datasets
    Band = None
    Output = None
    Image = None
    Shapefile = None
  # Build image overviews
    subprocess.call("gdaladdo --config COMPRESS_OVERVIEW DEFLATE "+OutputImage+" 2 4 8 16 32 64", shell=True)
    print("Done!")
    