from genericpath import isfile
import os
import logging as log
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.constants import END, W
from transfer import Transfer
from convert import Convert

'''
環境安裝
pip install -r requirements.txt
'''
ABSTRACT_DIR = os.path.dirname(os.path.abspath(__file__))

class UI:
    def __init__(self):
        self.initUI()
        self.transfer = Transfer()
    

    def initUI(self):
        #window
        self.window = tk.Tk()
        self.window.resizable(width = False, height = False)
        self.window.title('window')
        self.window.geometry('1000x470')
        self.background_image_1  = tk.PhotoImage(file= ABSTRACT_DIR + r"\background\bg1.png")
        self.background_image_2  = tk.PhotoImage(file= ABSTRACT_DIR + r"\background\bg2.png")

        #frame
        self.valid_auto_labelling_frame = tk.Frame(self.window, width=500, height=500)
        
        self.xml_to_txt_frame = tk.Frame(self.window, width=500, height=500)

        #valid_auto_labelling_frame widgets
        self.bg_1_label = tk.Label(self.valid_auto_labelling_frame, image=self.background_image_1)
        self.valid_title_label = tk.Label(self.valid_auto_labelling_frame, text = "未標記 -> xml", font=("Lucida Grande", 30))
        self.choose_transfer_img_label = tk.Label(self.valid_auto_labelling_frame, text="transfer_img : ", font=("Lucida Grande", 12))
        self.choose_transfer_img_entry = tk.Entry(self.valid_auto_labelling_frame, width= 45)
        self.choose_transfer_txt_label = tk.Label(self.valid_auto_labelling_frame, text="transfer_txt : ", font=("Lucida Grande", 12))
        self.choose_transfer_txt_entry = tk.Entry(self.valid_auto_labelling_frame, width= 45)
        self.choose_transfer_result_label = tk.Label(self.valid_auto_labelling_frame, text="transfer_result : ", font=("Lucida Grande", 12))
        self.choose_transfer_result_entry = tk.Entry(self.valid_auto_labelling_frame, width= 45)
        self.valid_transfer_btn = tk.Button(self.valid_auto_labelling_frame,text="轉換", width= 10, height= 2, font=("Lucida Grande", 15))

        #xml_to_txt_frame widgets
        self.bg_2_label = tk.Label(self.xml_to_txt_frame, image= self.background_image_2)
        self.xml_to_txt_title_label = tk.Label(self.xml_to_txt_frame, text="xml -> txt 轉換", font=("Lucida Grande", 30))
        self.choose_label_txt_label = tk.Label(self.xml_to_txt_frame, text="label_txt : ", font=("Lucida Grande", 12))
        self.choose_label_txt_entry = tk.Entry(self.xml_to_txt_frame, width=45)
        self.choose_label_xml_label= tk.Label(self.xml_to_txt_frame, text="label_xml : ", font=("Lucida Grande", 12))
        self.choose_label_xml_entry = tk.Entry(self.xml_to_txt_frame, width=45)
        self.xml_to_txt_transfer_btn = tk.Button(self.xml_to_txt_frame, text= "轉換", width= 10, height= 2, font=("Lucida Grande", 15))


    def createUILayout(self): 
        #frame 對 window 布局
        self.valid_auto_labelling_frame.grid(column = 0, row = 0)
        self.valid_auto_labelling_frame.grid_propagate(0)
        self.xml_to_txt_frame.grid(column = 1, row = 0)
        self.xml_to_txt_frame.grid_propagate(0)

        #valid frame 中 widget布局
        self.bg_1_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.valid_title_label.grid(row = 0, columnspan=2, pady=30, padx=140)
        self.choose_transfer_img_label.grid(column = 0, row = 1, pady=15)
        self.choose_transfer_img_entry.grid(column = 1, row = 1, pady=15, sticky=W)
        self.choose_transfer_txt_label.grid(column = 0, row = 2, pady=15)
        self.choose_transfer_txt_entry.grid(column = 1, row = 2, pady=15, sticky=W)
        self.choose_transfer_result_label.grid(column = 0, row = 3, pady=15)
        self.choose_transfer_result_entry.grid(column = 1, row = 3, pady=15, sticky=W)
        self.valid_transfer_btn.grid(row = 4, columnspan = 2, pady= 20)
        
        #xml_to_txt frame 中 widget布局
        self.bg_2_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.xml_to_txt_title_label.grid(row = 0, columnspan=2, padx = 140, pady = 30)
        self.choose_label_txt_label.grid(column = 0, row = 1, pady=15)
        self.choose_label_txt_entry.grid(column = 1, row = 1, pady=15, sticky=W)
        self.choose_label_xml_label.grid(column = 0, row = 2, pady=15)
        self.choose_label_xml_entry.grid(column = 1, row = 2, pady=15, sticky=W)
        self.xml_to_txt_transfer_btn.grid(row = 3, columnspan = 2, pady= 60)


    def setUIAction(self):
        #bind valid frame
        self.choose_transfer_img_entry.bind("<Double-Button-1>", self.choose_img_path)
        self.choose_transfer_txt_entry.bind("<Double-Button-1>", self.choose_txt_path)
        self.choose_transfer_result_entry.bind("<Double-Button-1>", self.choose_result_path)
        self.valid_transfer_btn.bind("<1>", self.valid_transfer_process)

        #bind xml_to_txt frame
        self.choose_label_txt_entry.bind("<Double-Button-1>", self.choose_label_txt_path)
        self.choose_label_xml_entry.bind("<Double-Button-1>", self.choose_label_xml_path)
        self.xml_to_txt_transfer_btn.bind("<1>", self.xml_to_txt_transfer_process)

    def choose_img_path(self, event):
        filepath = filedialog.askdirectory()
        self.choose_transfer_img_entry.insert(0, str(filepath))
    
    def choose_txt_path(self, event):
        filepath = filedialog.askdirectory()
        self.choose_transfer_txt_entry.insert(0, str(filepath))

    def choose_result_path(self, event):
        filepath = filedialog.askdirectory()
        self.choose_transfer_result_entry.insert(0, str(filepath))

    def choose_label_txt_path(self, event):
        filepath = filedialog.askdirectory()
        self.choose_label_txt_entry.insert(0, str(filepath))

    def choose_label_xml_path(self, event):
        filepath = filedialog.askdirectory()
        self.choose_label_xml_entry.insert(0, str(filepath))
    
    #valid轉換
    def valid_transfer_process(self, event):
        self.transfer.process(self.choose_transfer_txt_entry.get(),
                                self.choose_transfer_result_entry.get(),
                                self.choose_transfer_img_entry.get())
        self.choose_transfer_txt_entry.delete(0, END)
        self.choose_transfer_result_entry.delete(0, END)
        self.choose_transfer_img_entry.delete(0, END)

    #xml_to_txt轉換
    def xml_to_txt_transfer_process(self, event):
        path = ABSTRACT_DIR + r'\classes.txt'
        if not os.path.isfile(path):
            messagebox.showerror("錯誤", "檔案不存在")
            return
        
        classes = []
        with open(path, 'r') as p:
            for line in p.read().splitlines():
                classes.append(str(line))
        print(classes)

        convert = Convert(classes, self.choose_label_txt_entry.get(), 
                                    self.choose_label_xml_entry.get())
        convert.show()
        convert.process()

        self.choose_label_txt_entry.delete(0, END)
        self.choose_label_xml_entry.delete(0, END)

    def start(self):
        self.window.mainloop()


if __name__ == '__main__':
    ui = UI()
    ui.createUILayout()
    ui.setUIAction()
    ui.start()
    