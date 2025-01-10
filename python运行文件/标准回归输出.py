import statsmodels.formula.api as smf
import wooldridge as woo
import pandas as pd
import statsmodels.api as sm
import linearmodels as plm
import scipy.stats as stats
from statsmodels.iolib.summary2 import summary_col

data_w=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\市长数据_lagged.xlsx",'Sheet1')
data_h=data_w[['Fiscal_transparency_log','Fiscal_transparency','Fiscal_transparency_lagged_log','Fiscal_transparency_lagged','industry_structrue','Regional_GDP_log','past_experience_age_before','past_experience_age_after','perGDP_log','fiscal_expend_education_science','past_experience_before','past_experience_after','Fiscal_autonomy','population_log','city','year','past_experience','interaction_y','interaction_z','past_experience_dummy','tenure2','tenure3','tenure4','tenure5','tenure6','tenure7','tenure8','tenure9','tenure12','male','age','education']]
data_h=data_h.set_index(['city','year'],drop=False)

data_1=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\市长数据_lagged.xlsx",'2015')
data_2015=data_1[['Fiscal_transparency_log','Fiscal_transparency','Fiscal_transparency_lagged_log','industry_structrue','Regional_GDP_log','past_experience_age_before','past_experience_age_after','perGDP_log','fiscal_expend_education_science','past_experience_before','past_experience_after','Fiscal_autonomy','population_log','city','year','past_experience','interaction_y','interaction_z','past_experience_dummy','tenure2','tenure3','tenure4','tenure5','tenure6','tenure7','tenure8','tenure9','tenure12','male','age','education']]
data_2015=data_2015.set_index(['city','year'],drop=False)

data_2=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\市长数据_lagged.xlsx",'2016')
data_2016=data_2[['Fiscal_transparency_log','Fiscal_transparency','Fiscal_transparency_lagged_log','industry_structrue','Regional_GDP_log','past_experience_age_before','past_experience_age_after','perGDP_log','fiscal_expend_education_science','past_experience_before','past_experience_after','Fiscal_autonomy','population_log','city','year','past_experience','interaction_y','interaction_z','past_experience_dummy','tenure2','tenure3','tenure4','tenure5','tenure6','tenure7','tenure8','tenure9','tenure12','male','age','education']]
data_2016=data_2016.set_index(['city','year'],drop=False)

data_3=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\市长数据_lagged.xlsx",'2017')
data_2017=data_3[['Fiscal_transparency_log','Fiscal_transparency','Fiscal_transparency_lagged_log','industry_structrue','Regional_GDP_log','past_experience_age_before','past_experience_age_after','perGDP_log','fiscal_expend_education_science','past_experience_before','past_experience_after','Fiscal_autonomy','population_log','city','year','past_experience','interaction_y','interaction_z','past_experience_dummy','tenure2','tenure3','tenure4','tenure5','tenure6','tenure7','tenure8','tenure9','tenure12','male','age','education']]
data_2017=data_2017.set_index(['city','year'],drop=False)

data_4=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\市长数据_lagged.xlsx",'2018')
data_2018=data_4[['Fiscal_transparency_log','Fiscal_transparency','Fiscal_transparency_lagged_log','industry_structrue','Regional_GDP_log','past_experience_age_before','past_experience_age_after','perGDP_log','fiscal_expend_education_science','past_experience_before','past_experience_after','Fiscal_autonomy','population_log','city','year','past_experience','interaction_y','interaction_z','past_experience_dummy','tenure2','tenure3','tenure4','tenure5','tenure6','tenure7','tenure8','tenure9','tenure12','male','age','education']]
data_2018=data_2018.set_index(['city','year'],drop=False)

data_5=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\市长数据_lagged.xlsx",'2019')
data_2019=data_5[['Fiscal_transparency_log','Fiscal_transparency','Fiscal_transparency_lagged_log','industry_structrue','Regional_GDP_log','past_experience_age_before','past_experience_age_after','perGDP_log','fiscal_expend_education_science','past_experience_before','past_experience_after','Fiscal_autonomy','population_log','city','year','past_experience','interaction_y','interaction_z','past_experience_dummy','tenure2','tenure3','tenure4','tenure5','tenure6','tenure7','tenure8','tenure9','tenure12','male','age','education']]
data_2019=data_2019.set_index(['city','year'],drop=False)

data_6=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\市长数据_lagged.xlsx",'2020')
data_2020=data_6[['Fiscal_transparency_log','Fiscal_transparency','Fiscal_transparency_lagged_log','industry_structrue','Regional_GDP_log','past_experience_age_before','past_experience_age_after','perGDP_log','fiscal_expend_education_science','past_experience_before','past_experience_after','Fiscal_autonomy','population_log','city','year','past_experience','interaction_y','interaction_z','past_experience_dummy','tenure2','tenure3','tenure4','tenure5','tenure6','tenure7','tenure8','tenure9','tenure12','male','age','education']]
data_2020=data_2020.set_index(['city','year'],drop=False)

