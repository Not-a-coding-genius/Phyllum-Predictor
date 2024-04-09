# MyFlir allows us to check for temperature range of the image but does not give us access to the original file
# While storing the file into the Photos library its already modified losing its temperature metadata (tmin, tmax, emissivity, scale, etc.)
# As I couldn't access to the original file I have to work with the only one that I have and I have to set the temperature range manually

import PIL
from PIL import Image
from PIL.ExifTags import TAGS
import cv2

import pandas as pd
import numpy as np
from numpy import asarray
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def metadata ():
    #checking for metadata and if the image stores its min and max temperatures
    exifdata = image.getexif()

    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag:25}: {data}")

# Open thermal images, as I'm comparing two, I have to run this program two times, one for the file ending in 323 and the following one for the one ending in 247. In this case it will be running the one ending in 323, to run the following one simply comment the next line and uncomment the other one

base = "halo1" # tmin = 29.6; tmax = 44.1
#base = "flir_20230216T213247" # tmin = 22.6; tmax = 28.1

ext = ".jpg"
image_source = base + ext

image = PIL.Image.open(image_source)

metadata()

gray16_image = cv2.imread(image_source, cv2.IMREAD_ANYDEPTH) # Convert image to a grayscale so we can get each pixels temperature

np_gray16 = asarray(gray16_image)

np_gray16_min = np_gray16.min()
np_gray16_max = np_gray16.max()

np_gray16_norm = (np_gray16 - np_gray16_min) * (1/(np_gray16_max - np_gray16_min)) # Normalize temperatures

# Set an standard temperature range
tmin = float(input("Enter images minimum temperature: ")) # tmin = 22.6
tmax = float(input("Enter images maximum temperature: ")) # tmax = 28.1

np_temp = tmin + (np_gray16_norm) * (tmax - tmin)

#dest = base + "_temp_mx.xlsx"
dest = base + "_temp_mx.csv"

df = pd.DataFrame (np_temp)
df.to_csv(dest, header = False, index=False) # creates an excel file with the temperature data of each image

trangemin = 20
trangemax = 50
np_temp_aux = tmin + (np_gray16_norm) * (tmax - tmin)

# Temperature ranges for standardized images require us to make a tiny modification in images data because we will need the same maximum and minimum temperature value in every image. Doing this we are setting the range references for the color pallette. We will set first cell as the minimum temperature of the range and the last one as the maximum
np_temp_aux[0,0] = trangemin # first pixel of the image will have its temperature value equal to trangemin

x = np_temp.shape[0]
y = np_temp.shape[1]
np_temp_aux[x-1,y-1] = trangemax # # last pixel of the image will have its temperature value equal to trangemax

np_temp_norm = (np_temp - tmin) * (1/(tmax - tmin))
np_temp_aux_norm = (np_temp - trangemin) * (1/(trangemax - trangemin))

# Set the heat maps, note that heach specific heatmap will have different temperature ranges
# Normalized heat map ranges will be independent of input image temperatures and will allways go from 20 to 50

inferno = plt.colormaps.get_cmap('inferno')

np_temp_hm = inferno(np_temp_norm)
np_temp_norm_hm = inferno(np_temp_aux_norm)

# Save normalized images as JPG files
np_temp_hm = Image.fromarray((np_temp_hm[:, :, :3] * 255).astype(np.uint8))
np_temp_norm_hm = Image.fromarray((np_temp_norm_hm[:, :, :3] * 255).astype(np.uint8))

image_temp = np_temp_hm.convert('RGB')
image_temp_norm = np_temp_norm_hm.convert('RGB')

image_temp_dest = base + "_col" + ext
image_temp_norm_dest = base + "_col_norm" + ext

image_temp.save(image_temp_dest, format='JPEG', quality=95) # save thermal image now with inferno heatmap rather than iron
image_temp_norm.save(image_temp_norm_dest, format='JPEG', quality=95) # save normalized thermal image now with inferno heatmap rather than iron