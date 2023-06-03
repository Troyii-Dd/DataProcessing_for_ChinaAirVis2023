import pandas as pd

'''
# 大气污染成因
1.标准型：各污染物特征值均未超出污染物特征值上下限，污染特征未发生显著变化；
2.偏二次型：pm25超出上限；
3.偏沙尘型：pm10超出上限；
4.偏机动车型：no2与co特征值超出上限；
5.偏燃煤型：so2特征值明显超出上限；
6.偏烟花型：pm25和so2特征值明显超出上限；
7.偏钢铁型：so2、no2与co特征值超出上限；
8.其他型：其他情况。
'''

# province, year, month, day, C_pm25, C_pm10, C_so2, C_no2, C_co, C_o3, date
df = pd.read_csv('./Data/pollutionType/ProvData/EI_daily_fin.csv', encoding='utf-8')
# prov, year, month, Max_6种污染物
PS_fin = pd.read_csv('./Data/pollutionType/ProvData/PS_fin.csv', encoding='utf-8')

Type = list()  # 污染类型
for i in range(len(df['province'])):
    for j in range(len(PS_fin['prov'])):
        if df['province'][i] == PS_fin['prov'][j] and \
                df['year'][i] == PS_fin['year'][j] and \
                df['month'][i] == PS_fin['month'][j]:  # 某市某年月数据一一对应
            if df['C_pm25'][i] < PS_fin['Max_pm25'][j] and \
                    df['C_pm10'][i] < PS_fin['Max_pm10'][j] and \
                    df['C_so2'][i] < PS_fin['Max_so2'][j] and \
                    df['C_no2'][i] < PS_fin['Max_no2'][j] and \
                    df['C_co'][i] < PS_fin['Max_co'][j] and \
                    df['C_o3'][i] < PS_fin['Max_o3'][j]:
                Type.append('标准型')
            elif df['C_pm25'][i] > PS_fin['Max_pm25'][j] and \
                    df['C_pm10'][i] < PS_fin['Max_pm10'][j] and \
                    df['C_so2'][i] < PS_fin['Max_so2'][j] and \
                    df['C_no2'][i] < PS_fin['Max_no2'][j] and \
                    df['C_co'][i] < PS_fin['Max_co'][j] and \
                    df['C_o3'][i] < PS_fin['Max_o3'][j]:
                Type.append('偏二次型')
            elif df['C_pm10'][i] > PS_fin['Max_pm10'][j] and \
                    df['C_pm25'][i] < PS_fin['Max_pm25'][j] and \
                    df['C_so2'][i] < PS_fin['Max_so2'][j] and \
                    df['C_no2'][i] < PS_fin['Max_no2'][j] and \
                    df['C_co'][i] < PS_fin['Max_co'][j] and \
                    df['C_o3'][i] < PS_fin['Max_o3'][j]:
                Type.append('偏沙尘型')
            elif df['C_no2'][i] > PS_fin['Max_no2'][j] and \
                    df['C_co'][i] > PS_fin['Max_co'][j] and \
                    df['C_pm25'][i] < PS_fin['Max_pm25'][j] and \
                    df['C_pm10'][i] < PS_fin['Max_pm10'][j] and \
                    df['C_so2'][i] < PS_fin['Max_so2'][j] and \
                    df['C_o3'][i] < PS_fin['Max_o3'][j]:
                Type.append('偏机动车型')
            elif df['C_so2'][i] > PS_fin['Max_so2'][j] and \
                    df['C_pm25'][i] < PS_fin['Max_pm25'][j] and \
                    df['C_pm10'][i] < PS_fin['Max_pm10'][j] and \
                    df['C_no2'][i] < PS_fin['Max_no2'][j] and \
                    df['C_co'][i] < PS_fin['Max_co'][j] and \
                    df['C_o3'][i] < PS_fin['Max_o3'][j]:
                Type.append('偏燃煤型')
            elif df['C_so2'][i] > PS_fin['Max_so2'][j] and \
                    df['C_pm25'][i] > PS_fin['Max_pm25'][j] and \
                    df['C_pm10'][i] < PS_fin['Max_pm10'][j] and \
                    df['C_no2'][i] < PS_fin['Max_no2'][j] and \
                    df['C_co'][i] < PS_fin['Max_co'][j] and \
                    df['C_o3'][i] < PS_fin['Max_o3'][j]:
                Type.append('偏烟花型')
            elif df['C_so2'][i] > PS_fin['Max_so2'][j] and \
                    df['C_no2'][i] > PS_fin['Max_no2'][j] and \
                    df['C_co'][i] > PS_fin['Max_co'][j] and \
                    df['C_pm25'][i] < PS_fin['Max_pm25'][j] and \
                    df['C_pm10'][i] < PS_fin['Max_pm10'][j] and \
                    df['C_o3'][i] < PS_fin['Max_o3'][j]:
                Type.append('偏钢铁型')
            else:
                Type.append('其他型')

# 把Type添加到df
df['Type'] = Type
# df = pd.merge(df, Type, on=['province', 'year', 'month', 'day'], how='inner')

# 删除中间数据：year, month, day, C_pm25, C_pm10, C_so2, C_no2, C_co, C_o3
df = df.drop(['year', 'month', 'day', 'C_pm25', 'C_pm10', 'C_so2', 'C_no2', 'C_co', 'C_o3'], axis=1)

# 保存数据
df.to_csv('PollutionType_prov_daily.csv', encoding='utf-8-sig', index=False)
