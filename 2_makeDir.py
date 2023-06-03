import os

# path_daily = './Data/GeoData/ProvData/daily/'
path_daily = './Data/calAQI/sepAQI_city_daily/'
for i in range(3, 9):  # 2013-2018
    for j in range(1, 13):
        isExists = os.path.exists(path_daily + f'201{i}{j:02d}')
        if not isExists:
            os.makedirs(path_daily + f'201{i}{j:02d}')
        else:
            continue

'''
path_hourly = './Data/GeoData/ProvData/hourly/'
for i in range(3, 9):  # 2013-2018
    isExists = os.path.exists(path_hourly + f'201{i}')
    if not isExists:
        os.makedirs(path_hourly + f'201{i}')
    else:
        continue
'''
