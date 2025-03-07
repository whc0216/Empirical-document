import pandas as pd

data = pd.read_csv(r"C:\Users\13298\Desktop\final_panel_corrected.csv")
df = pd.DataFrame(data)
df = df.sort_values(['city_group_a', 'city_group_b', 'year']).reset_index(drop=True)

max_pre = max_post = max_treat = 0

for _, group in df.groupby(['city_group_a', 'city_group_b']):
    connect = group.connect.values
    in_block = False
    current_block_length = 0
    pre_zeros = []
    post_zeros = []
    
    blocks = []
    start = None
    for i, val in enumerate(connect):
        if val == 1:
            if not in_block:
                start = i
                pre_count = 0
                j = i-1
                while j >= 0 and connect[j] == 0:
                    pre_count += 1
                    j -= 1
                pre_zeros.append(pre_count)
            current_block_length += 1
            in_block = True
        else:
            if in_block:
                post_count = 0
                j = i
                while j < len(connect) and connect[j] == 0:
                    post_count += 1
                    j += 1
                post_zeros.append(post_count)
                blocks.append(current_block_length)
                current_block_length = 0
            in_block = False
    
    if in_block:
        post_count = 0
        j = len(connect)
        while j < len(connect) and connect[j] == 0:
            post_count += 1
            j += 1
        post_zeros.append(post_count)
        blocks.append(current_block_length)
    
    if pre_zeros:
        max_pre = max(max_pre, max(pre_zeros))
    if post_zeros:
        max_post = max(max_post, max(post_zeros))
    if blocks:
        max_treat = max(max_treat, max(blocks))

for i in range(1, max_pre+1):
    df[f'pre{i}'] = 0
for i in range(1, max_treat+1):
    df[f'treat{i}'] = 0
for i in range(1, max_post+1):
    df[f'post{i}'] = 0

def process_group(group):
    group = group.copy()
    connect = group.connect.values
    indices = group.index
    n = len(connect)
    
    blocks = []
    start = None
    for i in range(n):
        if connect[i] == 1 and start is None:
            start = i
        elif connect[i] == 0 and start is not None:
            end = i-1
            blocks.append((start, end))
            start = None
    if start is not None:
        blocks.append((start, n-1))
    
    for s, e in blocks:
        treat_length = e - s + 1
        for i in range(treat_length):
            treat_num = i + 1
            group.loc[indices[s+i], f'treat{treat_num}'] = 1
        
        pre_num = 1
        j = s - 1
        while j >= 0 and connect[j] == 0 and pre_num <= max_pre:
            group.loc[indices[j], f'pre{pre_num}'] = 1
            pre_num += 1
            j -= 1
        
        post_num = 1
        j = e + 1
        while j < n and connect[j] == 0 and post_num <= max_post:
            group.loc[indices[j], f'post{post_num}'] = 1
            post_num += 1
            j += 1
    
    return group

df = df.groupby(['city_group_a', 'city_group_b']).apply(process_group)
df = df.reset_index(drop=True)
df.fillna(0, inplace=True)

def print_variable_stats(group):
    treat_vars = [col for col in group.columns if col.startswith('treat')]
    pre_treat_vars = [col for col in group.columns if col.startswith('pre')]
    post_treat_vars = [col for col in group.columns if col.startswith('post')]
    
    for treat_var in treat_vars:
        treat_count = group[treat_var].sum()
        treat_stats = group[treat_var].describe()
        print(f"\n{treat_var} 变量的数量: {treat_count}")
        
    for pre_treat_var in pre_treat_vars:
        pre_treat_count = group[pre_treat_var].sum()
        pre_treat_stats = group[pre_treat_var].describe()
        print(f"\n{pre_treat_var} 变量的数量: {pre_treat_count}")

    for post_treat_var in post_treat_vars:
        post_treat_count = group[post_treat_var].sum()
        post_treat_stats = group[post_treat_var].describe()
        print(f"\n{post_treat_var} 变量的数量: {post_treat_count}")
        
print_variable_stats(df)

df.to_csv("panel_event_study_lag.csv", index=False, encoding="utf_8_sig")