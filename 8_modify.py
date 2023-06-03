import pandas as pd

# city:
in_path = './Data/statTime/CityData/'
out_path = './Data/statTime/CityData/'

# province:
# in_path = './Data/statTime/ProvData/'
# out_path = './Data/statTime/ProvData/'

## df = pd.read_csv(in_path + 'daily.csv', encoding='utf-8')
df = pd.read_csv(in_path + 'hourly.csv', encoding='utf-8')

# city:
df.drop(df.columns[[0,14,15]], axis=1, inplace=True)
# province:
# df.drop(df.columns[[0,13,14]], axis=1, inplace=True)

df['date'] = pd.to_datetime(df['date'])
df.rename(columns={'pm2.5(微克每立方米)': 'pm2.5',
                   'pm10(微克每立方米)': 'pm10',
                   'so2(微克每立方米)': 'so2',
                   'no2(微克每立方米)': 'no2',
                   'co(毫克每立方米)': 'co',
                   'o3(微克每立方米)': 'o3',
                   'u(m/s)': 'U',
                   'v(m/s)': 'V',
                   'temp(k)': 'temp',
                   'rh(%)': 'rh',
                   'psfc(pa)': 'psfc'}, inplace=True)

## df.to_csv(out_path + 'daily.csv', encoding='utf-8-sig')
df.to_csv(out_path + 'hourly.csv', encoding='utf-8-sig')