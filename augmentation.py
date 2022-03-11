import xml.etree.ElementTree as ET
import pickle
import os
from os import getcwd
import numpy as np
from PIL import Image
import shutil
import matplotlib.pyplot as plt

import imgaug as ia
from imgaug import augmenters as iaa

ia.seed(1)


def read_xml_annotation(root, image_id):
    in_file = open(os.path.join(root, image_id))
    tree = ET.parse(in_file)
    root = tree.getroot()
    bndboxlist = []

    for object in root.findall('object'):  # 找到root节点下的所有country节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        xmin = int(bndbox.find('xmin').text)
        xmax = int(bndbox.find('xmax').text)
        ymin = int(bndbox.find('ymin').text)
        ymax = int(bndbox.find('ymax').text)
        # print(xmin,ymin,xmax,ymax)
        bndboxlist.append([xmin, ymin, xmax, ymax])
        # print(bndboxlist)

    bndbox = root.find('object').find('bndbox')
    return bndboxlist


# (506.0000, 330.0000, 528.0000, 348.0000) -> (520.4747, 381.5080, 540.5596, 398.6603)
def change_xml_annotation(root, image_id, new_target):
    new_xmin = new_target[0]
    new_ymin = new_target[1]
    new_xmax = new_target[2]
    new_ymax = new_target[3]

    in_file = open(os.path.join(root, str(image_id) + '.xml'))  # 这里root分别由两个意思
    tree = ET.parse(in_file)
    xmlroot = tree.getroot()
    object = xmlroot.find('object')
    bndbox = object.find('bndbox')
    xmin = bndbox.find('xmin')
    xmin.text = str(new_xmin)
    ymin = bndbox.find('ymin')
    ymin.text = str(new_ymin)
    xmax = bndbox.find('xmax')
    xmax.text = str(new_xmax)
    ymax = bndbox.find('ymax')
    ymax.text = str(new_ymax)
    tree.write(os.path.join(root, str("%06d" % (str(id) + '.xml'))))


def change_xml_list_annotation(root, image_id, new_target, saveroot, id):
    in_file = open(os.path.join(root, str(image_id) + '.xml'))  # XML_DIR/03001.xml
    tree = ET.parse(in_file)
    elem = tree.find('filename')  # <filename>03001.jpg</filename>
    elem.text = (id + '.jpg')  # '030010'
    xmlroot = tree.getroot()
    index = 0

    for object in xmlroot.findall('object'):  # 找到root节点下的所有country节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        # xmin = int(bndbox.find('xmin').text)
        # xmax = int(bndbox.find('xmax').text)
        # ymin = int(bndbox.find('ymin').text)
        # ymax = int(bndbox.find('ymax').text)

        new_xmin = new_target[index][0]
        new_ymin = new_target[index][1]
        new_xmax = new_target[index][2]
        new_ymax = new_target[index][3]

        xmin = bndbox.find('xmin')
        xmin.text = str(new_xmin)
        ymin = bndbox.find('ymin')
        ymin.text = str(new_ymin)
        xmax = bndbox.find('xmax')
        xmax.text = str(new_xmax)
        ymax = bndbox.find('ymax')
        ymax.text = str(new_ymax)

        index = index + 1

    tree.write(os.path.join(saveroot, id + '.xml'))


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


def get_annotation_category(root, image_id):
    in_file = open(os.path.join(root, image_id))
    tree = ET.parse(in_file)
    root = tree.getroot()
    name_list = []

    for object in root.findall('object'):  # 循环查看img下面所有的object
        name = object.find('name')  # 记录object下面的name值
        name_list.append(name.text)     # 将所有的name-object记录在name_list中

    # 按name的优先级对name_list进行索引
    if 10 in name_list:
        multiple = 1000
    elif 9 in name_list:
        multiple = 18
    elif 11 in name_list:
        multiple = 16
    elif 8 in name_list:
        multiple = 15
    elif 2 in name_list:
        multiple = 8
    elif 13 in name_list:
        multiple = 5
    elif 5 in name_list:
        multiple = 4
    elif 7 in name_list:
        multiple = 3
    elif 14 in name_list:
        multiple = 2
    else:
        multiple = 1

    return multiple


