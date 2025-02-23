import pandas as pd
from datetime import datetime

def validate_year_consistency(file_path, method_name):
    df = pd.read_csv(file_path, parse_dates=["wk_b", "wk_e"])
    errors = []

    for idx, row in df.iterrows():
        year = row["year"]
        wk_b = row["wk_b"]
        wk_e = row["wk_e"]
        
        if method_name == "method1":
            valid = (wk_b.year <= year) & (year <= wk_e.year)
            error_type = "年份超出任期范围"
        
        elif method_name == "method2":
            check_date = datetime(year, 12, 1)
            valid = (wk_b <= check_date) & (check_date < wk_e)
            error_type = "12月1日不在任期内"
        
        elif method_name == "method3":
            check_date = datetime(year, 1, 1)
            valid = (wk_b <= check_date) & (check_date < wk_e)
            error_type = "1月1日不在任期内"
        
        else:
            continue
        
        if not valid:
            errors.append({
                "行号": idx + 1,  
                "year": year,
                "wk_b": wk_b.strftime("%Y/%m/%d"),
                "wk_e": wk_e.strftime("%Y/%m/%d"),
                "错误类型": error_type
            })
    
    return pd.DataFrame(errors)

methods = [
    (r"C:\Users\13298\Desktop\project_connect\data\processed\connected_groups_method1.csv", "方法1"),
    (r"C:\Users\13298\Desktop\project_connect\data\processed\connected_groups_method2.csv", "方法2"),
    (r"C:\Users\13298\Desktop\project_connect\data\processed\connected_groups_method3.csv", "方法3")
]

for file, method in methods:
    error_df = validate_year_consistency(file, method)
    print(f"\n=== {method} 异常记录检查 ===")
    if not error_df.empty:
        print(f"发现 {len(error_df)} 条异常记录（前50条）:")
        print(error_df.head(50).to_string(index=False))
        error_df.to_csv(f"年份异常_{method}.csv", index=False, encoding="utf-8-sig")
    else:
        print("无异常记录")
