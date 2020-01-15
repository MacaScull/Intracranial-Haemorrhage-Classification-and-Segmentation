import pydicom 
import csv

import tensorflow as tf
from tensorflow.keras import datasets, layers, models

def dataSplit(data, split):
    Xtrain, ytrain, Xtest, ytest = [], [], [], []
    trainlen = round(len(data)*split)
    
    for i in range(len(data)):
        if i < trainlen:
            Xtrain.append(data[i][0])
            ytrain.append(data[i][1])
        else:
            Xtest.append(data[i][0])
            ytest.append(data[i][1])

    return Xtrain, ytrain, Xtest, ytest

data = []
i = 1

with open('./Labels/presenceLabels.csv', 'r') as file:
    file = csv.reader(file)
    for row in file:
        if i == 101:
            break
        print(i , ': ', row[1], ' ', row[2])
        img = pydicom.dcmread('G:/Datasets/rsna-intracranial-hemorrhage-detection/stage_1_train_images/'+ row[1] + '.dcm').pixel_array
        data.append([img, row[2]])
        i += 1


Xtrain, ytrain, Xtest, ytest = dataSplit(data, 0.7)

model = models.Sequential()
model.add(layers.)