if __name__ == "__main__":

    IMG_DIR = "JPEGImagesOri"
    XML_DIR = "AnnotationsOri"

    AUG_XML_DIR = "Annotations"  # 存储增强后的XML文件夹路径
    try:
        shutil.rmtree(AUG_XML_DIR)
    except FileNotFoundError as e:
        a = 1
    mkdir(AUG_XML_DIR)

    AUG_IMG_DIR = "JPEGImages"  # 存储增强后的影像文件夹路径
    try:
        shutil.rmtree(AUG_IMG_DIR)
    except FileNotFoundError as e:
        a = 1
    mkdir(AUG_IMG_DIR)

    AUGLOOP = 20  # 每张影像增强的数量

    boxes_img_aug_list = []
    new_bndbox = []
    new_bndbox_list = []

    # 影像增强
    seq = iaa.Sequential([
        iaa.Flipud(0.5),  # vertically flip 50% of all images
        iaa.Fliplr(0.5),  # horizontally flip 50% of all images
        iaa.Multiply((1.2, 1.5)),  # change brightness, doesn't affect BBs
        iaa.GaussianBlur(),  # iaa.GaussianBlur(0.5),
        iaa.Crop(percent=(0, 0.3), keep_size=True),
        iaa.Affine(
            translate_px={"x": 15, "y": 15},
            scale=(0.8, 0.95),
            rotate=(-30, 30),
            cval=(125),  # 填充颜色
            shear=(8, 8)   # 错切变换，x,y 方向都变
        )  # translate by 40/60px on x/y axis, and scale to 50-70%, affects BBs
    ], random_order=True)  # Whether to apply the child augmenters in random order.

    for root, sub_folders, files in os.walk(XML_DIR):

        for name in files:  # 每一个文件的名称
            try:
                bndbox = read_xml_annotation(XML_DIR, name)
            except:
                print('*********xml无标注**********')
                continue
            shutil.copy(os.path.join(XML_DIR, name), AUG_XML_DIR)
            shutil.copy(os.path.join(IMG_DIR, name[:-4] + '.jpg'), AUG_IMG_DIR)

            # 检测标签类别，按照标签扩增的优先级，确定该图片需要扩增的数量
            multiple = get_annotation_category(XML_DIR, name)

            for epoch in range(AUGLOOP * multiple):
                seq_det = seq.to_deterministic()  # 保持坐标和图像同步改变，而不是随机
                # 读取图片
                img = Image.open(os.path.join(IMG_DIR, name[:-4] + '.jpg'))
                # sp = img.size
                img = np.asarray(img)
                xml_error = False
                # 对该img中的所有bndbox进行坐标增强
                for i in range(len(bndbox)):
                    bbs = ia.BoundingBoxesOnImage([
                        ia.BoundingBox(x1=bndbox[i][0], y1=bndbox[i][1], x2=bndbox[i][2], y2=bndbox[i][3]),
                    ], shape=img.shape)
                    bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]  # 增强后的bndbox
                    boxes_img_aug_list.append(bbs_aug)  # bndbox的list
                    # ia.imshow(bbs_aug.draw_on_image(img, size=2))   # visual

                    # new_bndbox_list:[[x1,y1,x2,y2],...[],[]]
                    n_x1 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x1)))
                    n_y1 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y1)))
                    n_x2 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x2)))
                    n_y2 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y2)))
                    if n_x1 == 1 and n_x1 == n_x2:
                        n_x2 += 1
                    if n_y1 == 1 and n_y2 == n_y1:
                        n_y2 += 1
                    if n_x1 >= n_x2 or n_y1 >= n_y2:
                        print('error', name)
                        xml_error = True
                        continue
                    new_bndbox_list.append([n_x1, n_y1, n_x2, n_y2])

                    # image_aug = seq_det.augment_images([img])[0]
                    # image_auged = bbs_aug.draw_on_image(image_aug, thickness=1)
                    # ia.imshow(image_auged)  # visual
                if xml_error:
                    xml_error = False
                    continue

                # 对该img进行图像增强
                image_aug = seq_det.augment_images([img])[0]
                # path = os.path.join(AUG_IMG_DIR,
                #                     str("%06d" % (len(files) + int(name[:-4]) + epoch * 250)) + '.jpg')
                path = os.path.join(AUG_IMG_DIR,
                                    name[:-4] + '-' + str(epoch) + '.jpg')

                Image.fromarray(image_aug).save(path)  # 存储变化后的图片

                # 存储变化后的XML
                # change_xml_list_annotation(XML_DIR, name[:-4], new_bndbox_list, AUG_XML_DIR,
                #                            len(files) + int(name[:-4]) + epoch * 250)
                try:
                    change_xml_list_annotation(XML_DIR, name[:-4], new_bndbox_list, AUG_XML_DIR,
                                               name[:-4] + '-' + str(epoch))
                except:
                    print("change_xml_list_annotation error!")
                print(name[:-4] + '-' + str(epoch) + '.jpg')  # 图像保存的路径
                new_bndbox_list = []
