import pandas as pd

df = pd.read_csv('./Data/statTime/CityData/daily.csv', encoding='utf-8')
df.drop(df.columns[[0]], axis=1, inplace=True)
df.drop(['U', 'V', 'temp', 'rh', 'psfc'], axis='columns', inplace=True)
df['date'] = pd.to_datetime(df['date'])

P_sum = df[['pm2.5', 'pm10', 'so2', 'no2', 'co', 'o3']].sum(axis=1)
# 计算每个城市在所有日期的污染物百分比成分谱（归一化）
# 以pm2.5为例
df['P_pm25'] = df['pm2.5'].iloc[:] / P_sum

df['year'] = df['date'].dt.year  # 提取年份
df['month'] = df['date'].dt.month  # 提取月份
df['day'] = df['date'].dt.day  # 提取天数

city = df['city']
city = city.drop_duplicates()
city = list(city)

month_31 = [1, 3, 5, 7, 8, 10, 12]  # 31天的月份

P_pm25_ = list()  # 所有城市每个月pm2.5百分比成分谱的均值
sum_ = 0  # 计数器

# 计算某市这个月的pm2.5百分比成分谱`均值`
for i in range(len(city)):
    for j in range(len(df['city'])):
        if df['city'][j] == city[i]:  # 选取某市的数据
            if df['year'][j] == 2016:  # 闰年
                if df['month'][j] in month_31:  # 31天的月份
                    sum_ += df['P_pm25'][j]
                    # 算完一个月，计数器清零
                    if df['day'][j] == 31:
                        P_pm25_.append([df['city'][j], df['year'][j], df['month'][j], sum_ / 31])  # 均值
                        sum_ = 0
                elif df['month'][j] == 2:  # 闰年2月
                    sum_ += df['P_pm25'][j]
                    if df['day'][j] == 29:
                        P_pm25_.append([df['city'][j], df['year'][j], df['month'][j], sum_ / 29])
                        sum_ = 0
                else:  # 30天的月份
                    sum_ += df['P_pm25'][j]
                    if df['day'][j] == 30:
                        P_pm25_.append([df['city'][j], df['year'][j], df['month'][j], sum_ / 30])
                        sum_ = 0
            else:  # 非闰年
                if df['month'][j] in month_31:  # 31天的月份
                    sum_ += df['P_pm25'][j]
                    if df['day'][j] == 31:
                        P_pm25_.append([df['city'][j], df['year'][j], df['month'][j], sum_ / 31])
                        sum_ = 0
                elif df['month'][j] == 2:  # 非闰年2月
                    sum_ += df['P_pm25'][j]
                    if df['day'][j] == 28:
                        P_pm25_.append([df['city'][j], df['year'][j], df['month'][j], sum_ / 28])
                        sum_ = 0
                else:  # 30天的月份
                    sum_ += df['P_pm25'][j]
                    if df['day'][j] == 30:
                        P_pm25_.append([df['city'][j], df['year'][j], df['month'][j], sum_ / 30])
                        sum_ = 0
P_pm25_ = pd.DataFrame(P_pm25_)
P_pm25_.columns = ['city', 'year', 'month', 'P_pm25_']
P_pm25_.to_csv('P_pm25_.csv', encoding='utf-8-sig', index=False)  # 保存一下中间结果：均值

P_pm25_ = pd.read_csv('./P_pm25_.csv', encoding='utf-8')
# 计算某市，某日，某污染物（如pm2.5）的当日特征值
# C_pm25 = P_pm25 / P_pm25_
C_pm25 = list()
for i in range(len(city)):
    for j in range(len(df['city'])):
        if df['city'][j] == city[i]:  # 选取某市数据
            for k in range(len(P_pm25_['city'])):
                if df['city'][j] == P_pm25_['city'][k] and \
                        df['year'][j] == P_pm25_['year'][k] and \
                        df['month'][j] == P_pm25_['month'][k]:
                    C_pm25.append([df['city'][j], df['year'][j],
                                   df['month'][j], df['day'][j],
                                   df['P_pm25'][j] / P_pm25_['P_pm25_'][k]])
C_pm25 = pd.DataFrame(C_pm25)
C_pm25.columns = ['city', 'year', 'month', 'day', 'C_pm25_']
C_pm25.to_csv('C_pm25.csv', encoding='utf-8-sig', index=False)  # 保存：特征值

# 把C_pm25添加到df
df = pd.merge(df, C_pm25, on=['city', 'year', 'month', 'day'], how='inner')
# 删除中间数据：P_pm25, year, month, day
df.drop(['P_pm25', 'year', 'month', 'day', 'pm2.5', 'pm10', 'so2', 'no2', 'co', 'o3'], axis=1, inplace=True)
# 保存数据
df.to_csv('EI_daily_pm25.csv', encoding='utf-8-sig', index=False)
