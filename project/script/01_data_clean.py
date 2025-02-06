import pandas as pd

file1_path = r"C:\Users\王浩晨\Desktop\project\data\raw\数字化转型下的人大预算监督与政府支出效率数据.xlsx"
df1 = pd.read_excel(file1_path)

file2_path = r"C:\Users\王浩晨\Desktop\project\data\processed\数据支出.xlsx"
df2 = pd.read_excel(file2_path)

def add_city_indicator(city):
    if not str(city).endswith("市"):
        return str(city) + "市"
    return city

df1['city'] = df1['city'].apply(add_city_indicator)
df2['city'] = df2['city'].apply(add_city_indicator)

merged_df = pd.merge(df2, df1[['city', 'year', 'Efficiency1']], on=['city', 'year'], how='left')

merged_df['past_experience']=merged_df['last']-merged_df['now']

merged_df['past_experience_dummy1'] = (merged_df['past_experience'] > 0).astype(int)

merged_df['past_experience_dummy2'] = ((merged_df['last'] > 1) & (merged_df['now'] < 1)).astype(int)

now_threshold = merged_df['now'].quantile(0.75)
last_threshold = merged_df['last'].quantile(0.25)
merged_df['past_experience_dummy3'] = ((merged_df['now'] < now_threshold) & (merged_df['last'] > last_threshold)).astype(int)

data=merged_df