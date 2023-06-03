import pandas as pd
import numpy as np
import math

df = pd.read_csv('./Data/statTime/CityData/daily.csv', encoding='utf-8')
df.drop(df.columns[[0]], axis=1, inplace=True)
df.drop(['pm2.5', 'pm10', 'so2', 'no2', 'co', 'o3'], axis='columns', inplace=True)

df1 = df[['province', 'city', 'rh', 'date']]
df2 = df[['province', 'city', 'psfc', 'date']]

# 开尔文转摄氏度
temp_C = df['temp'] - 273.15
df['temp_C'] = temp_C
df.drop('temp', axis=1, inplace=True)
df.rename(columns={'temp_C': 'temp'}, inplace=True)

# 计算日均风速
# ws = math.sqrt(U ** 2 + V ** 2)
U = df['U']
V = df['V']
U2 = U ** 2
V2 = V ** 2
ws = list(np.zeros(len(U2)))
for i in range(len(U2)):
    ws = math.sqrt(U2[i] + V2[i])
df['ws'] = ws

# 计算风向
deg = 180.0 / math.pi
wd = 180.0 + deg * np.arctan2(U, V)
df['wd'] = wd

# 判断风向
# 东北风：0-90
# 东南风：90-180
# 西南风：180-270
# 西北风：270-360
wd_ = list(np.zeros(len(wd)))
for i in range(len(wd)):
    if 0 < wd[i] < 90:
        wd_[i] = '东北风'
    elif 90 < wd[i] < 180:
        wd_[i] = '东南风'
    elif 180 < wd[i] < 270:
        wd_[i] = '西南风'
    elif 270 < wd[i] < 360:
        wd_[i] = '西北风'
    elif wd[i] == 0 or wd[i] == 360:
        wd_[i] = '正北风'
    elif wd[i] == 90:
        wd_[i] = '正东风'
    elif wd[i] == 180:
        wd_[i] = '正南风'
    elif wd[i] == 270:
        wd_[i] = '正西风'
df['wd_'] = wd_

df3 = df[['province', 'city', 'ws', 'wd', 'wd_', 'date']]
df4 = df[['province', 'city', 'temp', 'date']]

df1.to_csv('./daily_rh.csv', encoding='utf-8-sig', index=False)  # 相对湿度
df2.to_csv('./daily_psfc.csv', encoding='utf-8-sig', index=False)  # 地面气压
df3.to_csv('./daily_w.csv', encoding='utf-8-sig', index=False)  # 风速、风向
df4.to_csv('./daily_temp.csv', encoding='utf-8-sig', index=False)  # 摄氏度
