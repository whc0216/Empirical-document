import pandas as pd
import statsmodels.formula.api as smf
import scipy.stats as stats
from statsmodels.iolib.summary2 import summary_col

data_w = pd.read_excel("C:\\Users\\王浩晨\\Desktop\\实证文件\\panel\\数据2.xlsx")
data_h = data_w.loc[:, ['Fiscal_transparency_log', 'Fiscal_transparency_lagged',
                        'province',
                        'industry_structure', 'Regional_GDP_log', 'perGDP_log', 'Fiscal_autonomy',
                        'population_log', 'city', 'year', 'past_experience_delta', 'male', 'age','strict_wide_d_lagged', 'education']].copy()

data_h['year_dummy'] = (data_h['year'] >= 2018).astype(int)

data_h['treat_dummy1'] = (data_h['past_experience_delta'] > 0).astype(int)

data_h['treat_year_interaction'] = data_h['treat_dummy1'] * data_h['year_dummy']

data_h = data_h[data_h['past_experience_delta'] != 0]

regression = smf.ols(formula='''Fiscal_transparency_lagged ~ 
                              treat_dummy1 + year_dummy + treat_year_interaction +
                              male + age + education + industry_structure + 
                              Fiscal_autonomy + population_log + perGDP_log + 
                              C(year) + C(city)''', 
                    data=data_h)
result_reg = regression.fit()

result = summary_col([result_reg],
                    model_names=['Model 1'],
                    stars=True,
                    regressor_order=['const',
                                   'treat_dummy1',
                                   'year_dummy',
                                   'treat_year_interaction',
                                   'male',
                                   'age',
                                   'education',
                                   'industry_structure',
                                   'Fiscal_autonomy',
                                   'population_log',
                                   'perGDP_log'],
                    drop_omitted=True,
                    info_dict={'Observations': lambda x: f"{int(x.nobs)}"})

# 打印结果
print(result)