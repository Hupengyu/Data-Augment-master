"""
File: MaskForAugmentation.py
"""
from PIL import Image
from pylab import *
import os
import xml.etree.ElementTree as ET
import random
from shutil import copyfile

"""将数据集中的标注框从图片中剪裁出来
anno_dir存放xml文件，image_dir存放图片
mask_image_dir存放生成的图片，anno_dir存放生成的xml
occlusion_dir存放作为遮挡的图片
up_path存放作为上半部分遮挡的图片
"""
anno_dir = 'AnnotationsOri/'    # 标签文件夹
image_dir = 'JPEGImagesOri/'    # 图片文件夹
mask_image_dir = 'JPEGImages/'  # 存储遮挡后的图片的文件夹
mask_xml_dir = 'Annotations/'   # 存储遮挡后的xml的文件夹(所有的遮挡并不会改变xml的信息——因为遮挡不会更改位置)
occlusion_dir = 'occ/'  # 遮挡所使用的图片的文件夹
Ratio = [1 / 4, 1 / 2, 3 / 4]
IsImage = False  # 使用图片进行遮挡
IsFilling = True    # 使用纯色进行遮挡


def _main():
    # 获取全部图片文件名和遮挡图片名
    filelist = os.listdir(image_dir)
    filelist_occlusion = os.listdir(occlusion_dir)
    for file in filelist:   # 遍历图片
        anno_file = os.path.splitext(file)[0] + '.xml'  # 根据图片名称得到AnnotationsOri中对应的xml
        num, annos = _ParseAnnotation(anno_file)        # 获取目标的数量，以及目标信息的字典集合
        for j in range(num):    # 遍历object
            # 随机选取作为遮挡的图片和遮挡面积比例
            # ra = random.randint(0, len(filelist_occlusion) - 1)     # 确定遮挡图片
            occ = random.randint(0, len(Ratio) - 1)     # 确定遮挡比例
            # if IsImage:
            #     _Mask_Image(j, annos[j], anno_file, filelist_occlusion[ra], Ratio[occ])
            if IsFilling:
                _Mask_Filling(j, annos[j], anno_file, Ratio[occ])
        print(file + ': ' + str(num))


def _ParseAnnotation(filepath):
    """
    Parse the xml which include the information of object annotation.
    Give an xml path, it will return the dict including the anntotaion information(name, box)
    """
    if os.path.exists(anno_dir + filepath) == False:
        print(filepath + ' :not found')
    tree = ET.parse(anno_dir + filepath)
    annos = [None] * 30
    num = 0
    for annoobject in tree.iter():
        if 'object' in annoobject.tag:
            for element in list(annoobject):
                if 'name' in element.tag:
                    name = element.text
                if 'bndbox' in element.tag:
                    for size in list(element):
                        if 'xmin' in size.tag:
                            xmin = size.text
                        if 'ymin' in size.tag:
                            ymin = size.text
                        if 'xmax' in size.tag:
                            xmax = size.text
                        if 'ymax' in size.tag:
                            ymax = size.text
                            annos[num] = {'name': name, 'xmin': int(xmin), 'ymin': int(ymin), 'xmax': int(xmax),
                                          'ymax': int(ymax)}
                            # annos[num] = {'name':name, 'xmin':xmin, 'ymin':ymin, \
                            #           'xmax':xmax, 'ymax':ymax}
                            num += 1
    # 返回值是图片目标的数量，以及目标信息的字典集合
    return num, annos


