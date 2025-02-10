import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
from statsmodels.iolib.summary2 import summary_col

data = pd.read_excel(r"C:\Users\13298\Desktop\project\data\processed\panel.xlsx")

data['past_experience']=data['last']-data['now']

data['past_experience_dummy'] = (data['past_experience'] > 0).astype(int)

science_data=pd.read_excel(r"C:\Users\13298\Desktop\project\data\raw\数字化转型下的人大预算监督与政府支出效率数据.xlsx")

science_data['city'] = science_data['city'].apply(lambda x: x if x.endswith('市') else x + '市')

data = pd.merge(data, science_data[['city', 'year', 'WG_ZB','SFJG','pro_1to11','pro_1to11_num','Edu','Tec','Sec','Med','Investment','Pubservice']], on=['city', 'year'], how='left')

regression1 = smf.ols(formula='WG_ZB ~ past_experience_dummy + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=data)
result_reg1 = regression1.fit()

regression2 = smf.ols(formula='SFJG ~ past_experience_dummy + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=data)
result_reg2 = regression2.fit()

regression3 = smf.ols(formula='pro_1to11 ~ past_experience_dummy+ industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=data)
result_reg3 = regression3.fit()

regression4 = smf.ols(formula='pro_1to11_num ~ past_experience_dummy + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=data)
result_reg4 = regression4.fit()

regression5 = smf.ols(formula='Investment ~ past_experience_dummy + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=data)
result_reg5 = regression5.fit()

regression6 = smf.ols(formula='Edu ~ past_experience_dummy+ industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=data)
result_reg6 = regression6.fit()

regression7 = smf.ols(formula='Tec ~ past_experience_dummy + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=data)
result_reg7 = regression7.fit()

regression8 = smf.ols(formula='Sec ~ past_experience_dummy + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=data)
result_reg8 = regression8.fit()

regression9 = smf.ols(formula='Med ~ past_experience_dummy+ industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=data)
result_reg9 = regression9.fit()

regression10 = smf.ols(formula='Pubservice ~ past_experience_dummy+ industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=data)
result_reg10= regression10.fit()

result=summary_col([result_reg1,result_reg2,result_reg3,result_reg4,result_reg5,result_reg6,result_reg7,result_reg8,result_reg9,result_reg10],
                   model_names=['(1)','(2)','(3)','(4)','(5)','(6)','(7)','(8)','(9)','(10)'],
                   stars=True,
                   regressor_order=['Intercept','past_experience_dummy',
                                    'male', 'age', 'education', 'industry_structure','Fiscal_autonomy', 'population_log', 'perGDP_log'],
                    drop_omitted=True,
                    info_dict={'Observations': lambda x: str(int(x.nobs))})

print(result)