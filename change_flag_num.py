import os
import glob

seq_dir = os.path.expanduser('./')
files = glob.glob(seq_dir + '*.txt')
for f, file in enumerate(files):
    readfile = open(file, 'r')  # 读取文件
    fline = readfile.readlines()  # 读取txt文件中每一行
    savetxt = open(file, 'w')

    for j in fline:
        s = j
        if j[:1] == '5' or '6':
            s = '10' + j[1:]
        savetxt.write(s)  # 写入新的文件中
