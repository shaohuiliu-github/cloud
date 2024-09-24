import pandas as pd
import numpy as np

# 1. 读取 CSV 文件
df = pd.read_csv('20Ma_depth0_dt.csv')

# 2. 计算方向余弦 l_r, m_r, n_r (基于 X, Y, Z 坐标)
df['r'] = np.sqrt(df['Points:0']**2 + df['Points:1']**2 + df['Points:2']**2)
df['theta'] = np.arccos(df['Points:2'] / df['r'])
df['phi'] = np.arctan2(df['Points:1'], df['Points:0'])

df['l_r'] = np.sin(df['theta']) * np.cos(df['phi'])
df['m_r'] = np.sin(df['theta']) * np.sin(df['phi'])
df['n_r'] = np.cos(df['theta'])

# 3. 计算 stress_rr
df['stress_rr'] = (df['stress:0'] * df['l_r']**2 + 
                   df['stress:4'] * df['m_r']**2 + 
                   df['stress:8'] * df['n_r']**2 +
                   2 * df['stress:1'] * df['l_r'] * df['m_r'] + 
                   2 * df['stress:2'] * df['l_r'] * df['n_r'] + 
                   2 * df['stress:5'] * df['m_r'] * df['n_r'])

# 4. 计算压力 p 的平均值
p_mean = df['p'].mean()

# 5. 计算动态地形 (dynamic_topography)
df['dynamic_topography'] = (df['stress_rr'] - p_mean) / (3600 * 9.81*10)

# 6. 保存结果为 CSV 文件（只保留 X, Y, Z 和 dynamic_topography）
df_output = df[['dynamic_topography', 'Points:0', 'Points:1', 'Points:2']]
df_output.to_csv('dt_0km.csv', index=False)