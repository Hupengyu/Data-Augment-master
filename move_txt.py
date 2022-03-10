import os
import shutil  # 文件移动所需的库

# 想要移动文件所在的根目录
rootdir = 'img'
# 获取目录下文件名清单
files = os.listdir(rootdir)
print(files) # 输出文件名单

for file in files:
    if '.txt' in file:  # 因为索要移动的文件名均有‘_’,因此利用此判断其是否是所需要移动的文件
        full_path = os.path.join(rootdir, file) # 完整的路径
        des_path = 'txt'         # 目标路径
        shutil.move(full_path, des_path)                 # 移动文件到目标路径
        print(full_path)
        print(des_path)
