import excel "C:\Users\王浩晨\Desktop\project\data\processed\数据支出.xlsx", firstrow clear

gen past_experience = last - now
gen past_experience_dummy = (past_experience > 0)

encode city, gen(city_numeric)
sort city_numeric year
xtset city_numeric year

bysort city (year): gen temp_rank = sum(past_experience_dummy) if past_experience_dummy == 1

forvalues i = 1(1)7 {  
    gen rel_time_`i' = 0
    replace rel_time_`i' = 1 if temp_rank == `i'
}

forvalues i = 1(1)6 {  
    gen rel_time_m`i' = 0
    bysort city (year): replace rel_time_m`i' = 1 if past_experience_dummy[_n+`i'] == 1 & sum(past_experience_dummy) == 0
}

bysort city: egen ever_treated = max(past_experience_dummy)
gen control_cohort = (ever_treated == 0)
drop temp_rank

eventstudyinteract Efficiency1 rel_time_m6 rel_time_m5 rel_time_m4 rel_time_m2 rel_time_m1 rel_time_1 rel_time_2 rel_time_3 rel_time_4 rel_time_5 rel_time_6 rel_time_7,absorb(city_numeric year) cohort(year) control_cohort(control_cohort) covariates(industry_structure Fiscal_autonomy population_log perGDP_log age male education)

sort city year

gen csdid_treat = 0

bysort city: egen first_treat_year = min(cond(past_experience_dummy == 1, year, .))
replace csdid_treat = first_treat_year if first_treat_year != .
drop first_treat_year

csdid Efficiency1 industry_structure Fiscal_autonomy population_log perGDP_log age male education,[ivar(city_numeric)] time(year) gvar(csdid_treat) agg(simple)

did_multiplegt (dyn) Efficiency1 city_numeric year past_experience_dummy

did_imputation Efficiency1 city_numeric year csdid_treat,autosample fe(city_numeric year) 

jwdid Efficiency1,ivar(city_numeric) tvar(year) gvar(csdid_treat) fevar(city_numeric year)