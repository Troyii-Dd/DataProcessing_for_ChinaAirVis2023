import pandas as pd
import re
import os


def extract_date(string):
    match = re.match('.*(\d{10})', string)
    if match != None:
        date = match.group(1)
        date = date[:4] + '-' + date[4:6] + '-' + date[6:8] + '-' + date[-2:]
        return date


in_path = './Data/GeoData/CityData/hourly'
out_path = './Data/statTime/CityData/'

allFiles = []
for i in os.listdir(in_path):
    for j in os.listdir(os.path.join(in_path, i)):
        path = os.path.join(in_path, i, j)
        allFiles.append(path)

df_list = []
for file_ in allFiles:
    df = pd.read_csv(file_, index_col=None, header=0)
    df.columns = map(str.lower, df.columns)
    df['date'] = extract_date(file_)
    df_list.append(df)

df = pd.concat(df_list)
# print(df)
df.to_csv(out_path + 'hourly.csv', encoding='utf-8-sig')
