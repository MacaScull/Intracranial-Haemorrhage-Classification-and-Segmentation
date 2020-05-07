import csv
import pandas as pd
import hashlib
import pydicom
import operator
import shutil 


# ## Presence label CSV file creation
# arr = []

# ## Summarise data into presence or no presence utilising the any label
# print('Collecting data...')
# with open('stage_1_train.csv', 'r') as file:
#     readCSV = csv.reader(file)
#     for row in readCSV:
#         if row[0][13:] == 'any':
#             h = hashlib.sha1(row[0][:12].encode('utf'))
#             arr.append([h.hexdigest() ,row[0][:12], row[1]])

# ## Convert list to a dataframe and then produce a CSV file 
# print('Writing label csv file...')
# arr = pd.DataFrame(arr)
# arr = arr.drop_duplicates()
# arr.to_csv('presenceLabels.csv', header=False, index=False, mode='w',)

# print('Label file successfully created!')

## Check if there are any duplicate hash values 
# arr = pd.read_csv('presenceLabels.csv', index_col=False, names=['Hash', 'ID', 'Label'], header=None)
# print(arr.Hash.duplicated().sum())
# dup = pd.DataFrame(arr.Hash.duplicated(), columns=['Hash'])
# index = dup[dup['Hash'] == True].index.tolist()
# print(index)

# ## Subtype label CSV file creation
# arr, loc = [], []

# ## Locate all data from the CSV file, taking index of all haemorrhage data if any == 1 then produce the the rest of the indexes for that ID
# print('Locating data...')
# with open('stage_1_train.csv', 'r') as file:
#     readCSV = csv.reader(file)
#     for row in readCSV:
#         if row[0][13:] == 'any' and row[1] == '1':
#             for i in range(-5, 0):
#                 loc.append((readCSV.line_num)+i)

# ## Collect all data about IDs containing a haemorrhage utilising indexing
# print('Collecting data...')
# with open('stage_1_train.csv', 'r') as file:
#     readCSV = csv.reader(file)
#     readCSV = list(readCSV)
#     for i in loc:
#         h = hashlib.sha1(readCSV[i-1][0][:12].encode('utf'))
#         arr.append([h.hexdigest(), readCSV[i-1][0], readCSV[i-1][1]])

# ## Convert list to a dataframe and then produce a CSV file 
# print('Writing label csv file...')
# arr = pd.DataFrame(arr)
# arr.to_csv('subtypeLabels.csv', header=False, index=False, mode='w',)

# print('Label file successfully created!')

# ## Check if there are any duplicate hash values 
# arr = pd.read_csv('subtypeLabels.csv', index_col=False, names=['Hash', 'ID', 'Label'], header=None)
# print(arr.ID.duplicated().sum())
# dup = pd.DataFrame(arr.ID.duplicated(), columns=['ID'])
# index = dup[dup['ID'] == True].index.tolist()
# print(index)


## Subtype label CSV file creation alt
# arr, loc = [], []

# ## Locate all data from the CSV file, taking index of all haemorrhage data if any == 1 then produce the the rest of the indexes for that ID
# print('Locating data...')
# with open('subtypeLabels.csv', 'r') as file:
#     readCSV = csv.reader(file)
#     for row in readCSV:
#         print(row)

## Convert list to a dataframe and then produce a CSV file 
# print('Writing label csv file...')
# arr = pd.DataFrame(arr)
# arr.to_csv('subtypeLabels.csv', header=False, index=False, mode='w',)

# print('Label file successfully created!')

# i = 0
# ctr0 = 0
# ctr1 = 0
# total = 251
# sub = 126

# print('Locating and copying data...')

