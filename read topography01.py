# 注意
# 导出数据的时候，记得切去CMB的数据，再使用这些代码转换

import pandas as pd
import numpy as np

# 读取 CSV 数据，跳过第一行，并将列数据转换为数值型
df = pd.read_csv('dt_0km.csv', skiprows=1, header=None, names=['value', 'x', 'y', 'z'], dtype=str)

# 将数据转换为数值类型
df['value'] = pd.to_numeric(df['value'], errors='coerce')
df['x'] = pd.to_numeric(df['x'], errors='coerce')
df['y'] = pd.to_numeric(df['y'], errors='coerce')
df['z'] = pd.to_numeric(df['z'], errors='coerce')

# 计算 r, phi, theta
df['r'] = np.sqrt(df['x']**2 + df['y']**2 + df['z']**2)
df['phi'] = np.arctan2(df['y'], df['x'])  # 计算角度 phi (弧度)
df['theta'] = np.arccos(df['z'] / df['r'])  # 计算角度 theta (弧度)

# 转换为经纬度
df['latitude'] = 90 - (df['theta'] * 180 / np.pi)
df['longitude'] = df['phi'] * 180 / np.pi

# 创建新的 DataFrame 只包含纬度、经度和 value
new_df = df[['latitude', 'longitude', 'value']]

# 保存为新的 CSV 文件
new_df.to_csv('latitude_longitude_dt0km.csv', index=False)
