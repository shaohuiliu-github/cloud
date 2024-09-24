import pandas as pd
import numpy as np
import xarray as xr
from scipy.interpolate import griddata

# 读取 CSV 文件
df = pd.read_csv('latitude_longitude_dt0km.csv')

# 定义目标网格的分辨率
lat_grid = np.linspace(df['latitude'].min(), df['latitude'].max(), 1000)
lon_grid = np.linspace(df['longitude'].min(), df['longitude'].max(), 2000)

# 创建目标网格
lon_grid, lat_grid = np.meshgrid(lon_grid, lat_grid)

# 使用 griddata 插值，将原始数据插值到目标网格上
values_grid = griddata(
    (df['latitude'], df['longitude']), df['value'],
    (lat_grid, lon_grid), method='linear'
)

# 创建 xarray Dataset
ds = xr.Dataset(
    {
        "value": (["latitude", "longitude"], values_grid)
    },
    coords={
        "latitude": lat_grid[:, 0],
        "longitude": lon_grid[0, :]
    }
)

# 保存为 NetCDF 文件
ds.to_netcdf('latitude_longitude_dt0km.nc')
