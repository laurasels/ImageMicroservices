import os
import PIL
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
import xml.etree.ElementTree as ET
from PIL import Image
import os, os.path
import csv

pathxml = 'annotationsxml'
pathimage = 'images'
output = 'imagesbox'

def getbox(elem):
    obj = {} #dictionary met bounding box
    #loop over alle eigenschappen van de box
    for attr in list(elem):
        if 'bndbox' in attr.tag:
            for dim in list(attr):
                if 'xmin' in dim.tag:
                    obj['xmin'] = int(round(float(dim.text)))
                if 'ymin' in dim.tag:
                    obj['ymin'] = int(round(float(dim.text)))
                if 'xmax' in dim.tag:
                    obj['xmax'] = int(round(float(dim.text)))
                if 'ymax' in dim.tag:
                    obj['ymax'] = int(round(float(dim.text)))
                    print(xml, str('xmin'), obj['xmin'], str('ymin'), obj['ymin'],str('xmax'), obj['xmax'], str('ymax'), obj['ymax']) 
    return obj           

#loop over elke xml file
for xml in sorted(os.listdir(pathxml)):
    tree = ET.parse(os.path.join(pathxml,xml))
    f=os.path.splitext(os.path.basename(xml))[0]+'.jpg' #get file without extension
    im = Image.open(os.path.join(pathimage,f)) #open image
    draw = ImageDraw.Draw(im) #draw image
    #lopen over elk element in de xml
    for elem in tree.iter():
        #als het een box is:
        if 'object' in elem.tag:
            obj=getbox(elem)
            draw.rectangle(((obj['xmin'], obj['ymin']), (obj['xmax'], obj['ymax'])), outline="#ff8888") #draw box
    outputpath = output + '/'+ f.replace('.jpg', '.bmp') 
    im.save(outputpath)



	
    