# with open('G:/Datasets/presenceLabels.csv', 'r') as file:
#     reader = csv.reader(file)
#     sortedlist = sorted(reader, key=operator.itemgetter(2), reverse=True)
#     for row in sortedlist:
#         if ctr0 < sub and row[2] == '0':
#             if i < total:
#                 print(i, row[1], row[2])
#                 ps = pydicom.dcmread('G:/Datasets/rsna-intracranial-hemorrhage-detection/stage_1_train_images/' + row[1] + '.dcm')
#                 if ps.Rows != 512 or ps.Columns != 512:
#                     continue
#                 shutil.copy2('G:/Datasets/rsna-intracranial-hemorrhage-detection/stage_1_train_images/' + row[1] + '.dcm','G:/Datasets/Data/')
#                 i += 1
#                 ctr0 += 1
#             else:
#                 break
#         elif ctr1 < sub and row[2] == '1':
#             if i < total:
#                 print(i, row[1], row[2])
#                 ps = pydicom.dcmread('G:/Datasets/rsna-intracranial-hemorrhage-detection/stage_1_train_images/' + row[1] + '.dcm')
#                 if ps.Rows != 512 or ps.Columns != 512:
#                     continue
#                 shutil.copy2('G:/Datasets/rsna-intracranial-hemorrhage-detection/stage_1_train_images/' + row[1] + '.dcm','G:/Datasets/Data/'+row[1]+'.dcm')
#                 i += 1
#                 ctr1 += 1
#             else:
#                 break

# print("Copying finished!")

i = 0

# with open('G:/Datasets/presenceLabels.csv', 'r') as file:
#     reader = csv.reader(file)
#     sortedlist = sorted(reader, key=operator.itemgetter(2), reverse=True)
#     for row in sortedlist:
#         if row[2] == '1':
#             if i < 251:
#                 print(row[1])
#                 #print(i, row[1], row[2])
#                 ps = pydicom.dcmread('G:/Datasets/rsna-intracranial-hemorrhage-detection/stage_1_train_images/' + row[1] + '.dcm')
#                 if ps.Rows != 512 or ps.Columns != 512:
#                     continue
#                 shutil.copy2('G:/Datasets/rsna-intracranial-hemorrhage-detection/stage_1_train_images/' + row[1] + '.dcm','G:/Datasets/Data/'+row[1]+'.dcm')
#                 i += 1

# skip = 0
# total = 501
# with open('D:/Uni/Year 3/Project/Intracranial-Haemorrhage-Classification-and-Segmentation/Labels/subtypeLabels.csv', 'r') as file:
#     print('Loading data...')
#     reader = csv.reader(file)
#     temp = []
#     for row in reader:
#         if i < total:
#             if skip == 0:
#                 print(i, row[1][:12])
#                 ps = pydicom.dcmread('G:/Datasets/rsna-intracranial-hemorrhage-detection/stage_1_train_images/' + row[1][:12] + '.dcm')
#                 if ps.Rows != 512 or ps.Columns != 512:
#                     i -= 1
#                 shutil.copy2('G:/Datasets/rsna-intracranial-hemorrhage-detection/stage_1_train_images/' + row[1][:12] + '.dcm','G:/Datasets/SubData/' + row[1][:12] + '.dcm')
#                 skip = 4
#                 i +=1
#             else:
#                 skip -= 1
#         else:
#             break

def check(s, i, ctr):
    if s == 'epidural' and i == '1':
        ctr[0] += 1
    elif s == 'intraparenchymal' and i == '1':
        ctr[1] += 1
    elif s == 'intraventricular' and i == '1':
        ctr[2] += 1
    elif s == 'subarachnoid' and i == '1':
        ctr[3] += 1
    elif s == 'subdural' and i == '1':
        ctr[4] += 1
    
    return ctr


ctr = [0,0,0,0,0]
skip = 0
total = 501
with open('D:/Uni/Year 3/Project/Intracranial-Haemorrhage-Classification-and-Segmentation/Labels/subtypeLabels.csv', 'r') as file:
    print('Loading data...')
    reader = csv.reader(file)
    temp = []
    for row in reader:
        if i < total:
            if skip == 0:
                #print(i, row[1][:12])
                ps = pydicom.dcmread('G:/Datasets/rsna-intracranial-hemorrhage-detection/stage_1_train_images/' + row[1][:12] + '.dcm')
                if ps.Rows != 512 or ps.Columns != 512:
                    i -= 1
                check(row[1][13:], row[2], ctr)
                skip = 4
                i +=1
            else:
                check(row[1][13:], row[2], ctr)
                skip -= 1
        else:
            break

print(ctr)
