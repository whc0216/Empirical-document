import os
import subprocess

folder_path = r"C:\Users\王浩晨\Desktop\新建文件夹\script"
file_path = os.path.join(folder_path, "03_analysis_event-study.py")

subprocess.run(['python', file_path], check=True)