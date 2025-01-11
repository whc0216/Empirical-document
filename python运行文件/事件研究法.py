import pandas as pd
import statsmodels.formula.api as smf
import scipy.stats as stats
from statsmodels.iolib.summary2 import summary_col
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data_w=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\实证文件\\panel\\数据2.xlsx")
data_h=data_w[['From','last','last_log','past_experience_budget_ratio','past_experience_budget_delta','past_experience_delta','province','Fiscal_transparency_lagged','Fiscal_transparency','Fiscal_transparency_log','industry_structure','Regional_GDP_log','perGDP_log','Fiscal_autonomy','population_log','city','year','past_experience_ratio','male','age','education']]
data=pd.DataFrame(data_h)

def create_event_variables(group):
    group = group.sort_values('year')

    positive_mask = group['past_experience_delta'] > 0
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
        if value > 0:
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

for i in range(1, 10):
    formula = f'Fiscal_transparency_lagged ~ treat * treat{i} + male + age + education + industry_structure + Fiscal_autonomy + population_log + perGDP_log + C(year) + C(city)'
    reg = smf.ols(formula=formula, data=data)
    results.append(reg.fit())

for i in range(1, 9):
    formula = f'Fiscal_transparency_lagged ~ treat * pre_treat{i} + male + age + education + industry_structure + Fiscal_autonomy + population_log + perGDP_log + C(year) + C(city)'
    reg = smf.ols(formula=formula, data=data)
    results.append(reg.fit())

for i in range(1, 9):
    formula = f'Fiscal_transparency_lagged ~ treat * post_treat{i} + male + age + education + industry_structure + Fiscal_autonomy + population_log + perGDP_log + C(year) + C(city)'
    reg = smf.ols(formula=formula, data=data)
    results.append(reg.fit())

