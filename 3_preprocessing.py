import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import concurrent.futures as cf


def temp(in_path, template_path, out_path):
    df = pd.read_csv(in_path, encoding='utf-8')
    df.columns = [item.strip() for item in df.columns.values]
    del df['']
    df_template = pd.read_csv(template_path, encoding='utf-8')
    df['province'] = df_template['province']
    df['city'] = df_template['city']

    # 删除省份/城市字段为空的数据（表明该坐标点不在国内或无法在高德地图中查询）
    df = df.drop(df[df['province'] == '[]'].index)
    df = df.drop(df[(df['city'] == '[]') & (df['province'] != '台湾省')].index)

    # df = df.groupby(['province', 'city']).mean()
    df = df.groupby(by='province').mean()
    df.to_csv(out_path, encoding='utf-8-sig')
    # df = pd.read_csv(out_path, encoding='utf-8-sig')
    # df.to_excel(out_path[:-3]+'xlsx', index=0, encoding='utf-8-sig')
    # os.remove(out_path)


def day(template_path):
    root = 'E:/RawData/daily'
    for i in os.listdir(root):
        with tqdm(total=31) as bar:
            with cf.ThreadPoolExecutor() as tp:
                for j in os.listdir(os.path.join(root, i)):
                    csv_path = os.path.join(root, i, j)
                    tp.submit(temp(csv_path, 'template.csv', os.path.join(
                        './Data/GeoData/ProvData/daily', i, j))).add_done_callback(lambda fn: bar.update())


def hour(template_path):
    root = 'E:/RawData/hourly'
    for i in os.listdir(root):
        with tqdm(total=744) as bar:
            with cf.ThreadPoolExecutor() as tp:
                for j in os.listdir(os.path.join(root, i)):
                    csv_path = os.path.join(root, i, j)
                    tp.submit(temp(csv_path, 'template.csv', os.path.join(
                        './Data/GeoData/ProvData/hourly', i, j))).add_done_callback(lambda fn: bar.update())


if __name__ == '__main__':
    day('template.csv')
    hour('template.csv')
