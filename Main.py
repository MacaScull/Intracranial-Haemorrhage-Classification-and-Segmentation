## Author: Macauley Scullion
## Last edited: 23/04/20

##-----------------------------------About-----------------------------------##

## - Single hash comment correlates with a removable piece of code e.g. #
## - Double hash comment correlates with a code comment e.g. ##

##---------------------------------------------------------------------------##

##Imports 
import sys
import pydicom 
import pydicom.pixel_data_handlers.util as util
import csv
import numpy as np
import operator
import random
import tensorflow as tf 
from tensorflow.keras import datasets, layers, models, callbacks, optimizers
import matplotlib.pyplot as plt
from skimage.transform import resize
from scipy import ndimage as ndi

## Data handler class, this contains all vital information produced by the Network class.
class dataHandler:
    ## Class variables.
    ID = ''
    dicom = ''
    image = []
    windowed = []
    presenceResults = []
    presence = False
    subtypeResults = []
    subtype = []

    ## Reasd dicom function, reads and stores DICOM information and the image.
    def readDicom(self, file):
        self.ID = file
        self.dicom = pydicom.dcmread('/content/drive/My Drive/Artefact/Samples/'+ file)
        self.image = self.dicom.pixel_array

    ## Window image function, utilises threholds to range the image.
    def windowImage(self, img, intercept, slope,):
        img = img * slope + intercept
        img[img < -100] = -100
        img[img > 1000] = 1000
        
        self.image = img 

    ## Pre-process function, checks the image is of the right input size, windows said image and reshapes it as approriate CNN input.
    def preprocess(self):
        self.image = np.asarray(self.image)
        if self.dicom.Rows != 512 or self.dicom.Columns != 512:
            self.image = resize(self.image, (512, 512))

        self.windowImage(self.image, self.dicom.RescaleIntercept, self.dicom.RescaleSlope)
        self.image = self.image.reshape(1, 512, 512, 1)

    ## Presence check function, get the index of the largest result thus the classification.
    def presenceCheck(self):
        check = np.argmax(self.presenceResults)
        if check == 1:
            self.presence = True

    ## Subtype check, any result higher than 0.5 is class as present and will be obtained from the subtypes array.
    def subtypeCheck(self):
        subtypes = ['Epidural', 'Intraparenchymal', 'Intraventricular', 'Subarachnoid', 'Subdural']
        for i in range(len(self.subtypeResults[0])):
            if self.subtypeResults[0][i] > 0.5:
              self.subtype.append(subtypes[i])

    ## Displays all information about the haemorrhage, its presence and subtype, if any.
    def displayInfo(self):
        print('\n', file[:-4])
        print("Haemorrhage presence results: %r" % (self.presence))
        print("Haemorrhage presence predict results: \n- Non-Haemorrhage: %f \n- Haemorrhage: %f" % (self.presenceResults[0][0], self.presenceResults[0][1]))
        if self.presence == True:
          print("Haemorrhage subtype results: ", self.subtype)
          print("Haemorrhage subtype predict results: \n- Epidural: %f \n- Intraparenchymal: %f \n- Intraventricular: %f \n- Subarachnoid: %f \n- Subdural: %f" % (self.subtypeResults[0][0], self.subtypeResults[0][1], self.subtypeResults[0][2], self.subtypeResults[0][3], self.subtypeResults[0][4]))
       

## Network class, contains all information and data about the CNNs
class network:
    ## Class variables.
    model = ''

    ## Create model function, will create a CNN based on parameters passed and stores it.
    def createModel(self, opt, loss, act, init, classes, final):
    
        model = models.Sequential()
        model.add(layers.Conv2D(32, (9,9), activation=act, input_shape=(512,512,1)))
        model.add(layers.AveragePooling2D((2,2)))
        model.add(layers.Conv2D(64, (9, 9), activation=act))
        model.add(layers.AveragePooling2D((2,2)))
        model.add(layers.Conv2D(64, (6, 6), activation=act))
        model.add(layers.MaxPooling2D((2,2)))
        model.add(layers.Conv2D(96, (6, 6), activation=act))
        model.add(layers.MaxPooling2D((2,2)))
        model.add(layers.Conv2D(128, (3, 3), activation=act))
        model.add(layers.MaxPooling2D((2,2)))
        model.add(layers.Conv2D(128, (3, 3), activation=act))
        model.add(layers.Flatten())
        model.add(layers.Dense(128, activation=act, kernel_initializer=init))
        model.add(layers.Dense(classes, activation=final, kernel_initializer=init))
        model.compile(optimizer=opt, loss=loss, metrics=['accuracy'])

        self.model = model

    ## Model load function, will create the model and load its approriate weights into the model based on a boolean value. 
    def modelLoad(self, mode):
        if mode == False:
            self.createModel('Adam', 'sparse_categorical_crossentropy', 'tanh', 'lecun_uniform', 2, 'softmax')
            self.model.load_weights('/content/drive/My Drive/Artefact/Weights/Presence/cp.cpkt')
        if mode == True:
            self.createModel('Adam', 'binary_crossentropy', 'tanh', 'uniform', 5, 'sigmoid')
            self.model.load_weights('/content/drive/My Drive/Artefact/Weights/Subtype/cp.cpkt')
        
    ## Model predict function, will preprocess data, load the model, predict classification and finally, check results of the prediction. 
    def modelpredict(self, data, mode):
      if mode == False:
          data.preprocess()
          model.modelLoad(mode)
          data.presenceResults = self.model.predict(data.image)
          data.presenceCheck()
      else:
          model.modelLoad(mode)
          data.subtypeResults = self.model.predict(data.image)
          data.subtypeCheck()