result = summary_col(results,
                    model_names=[f'Model{i+1}' for i in range(len(results))],
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

interaction_results = []

for i, result in enumerate(results[:9]):  
    interaction_term = f'treat:treat{i+1}'
    coef = result.params.get(interaction_term)
    std_err = result.bse.get(interaction_term)
    t_stat = result.tvalues.get(interaction_term)
    p_value = result.pvalues.get(interaction_term)
    
    interaction_results.append({
        'Interaction': f'treat × treat{i+1}',
        'Coefficient': coef,
        'Std.Err': std_err,
        't-stat': t_stat,
        'P-value': p_value
    })

for i, result in enumerate(results[9:17]):  
    interaction_term = f'treat:pre_treat{i+1}'
    coef = result.params.get(interaction_term)
    std_err = result.bse.get(interaction_term)
    t_stat = result.tvalues.get(interaction_term)
    p_value = result.pvalues.get(interaction_term)
    
    interaction_results.append({
        'Interaction': f'treat × pre_treat{i+1}',
        'Coefficient': coef,
        'Std.Err': std_err,
        't-stat': t_stat,
        'P-value': p_value
    })

for i, result in enumerate(results[17:]):  
    interaction_term = f'treat:post_treat{i+1}'
    coef = result.params.get(interaction_term)
    std_err = result.bse.get(interaction_term)
    t_stat = result.tvalues.get(interaction_term)
    p_value = result.pvalues.get(interaction_term)
    
    interaction_results.append({
        'Interaction': f'treat × post_treat{i+1}',
        'Coefficient': coef,
        'Std.Err': std_err,
        't-stat': t_stat,
        'P-value': p_value
    })

results_df = pd.DataFrame(interaction_results)
results_df['Stars'] = results_df['P-value'].apply(lambda x: 
    '***' if x < 0.01 else 
    '**' if x < 0.05 else 
    '*' if x < 0.1 else '')

pd.set_option('display.float_format', lambda x: '%.4f' % x)

print("\n============= 交互项系数估计结果 =============")
print("\n1. treat × treat 系列：")
print("----------------------------------------")
treat_results = results_df[results_df['Interaction'].str.contains('treat × treat')]
for _, row in treat_results.iterrows():
    print(f"{row['Interaction']}:")
    print(f"系数: {row['Coefficient']:.4f}{row['Stars']}")
    print(f"标准误: ({row['Std.Err']:.4f})")
    print(f"t值: [{row['t-stat']:.3f}]")
    print(f"p值: {row['P-value']:.4f}")
    print("----------------------------------------")

print("\n2. treat × pre_treat 系列：")
print("----------------------------------------")
pre_results = results_df[results_df['Interaction'].str.contains('pre_treat')]
for _, row in pre_results.iterrows():
    print(f"{row['Interaction']}:")
    print(f"系数: {row['Coefficient']:.4f}{row['Stars']}")
    print(f"标准误: ({row['Std.Err']:.4f})")
    print(f"t值: [{row['t-stat']:.3f}]")
    print(f"p值: {row['P-value']:.4f}")
    print("----------------------------------------")

print("\n3. treat × post_treat 系列：")
print("----------------------------------------")
post_results = results_df[results_df['Interaction'].str.contains('post_treat')]
for _, row in post_results.iterrows():
    print(f"{row['Interaction']}:")
    print(f"系数: {row['Coefficient']:.4f}{row['Stars']}")
    print(f"标准误: ({row['Std.Err']:.4f})")
    print(f"t值: [{row['t-stat']:.3f}]")
    print(f"p值: {row['P-value']:.4f}")
    print("----------------------------------------")

def prepare_plot_data(results_df):
    pre_treat = results_df[results_df['Interaction'].str.contains('pre_treat')].copy()
    treat = results_df[results_df['Interaction'].str.contains('treat × treat')].copy()
    post_treat = results_df[results_df['Interaction'].str.contains('post_treat')].copy()
    
    pre_treat['time'] = range(-len(pre_treat), 0)  
    treat['time'] = range(0, len(treat))  
    post_treat['time'] = range(len(treat), len(treat) + len(post_treat))  
    return pre_treat, treat, post_treat

plt.figure(figsize=(15, 8))
plt.grid(True, linestyle='--', alpha=0.7)

pre_treat, treat, post_treat = prepare_plot_data(results_df)

plt.errorbar(pre_treat['time'], pre_treat['Coefficient'], 
            yerr=pre_treat['Std.Err'], 
            fmt='o', color='blue', label='Pre-treat',
            capsize=5, capthick=1, elinewidth=1, markersize=8)

plt.errorbar(treat['time'], treat['Coefficient'], 
            yerr=treat['Std.Err'], 
            fmt='o', color='red', label='Treat',
            capsize=5, capthick=1, elinewidth=1, markersize=8)


plt.errorbar(post_treat['time'], post_treat['Coefficient'], 
            yerr=post_treat['Std.Err'], 
            fmt='o', color='green', label='Post-treat',
            capsize=5, capthick=1, elinewidth=1, markersize=8)

plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
plt.axvline(x=-0.5, color='black', linestyle='--', alpha=0.5)


for data in [pre_treat, treat, post_treat]:
    for i, row in data.iterrows():
        if row['Stars']:
            plt.text(row['time'], row['Coefficient'], row['Stars'], 
                    horizontalalignment='left', verticalalignment='bottom')


plt.title('Event Study', fontsize=14, pad=20)
plt.xlabel('Relative Period', fontsize=12)
plt.ylabel('Coefficient Estimates', fontsize=12)
plt.legend(loc='best')

all_times = list(pre_treat['time']) + list(treat['time']) + list(post_treat['time'])
x_labels = (
    [f"t-{i}" for i in range(len(pre_treat), 0, -1)] +  
    ['t'] * len(treat) +  
    [f"t+{i+1}" for i in range(len(post_treat))]  
)
plt.xticks(all_times, x_labels, rotation=45)


plt.grid(True, linestyle='--', alpha=0.3)

plt.tight_layout()

plt.show()