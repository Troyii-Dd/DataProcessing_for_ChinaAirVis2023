# 拆分AQI_city_daily -> 文件夹：201301, 201302, ... -> 20130101.csv, 20130102.csv, ...
import pandas as pd

df = pd.read_csv('./Data/calAQI/temp.csv', encoding='utf-8')
path = './Data/calAQI/sepAQI_city_daily/'

df['date'] = pd.to_datetime(df['date'])
date = df['date'].drop_duplicates()
date.reset_index()

year = date.dt.year
month = date.dt.month
day = date.dt.day

year = list(year)
month = list(month)
day = list(day)

m = 0
n = 369  # city: 369
for i in range(2191):  # 2191天
    temp = df.iloc[m: n]  # 被拆分的一段
    year_ = year[i]
    month_ = month[i]
    day_ = day[i]
    temp.to_csv(path + f'{year_}' + f'{month_:02d}' +
                '/CN-Reanalysis-daily-' + f'{year_}' + f'{month_:02d}' + f'{day_:02d}' + '00.csv',
                encoding='utf-8-sig', index=False)
    m += 369
    n += 369