## Segmentation class, contain all function to segment the haemorrhage from the image.
class segment:  
    ## Class variables.
    dicom = ''
    windowed = []
    mask = []
    haemorrhage = []
    highlighted = []
    image = []

    ## Initialise function, will read DICOM information and store it.
    def __init__(self, instance):
        self.dicom = pydicom.dcmread('/content/drive/My Drive/Artefact/Samples/' + instance)
        self.image = self.dicom.pixel_array
        
    ## Window image, will window the image into set format using a threshold
    def windowImage(self, intercept, slope):
        img = self.image * int(slope) + int(intercept)
        img_min = 40 - 80 // 2
        img_max = 40 + 80 // 2
        img[img < img_min] = img_min
        img[img > img_max] = img_max
        self.windowed = img
      
    ## Peak finder function, will scan the image until a peak is found and coordinates of the peak are then saved.
    def peakFinder(self, img):
        ctr = 0
        mid = int(len(img[0]) / 2)
        for i in range(1, len(img)-1):
            if img[i][mid] == img.max():
                for j in range(mid-10, mid+10):
                    if img[i][j] == img.max():
                        ctr += 1
                if ctr > 15:
                    x = i
                    y = mid
                    return [x, y]
                else:
                    ctr = 0
    
    ## Skull strip function, will threhold the skull from a binary image based on the label at the peak. 
    def skullStrip(self, peak):
        label, objects_num = ndi.label(self.mask)
        for i in range(len(self.mask)):
            for j in range(len(self.mask[0])):
                if label[i][j] == label[peak[0]][peak[1]]:
                    continue
                else:
                    self.mask[i][j] = 0
        
    ## Skull mask function, will find a peak where the skull is, then threshold the skull out of the image and strip the skull out of the threshold.
    def skullMask(self):
        peak = self.peakFinder(self.windowed)
        skull = self.windowed
        thresh = skull < (skull.max() * 0.95)
        skull[thresh] = 0 
        self.mask = skull
        self.skullStrip(peak)
        self.windowImage(self.dicom.RescaleIntercept, self.dicom.RescaleSlope)
        
    ## Brain extraction function, will threshold the brain out of a windowed image. 
    def brainExtract(self, img):
        thresh = self.brain < 1
        img[thresh] = 0
        self.haemorrhage = img
    
    ## Haemorrhage extraction function, will threshold the brain based on a provided value. Further labelling the result and obtaining the second largest object within it.
    def haemExtract(self, value):
        thresh = self.haemorrhage < (self.haemorrhage.max() * value) #Performance can change on threshold of 0.5 and 0.6
        self.haemorrhage[thresh] = 0
        labels, num = ndi.label(self.haemorrhage)
        try:
            largestCC = np.argmax(np.bincount(labels.flat)[1:])+1
        except:
            largestCC = 0
        for i in range(len(self.haemorrhage)):
                    for j in range(len(self.haemorrhage[0])):
                        if labels[i][j] == largestCC:
                            continue
                        else:
                            self.haemorrhage[i][j] = 0
        
    ## Highlight function, will stack windowed images to make RGB format and increase the haemorrhage location on the red channel. 
    def highlight(self):
        self.windowImage(self.dicom.RescaleIntercept, self.dicom.RescaleSlope)
        r = np.copy(self.windowed)
        g = np.copy(self.windowed)
        b = np.copy(self.windowed)
        r += self.haemorrhage 
        scan = np.stack((r, g, b), axis=2)
        self.highlighted = scan * 2
    
    ## Get data function, pipeline function to utilise all other functions to extract the haemorrhage. 
    def getData(self, thresh):
        self.windowImage(self.dicom.RescaleIntercept, self.dicom.RescaleSlope)
        self.skullMask()
        filledMask = ndi .binary_fill_holes(self.mask)
        self.brain = filledMask - self.mask
        self.brainExtract(self.windowed)
        self.haemExtract(thresh)
        self.highlight()

## CMD script call argument check function, allows for the user to speciify their own threshold values and CT instances. 
def argCheck(argv, file, thresh):
    ## Nested for loop to check argument instances. 
    for i in range(1, len(argv)):
        if argv[i] == '-f':
            try:
                file = argv[i+1]
            except:
                print('No arguement after -f, please ensure you chose a file for the argument!')
                print('Terminating program...')
                sys.exit()
            if file[-4:] != '.dcm':
                print('Please enter a file which is in the .dcm format, file name and format entered %s' % (argv[i+1]))
                print('Terminating program...')
                sys.exit()
        elif argv[i-1] == '-f':
            continue
        elif argv[i] == '-sa':
            if i+1 > len(argv)-1:
                print('No arguement after -sa, please ensure you chose a float value between 0.0 and 1.0 for the argument!')
                print('Terminating program...')
                sys.exit()
            try:
                if 1.0 > float(argv[i+1]) and float(argv[i+1]) > 0.0:
                    thresh = float(argv[i+1])
                else:
                    print('Please enter a float value between 0.0 and 1.0, value entered: %s!' % (argv[i+1]))
                    print('Terminating program...')
                    sys.exit()
            except:
                print('Please enter a float value between 0.0 and 1.0, value entered: ' % (argv[i+1]), *self.presenceResults)
                print('Terminating program...')
                sys.exit()
        elif argv[i-1] == '-sa':
            continue
        else:
            print('Unexpected arguements, look at ReadMe file for more information on program arguements.')
            sys.exit()

    return file, thresh
def main(argv):
    file = ''
    thresh = -1.0
    file, thresh = argCheck(argv, file, thresh)

    if file == '':
        print('Please input a dicom filename, including the file format extension.')
        file = input()
    
    data = dataHandler()
    model = network()

    model.modelLoad(False)

    data.readDicom(file)

    print(data.image().min(), data.image().max())


if __name__ == '__main__':
    main(sys.argv)