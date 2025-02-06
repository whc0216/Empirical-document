import importlib.util
module_name = '01_data_clean'
module_path = "C:\\Users\\王浩晨\\Desktop\\project\\script\\01_data_clean.py"

spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

data = module.data

import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.iolib.summary2 import summary_col

data_describe = data[['Efficiency1', 'past_experience','From', 'year','industry_structure','Fiscal_autonomy','male', 'age', 'education', 'population_log', 'perGDP_log']]
descriptive_stats = data_describe.describe(include='all')
print(descriptive_stats)

numerical_vars = ['Efficiency1', 'past_experience', 'industry_structure','Fiscal_autonomy','population_log', 'perGDP_log']
data[numerical_vars].boxplot(figsize=(12, 8))
plt.title('箱线图')
plt.ylabel('值')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(False)
plt.show()