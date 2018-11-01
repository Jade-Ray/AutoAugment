# coding:utf-8

from autoaugment import ImageNetPolicy
import xml.etree.ElementTree as ET
import PIL
import os
import shutil

img_path = "F:/YOLOv3/gongjiao-up"
xml_path = "F:/YOLOv3/gongjiaoxml-up"
trans_img_path = "F:/YOLOv3/transimg"
trans_xml_path = "F:/YOLOv3/transxml"

temp = 1
trans_num = 0


def clear_dir(Obj_path):
    for file in os.listdir(Obj_path):
        if os.path.isfile(os.path.join(Obj_path, file)):
            os.remove(os.path.join(Obj_path, file))


def update_name():
    global temp
    img_new_name = '%06d' % temp + '.jpg'
    xml_new_name = '%06d' % temp + '.xml'
    temp += 1
    return img_new_name, xml_new_name


def copy_files(srcImgFile, srcXmlFile):
    img_new_name, xml_new_name = update_name()
    targetImgFile = os.path.join(trans_img_path, img_new_name)
    targetXmlFile = os.path.join(trans_xml_path, xml_new_name)
    shutil.copyfile(srcImgFile, targetImgFile)
    shutil.copyfile(srcXmlFile, targetXmlFile)


def save_files(TransImg, TransXml):
    img_new_name, xml_new_name = update_name()
    TransXml.write(os.path.join(trans_xml_path, xml_new_name))
    TransImg.save(os.path.join(trans_img_path, img_new_name))
    print('Save ', img_new_name, ' and ', xml_new_name)


clear_dir(trans_img_path)
clear_dir(trans_xml_path)
for file in os.listdir(img_path):
    if os.path.isfile(os.path.join(img_path, file)):
        if os.path.splitext(os.path.join(img_path, file))[1] == '.jpg':
            srcImgFile = os.path.join(img_path, file)
            srcXmlFile = os.path.join(xml_path, os.path.splitext(file)[0] + '.xml')
            copy_files(srcImgFile, srcXmlFile)
            image = PIL.Image.open(srcImgFile)          
            policy = ImageNetPolicy()
            for nums in range(5):
                tree = ET.parse(srcXmlFile)
                transformed, tree, no_trans = policy(image, tree, nums)
                # print(no_trans)
                if no_trans == 0:
                    save_files(transformed, tree)

# for i in range(6)

