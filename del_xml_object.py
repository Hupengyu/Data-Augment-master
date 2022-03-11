#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
import shutil


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


def del_xml_object(origin_ann_dir, new_ann_dir):
    for dirpaths, dirnames, filenames in os.walk(origin_ann_dir):  # os.walk游走遍历目录名
        for filename in filenames:
            print("process...")
            if os.path.isfile(r'%s%s' % (origin_ann_dir, filename)):  # 获取原始xml文件绝对路径，isfile()检测是否为文件 isdir检测是否为目录
                origin_ann_path = os.path.join(r'%s%s' % (origin_ann_dir, filename))  # 如果是，获取绝对路径（重复代码）
                new_ann_path = os.path.join(r'%s%s' % (new_ann_dir, filename))
                tree = ET.parse(origin_ann_path)  # ET是一个xml文件解析库，ET.parse（）打开xml文件。parse--"解析"
                root = tree.getroot()  # 获取根节点
                for object in root.findall('object'):  # 找到根节点下所有“object”节点
                    name = str(object.find('name').text)  # 找到object节点下name子节点的值（字符串）
                    # 如果name等于str，则删除该节点
                    if name in ["222"]:
                        root.remove(object)


                    # 如果name等于str，则修改name
                    # if (name in ["6"]):
                    #     object.find('name').text = "9"

                # # 检查是否存在labelmap中没有的类别
                # for object in root.findall('object'):
                #     name = str(object.find('name').text)
                #     if not (name in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]):
                #         print(filename + "------------->label is error--->" + name)
                tree.write(new_ann_path)  # tree为文件，write写入新的文件中。


if __name__ == "__main__":
    origin_ann_dir = 'xml/'  # 设置原始标签路径为 Annos
    new_ann_dir = 'Annotations-1/'  # 设置新标签路径 Annotations

    mkdir(origin_ann_dir)
    mkdir(new_ann_dir)

    del_xml_object(origin_ann_dir, new_ann_dir)
