import pandas as pd
import os

# 定义路径
data_folder_path = 'D:/联培/data/1995-2017-2022/'  

# 初始化一个空的DataFrame来存储所有年份的数据
combined_df = pd.DataFrame()

# 遍历1995年至2022年的数据文件
for year in range(1995, 2023):
    file_name = f'china_beef_imports_carbon_emission_{year}.csv'
    file_path = os.path.join(data_folder_path, file_name)

    if os.path.exists(file_path):
        # 加载数据
        year_data = pd.read_csv(file_path)

        # 提取所需的列并重命名隐含碳排放列
        year_data = year_data[['Country Code', 'Country', 'ISO3', 'Implied Carbon Emission']].rename(
            columns={'Implied Carbon Emission': f'Implied Carbon Emission {year}'})

        # 合并数据
        if combined_df.empty:
            combined_df = year_data
        else:
            combined_df = pd.merge(combined_df, year_data, on=['Country Code', 'Country', 'ISO3'], how='outer')

# 填充缺失值为0
combined_df = combined_df.fillna(0)

# 保存结果为CSV文件
output_file_path = os.path.join(data_folder_path, 'combined_beef_imports_carbon_emission_1995_2022.csv')
combined_df.to_csv(output_file_path, index=False)

print(f"Combined data saved to {output_file_path}")
