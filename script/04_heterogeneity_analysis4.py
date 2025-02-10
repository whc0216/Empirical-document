import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
from statsmodels.iolib.summary2 import summary_col

#审计体制改革
data = pd.read_excel(r"C:\Users\13298\Desktop\project\data\processed\panel.xlsx")

data['past_experience']=data['last']-data['now']

data['past_experience_dummy'] = (data['past_experience'] > 0).astype(int)

science_data=pd.read_excel(r"C:\Users\13298\Desktop\project\data\raw\数字化转型下的人大预算监督与政府支出效率数据.xlsx")

science_data['city'] = science_data['city'].apply(lambda x: x if x.endswith('市') else x + '市')

data = pd.merge(data, science_data[['city', 'year', 'Audit_After_2015']], on=['city', 'year'], how='left')

group_1 = data[data['Audit_After_2015'] == 1]
group_0 = data[data['Audit_After_2015'] == 0]

regression1 = smf.ols(formula='Efficiency1 ~ past_experience_dummy + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=data)
result_reg1 = regression1.fit()

regression2 = smf.ols(formula='Efficiency1 ~ past_experience_dummy + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=group_0)
result_reg2 = regression2.fit()

regression3 = smf.ols(formula='Efficiency1 ~ past_experience_dummy+ industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=group_1)
result_reg3 = regression3.fit()

result=summary_col([result_reg1,result_reg2,result_reg3],
                   model_names=['(1)','(2)','(3)'],
                   stars=True,
                   regressor_order=['Intercept','past_experience_dummy',
                                    'male', 'age', 'education', 'industry_structure','Fiscal_autonomy', 'population_log', 'perGDP_log'],
                    drop_omitted=True,
                    info_dict={'Observations': lambda x: str(int(x.nobs))})

print(result)