import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
from statsmodels.iolib.summary2 import summary_col

data=pd.read_excel(r"C:\Users\13298\Desktop\project\data\processed\panel.xlsx")

data['past_experience']=data['last']-data['now']

data['past_experience_dummy1'] = (data['past_experience'] > 0).astype(int)
data['past_experience_dummy2'] = ((data['last'] > 1) & (data['now'] < 1)).astype(int)

quantiles = [0.50, 0.60, 0.70, 0.75, 0.80, 0.90]

def create_dummies(group):
    for q in quantiles:
        now_threshold = group['now'].quantile(q)
        last_threshold = group['last'].quantile(1 - q)  
        col_name = f'past_experience_dummy_{int(q * 100)}'
        group[col_name] = ((group['now'] < now_threshold) & (group['last'] > last_threshold)).astype(int)
    return group
data = data.groupby('year').apply(create_dummies)

base_formula = 'Efficiency1 ~ {} + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)'

results = []

model_names = []

regression1 = smf.ols(formula=base_formula.format('past_experience_dummy1'), data=data)
result_reg1 = regression1.fit()
results.append(result_reg1)
model_names.append('(1)')
regression2 = smf.ols(formula=base_formula.format('past_experience_dummy2'), data=data)
result_reg2 = regression2.fit()
results.append(result_reg2)
model_names.append('(2)')

for q in quantiles:
    dummy_col = f'past_experience_dummy_{int(q * 100)}'
    regression = smf.ols(formula=base_formula.format(dummy_col), data=data)
    result_reg = regression.fit()
    results.append(result_reg)
    model_names.append(f'({len(model_names) + 1})')

result = summary_col(results,
                     model_names=model_names,
                     stars=True,
                     regressor_order=['Intercept'] + [f'past_experience_dummy_{int(q * 100)}' for q in quantiles] + 
                                     ['past_experience_dummy1', 'past_experience_dummy2', 
                                      'male', 'age', 'education', 'industry_structure',
                                      'Fiscal_autonomy', 'population_log', 'perGDP_log'],
                     drop_omitted=True,
                     info_dict={'Observations': lambda x: str(int(x.nobs))})
print(result)

data['past_experience_from'] = data.apply(lambda row: row['last'] - row['now'] if row['From'] == 2 else 0, axis=1)

data['past_experience_from_dummy'] = (data['past_experience_from'] > 0).astype(int)

regression = smf.ols(formula='Efficiency1 ~ past_experience_from_dummy+industry_structure+Fiscal_autonomy+population_log+perGDP_log +male+age+education+ C(year) + C(city)', data=data)
result_reg = regression.fit()

result=summary_col([result_reg],
                   model_names=['(1)'],
                   stars=True,
                   regressor_order=['Intercept','past_experience_from_dummy',
                                    'male', 'age', 'education', 'industry_structure',
                                   'Fiscal_autonomy', 'population_log', 'perGDP_log'],
                    drop_omitted=True,
                    info_dict={'Observations': lambda x: str(int(x.nobs))})

print(result)