import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.iolib.summary2 import summary_col

# 读取数据

data_w = pd.read_excel("C:\\Users\\王浩晨\\Desktop\\数据_支出.xlsx")
data_h = data_w[['Efficiency1', 'past_experience', 'From', 'year', 'city']]
data_c = pd.DataFrame(data_h)

# 创建哑变量，表示past_experience_delta是否大于0
data_c['past_experience_dummy'] = (data_c['past_experience'] > 0).astype(int)


# 打印处理后的数据
print("处理后的数据:")
print(data_c)

# 按city进行分组，并按year排序
def filter_sequence(group):
    # 按year排序
    group = group.sort_values('year')
    
    # 找到第一次出现1的索引
    first_one_index = group[group['past_experience_dummy'] == 1].index
    if len(first_one_index) == 0:
        return group
    
    # 找到第一次出现1之前的0的索引
    zeros_before_first_one = group[group['past_experience_dummy'] == 0].index
    if len(zeros_before_first_one) == 0:
        return group
    
    # 只保留从第一次出现1开始的所有数据
    group = group[group.index >= first_one_index[0]]
    
    # 初始化pre_treat变量
    for i in range(1, len(zeros_before_first_one) + 1):
        group[f'pre_treat{i}'] = 0
    
    # 初始化treat变量
    for i in range(1, len(first_one_index) + 1):
        group[f'treat{i}'] = 0
    
    # 创建pre_treat变量
    for i in range(len(zeros_before_first_one)):
        if i < len(first_one_index):
            group.loc[zeros_before_first_one[i], f'pre_treat{i+1}'] = 1
    
    # 创建treat变量
    for i in range(len(first_one_index)):
        group.loc[first_one_index[i], f'treat{i+1}'] = 1
    
    return group

# 按city进行分组，并应用filter_sequence函数
filtered_grouped = data_c.groupby('city').apply(filter_sequence)

# 重置索引并填充NaN为0
filtered_grouped.reset_index(drop=True, inplace=True)
filtered_grouped.fillna(0, inplace=True)

print(filtered_grouped)

# 打印每个treat和pre_treat变量的数量与描述性统计
def print_variable_stats(group):
    # 找到所有的treat和pre_treat变量
    treat_vars = [col for col in group.columns if col.startswith('treat')]
    pre_treat_vars = [col for col in group.columns if col.startswith('pre_treat')]
    
    # 打印每个treat变量的数量与描述性统计
    for treat_var in treat_vars:
        treat_count = group[treat_var].sum()
        treat_stats = group[treat_var].describe()
        print(f"\n{treat_var} 变量的数量: {treat_count}")
        print(f"{treat_var} 变量的描述性统计:\n{treat_stats}")
    
    # 打印每个pre_treat变量的数量与描述性统计
    for pre_treat_var in pre_treat_vars:
        pre_treat_count = group[pre_treat_var].sum()
        pre_treat_stats = group[pre_treat_var].describe()
        print(f"\n{pre_treat_var} 变量的数量: {pre_treat_count}")
        print(f"{pre_treat_var} 变量的描述性统计:\n{pre_treat_stats}")


# 进行回归分析
# 构建回归公式，包含所有创建的pre_treat和treat变量
# 你可以根据实际情况调整公式
treat_vars = [col for col in filtered_grouped.columns if col.startswith('treat')]
pre_treat_vars = [col for col in filtered_grouped.columns if col.startswith('pre_treat')]

formula = 'Efficiency1 ~treat1+ treat2 +treat3 + treat4 + treat5 +treat6  +pre_treat2 + pre_treat3 + pre_treat4  +pre_treat5 +pre_treat6  + C(year) + C(city)'

regression = smf.ols(formula=formula, data=filtered_grouped)
result_reg = regression.fit()

# 创建回归结果的摘要
result = summary_col([result_reg],
                   stars=True,
                   regressor_order=['Intercept'] + pre_treat_vars + treat_vars + \
                                   ['Efficiency1', 'male', 'age', 'education', 'industry_structure',
                                   'Fiscal_autonomy', 'population_log', 'perGDP_log', 'C(year)', 'C(city)'],
                    drop_omitted=True,
                    info_dict={'Observations': lambda x: str(int(x.nobs))})

# 打印回归结果摘要
print(result)