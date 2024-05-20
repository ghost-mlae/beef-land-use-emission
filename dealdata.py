
import pandas as pd
import os
"""
# 根文件路径和年份范围
base_path = 'D:/联培/data/BACI_HS92_V202401b/'
years = range(1995, 2017)  # 1995 到 2017 年

# 要过滤的 k 值列表
k_values = [20110, 20120, 20130, 20210, 20220, 20230]

for year in years:
    # 构建文件路径
    file_path = f'{base_path}/BACI_HS92_Y{year}_V202401b.csv'

    # 检查文件是否存在
    if os.path.exists(file_path):
        # 读取数据
        df = pd.read_csv(file_path)

        # 过滤数据
        filtered_df = df[df['k'].isin(k_values)]

        # 输出文件路径
        output_file_path = f'{base_path}/beef_data_{year}.csv'

        # 保存过滤后的数据到新的CSV文件
        filtered_df.to_csv(output_file_path, index=False)

        print(f'Filtered data for year {year} saved to {output_file_path}')
    else:
        print(f'File for year {year} not found: {file_path}')

"""

import pandas as pd
import os

# 根文件路径和年份范围
base_path = 'D:/联培/data/1995-2017-2022/'
years = range(2022, 2023)  # 1995 到 2017 年

for year in years:
    # 构建文件路径
    file_path = f'{base_path}/beef_data_{year}.csv'

    # 检查文件是否存在
    if os.path.exists(file_path):
        # 读取数据
        df = pd.read_csv(file_path)

        # 将 `q` 列转换为数值类型，不能转换的设置为 NaN
        df['q'] = pd.to_numeric(df['q'], errors='coerce')

        # 按 `i`, `j` 列进行分组，并对每组的 `v` 和 `q` 列进行求和
        grouped_df = df.groupby(['i', 'j'])[['v', 'q']].sum().reset_index()

        # 取每组 `i`, `j` 的第一个 `t` 值
        t_values = df.groupby(['i', 'j'])['t'].first().reset_index()

        # 将 `t` 列合并到分组结果中
        result_df = pd.merge(t_values, grouped_df, on=['i', 'j'])

        # 调整列的顺序为 `t, i, j, v, q`
        result_df = result_df[['t', 'i', 'j', 'v', 'q']]

        # 输出文件路径
        output_file_path = f'{base_path}/beef_{year}.csv'

        # 保存处理后的数据到新的CSV文件
        result_df.to_csv(output_file_path, index=False)

        print(f'Processed data for year {year} saved to {output_file_path}')
    else:
        print(f'File for year {year} not found: {file_path}')

""""

import pandas as pd

# 读取之前生成的分组数据文件
grouped_data_path = '/mnt/data/grouped_data.csv'
grouped_df = pd.read_csv(grouped_data_path)

# 读取新的国家代码文件
country_codes_path = '/mnt/data/country_codes_V202401b.csv'
country_codes_df = pd.read_csv(country_codes_path)

# 假设国家代码文件中有 'i' 和 'country_code' 列，我们需要将 'i' 和 'j' 替换为对应的国家代码
# 将 'i' 列替换为国家代码
grouped_df = grouped_df.merge(country_codes_df[['i', 'country_code']], on='i', how='left')
grouped_df = grouped_df.rename(columns={'country_code': 'i_code'}).drop(columns=['i']).rename(columns={'i_code': 'i'})

# 将 'j' 列替换为国家代码
grouped_df = grouped_df.merge(country_codes_df[['i', 'country_code']], left_on='j', right_on='i', how='left')
grouped_df = grouped_df.rename(columns={'country_code': 'j_code'}).drop(columns=['j', 'i']).rename(columns={'j_code': 'j'})

# 保存结果到一个新的 CSV 文件
output_path = '/mnt/data/replaced_grouped_data.csv'
grouped_df.to_csv(output_path, index=False)

output_path
"""