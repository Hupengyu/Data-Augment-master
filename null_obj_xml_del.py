import xml.etree.ElementTree as ET
import os
import shutil


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
    name_list_is_null = False

    for object in root.findall('object'):  # 循环查看img下面所有的object
        name = object.find('name')  # 记录object下面的name值
        name_list.append(name.text)     # 将所有的name-object记录在name_list中

    # 按name的优先级对name_list进行索引
    if name_list is None:
        name_list_is_null = True

    return name_list_is_null


if __name__ == "__main__":

    XML_DIR = "Annotations"
    IMG_DIR = "JPEGImages"

    GARBAGE = "AAA"
    mkdir(GARBAGE)

    boxes_img_aug_list = []
    new_bndbox = []
    new_bndbox_list = []

    for root, sub_folders, files in os.walk(XML_DIR):

        for name in files:  # 每一个文件的名称
            try:
                bndbox = read_xml_annotation(XML_DIR, name)
            except:
                print('*********xml无标注**********')
                print(os.path.join(IMG_DIR, name[:-4] + '.jpg'))
                print(os.getcwd())
                shutil.move(os.path.join(XML_DIR, name), GARBAGE)
                shutil.move(os.path.join(IMG_DIR, name[:-4] + '.jpg'), GARBAGE)
            # shutil.copy(os.path.join(XML_DIR, name), SMOKE_XML_DIR)
            # shutil.copy(os.path.join(IMG_DIR, name[:-4] + '.jpg'), SMOKE_IMG_DIR)

            # 检测标签类别，确定吸烟数据集
            # name_list_is_null = get_annotation_category(XML_DIR, name)
            # print(name_list_is_null)
            #
            # if name_list_is_null:
            #     print('rmtree')
            #     print(os.path.join(IMG_DIR, name[:-4] + '.jpg'))
            #     shutil.rmtree(os.path.join(XML_DIR, name))
            #     shutil.rmtree(os.path.join(IMG_DIR, name[:-4] + '.jpg'))
