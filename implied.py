

#中国隐含碳排放


import pandas as pd

# 加载数据


import pandas as pd


# 加载数据
beef_file_path = 'D:/联培/data/1995-2017-2022/beef_2022.csv'
land_use_file_path = 'D:/联培/data/1995-2017-2022/land use emission1995-2017updated.csv'

beef_data = pd.read_csv(beef_file_path, encoding='latin1')
land_use_data = pd.read_csv(land_use_file_path, encoding='latin1')

# 检查列名
print(land_use_data.columns)

# 提取2017年的土地利用碳排放数据
land_use_2017 = land_use_data[['Id', 'ï»¿Area', 'ISO', '2017']].rename(columns={'Id': 'id', 'ï»¿Area': 'Country', 'ISO': 'ISO3', '2017': 'land use emission'})

# 定义计算隐含碳排放的函数
def calculate_implied_carbon(importer, exporter):
    # 过滤出特定进口国和出口国的数据
    country_data = beef_data[(beef_data['i'] == exporter) & (beef_data['j'] == importer) & (beef_data['t'] ==2022)]

    # 获取特定进口国从出口国进口的数量
    import_quantity = country_data['q'].sum()

    # 获取出口国的总出口量
    total_export = beef_data[(beef_data['i'] == exporter) & (beef_data['t'] ==2022)]['q'].sum()

    # 检查是否存在土地利用碳排放数据
    if exporter not in land_use_2017['id'].values:
        print(f"Exporter {exporter} not found in land use data for 2017")
        return None, None, None, None
        # 获取出口国的土地利用碳排放
    land_use_emission_row = land_use_2017[land_use_2017['id'] == exporter]
    if land_use_emission_row.empty:
        print(f"Land use emission data for exporter {exporter} in 2017 not found")
        return None, None, None, None

    land_use_emission = land_use_emission_row['land use emission'].values[0]

    # 计算隐含碳排放
    implied_emission = (import_quantity / total_export) * float(land_use_emission)

    return import_quantity, total_export, land_use_emission, implied_emission

# 获取所有出口到中国的国家列表
exporting_countries = beef_data[(beef_data['j'] == 156) & (beef_data['t'] ==2022)]['i'].unique()

# 计算所有国家的隐含碳排放
all_results = []

for country in exporting_countries:
    import_quantity, total_export, land_use_emission, implied_emission = calculate_implied_carbon(156, country)
    if import_quantity is None:
        continue
    all_results.append((country, import_quantity, total_export, land_use_emission, implied_emission))



# 将结果转换为DataFrame
all_results_df = pd.DataFrame(all_results,
                              columns=['Country Code', 'Imported Quantity (metric tons)', 'Total Export (metric tons)',
                                       'Land Use Emission', 'Implied Carbon Emission'])

# 根据land_use_2017数据，添加国家名称和简称
all_results_df = all_results_df.merge(land_use_2017[['id', 'Country', 'ISO3']], left_on='Country Code', right_on='id', how='left')
all_results_df = all_results_df.drop(columns=['id'])

# 重新排列列顺序
all_results_df = all_results_df[['Country Code', 'Country', 'ISO3', 'Imported Quantity (metric tons)', 'Total Export (metric tons)', 'Land Use Emission', 'Implied Carbon Emission']]


# 保存结果为CSV文件
output_file_path = 'D:/联培/data/1995-2017-2022/china_beef_imports_carbon_emission_2022-test.csv'
all_results_df.to_csv(output_file_path, index=False)

output_file_path
"""
####################################################

import pandas as pd

# 定义计算隐含碳排放的函数
def calculate_implied_carbon(beef_data, land_use_data, importer, exporter, year):
    # 过滤出特定年份、进口国和出口国的数据
    country_data = beef_data[(beef_data['i'] == exporter) & (beef_data['j'] == importer) & (beef_data['t'] == year)]

    # 获取特定进口国从出口国进口的数量
    import_quantity = country_data['q'].sum()

    # 获取出口国的总出口量
    total_export = beef_data[(beef_data['i'] == exporter) & (beef_data['t'] == year)]['q'].sum()

    # 使用2017年的土地利用碳排放数据
    if year > 2017:
        year = 2017

    # 检查是否能在 land_use_data 中找到相应的 exporter
    if exporter not in land_use_data['Id'].values:
        print(f"Exporter {exporter} not found in land use data for year {year}")
        return None, None, None, None

    # 获取出口国的土地利用碳排放
    land_use_emission_row = land_use_data[land_use_data['Id'] == exporter]
    if land_use_emission_row.empty or str(year) not in land_use_emission_row:
        print(f"Land use emission data for exporter {exporter} in year {year} not found")
        return None, None, None, None

    land_use_emission = land_use_emission_row[str(year)].values[0]

    # 计算隐含碳排放
    implied_emission = (import_quantity / total_export) * float(land_use_emission)

    return import_quantity, total_export, land_use_emission, implied_emission

# 加载土地利用碳排放数据
land_use_file_path = 'D:/联培/data/1995-2017-2022/land use emission1995-2017updated.csv'  
land_use_data = pd.read_csv(land_use_file_path, encoding='latin1')

# 提取国家名称和简称信息
country_info = land_use_data[['Id', 'ï»¿Area', 'ISO']].rename(columns={'Id': 'id', 'ï»¿Area': 'Country', 'ISO': 'ISO3'})


# 计算每一年的隐含碳排放并保存结果
for year in range(1995, 2023):  # 修改为 1995 到 2022 年的范围
    beef_file_path = f'D:/联培/data/1995-2017-2022/beef_{year}.csv'  
    beef_data = pd.read_csv(beef_file_path, encoding='latin1')

    # 获取所有出口到中国的国家列表
    exporting_countries = beef_data[beef_data['j'] == 156]['i'].unique()

    all_results = []

    for country in exporting_countries:
        import_quantity, total_export, land_use_emission, implied_emission = calculate_implied_carbon(beef_data, land_use_data, 156, country, year)
        if import_quantity is None:
            continue
        country_name = country_info[country_info['id'] == country]['Country'].values[0]
        iso3_code = country_info[country_info['id'] == country]['ISO3'].values[0]
        all_results.append((country, country_name, iso3_code, import_quantity, total_export, land_use_emission, implied_emission))

    # 将结果转换为DataFrame
    all_results_df = pd.DataFrame(all_results,
                                  columns=['Country Code', 'Country', 'ISO3', 'Imported Quantity (metric tons)', 'Total Export (metric tons)',
                                           'Land Use Emission', 'Implied Carbon Emission'])

    # 保存结果为CSV文件
    output_file_path = f'D:/联培/data/1995-2017-2022/china_beef_imports_carbon_emission_{year}.csv'
    all_results_df.to_csv(output_file_path, index=False)

    print(f"Results for {year} saved to {output_file_path}")

"""
