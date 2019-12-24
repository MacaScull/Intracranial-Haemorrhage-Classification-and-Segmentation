import csv
import pandas as pd

arr = []

print('Collecting data...')
with open('stage_1_train.csv', 'r') as file:
    readCSV = csv.reader(file)
    for row in readCSV:
        if row[0][13:] == 'any':
            arr.append([row[0][:12], row[1]])

print('Writing label csv file...')
arr = pd.DataFrame(arr)
arr.to_csv('presenceLabels.csv', header=False, index=False, mode='w',)

print('Label file successfully created!')