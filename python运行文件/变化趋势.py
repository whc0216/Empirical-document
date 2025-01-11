import pandas as pd
import statsmodels.formula.api as smf
import scipy.stats as stats
from statsmodels.iolib.summary2 import summary_col
import numpy as np

data_w=pd.read_excel("C:\\Users\\王浩晨\\Desktop\\实证文件\\panel\\数据.xlsx")
data_h=data_w[['From','last','last_log','past_experience_budget_ratio','past_experience_budget_delta','past_experience_delta','province','Fiscal_transparency_lagged','Fiscal_transparency','Fiscal_transparency_log','industry_structure','Regional_GDP_log','perGDP_log','Fiscal_autonomy','population_log','city','year','past_experience_ratio','male','age','education']]
data=pd.DataFrame(data_h)

city_groups = data.groupby('city').apply(lambda x: x.sort_values('year')).reset_index(drop=True)

def check_pattern(group):
    signs = (group['past_experience_delta'] > 0).astype(int)

    sign_changes = signs.diff().fillna(0) != 0

    change_count = sign_changes.sum()

    if change_count >= 3:
        years = group['year'].tolist()
        values = group['past_experience_delta'].tolist()
        signs = signs.tolist()
        return pd.Series({
            'changes': change_count,
            'years': years,
            'values': values,
            'sign_sequence': signs
        })
    return None

results = []
for city, group in city_groups.groupby('city'):
    result = check_pattern(group)
    if result is not None:
        results.append({
            'city': city,
            'changes': result['changes'],
            'years': result['years'],
            'values': result['values'],
            'sign_sequence': result['sign_sequence']
        })

print(f"\n总共找到 {len(results)} 个符合条件的城市")
print("\n详细信息：")
print("=" * 80)

for i, result in enumerate(results, 1):
    print(f"\n城市 {i}: {result['city']}")
    print("-" * 40)
    print("年份序列：", result['years'])
    print("值序列：", [f"{x:.3f}" for x in result['values']])
    print("符号序列：", result['sign_sequence'])
    
    changes = []
    for j in range(1, len(result['sign_sequence'])):
        if result['sign_sequence'][j] != result['sign_sequence'][j-1]:
            if result['sign_sequence'][j] == 1:
                changes.append(f"在{result['years'][j]}年转为正值")
            else:
                changes.append(f"在{result['years'][j]}年转为负值")
    print("变化过程：", " -> ".join(changes))
    print("=" * 80)

if results:
    changes_count = pd.Series([r['changes'] for r in results])
    print("\n统计分析：")
    print(f"符合条件的城市中：")
    print(f"最少符号变化次数：{changes_count.min()}")
    print(f"最多符号变化次数：{changes_count.max()}")
    print(f"平均符号变化次数：{changes_count.mean():.2f}")
    
    print("\n符号变化次数分布：")
    print(changes_count.value_counts().sort_index())
    
    total_cities = len(data['city'].unique())
    print(f"\n符合条件的城市占总城市数的比例：{len(results)/total_cities:.2%}")