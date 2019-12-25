import csv
import pandas as pd

## Presence label CSV file creation
arr = []

# Summarise data into presence or no presence utilising the any label
print('Collecting data...')
with open('stage_1_train.csv', 'r') as file:
    readCSV = csv.reader(file)
    for row in readCSV:
        if row[0][13:] == 'any':
            arr.append([row[0][:12], row[1]])

# Convert list to a dataframe and then produce a CSV file 
print('Writing label csv file...')
arr = pd.DataFrame(arr)
arr.to_csv('presenceLabels.csv', header=False, index=False, mode='w',)

print('Label file successfully created!')


## Subtype label CSV file creation
arr, loc = [], []

# Locate all data from the CSV file, taking index of all haemorrhage data if any == 1 then produce the the rest of the indexes for that ID
print('Locating data...')
with open('stage_1_train.csv', 'r') as file:
    readCSV = csv.reader(file)
    for row in readCSV:
        if row[0][13:] == 'any' and row[1] == '1':
            for i in range(-5, 0):
                loc.append((readCSV.line_num)+i)

# Collect all data about IDs containing a haemorrhage utilising indexing
print('Collecting data...')
with open('stage_1_train.csv', 'r') as file:
    readCSV = csv.reader(file)
    readCSV = list(readCSV)
    for i in loc:
        arr.append(readCSV[i-1])

# Convert list to a dataframe and then produce a CSV file 
print('Writing label csv file...')
arr = pd.DataFrame(arr)
arr.to_csv('subtypeLabels.csv', header=False, index=False, mode='w',)

print('Label file successfully created!')