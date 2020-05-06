import pydicom
import png 
import numpy as np
from PIL import Image

## Read in a dicom file 
path = 'samples-dicom\ID_000a33979.dcm'
ps = pydicom.dcmread(path)


## Manipulate the dcm pixel_array to prevent losses during conversion
shape = ps.pixel_array.shape
img2 = ps.pixel_array.astype(float)
img2_scaled = (np.maximum(img2, 0) / img2.max()) * 255.0
img2_scaled = np.uint8(img2_scaled)

## Write the modified image array to png 
with open('.\\test.png', 'wb') as png_file:
    w = png.Writer(shape[1], shape[0], greyscale=True)
    w.write(png_file, img2_scaled)


## Resize the image 
img = Image.open('.\\test.png')
width, height = 256, 256
img = img.resize((width, height), Image.BILINEAR)
img.save('.\\test-2.png')