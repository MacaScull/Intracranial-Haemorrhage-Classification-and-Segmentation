import csv
import pandas as pd
import hashlib

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