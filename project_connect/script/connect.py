import pandas as pd

def process_single_method(method_file, output_suffix):
    df = pd.read_csv(method_file)

    connected_groups = []
    grouped = df.sort_values(["id", "year"]).groupby("id")
    
    for id_num, group in grouped:
        unique_cities = group["cityabbr"].nunique()
        if unique_cities >= 2:
            connected_groups.extend(group.to_dict("records"))

    if connected_groups:
        result_df = pd.DataFrame(connected_groups)
        output_name = f"connected_groups_{output_suffix}.csv"
        result_df.to_csv(output_name, index=False, encoding="utf-8-sig")
        print(f"文件 {output_name} 已生成，包含 {len(result_df)} 条记录（未去重）")
    else:
        print(f"{method_file} 无有效连接组")

method_files = [
    ("result_method1_longest_tenure.csv", "method1"),
    ("result_method2_year_end_dec1.csv", "method2"),
    ("result_method3_year_start_jan1.csv", "method3")
]

for file, suffix in method_files:
    process_single_method(file, suffix)