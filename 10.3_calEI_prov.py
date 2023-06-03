import pandas as pd
import math

# 读取省份数据
df = pd.read_csv('./Data/statTime/ProvData/daily.csv', encoding='utf-8')
df.drop(df.columns[[0]], axis=1, inplace=True)
df['date'] = pd.to_datetime(df['date'])
df.drop(['U', 'V', 'temp', 'rh', 'psfc'], axis='columns', inplace=True)

P_sum = df[['pm2.5', 'pm10', 'so2', 'no2', 'co', 'o3']].sum(axis=1)
df['P_pm25'] = df['pm2.5'].iloc[:] / P_sum

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

prov = df['province']
prov = prov.drop_duplicates()
prov = list(prov)

month_31 = [1, 3, 5, 7, 8, 10, 12]

sum_ = 0
P_pm25_ = list()
S_pm25 = list()

# 计算某省这个月的pm2.5百分比成分谱`均值`
for i in range(len(prov)):
    for j in range(len(df['province'])):
        if df['province'][j] == prov[i]:  # 选取某省的数据
            if df['year'][j] == 2016:  # 闰年
                if df['month'][j] in month_31:  # 31天的月份
                    sum_ += df['P_pm25'][j]
                    # 算完一个月，计数器清零
                    if df['day'][j] == 31:
                        P_pm25_.append([df['province'][j], df['year'][j], df['month'][j], sum_ / 31])  # 均值
                        sum_ = 0
                elif df['month'][j] == 2:  # 闰年2月
                    sum_ += df['P_pm25'][j]
                    if df['day'][j] == 29:
                        P_pm25_.append([df['province'][j], df['year'][j], df['month'][j], sum_ / 29])
                        sum_ = 0
                else:  # 30天的月份
                    sum_ += df['P_pm25'][j]
                    if df['day'][j] == 30:
                        P_pm25_.append([df['province'][j], df['year'][j], df['month'][j], sum_ / 30])
                        sum_ = 0
            else:  # 非闰年
                if df['month'][j] in month_31:  # 31天的月份
                    sum_ += df['P_pm25'][j]
                    if df['day'][j] == 31:
                        P_pm25_.append([df['province'][j], df['year'][j], df['month'][j], sum_ / 31])
                        sum_ = 0
                elif df['month'][j] == 2:  # 非闰年2月
                    sum_ += df['P_pm25'][j]
                    if df['day'][j] == 28:
                        P_pm25_.append([df['province'][j], df['year'][j], df['month'][j], sum_ / 28])
                        sum_ = 0
                else:  # 30天的月份
                    sum_ += df['P_pm25'][j]
                    if df['day'][j] == 30:
                        P_pm25_.append([df['province'][j], df['year'][j], df['month'][j], sum_ / 30])
                        sum_ = 0
P_pm25_ = pd.DataFrame(P_pm25_)
P_pm25_.columns = ['prov', 'year', 'month', 'P_pm25_']
P_pm25_.to_csv('P_pm25_.csv', encoding='utf-8-sig', index=False)

