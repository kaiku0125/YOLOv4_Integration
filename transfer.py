import os
from pathlib import Path
from PIL import Image

   #xml檔案裡命照片路徑
# ImagePath = 'C:\Users\chuankai\Desktop\s409FMdata\transfer_img'

class Transfer():    
    def __init__(self):
        pass
       

    def creat_mapping_dic(self, result_txt, threshold=0.0):  # 设置一个阈值，用来删掉置信度低的预测框信息
    
        mapping_dic = {}  # 创建一个字典，用来存放信息
        txt = open(result_txt, 'r').readlines()  # 按行读取TXT文件
    
        for info in txt:  # 提取每一行
            info = info.split()  # 将每一行（每个预测框）的信息切分开
    
            photo_name = info[0]  # 图片名称
            probably = float(info[1])  # 当前预测框的置信度
            if probably < threshold:
                continue
            else:
                xmin = int(float(info[2]))
                ymin = int(float(info[3]))
                xmax = int(float(info[4]))
                ymax = int(float(info[5]))
    
                position = [xmin, ymin, xmax, ymax]
    
                if photo_name not in mapping_dic:  # mapping_dic的每个元素的key值为图片名称，value为一个二维list，其中存放当前图片的若干个预测框的位置
                    mapping_dic[photo_name] = []
                mapping_dic[photo_name].append(position)
        return mapping_dic
 
 
    def creat_result_txt(self, raw_txt_path, target_path, image_path, threshold=0.0):  # raw_txt_path为yolo按类输出的TXT的路径 target_path 为转换后的TXT存放路径
    
        all_files = os.listdir(raw_txt_path)  # 获取所以的原始txt
    
        for each_file in all_files:  # 遍历所有的原始txt文件，each_file为一个文件名，例如‘car.txt’
    
            each_file_path = os.path.join(raw_txt_path, each_file)  # 获取当前txt的路径
            map_dic = self.creat_mapping_dic(each_file_path, threshold=threshold)  # 对当前txt生成map_dic
    
            for each_map in map_dic:  # 遍历当前存放信息的字典
                target_txt = each_map + '.xml'  # 生成目标txt文件名
                target_npg = each_map + '.jpg'
                img_jpg = Image.open(image_path + '/' + target_npg)
                target_txt_path = os.path.join(target_path, target_txt)  # 生成目标txt路径
    
                if target_txt not in os.listdir(target_path):
                    txt_write = open(target_txt_path, 'w')  # 如果目标路径下没有这个目标txt文件，则创建它,即模式设置为“覆盖”
                    txt_write.write('<?xml version="1.0" ?><annotation>')
                    txt_write.write('\n')
                    txt_write.write('    ' + '<folder>JPEGImages</folder>')
                    txt_write.write('\n')
                    txt_write.write('    ' + '<filename>' + target_npg + '</filename>')
                    txt_write.write('\n')
                    txt_write.write('    ' + '<path>' + image_path + '\\' + target_npg + '</path>')
                    txt_write.write('\n')
                    txt_write.write('    ' + '<source>')
                    txt_write.write('\n')
                    txt_write.write('        ' + '<database>Unknown</database>')
                    txt_write.write('\n')
                    txt_write.write('    ' + '</source>')
                    txt_write.write('\n')

                    if img_jpg.width != None:
                        txt_write.write('    ' + '<size>')
                        txt_write.write('\n')
                        txt_write.write('        ' + '<width>' + str(img_jpg.width) +'</width>')
                        txt_write.write('\n')
                        txt_write.write('        ' + '<height>'+ str(img_jpg.height) +'</height>')
                        txt_write.write('\n')
                        txt_write.write('        ' + '<depth>3</depth>')
                        txt_write.write('\n')
                        txt_write.write('    ' + '</size>')
                        txt_write.write('\n')
                        
                    txt_write.write('    ' + '<segmented>0</segmented>')
                    txt_write.write('\n')
                else:
                    txt_write = open(target_txt_path, 'a')  # 如果目标路径下有这个目标txt文件，则将模式设置为“追加”
    
                class_name = each_file[:-4]  # 获取当前原始txt的类名
                #txt_write.write(class_name)  # 对目标txt写入类名
                #txt_write.write('\n')  # 换行
    
                for info in map_dic[each_map]:  # 遍历某张图片的所有预测框信息
                
                    txt_write.write('    ' + '<object>')
                    txt_write.write('\n')  # 换行            
                    txt_write.write('        ' + '<name>' + class_name + '</name>')
                    txt_write.write('\n')  # 换行
                    txt_write.write('        ' + '<pose>Unspecified</pose>')
                    txt_write.write('\n')  # 换行
                    txt_write.write('        ' + '<truncated>0</truncated>')
                    txt_write.write('\n')  # 换行
                    txt_write.write('        ' + '<difficult>0</difficult>')
                    txt_write.write('\n')  # 换行
                    txt_write.write('        ' + '<bndbox>')
                    txt_write.write('\n')  # 换行
                    txt_write.write('            ' + '<xmin>' + str(info[0]) + '</xmin>')
                    txt_write.write('\n')  # 换行                
                    txt_write.write('            ' + '<ymin>' + str(info[1]) + '</ymin>')
                    txt_write.write('\n')  # 换行                
                    txt_write.write('            ' + '<xmax>' + str(info[2]) + '</xmax>')
                    txt_write.write('\n')  # 换行                
                    txt_write.write('            ' + '<ymax>' + str(info[3]) + '</ymax>')
                    txt_write.write('\n')  # 换行                
                    txt_write.write('        ' + '</bndbox>')
                    txt_write.write('\n')  # 换行                
                    txt_write.write('    ' + '</object>')
                    txt_write.write('\n')  # 换行
                    

        ImageFile = os.listdir(target_path)
        
        for each_map in ImageFile:
            target_txt = each_map
            target_txt_path = os.path.join(target_path, target_txt)  # 生成目标txt路径
            
            txt_write = open(target_txt_path, 'a')
            txt_write.write('</annotation>')
    
    #由UI.py進行呼叫
    def process(self, txt, result, img):
        self.creat_result_txt(txt, result, img, threshold=0.6)
        # self.creat_result_txt(r'C:\Users\chuankai\Desktop\s409FMdata\transfer_txt',         #darknet 模擬出來的結果txt路徑
        #          r'C:\Users\chuankai\Desktop\s409FMdata\transfer_result',         #轉換後xml存放路徑  
        #          r'C:\Users\chuankai\Desktop\s409FMdata\transfer_img',
        #          threshold=0.6)      #txt辨識率設定

        print('xml OK!!')
    
 
