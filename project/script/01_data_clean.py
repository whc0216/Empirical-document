import pandas as pd

data_w = pd.read_excel("C:\\Users\\王浩晨\\Desktop\\project\\data\\processed\\数据支出.xlsx")
data_h = data_w[['Efficiency1', 'From', 'year', 'city', 'industry_structure','last','now','Fiscal_autonomy','male', 'age', 'education', 'population_log', 'perGDP_log']]
data = pd.DataFrame(data_h)

data['past_experience']=data['last']-data['now']