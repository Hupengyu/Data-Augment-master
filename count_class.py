# -*- coding:utf-8 -*-
import os
import xml.etree.ElementTree as ET
import numpy as np

# np.set_printoptions(suppress=True, threshold=np.nan)
import matplotlib
from PIL import Image


def parse_obj(xml_path, filename):
    tree = ET.parse(xml_path + '\\' + filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        objects.append(obj_struct)
    return objects


def read_image(image_path, filename):
    im = Image.open(image_path + filename)
    W = im.size[0]
    H = im.size[1]
    area = W * H
    im_info = [W, H, area]
    return im_info


if __name__ == '__main__':
    # xml_path = r"fireimg/xml"
    xml_path = '17_混凝土露筋/17_xml'
    filenamess = os.listdir(xml_path)
    filenames = []
    for name in filenamess:
        name = name.replace('.xml', '')
        filenames.append(name)
    recs = {}
    obs_shape = {}
    # classnames = ['kj_falsework','lk_falsework','ms_falsework','pk_falsework','wk_falsework','fz_falsework','dl','gjwqj','gjtzj',
    #               'gjtsz','pdx','ydsczpt','xtsxlpt','wltsj','td','sgdt','aqw','dhj','fdc','gjjx','jkzh','jbj',
    #               'zdq','ypj','mbzj','pp','qp','scddgj','zgjx','qsb']
    # classnames = ['11','2','3']
    classnames = ['17', '18', '19', '20', '21', '22', '23']
    """
    2--未戴安全帽 1336个
    3--未穿反光衣 12246个 
    4--未戴口罩 8046个 
    5--抽烟  2049 
    6--玩手机 6067 
    7--翻越围栏 2547 
    8--火灾  4565个 
    11--接火盆不规范 2340个

    """
    # , 'mbzj', 'xt', 'jkfh'
    num_objs = {}
    obj_avg = {}
    for i, name in enumerate(filenames):
        recs[name] = parse_obj(xml_path, name + '.xml')

    for name in filenames:
        for object in recs[name]:
            if object['name'] not in num_objs.keys():
                num_objs[object['name']] = 1
            else:
                num_objs[object['name']] += 1
            if object['name'] not in classnames:
                classnames.append(object['name'])
                for i in range(2):
                    i = i + 1
                    app = []
                    app.append(xml_path + name)
                    print(app)
    for name in classnames:
        print('{}:{}个'.format(name, num_objs[name]))
    print('信息统计算完毕。')

# 18
"""
删除1
2增加3000
4去除2000
6去除1000
5增加3000
8增加4000
7增加2500
9增加4000
11 增加4500
12 增加4500
"""