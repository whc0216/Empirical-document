import pandas as pd
import numpy as np

data_w=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\数据.xlsx")
data=data_w[['strict_d', 'past_experience', 'province',
                     'Fiscal_transparency_log', 'industry_structrue',
                     'perGDP_log', 'Fiscal_autonomy', 'population_log', 'city',
                     'year',  'male', 'age', 'education']]
data.info
data_c=pd.DataFrame(data)

print(data.describe())