def _Mask_Image(num, annotation, file, occlusion, ratio):
    """
    Using the image to occlusion objects at a certain ratio.
      num: the number of object in the picture
      annotation: the information of object annotation
      1: the xml 1 name
      occlusion: the number of occlusion picture
      ratio: the ratio of occlusioning area
    """
    """对目标进行一定比例的遮挡，使用图片作为遮挡物"""
    filenum = os.path.splitext(file)
    filename = filenum[0] + '.jpg'  # 生成图片的名称
    if os.path.exists(image_dir + filename) != True:
        print(filename + 'not found')
        return
    if os.path.exists(occlusion_dir + occlusion) != True:
        print(occlusion + 'not found')
        return

    # 获取标注框的位置信息，和目标的长度和宽度
    box = (annotation['xmin'], annotation['ymin'], annotation['xmax'], annotation['ymax'])
    w = box[2] - box[0]
    h = box[3] - box[1]

    # 获取遮挡物图片
    pil_im_crop = Image.open(occlusion_dir + occlusion)
    # 获取待遮挡图片
    pil_im = Image.open(image_dir + filename)

    # ----对目标分别进行左上，右上，左下， 右下四个位置进行遮挡-----

    # 根据遮挡比例ratio计算遮挡位置的坐标【默认是从左上角进行遮挡】
    place = (box[0], box[1], int(box[2] - (1 - ratio) * w), int(box[3] - (1 - ratio) * h))
    # 计算遮挡位置的长宽
    size = (place[2] - place[0], place[3] - place[1])
    # 将遮挡物图片按照遮挡比例进行resize
    pil_im_crop_resize = pil_im_crop.resize(size)
    # 遮挡
    pil_im.paste(pil_im_crop_resize, place)  # im, box(遮挡区域)

    # 保存遮挡后图片和xml文件
    pil_im.save(mask_image_dir + filenum[0] + '_' + '00' + str(num) + '.jpg')   # 保存遮挡后的图片
    copyfile(anno_dir + file, mask_xml_dir + filenum[0] + '_' + '00' + str(num) + '.xml')   # 直接把原图的xml完全复制，改个名就行——因为遮挡不改变标签
    pil_im.close()

    pil_im = Image.open(image_dir + filename)
    place = (int(box[0] + ratio * w), box[1], box[2], int(box[3] - (1 - ratio) * h))
    size = (place[2] - place[0], place[3] - place[1])
    pil_im_crop_resize = pil_im_crop.resize(size)
    pil_im.paste(pil_im_crop_resize, place)
    pil_im.save(mask_image_dir + filenum[0] + '_' + '01' + str(num) + '.jpg')
    copyfile(anno_dir + file, mask_xml_dir + filenum[0] + '_' + '01' + str(num) + '.xml')
    pil_im.close()

    pil_im = Image.open(image_dir + filename)
    place = (box[0], int(box[1] + ratio * h), int(box[2] - (1 - ratio) * w), box[3])
    size = (place[2] - place[0], place[3] - place[1])
    pil_im_crop_resize = pil_im_crop.resize(size)
    pil_im.paste(pil_im_crop_resize, place)
    pil_im.save(mask_image_dir + filenum[0] + '_' + '02' + str(num) + '.jpg')
    copyfile(anno_dir + file, mask_xml_dir + filenum[0] + '_' + '02' + str(num) + '.xml')
    pil_im.close()

    pil_im = Image.open(image_dir + filename)
    place = (int(box[0] + ratio * w), int(box[1] + ratio * h), box[2], box[3])
    size = (place[2] - place[0], place[3] - place[1])
    pil_im_crop_resize = pil_im_crop.resize(size)
    pil_im.paste(pil_im_crop_resize, place)
    pil_im.save(mask_image_dir + filenum[0] + '_' + '03' + str(num) + '.jpg')
    copyfile(anno_dir + file, mask_xml_dir + filenum[0] + '_' + '03' + str(num) + '.xml')
    pil_im.close()


def _Mask_Filling(num, annotation, file, ratio):
    """
    Using the certain color to filling the object for occlusioning
    num: the number of object in the picture
    annotation: the information of object annotation
    1: the xml 1 name
    ratio: the ratio of occlusioning area
    """
    """使用某一颜色的色块对目标遮挡"""
    filenum = os.path.splitext(file)
    filename = filenum[0] + '.jpg'
    if os.path.exists(image_dir + filename) != True:
        print(filename + 'not found')
        return
    box = (annotation['xmin'], annotation['ymin'], annotation['xmax'], annotation['ymax'])
    w = box[2] - box[0]
    h = box[3] - box[1]
    """filling with the black"""
    # 获取色块，(0, 0, 0)即黑色
    mask = Image.new('RGBA', (w, h), (127, 127, 127))   # 使用灰色的遮挡块

    # 对目标分别进行左部分、右部分、上部分、下部分位置进行遮挡
    pil_im = Image.open(image_dir + filename)
    place = (box[0], box[1], int(box[2] - (1 - ratio) * w), box[3])
    size = (place[2] - place[0], place[3] - place[1])
    pil_im_crop_resize = mask.resize(size)
    pil_im.paste(pil_im_crop_resize, place)
    pil_im.save(mask_image_dir + filenum[0] + '_' + '10' + str(num) + '.jpg')
    copyfile(anno_dir + file, mask_xml_dir + filenum[0] + '_' + '10' + str(num) + '.xml')
    pil_im.close()

    pil_im = Image.open(image_dir + filename)
    place = (int(box[0] + ratio * w), box[1], box[2], box[3])
    size = (place[2] - place[0], place[3] - place[1])
    pil_im_crop_resize = mask.resize(size)
    pil_im.paste(pil_im_crop_resize, place)
    pil_im.save(mask_image_dir + filenum[0] + '_' + '11' + str(num) + '.jpg')
    copyfile(anno_dir + file, mask_xml_dir + filenum[0] + '_' + '11' + str(num) + '.xml')
    pil_im.close()

    pil_im = Image.open(image_dir + filename)
    place = (box[0], box[1], box[2], int(box[3] - (1 - ratio) * h))
    size = (place[2] - place[0], place[3] - place[1])
    pil_im_crop_resize = mask.resize(size)
    pil_im.paste(pil_im_crop_resize, place)
    pil_im.save(mask_image_dir + filenum[0] + '_' + '12' + str(num) + '.jpg')
    copyfile(anno_dir + file, mask_xml_dir + filenum[0] + '_' + '12' + str(num) + '.xml')
    pil_im.close()

    pil_im = Image.open(image_dir + filename)
    place = (box[0], int(box[1] + ratio * h), box[2], box[3])
    size = (place[2] - place[0], place[3] - place[1])
    pil_im_crop_resize = mask.resize(size)
    pil_im.paste(pil_im_crop_resize, place)
    pil_im.save(mask_image_dir + filenum[0] + '_' + '13' + str(num) + '.jpg')
    copyfile(anno_dir + file, mask_xml_dir + filenum[0] + '_' + '13' + str(num) + '.xml')
    pil_im.close()


if __name__ == '__main__':
    _main()
