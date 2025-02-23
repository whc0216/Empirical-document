import pandas as pd

def check_duplicates_and_report(method_file, method_name):
    df = pd.read_csv(method_file)
    
    df["unique_id_count"] = df.groupby(["cityabbr", "year", "pst"])["id"].transform("nunique")
    
    violations = df[df["unique_id_count"] > 1]
    
    violation_groups = violations[["cityabbr", "year", "pst"]].drop_duplicates()
    violation_record_count = len(violations)
    violation_group_count = len(violation_groups)
    
    report = {
        "method": method_name,
        "违规城市-年份-职位组数": violation_group_count,
        "总违规记录数": violation_record_count,
        "违规记录": violations.sort_values(["cityabbr", "year", "pst", "id"])
    }
    return report

method_files = [
    (r"C:\Users\13298\Desktop\project_connect\data\processed\connected_groups_method1.csv", "方法1"),
    (r"C:\Users\13298\Desktop\project_connect\data\processed\connected_groups_method2.csv", "方法2"),
    (r"C:\Users\13298\Desktop\project_connect\data\processed\connected_groups_method3.csv", "方法3")
]

all_reports = []
for file, name in method_files:
    report = check_duplicates_and_report(file, name)
    all_reports.append(report)

for report in all_reports:
    print(f"\n=== {report['method']} 检查结果 ===")
    print(f"违规城市-年份-职位组数: {report['违规城市-年份-职位组数']} 组")
    print(f"总违规记录数: {report['总违规记录数']} 条")
    
    if report['总违规记录数'] > 0:
        sample_violations = (
            report['违规记录']
            .groupby(["cityabbr", "year", "pst"])
            .head(50)
            .sort_values(["cityabbr", "year", "pst"])
        )
        print("\n违规示例:")
        print(sample_violations[["cityabbr", "year", "pst", "id", "name"]].to_string(index=False))
        
    else:
        print("无违规记录")

print("\n检查完成！")