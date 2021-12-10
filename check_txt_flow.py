import os
import glob
import time

seq_dir = os.path.expanduser('./')
files = glob.glob(seq_dir + 'a.txt')
flow_init = []

# 读取初始化的txt内容
for f, file in enumerate(files):
    readfile = open(file, 'r')  # 读取文件
    fline = readfile.readlines()  # 读取txt文件中每一行
    flow_init.append(fline)
    print(flow_init)

while True:
    time.sleep(3)
    for f, file in enumerate(files):
        readfile = open(file, 'r')  # 读取文件
        fline = readfile.readlines()  # 读取txt文件中每一行
        flow_now = fline
        print(flow_now)
        if flow_now == flow_init or flow_now == '':
            print('dont push flow')
        else:
            flow_init = flow_now
            print('push flow')

        # for j in fline:
        #     s = j
        #     if j[:1] == '5' or '6':
        #         s = '10' + j[1:]
        #     savetxt.write(s)  # 写入新的文件中
