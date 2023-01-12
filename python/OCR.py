import tkinter as tk
from tkinter import filedialog
import cv2 #pip install opencv-python

import pytesseract
# 创建一个窗口
root = tk.Tk()
def select_file():
    try:
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename()
        # 读取文件
        image = cv2.imread(file_path)
        # 以下是你原来的代码，将读取的图像传入
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        threshold, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text = pytesseract.image_to_string(gray)
        print(text)
    except Exception as e:
        print("Error:", e)

# 创建一个按钮，用于打开文件选择对话框
button = tk.Button(root, text="Select File", command=select_file)
button.pack()



# 运行主循环
root.mainloop()
