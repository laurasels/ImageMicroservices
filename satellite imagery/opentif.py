#from PIL import Image
#im = Image.open('20180803_092316_Tri_320cm_RD_12bit_RGBI_Steenwijk.tif')
#im.show()

#%%
import matplotlib.pyplot as plt
from matplotlib import image

#img = image.imread('20180803_092316_Tri_320cm_RD_12bit_RGBI_Steenwijk_viascriptstijn.tif')

img = image.imread('tile_21000_16000.tif')
plt.imshow(img)

#%%

