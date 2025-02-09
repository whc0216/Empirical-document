import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col

file1 = r"c:\Users\13298\Desktop\project\data\raw\支出效率.xlsx"
file2 = r"C:\Users\13298\Desktop\project\data\raw\中国城市数据库4.0版.xlsx"
file3 = r"C:\Users\13298\Desktop\project\data\raw\官员数据.xlsx"
file4 = r"C:\Users\13298\Desktop\project\data\raw\市长个人信息.xlsx"

df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2, sheet_name="ARIMA填补(慎用)")
df3 = pd.read_excel(file3)
df4 = pd.read_excel(file4)

def add_city_suffix(df):
    df['city'] = df['city'].apply(lambda x: x if x.endswith('市') else x + '市')
    return df

df1 = add_city_suffix(df1)
df3 = add_city_suffix(df3)
df3 = pd.merge(df3, df1[['city', 'year', 'Efficiency1']], on=['city', 'year'], how='left')

df2 = add_city_suffix(df2)
merge_columns = ['city', 'year', '第二产业增加值(万元)', '地区生产总值(万元)', '地方财政一般预算内支出(万元)',
                 '地方财政一般预算内收入(万元)', '户籍人口(万人)', '人均地区生产总值(元)']
df3 = pd.merge(df3, df2[merge_columns], on=['city', 'year'], how='left')

df3['industry_structure'] = df3['第二产业增加值(万元)'] / df3['地区生产总值(万元)']
df3['Fiscal_autonomy'] = df3['地方财政一般预算内支出(万元)'] / df3['地方财政一般预算内收入(万元)']
df3['population_log'] = np.log10(df3['户籍人口(万人)'])
df3['perGDP_log'] = np.log10(df3['人均地区生产总值(元)'])

df3 = df3.drop_duplicates(subset=['city', 'year', 'leader'])

columns_to_describe1 = ['Efficiency1', 'industry_structure', 'Fiscal_autonomy', 'population_log', 'perGDP_log']
print(df3[columns_to_describe1].describe())

df4 = add_city_suffix(df4)
merge_columns_4 = ['city', 'leader', 'year', 'male', 'age', 'education', 'tenure']
df3 = pd.merge(df3, df4[merge_columns_4], on=['city', 'leader', 'year'], how='left')

columns_to_describe2 = ['male', 'age', 'education', 'tenure']
print(df3[columns_to_describe2].describe())

unmatched_data = df3[df3['male'].isna()]
print("没有匹配上的数据：")
print(unmatched_data[['city', 'leader', 'year']])

new_file_path = r"C:\Users\13298\Desktop\project\data\raw\直辖市缺失数据.xlsx"
new_df1 = pd.read_excel(new_file_path)

new_df1 = add_city_suffix(new_df1)

merge_columns_new = ['city', 'leader', 'year', 'male', 'age', 'education', 'tenure']
df3 = pd.merge(df3, new_df1[merge_columns_new], on=['city', 'leader', 'year'], how='left', suffixes=('', '_new'))

df3['male'] = df3['male'].fillna(df3['male_new'])
df3['age'] = df3['age'].fillna(df3['age_new'])
df3['education'] = df3['education'].fillna(df3['education_new'])
df3['tenure'] = df3['tenure'].fillna(df3['tenure_new'])

df3 = df3.drop(columns=['male_new', 'age_new', 'education_new', 'tenure_new'])

print(df3[['male', 'age', 'education', 'tenure']].describe(include='all'))

missing_education_data = df3[df3['education'].isna()]
print("education 列仍然缺失的数据：")
print(missing_education_data[['city', 'leader', 'year', 'education']])

missing_indexes = [803, 804]
df3.loc[missing_indexes, 'education'] = 1
# 再次打印 education 的描述性统计
print("更新后 education 列的描述性统计：")
print(df3['education'].describe(include='all'))

new_df2_path = r"c:\Users\13298\Desktop\project\data\raw\支出效率.xlsx"
new_df2 = pd.read_excel(new_df2_path)

df3 = pd.merge(df3, new_df2, left_on=['last_city', 'tenure_year'], right_on=['city', 'year'], how='left', suffixes=('', '_new2'))

df3.rename(columns={'Efficiency1_new2': 'last'}, inplace=True)

df3 = pd.merge(df3, new_df2[['city', 'year', 'Efficiency1']], left_on=['city', 'tenure_year'], right_on=['city', 'year'], how='left', suffixes=('', '_new3'))

df3.rename(columns={'Efficiency1_new3': 'now'}, inplace=True)

df3 = df3.drop_duplicates(subset=['city', 'year', 'leader'])

print(df3[['now', 'last']].describe())

missing_education_data = df3[df3['now'].isna()]
print("now 列仍然缺失的数据：")
print(missing_education_data[['city', 'leader', 'tenure_year', 'now']])

fill_value = 0.861423127

missing_indexes = [1888, 1889]

df3.loc[missing_indexes, 'now'] = fill_value

print(df3['now'].describe())

excel_file_path = r"C:\Users\13298\Desktop\project\data\processed\panel.xlsx"
df3.to_excel(excel_file_path, index=False)
print(f"数据已保存到 {excel_file_path}")