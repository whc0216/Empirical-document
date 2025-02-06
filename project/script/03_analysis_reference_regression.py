import importlib.util
module_name = '01_data_clean'
module_path = "C:\\Users\\王浩晨\\Desktop\\project\\script\\01_data_clean.py"

spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

data_c = module.data

import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.iolib.summary2 import summary_col

data_c['past_experience_dummy'] = (data_c['past_experience'] > 0).astype(int)
data_c['past_experience_dummy2'] = ((data_c['last'] > 1) & (data_c['now'] < 1)).astype(int)

now_threshold = data_c['now'].quantile(0.75)
last_threshold = data_c['last'].quantile(0.25)
data_c['past_experience_dummy3'] = ((data_c['now'] < now_threshold) & (data_c['last'] > last_threshold)).astype(int)
def filter_sequence(group):
    group = group.sort_values('year')

    first_one_index = group[group['past_experience_dummy'] == 1].index
    if len(first_one_index) == 0:
        return group

    zeros_before_first_one = group[group['past_experience_dummy'] == 0].index
    if len(zeros_before_first_one) == 0:
        return group

    group = group[group.index >= first_one_index[0]]

    for i in range(1, len(zeros_before_first_one) + 1):
        group[f'pre_treat{i}'] = 0

    for i in range(1, len(first_one_index) + 1):
        group[f'treat{i}'] = 0

    for i in range(len(zeros_before_first_one)):
        if i < len(first_one_index):
            group.loc[zeros_before_first_one[i], f'pre_treat{i + 1}'] = 1

    for i in range(len(first_one_index)):
        group.loc[first_one_index[i], f'treat{i + 1}'] = 1

    return group

filtered_grouped = data_c.groupby('city').apply(filter_sequence)

filtered_grouped.reset_index(drop=True, inplace=True)
filtered_grouped.fillna(0, inplace=True)

regression1 = smf.ols(formula='Efficiency1 ~ past_experience_dummy+industry_structure+Fiscal_autonomy+population_log+perGDP_log +male+age+education+ C(year) + C(city)', data=data_c)
result_reg1 = regression1.fit()

regression2 = smf.ols(formula='Efficiency1 ~ past_experience_dummy+industry_structure+Fiscal_autonomy+population_log+perGDP_log +male+age+education+ C(year) + C(city)', data=data_c)
result_reg2 = regression2.fit()

regression3 = smf.ols(formula='Efficiency1 ~ past_experience_dummy+industry_structure+Fiscal_autonomy+population_log+perGDP_log +male+age+education+ C(year) + C(city)', data=data_c)
result_reg3 = regression3.fit()

result=summary_col([result_reg1,result_reg2,result_reg3],
                   model_names=['(1)','(2)','(3)','(4)'],
                   stars=True,
                   regressor_order=['Intercept','past_experience_dummy','past_experience_dummy2','past_experience_dummy3',
                                    'male', 'age', 'education', 'industry_structure',
                                   'Fiscal_autonomy', 'population_log', 'perGDP_log'],
                    drop_omitted=True,
                    info_dict={'Observations': lambda x: str(int(x.nobs))})

print(result)