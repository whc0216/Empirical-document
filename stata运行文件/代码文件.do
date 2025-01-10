import excel "C:\Users\王浩晨\Desktop\实证文件\panel\数据2.xlsx", firstrow clear

encode city,gen(city_num)

quietly eststo model1:regress Fiscal_transparency_lagged past_experience_delta male age education industry_structure Fiscal_autonomy population_log perGDP_log i.year i.city_num
esttab model1, ///
	title("表：回归估计结果") mtitles("Model 1") ///
	se ar2 b(4) /// 
	keep(past_experience_delta male age education industry_structure Fiscal_autonomy      	population_log perGDP_log _cons) ///
	star(* 0.1 ** 0.05 *** 0.01) ///
	varwidth(25) label onecell nogap nobaselevels interaction(" X ") varlabels(_cons 常数项) ///
	stats(N r2 r2_a, fmt(0 4 4) labels("样本量" "R-square" "adj. R-square")) ///
	nobaselevels indicate("年份FEs=*.year" "地级市FEs=*.city_num") ///
	obslast

	
gen year_dummy=(year>=2018)
gen treat_dummy1=(strict_wide_d_lagged>0)
eststo did_model:reghdfe Fiscal_transparency_lagged treat_dummy1##year_dummy male age education industry_structure Fiscal_autonomy population_log perGDP_log, absorb(year city_num)

foreach year of numlist 2014/2022 {
    gen year_`year' = (year == `year')
}

quietly eststo did_model1:reg Fiscal_transparency_lagged year_2014##treat_dummy1 male age education industry_structure Fiscal_autonomy population_log perGDP_log i.year i.city_num
quietly eststo did_model2:reg Fiscal_transparency_lagged year_2015##treat_dummy1 male age education industry_structure Fiscal_autonomy population_log perGDP_log i.year i.city_num
quietly eststo did_model3:reg Fiscal_transparency_lagged year_2016##treat_dummy1 male age education industry_structure Fiscal_autonomy population_log perGDP_log i.year i.city_num
quietly eststo did_model4:reg Fiscal_transparency_lagged year_2017##treat_dummy1 male age education industry_structure Fiscal_autonomy population_log perGDP_log i.year i.city_num
quietly eststo did_model5:reg Fiscal_transparency_lagged year_2018##treat_dummy1 male age education industry_structure Fiscal_autonomy population_log perGDP_log i.year i.city_num
quietly eststo did_model6:reg Fiscal_transparency_lagged year_2019##treat_dummy1 male age education industry_structure Fiscal_autonomy population_log perGDP_log i.year i.city_num
quietly eststo did_model7:reg Fiscal_transparency_lagged year_2020##treat_dummy1 male age education industry_structure Fiscal_autonomy population_log perGDP_log i.year i.city_num
quietly eststo did_model8:reg Fiscal_transparency_lagged year_2021##treat_dummy1 male age education industry_structure Fiscal_autonomy population_log perGDP_log i.year i.city_num
quietly eststo did_model9:reg Fiscal_transparency_lagged year_2022##treat_dummy1 male age education industry_structure Fiscal_autonomy population_log perGDP_log i.year i.city_num

coefplot did_model1 did_model2 did_model3 did_model4 did_model5 did_model6 did_model7 did_model8 did_model9, ///
    keep(1.year_2014#1.treat_dummy1 1.year_2015#1.treat_dummy1 1.year_2016#1.treat_dummy1 1.year_2017#1.treat_dummy1 1.year_2018#1.treat_dummy1 1.year_2019#1.treat_dummy1 1.year_2020#1.treat_dummy1 1.year_2021#1.treat_dummy1 1.year_2022#1.treat_dummy1) ///
    title("Difference-in-Differences (DiD) Results") ///
    ytitle("Coefficient") ///
    xtitle("年份") ///
    vertical ///
    graphregion(color(white)) ///
    levels(95) ///
    coeflabels(1.year_2014#1.treat_dummy1 = "2014" ///
               1.year_2015#1.treat_dummy1 = "2015" ///
               1.year_2016#1.treat_dummy1 = "2016" ///
               1.year_2017#1.treat_dummy1 = "2017" ///
               1.year_2018#1.treat_dummy1 = "2018" ///
               1.year_2019#1.treat_dummy1 = "2019" ///
               1.year_2020#1.treat_dummy1 = "2020" ///
               1.year_2021#1.treat_dummy1 = "2021" ///
               1.year_2022#1.treat_dummy1 = "2022") ///
    legend(off) ///
    mcolor(black) ///
    ciopts(color(black)) ///
    msymbol(circle) ///
    lcolor(black) ///
    yline(0, lcolor(gray) lpattern(dash)) 