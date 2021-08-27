import copy
from logging import log
from lxml.etree import Element, SubElement, tostring, ElementTree

import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

# classes = ["mask", "no-mask"]  # 类别

class Convert():
    def __init__(self, classes_txt_array, label_txt_path, label_xml_path):
        self.classes = classes_txt_array
        self.txt_path = label_txt_path
        self.xml_path = label_xml_path
        pass
        
    def show(self):
        print(self.classes)

    def convert(self, size, box):
        dw = 1. / size[0]
        dh = 1. / size[1]
        x = (box[0] + box[1]) / 2.0
        y = (box[2] + box[3]) / 2.0
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return (x, y, w, h)


    def convert_annotation(self, image_id, txt_path, xml_path):
        in_file = open(xml_path  + '\%s.xml' % (image_id), encoding='UTF-8')
        # in_file = open('./label_xml\%s.xml' % (image_id), encoding='UTF-8')

        out_file = open(txt_path + '\%s.txt' % (image_id), 'w')  # 生成txt格式文件
        # out_file = open('./label_txt\%s.txt' % (image_id), 'w')  # 生成txt格式文件
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            cls = obj.find('name').text
            # print(cls)
            if cls not in self.classes:
                continue
            cls_id = self.classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                float(xmlbox.find('ymax').text))
            bb = self.convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


    def process(self):
        # xml_path = os.path.join(CURRENT_DIR, './label_xml/')
        xml_path = os.path.join(self.xml_path)
        txt_path = os.path.join(self.txt_path)

        # xml list
        img_xmls = os.listdir(xml_path)
        print(len(img_xmls))

        for img_xml in img_xmls:
            label_name = img_xml.split('.')[0]
            print(label_name)
            self.convert_annotation(label_name, self.txt_path, self.xml_path)

        if(len(xml_path) == len(txt_path)):
            print("轉換成功")