data_6=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\市长数据_lagged.xlsx",'2021')
data_2021=data_6[['Fiscal_transparency_log','Fiscal_transparency','Fiscal_transparency_lagged_log','industry_structrue','Regional_GDP_log','past_experience_age_before','past_experience_age_after','perGDP_log','fiscal_expend_education_science','past_experience_before','past_experience_after','Fiscal_autonomy','population_log','city','year','past_experience','interaction_y','interaction_z','past_experience_dummy','tenure2','tenure3','tenure4','tenure5','tenure6','tenure7','tenure8','tenure9','tenure12','male','age','education']]
data_2021=data_2021.set_index(['city','year'],drop=False)

data_6=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\市长数据_lagged.xlsx",'2022')
data_2022=data_6[['Fiscal_transparency_log','Fiscal_transparency','Fiscal_transparency_lagged_log','industry_structrue','Regional_GDP_log','past_experience_age_before','past_experience_age_after','perGDP_log','fiscal_expend_education_science','past_experience_before','past_experience_after','Fiscal_autonomy','population_log','city','year','past_experience','interaction_y','interaction_z','past_experience_dummy','tenure2','tenure3','tenure4','tenure5','tenure6','tenure7','tenure8','tenure9','tenure12','male','age','education']]
data_2022=data_2022.set_index(['city','year'],drop=False)

reg_fe=smf.ols(formula='Fiscal_transparency_log~Fiscal_transparency_lagged_log+past_experience_dummy+male+age+education+industry_structrue+fiscal_expend_education_science+Fiscal_autonomy+population_log+perGDP_log+C(year)+C(city)',data=data_h)
result_HC0=reg_fe.fit()
result_HC0.summary()

reg_fe=smf.ols(formula='Fiscal_transparency_log~Fiscal_transparency_lagged_log+past_experience_dummy+male+age+education+industry_structrue+fiscal_expend_education_science+Fiscal_autonomy+population_log+perGDP_log+C(year)+C(city)',data=data_2015)
result_2015=reg_fe.fit()
result_2015.summary()

reg_fe=smf.ols(formula='Fiscal_transparency_log~Fiscal_transparency_lagged_log+past_experience_dummy+male+age+education+industry_structrue+fiscal_expend_education_science+Fiscal_autonomy+population_log+perGDP_log+C(year)+C(city)',data=data_2016)
result_2016=reg_fe.fit()
result_2016.summary()

reg_fe=smf.ols(formula='Fiscal_transparency_log~Fiscal_transparency_lagged_log+past_experience_dummy+male+age+education+industry_structrue+fiscal_expend_education_science+Fiscal_autonomy+population_log+perGDP_log+C(year)+C(city)',data=data_2017)
result_2017=reg_fe.fit()
result_2017.summary()

reg_fe=smf.ols(formula='Fiscal_transparency_log~Fiscal_transparency_lagged_log+past_experience_dummy+male+age+education+industry_structrue+fiscal_expend_education_science+Fiscal_autonomy+population_log+perGDP_log+C(year)+C(city)',data=data_2018)
result_2018=reg_fe.fit()
result_2018.summary()

reg_fe=smf.ols(formula='Fiscal_transparency_log~Fiscal_transparency_lagged_log+past_experience_dummy+male+age+education+industry_structrue+fiscal_expend_education_science+Fiscal_autonomy+population_log+perGDP_log+C(year)+C(city)',data=data_2019)
result_2019=reg_fe.fit()
result_2019.summary()

reg_fe=smf.ols(formula='Fiscal_transparency_log~Fiscal_transparency_lagged_log+past_experience_dummy+male+age+education+industry_structrue+fiscal_expend_education_science+Fiscal_autonomy+population_log+perGDP_log+C(year)+C(city)',data=data_2020)
result_2020=reg_fe.fit()
result_2020.summary()

reg_fe=smf.ols(formula='Fiscal_transparency_log~Fiscal_transparency_lagged_log+past_experience_dummy+male+age+education+industry_structrue+fiscal_expend_education_science+Fiscal_autonomy+population_log+perGDP_log+C(year)+C(city)',data=data_2021)
result_2021=reg_fe.fit()
result_2021.summary()

reg_fe=smf.ols(formula='Fiscal_transparency_log~Fiscal_transparency_lagged_log+past_experience_dummy+male+age+education+industry_structrue+fiscal_expend_education_science+Fiscal_autonomy+population_log+perGDP_log+C(year)+C(city)',data=data_2022)
result_2022=reg_fe.fit()
result_2022.summary()

result=summary_col([result_HC0,result_2015,result_2016,result_2017,result_2018,result_2019,result_2020,result_2021,result_2022],
            model_names=['model1','model2','model3','model4','model5','model6','model7','model8','model9'],
            stars=True,regressor_order=['const','past_experience_dummy','Fiscal_transparency_lagged_log','male','age','education','industry_structrue','fiscal_expend_education_science','Fiscal_autonomy','population_log','perGDP_log'],
            drop_omitted=True,info_dict={'':lambda x:'',
                                         '':lambda x:'',
                                         'Observations':lambda x:str(int(x.nobs)),
                                         })

print(result)