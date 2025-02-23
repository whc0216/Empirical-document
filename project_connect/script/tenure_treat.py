import pandas as pd

df = pd.read_csv("tidy_pref_tenure.csv", parse_dates=["wk_b", "wk_e"])

def method_longest_tenure(df):
    df["wk_b"] = pd.to_datetime(df["wk_b"], errors="coerce")
    df["wk_e"] = pd.to_datetime(df["wk_e"], errors="coerce")

    invalid_dates = df[df["wk_b"].isna() | df["wk_e"].isna()]
    invalid_duration = df[df["wk_b"] > df["wk_e"]]
    
    if not invalid_dates.empty:
        print("发现日期格式错误记录（保存到 invalid_dates.csv）:")
        invalid_dates.to_csv("invalid_dates.csv", index=False)
    
    if not invalid_duration.empty:
        print("发现任期开始晚于结束的记录（保存到 invalid_duration.csv）:")
        invalid_duration.to_csv("invalid_duration.csv", index=False)

    df_clean = df.dropna(subset=["wk_b", "wk_e"]).query("wk_b <= wk_e")
    
    if df_clean.empty:
        return pd.DataFrame()
    
    df_clean["year"] = df_clean.apply(
        lambda row: list(range(row["wk_b"].year, row["wk_e"].year + 1)),
        axis=1
    )
    df_clean = df_clean[df_clean["year"].map(len) > 0]

    df_expanded = df_clean.explode("year").reset_index(drop=True)
    df_expanded["year"] = df_expanded["year"].astype(int)
    
    def calculate_tenure_days(row):
        year_start = pd.Timestamp(year=row["year"], month=1, day=1)
        year_end = pd.Timestamp(year=row["year"], month=12, day=31)
        start = max(row["wk_b"], year_start)
        end = min(row["wk_e"], year_end)
        return (end - start).days + 1 if start <= end else 0
    
    df_expanded["tenure_days"] = df_expanded.apply(calculate_tenure_days, axis=1)
    
    df_result = df_expanded.sort_values("tenure_days", ascending=False).drop_duplicates(
        subset=["arcd", "cityabbr", "pst", "year"], 
        keep="first"
    )
    
    final_cols = ["arcd", "prvn", "cityabbr", "pst", "name", "offcd", "id", "committee", "rank", "year", "wk_b", "wk_e"]
    return df_result[final_cols]


def method_year_end(df):
    """方法2：每年12月1日在任者归属该年"""
    result_rows = []
    for year in range(df["wk_b"].dt.year.min(), df["wk_e"].dt.year.max() + 1):
        check_date = pd.Timestamp(year=year, month=12, day=1)
        mask = (df["wk_b"] <= check_date) & (df["wk_e"] > check_date)  
        df_year = df[mask].copy()
        df_year["year"] = year
        result_rows.append(df_year)
    return pd.concat(result_rows)[["arcd", "prvn", "cityabbr", "pst", "name","offcd","id","committee","rank", "year", "wk_b", "wk_e"]]

def method_year_start(df):
    """方法3：每年1月1日在任者归属该年（向下取）"""
    result_rows = []
    for year in range(df["wk_b"].dt.year.min(), df["wk_e"].dt.year.max() + 1):
        check_date = pd.Timestamp(year=year, month=1, day=1)
        mask = (df["wk_b"] <= check_date) & (df["wk_e"] > check_date)
        df_year = df[mask].copy()
        df_year["year"] = year
        result_rows.append(df_year)
    return pd.concat(result_rows)[["arcd", "prvn", "cityabbr", "pst", "name","offcd","id","committee","rank", "year", "wk_b", "wk_e"]]

df_method1 = method_longest_tenure(df)
df_method2 = method_year_end(df)
df_method3 = method_year_start(df)

df_method1.to_csv("result_method1_longest_tenure.csv", index=False, encoding="utf-8-sig")
df_method2.to_csv("result_method2_year_end_dec1.csv", index=False, encoding="utf-8-sig")
df_method3.to_csv("result_method3_year_start_jan1.csv", index=False, encoding="utf-8-sig")

print("处理完成！文件已保存为 result_method1~3.csv")