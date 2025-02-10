import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
from statsmodels.iolib.summary2 import summary_col

data = pd.read_excel(r"C:\Users\13298\Desktop\project\data\processed\panel.xlsx")

data['past_experience']=data['last']-data['now']

data['past_experience_dummy'] = (data['past_experience'] > 0).astype(int)

fiscal_data = pd.read_excel(r"C:\Users\13298\Desktop\project\data\raw\财政透明度.xlsx")

data = pd.merge(data, fiscal_data[['city', 'year', 'Fiscal_transparency']], on=['city', 'year'], how='left')

province_avg = data.groupby('province')['Fiscal_transparency'].mean().reset_index()
province_avg.rename(columns={'Fiscal_transparency': 'province_avg_transparency'}, inplace=True)

data = pd.merge(data, province_avg, on='province', how='left')

data['Fiscal_transparency_dummy'] = np.where(data['Fiscal_transparency'] > data['province_avg_transparency'], 1, 0)

group_1 = data[data['Fiscal_transparency_dummy'] == 1]
group_0 = data[data['Fiscal_transparency_dummy'] == 0]

regression1 = smf.ols(formula='Efficiency1 ~ past_experience_dummy + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=data)
result_reg1 = regression1.fit()

regression2 = smf.ols(formula='Efficiency1 ~ past_experience_dummy + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=group_0)
result_reg2 = regression2.fit()

regression3 = smf.ols(formula='Efficiency1 ~ past_experience_dummy + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=group_1)
result_reg3 = regression3.fit()

result=summary_col([result_reg1,result_reg2,result_reg3],
                   model_names=['(1)','(2)','(3)'],
                   stars=True,
                   regressor_order=['Intercept','past_experience_dummy','Fiscal_transparency_dummy',
                                    'male', 'age', 'education', 'industry_structure','Fiscal_autonomy', 'population_log', 'perGDP_log'],
                    drop_omitted=True,
                    info_dict={'Observations': lambda x: str(int(x.nobs))})

print(result)