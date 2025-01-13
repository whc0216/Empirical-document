import pandas as pd
import statsmodels.formula.api as smf
import scipy.stats as stats
from statsmodels.iolib.summary2 import summary_col
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data_w=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\实证文件\\panel\\数据.xlsx")
data_h=data_w[['From','last','last_log','past_experience_budget_ratio','past_experience_budget_delta','past_experience_delta','province','Fiscal_transparency_lagged','Fiscal_transparency','Fiscal_transparency_log','industry_structure','Regional_GDP_log','perGDP_log','Fiscal_autonomy','population_log','city','year','past_experience_ratio','male','age','education']]
data=pd.DataFrame(data_h)
data['Fiscal_transparency_lagged_log'] = np.log10(data['Fiscal_transparency_lagged'])

def create_event_variables(group):
    group = group.sort_values('year')

    positive_mask = group['past_experience_delta'] < 0
    positive_years = group[positive_mask]['year'].tolist()

    treat_cols = [f'treat{i+1}' for i in range(9)]  
    pre_treat_cols = [f'pre_treat{i+1}' for i in range(8)]
    post_treat_cols = [f'post_treat{i+1}' for i in range(8)]
    
    for col in treat_cols + pre_treat_cols + post_treat_cols:
        group[col] = 0
    
    if not positive_years:  
        return group

    consecutive_positives = []
    current_sequence = []
    
    for year, value in zip(group['year'], group['past_experience_delta']):
        if value < 0:
            current_sequence.append(year)
        elif current_sequence:
            consecutive_positives.append(current_sequence)
            current_sequence = []
    if current_sequence:
        consecutive_positives.append(current_sequence)
    
    for i, sequence in enumerate(consecutive_positives):
        for j, year in enumerate(sequence):
            var_name = f'treat{j+1}'
            group.loc[group['year'] == year, var_name] = 1

    if positive_years:
        first_positive = positive_years[0]
        pre_years = group[group['year'] < first_positive]['year'].tolist()
        pre_years.sort(reverse=True) 
        
        for i, year in enumerate(pre_years):
            var_name = f'pre_treat{i+1}'
            group.loc[group['year'] == year, var_name] = 1

    if positive_years:
        last_positive = positive_years[-1]
        post_years = group[group['year'] > last_positive]['year'].tolist()
        
        for i, year in enumerate(post_years):
            var_name = f'post_treat{i+1}'
            group.loc[group['year'] == year, var_name] = 1
    
    return group

data = data.groupby('city').apply(create_event_variables).reset_index(drop=True)

print("\n变量创建完成。")
print("\n创建的treat变量：", [col for col in data.columns if col.startswith('treat')])
print("创建的pre_treat变量：", [col for col in data.columns if col.startswith('pre_treat')])
print("创建的post_treat变量：", [col for col in data.columns if col.startswith('post_treat')])

example_city = data['city'].iloc[0]
print(f"\n示例城市 {example_city} 的结果：")
example_data = data[data['city'] == example_city].sort_values('year')
display_cols = ['year', 'past_experience_delta'] + \
              [col for col in data.columns if col.startswith(('treat', 'pre_treat', 'post_treat'))]
print(example_data[display_cols])

print("\n基本统计：")
for col in [c for c in data.columns if c.startswith(('treat', 'pre_treat', 'post_treat'))]:
    count = data[col].sum()
    print(f"{col}: {count} 个观测值为1")
    
city_has_treat = data.groupby('city')['past_experience_delta'].apply(lambda x: (x > 0).any())
data['treat'] = data['city'].map(city_has_treat).astype(int)

results = []

formula = 'Fiscal_transparency_lagged_log ~  treat1 + treat2 + treat3 +treat4  +treat5+ + pre_treat2 + pre_treat3 + pre_treat4 +pre_treat5 + post_treat1 + post_treat2 + post_treat3 + post_treat4 + post_treat5 + male + age + education + industry_structure + Fiscal_autonomy + population_log + perGDP_log + C(year) + C(city)'
reg = smf.ols(formula=formula, data=data)
model1=reg.fit()
results.append(reg.fit())

formula = 'Fiscal_transparency_lagged_log ~  treat1 + treat2 + treat3 + pre_treat2 + pre_treat3 +treat4  +treat5+ + pre_treat4 + pre_treat5 +post_treat1 + post_treat2 + post_treat3 + post_treat4 + post_treat5 + C(year) + C(city)'
reg = smf.ols(formula=formula, data=data)
model2=reg.fit()
results.append(reg.fit())

result = summary_col(results,
                    model_names=['pre_treat1为基期','pre_treat1为基期','3','4','5','6','7','8'],
                    stars=True,
                    regressor_order=['Intercept',
                                   'treat',
                                   'treat1', 'treat2', 'treat3', 'treat4', 'treat5', 
                                   'treat6', 'treat7', 'treat8', 'treat9',
                                   'pre_treat1', 'pre_treat2', 'pre_treat3', 'pre_treat4',
                                   'pre_treat5', 'pre_treat6', 'pre_treat7', 'pre_treat8',
                                   'post_treat1', 'post_treat2', 'post_treat3', 'post_treat4',
                                   'post_treat5', 'post_treat6', 'post_treat7', 'post_treat8',
                                   'treat:treat1', 'treat:treat2', 'treat:treat3', 'treat:treat4',
                                   'treat:treat5', 'treat:treat6', 'treat:treat7', 'treat:treat8',
                                   'treat:treat9',
                                   'treat:pre_treat1', 'treat:pre_treat2', 'treat:pre_treat3',
                                   'treat:pre_treat4', 'treat:pre_treat5', 'treat:pre_treat6',
                                   'treat:pre_treat7', 'treat:pre_treat8',
                                   'treat:post_treat1', 'treat:post_treat2', 'treat:post_treat3',
                                   'treat:post_treat4', 'treat:post_treat5', 'treat:post_treat6',
                                   'treat:post_treat7', 'treat:post_treat8',
                                   'male', 'age', 'education', 'industry_structure',
                                   'Fiscal_autonomy', 'population_log', 'perGDP_log'],
                    drop_omitted=True,
                    info_dict={'Observations': lambda x: str(int(x.nobs))})

print(result)

hypotheses = 'pre_treat3=0,pre_treat4=0,pre_treat5=0'
f_test = model1.f_test(hypotheses)
print(f_test)

hypotheses = 'pre_treat3=0,pre_treat4=0,pre_treat5=0'
f_test = model2.f_test(hypotheses)
print(f_test)