P_pm25_ = pd.read_csv('./P_pm25_.csv', encoding='utf-8')
# 计算某省这个月的pm2.5百分比成分谱`标准差`
for i in range(len(prov)):
    for j in range(len(df['province'])):
        if df['province'][j] == prov[i]:  # 选取某省的数据
            if df['year'][j] == 2016:  # 闰年
                if df['month'][j] in month_31:  # 31天的月份
                    for k in range(len(P_pm25_['month'])):
                        if df['province'][j] == P_pm25_['prov'][k] and \
                                df['year'][j] == P_pm25_['year'][k] and \
                                df['month'][j] == P_pm25_['month'][k]:  # 某省某年月的数据一一对应
                            sum_ += math.pow(df['P_pm25'][j] - P_pm25_['P_pm25_'][k], 2)  # 平方和
                            # 算完一个月，计数器清零
                            if df['day'][j] == 31:
                                # 标准差
                                S_pm25.append(math.sqrt(sum_ / 30))
                                sum_ = 0  # 计数器清零
                elif df['month'][j] == 2:  # 闰年2月
                    for k in range(len(P_pm25_['month'])):
                        if df['province'][j] == P_pm25_['prov'][k] and \
                                df['year'][j] == P_pm25_['year'][k] and \
                                df['month'][j] == P_pm25_['month'][k]:
                            sum_ += math.pow(df['P_pm25'][j] - P_pm25_['P_pm25_'][k], 2)
                            if df['day'][j] == 29:
                                S_pm25.append(math.sqrt(sum_ / 28))
                                sum_ = 0
                else:  # 30天的月份
                    for k in range(len(P_pm25_['month'])):
                        if df['province'][j] == P_pm25_['prov'][k] and \
                                df['year'][j] == P_pm25_['year'][k] and \
                                df['month'][j] == P_pm25_['month'][k]:
                            sum_ += math.pow(df['P_pm25'][j] - P_pm25_['P_pm25_'][k], 2)
                            if df['day'][j] == 30:
                                S_pm25.append(math.sqrt(sum_ / 29))
                                sum_ = 0
            else:  # 非闰年
                if df['month'][j] in month_31:  # 31天的月份
                    for k in range(len(P_pm25_['month'])):
                        if df['province'][j] == P_pm25_['prov'][k] and \
                                df['year'][j] == P_pm25_['year'][k] and \
                                df['month'][j] == P_pm25_['month'][k]:
                            sum_ += math.pow(df['P_pm25'][j] - P_pm25_['P_pm25_'][k], 2)
                            if df['day'][j] == 31:
                                S_pm25.append(math.sqrt(sum_ / 30))
                                sum_ = 0
                elif df['month'][j] == 2:  # 非闰年2月
                    for k in range(len(P_pm25_['month'])):
                        if df['province'][j] == P_pm25_['prov'][k] and \
                                df['year'][j] == P_pm25_['year'][k] and \
                                df['month'][j] == P_pm25_['month'][k]:
                            sum_ += math.pow(df['P_pm25'][j] - P_pm25_['P_pm25_'][k], 2)
                            if df['day'][j] == 28:
                                S_pm25.append(math.sqrt(sum_ / 27))
                                sum_ = 0
                else:  # 30天的月份
                    for k in range(len(P_pm25_['month'])):
                        if df['province'][j] == P_pm25_['prov'][k] and \
                                df['year'][j] == P_pm25_['year'][k] and \
                                df['month'][j] == P_pm25_['month'][k]:
                            sum_ += math.pow(df['P_pm25'][j] - P_pm25_['P_pm25_'][k], 2)
                            if df['day'][j] == 30:
                                S_pm25.append(math.sqrt(sum_ / 29))
                                sum_ = 0
S_pm25 = pd.DataFrame(S_pm25, columns=['S_pm25'])
PS_pm25 = P_pm25_
PS_pm25['S_pm25'] = S_pm25['S_pm25']
PS_pm25.to_csv('PS_pm25.csv', encoding='utf-8-sig', index=False)

PS_pm25 = pd.read_csv('./PS_pm25.csv', encoding='utf-8')
Min_pm25 = list()
Max_pm25 = list()
for i in range(len(PS_pm25['P_pm25_'])):
    Min_pm25.append((PS_pm25['P_pm25_'][i] - PS_pm25['S_pm25'][i]) / PS_pm25['P_pm25_'][i])
    Max_pm25.append((PS_pm25['P_pm25_'][i] + PS_pm25['S_pm25'][i]) / PS_pm25['P_pm25_'][i])
PS_pm25['Min_pm25'] = pd.DataFrame(Min_pm25)
PS_pm25['Max_pm25'] = pd.DataFrame(Max_pm25)
PS_pm25.to_csv('PS_pm25_fin.csv', encoding='utf-8-sig', index=False)  # 保存：均值、标准差、特征值上下限

PS_pm25 = pd.read_csv('./PS_pm25_fin.csv', encoding='utf-8')
C_pm25 = list()
for i in range(len(prov)):
    for j in range(len(df['province'])):
        if df['province'][j] == prov[i]:
            for k in range(len(PS_pm25['prov'])):
                if df['province'][j] == PS_pm25['prov'][k] and \
                        df['year'][j] == PS_pm25['year'][k] and \
                        df['month'][j] == PS_pm25['month'][k]:
                    C_pm25.append(df['P_pm25'][j] / PS_pm25['P_pm25_'][k])
df['C_pm25'] = C_pm25
df.drop(['P_pm25', 'year', 'month', 'day', 'pm2.5', 'pm10', 'so2', 'no2', 'co', 'o3'], axis=1, inplace=True)
df.to_csv('EI_pm25_daily.csv', encoding='utf-8-sig', index=False)
