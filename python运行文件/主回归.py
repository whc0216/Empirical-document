import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.iolib.summary2 import summary_col

# 读取数据
data_w = pd.read_excel("C:\\Users\\王浩晨\\Desktop\\数据.xlsx")
data_h = data_w[['Fiscal_transparency_log', 'past_experience', 'From', 'province', 
                  'Fiscal_transparency', 'industry_structure', 'Regional_GDP_log', 
                  'perGDP_log', 'Fiscal_autonomy', 'population_log', 'city', 
                  'year', 'male', 'age', 'education']]
data_h = data_h.set_index(['city', 'province', 'year'], drop=False)
data_c = pd.DataFrame(data_h)

# 进行回归分析
regression = smf.ols(formula='Fiscal_transparency_log ~ past_experience + male + age + education + industry_structure + Fiscal_autonomy + population_log + perGDP_log + C(year) + C(city)', data=data_c)
result_reg = regression.fit()

# 输出结果
print(result_reg.summary())

# 生成拟合线
# 创建均匀分布的 x 值
x_values = np.linspace(data_c['past_experience'].min(), data_c['past_experience'].max(), 100)

# 根据回归系数计算预测值
intercept = result_reg.params['Intercept']
slope = result_reg.params['past_experience']

# 计算拟合线的 y 值
predicted_values = intercept + slope * x_values

# 绘制图形
plt.figure(figsize=(10, 6))
plt.plot(x_values, predicted_values, color='blue', label='Fitted Line')
plt.scatter(data_c['past_experience'], data_c['Fiscal_transparency_log'], alpha=0.5, label='Data Points', color='gray')
plt.title('Fitted Line for Fiscal Transparency Log vs. Past Experience')
plt.xlabel('Past Experience')
plt.ylabel('Fiscal Transparency Log')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()