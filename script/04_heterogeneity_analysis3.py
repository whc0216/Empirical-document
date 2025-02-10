import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
from statsmodels.iolib.summary2 import summary_col

data = pd.read_excel(r"C:\Users\13298\Desktop\project\data\processed\panel.xlsx")

data['past_experience']=data['last']-data['now']

data['past_experience_dummy'] = (data['past_experience'] > 0).astype(int)

after = data[data['year'] >= 2016]
before = data[data['year'] < 2016]

regression1 = smf.ols(formula='Efficiency1 ~ past_experience_dummy + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=data)
result_reg1 = regression1.fit()

regression2 = smf.ols(formula='Efficiency1 ~ past_experience_dummy + industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=after)
result_reg2 = regression2.fit()

regression3 = smf.ols(formula='Efficiency1 ~ past_experience_dummy+ industry_structure + Fiscal_autonomy + population_log + perGDP_log + male + age + education + C(year) + C(city)',data=before)
result_reg3 = regression3.fit()

result=summary_col([result_reg1,result_reg2,result_reg3],
                   model_names=['(1)','(2)','(3)'],
                   stars=True,
                   regressor_order=['Intercept','past_experience_dummy',
                                    'male', 'age', 'education', 'industry_structure','Fiscal_autonomy', 'population_log', 'perGDP_log'],
                    drop_omitted=True,
                    info_dict={'Observations': lambda x: str(int(x.nobs))})

print(result)