import pandas as pd
import numpy as np


# df1 = pd.read_csv('./Data/statTime/CityData/hourly.csv', encoding='utf-8')
df2 = pd.read_csv('./Data/statTime/CityData/daily.csv', encoding='utf-8')
# df3 = pd.read_csv('./Data/statTime/CityData/monthly.csv', encoding='utf-8')
# df4 = pd.read_csv('./Data/statTime/CityData/yearly.csv', encoding='utf-8')

df2.drop(df2.columns[[0]], axis=1, inplace=True)
df2.drop(['U', 'V', 'temp', 'rh', 'psfc'], axis='columns', inplace=True)

pm25 = df2['pm2.5'].values.tolist()
pm10 = df2['pm10'].values.tolist()
so2 = df2['so2'].values.tolist()
no2 = df2['no2'].values.tolist()
co = df2['co'].values.tolist()
o3 = df2['o3'].values.tolist()

key_list = ['pm2.5', 'pm10', 'so2', 'no2', 'co', 'o3']
value_list = [pm25, pm10, so2, no2, co, o3]
dict1 = dict(zip(key_list, value_list))
data1 = np.array([[dict1]])

Idata = [
    [0, 35, 75, 115, 150, 250, 350, 500],  # PM2.5 24小时平均
    [0, 50, 150, 250, 350, 420, 500, 600],  # PM10 24小时平均
    [0, 50, 150, 475, 800, 1600, 2100, 2620],  # SO2 24小时平均
    [0, 40, 80, 180, 280, 565, 750, 940],  # NO2 24小时平均
    [0, 2, 4, 14, 24, 36, 48, 60],  # CO 24小时平均
    [0, 100, 160, 215, 265, 800]  # O3 8小时滑动平均
]
qua = [0, 50, 100, 150, 200, 300, 400, 500]

IAQI = list(np.zeros(len(data1[0][0]["pm2.5"])))

Data = np.array(
    [data1[0][0]["pm2.5"], data1[0][0]["pm10"], data1[0][0]["so2"], data1[0][0]["no2"], data1[0][0]["co"],
     data1[0][0]["o3"]])
Data = list(map(list, zip(*Data)))
Data = np.array(Data)

T_IA = 0
i = j = k = 0
for i in range(len(Idata)):
    T_data = Data[:, i]
    T_Idata = Idata[i]
    for j in range(len(T_data)):
        for k in range(1, len(T_Idata)):
            if T_Idata[k] > T_data[j]:
                break
        if k == (len(T_Idata) - 1) and T_Idata[k] < T_data[j]:
            T_IA = T_Idata[k]
        else:
            T_IA = int(round((((qua[k] - qua[k - 1]) / (T_Idata[k] - T_Idata[k - 1])) * (
                    T_data[j] - T_Idata[k - 1]) + qua[k - 1]) + 0.5))
        if T_IA > IAQI[j]:
            IAQI[j] = T_IA
data1[0][0]["AQI"] = IAQI

data = data1[0][0]["AQI"]
df_temp = pd.DataFrame(data, columns=['AQI'])
df_temp['AQI'] = df_temp['AQI'].astype('int')
df2['AQI'] = df_temp['AQI']

Lv = list()
for i in df2['AQI']:
    if i > 300:
        Lv.append('六级')
    elif i > 200:
        Lv.append('五级')
    elif i > 150:
        Lv.append('四级')
    elif i > 100:
        Lv.append('三级')
    elif i > 50:
        Lv.append('二级')
    else:
        Lv.append('一级')
df2['Lv'] = pd.DataFrame(Lv)

df2.to_csv('AQI_daily.csv', encoding='utf-8-sig', index=False)
