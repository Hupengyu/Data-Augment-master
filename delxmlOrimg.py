"""
https://blog.csdn.net/gusui7202/article/details/83239142
qhy。
"""

import os
import os.path

h = 0
a = ''
b = ''
dele = []
pathh = 'all'
# dele.remove(1)
for filenames in os.walk(
        pathh):  # for dirpath,dirnames,filenames in os.walk(path)三元组，dirpath为搜索目录，dirnames（list）,为搜索目录下所有文件夹，filenames(list)为搜索目录下所有文件，这里用法其实很不好，filenames其实就是这个三元组，然后再将第三个提取出来，代码可读性太差了。
    filenames = list(filenames)
    filenames = filenames[2]
    for filename in filenames:
        print(filename)
        if h == 0:  # 如果第一次检索到这个名字则放到a里面
            a = filename
            h = 1
        elif h == 1:  # 这是第二次检索了，h=1说明已经存储了一个文件名在a中，然后读取了下一个文件名，然后判断是否一样。这个程序的Bug就是pic和label must put together.而且要贴在一起。
            print(filename)
            b = filename
            if a[0:a.rfind('.', 1)] == b[0:b.rfind('.',
                                                   1)]:  # 这里用了rfind来给出名字，然后比较，rfind找出字符最后一次出现的位置。这里.前面就是文字，而切片【a:b】不计b。
                h = 0
                # print(filename)
            else:
                h = 1
                dele.append(a)
                a = b
        else:
            print("wa1")
print(dele)
for file in dele:
    os.remove(pathh +'/'+ file)
    print("remove" + file + " is OK!")

# 再循环一次看看有没有遗漏的单身文件
for filenames in os.walk(pathh):
    filenames = list(filenames)
    filenames = filenames[2]
    for filename in filenames:
        print(filename)
        if h == 0:
            a = filename
            h = 1
        elif h == 1:
            print(filename)
            b = filename
            if a[0:a.rfind('.', 1)] == b[0:b.rfind('.', 1)]:
                h = 0
                print(filename)
            else:
                h = 1
                dele.append(a)
                a = b
        else:
            print("wa1")
print(dele)
# 清除单身的xml或者jpg 在Windows运行