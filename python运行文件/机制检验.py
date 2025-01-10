import pandas as pd
import statsmodels.formula.api as smf
import scipy.stats as stats
from statsmodels.iolib.summary2 import summary_col

data_w=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\数据2.xlsx",'Sheet1')
data_h=data_w[['word_time','word_time_dummy','word_time_dummy_lagged','word_time_general_log','Fiscal_transparency_log','past_experience','From','province','Fiscal_transparency','industry_structure','Regional_GDP_log','perGDP_log','Fiscal_autonomy','population_log','city','year','male','age','education']]
data_h=data_h.set_index(['city','province','year'],drop=False)
data_c=pd.DataFrame(data_h)

regression7=smf.ols(formula='Fiscal_transparency_log~past_experience+male+age+education+industry_structure+Fiscal_autonomy+population_log+perGDP_log+C(year)+C(city)',data=data_c)
result7=regression7.fit()
result7.summary()

regression8=smf.ols(formula='Fiscal_transparency_log~past_experience+word_time+male+age+education+industry_structure+Fiscal_autonomy+population_log+perGDP_log+C(year)+C(city)',data=data_c)
result8=regression8.fit()
result8.summary()

regression1=smf.ols(formula='word_time~past_experience+male+age+education+industry_structure+Fiscal_autonomy+population_log+perGDP_log+C(year)+C(city)',data=data_c)
result1=regression1.fit()
result1.summary()

result=summary_col([result7,result8,result1],
            model_names=['model1','model2','model3','model4','model5','model6','model7','model8','model9'],                                       
            stars=True,regressor_order=['Intercept','past_experience','word_time','word_time_lagged','word_time_dummy','word_time_dummy_lagged','word_time_general_log','Fiscal_transparency_log','male','age','education','industry_structure','Fiscal_autonomy','population_log','perGDP_log'],
            drop_omitted=True,info_dict={'':lambda x:'',
                                         '':lambda x:'',
                                         'Observations':lambda x:str(int(x.nobs)),
                                         })

print(result)