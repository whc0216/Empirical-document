import excel "C:\Users\王浩晨\Desktop\数据2.xlsx",firstrow clear

// 先获取年份的唯一值
levelsof year, local(years)

// 创建一个空的 local 来存储图形名称
local graphs ""

// 为每年创建 dotplot
foreach y of local years {
    histogram Fiscal_transparency_lagged if year == `y', ///
        title("年份: `y'") ///
        name(dot`y', replace)
    
    // 将每个图形名称添加到 local 中
    local graphs `graphs' dot`y'
}

// 组合所有图形
graph combine `graphs', rows(3) ///
    title("Fiscal_transparency_lagged") ///
    scheme(s2color)