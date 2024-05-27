import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import os
import math
from CropDialog import CropDialog
import numpy as np
from LinearPredictiveCoder import LinearPredictiveCoder

class ImageWindow(tk.Toplevel):
    def __init__(self, master=None, image_path=None, image=None):
        super().__init__(master)
        self.title("Image Viewer")
        self.canvas = tk.Canvas(self)
        self.canvas.pack()
        self.image_path = image_path
        self.photo = None
        self.image = image
        self.create_widgets()
        self.update()
        self.minsize(300, 100)

    def create_widgets(self):
        # 创建第一行的按钮和标签
        frame1 = tk.Frame(self)
        frame1.pack(side=tk.TOP)

        self.save_button = tk.Button(frame1, text="保存图片", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.crop_button = tk.Button(frame1, text="裁剪图片", command=self.crop_image_dialog)
        self.crop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.gray_button = tk.Button(frame1, text="转换为灰度", command=self.convert_to_grayscale)
        self.gray_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.histogram_button = tk.Button(frame1, text="直方图均衡", command=self.histogram_equalization)
        self.histogram_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.bw_button = tk.Button(frame1, text="转换为黑白", command=self.convert_to_black_white)
        self.bw_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.threshold_label = tk.Label(frame1, text="阈值:")
        self.threshold_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.threshold_entry = tk.Entry(frame1)
        self.threshold_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 创建第二行的标签、输入框和按钮
        frame2 = tk.Frame(self)
        frame2.pack(side=tk.TOP)

        self.encode_button = tk.Button(frame2, text="编码", command=self.encode_image)
        self.encode_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.decode_button = tk.Button(frame2, text="解码", command=self.decode_image)
        self.decode_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.predictor_order_label = tk.Label(frame2, text="预测阶数:")
        self.predictor_order_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.predictor_order_entry = tk.Entry(frame2)
        self.predictor_order_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.prediction_coefficients_label = tk.Label(frame2, text="预测系数:")
        self.prediction_coefficients_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.prediction_coefficients_entry = tk.Entry(frame2)
        self.prediction_coefficients_entry.pack(side=tk.LEFT, padx=5, pady=5)


    def show_image(self, image_path=None, image=None):
        # 显示图片
        if image_path:
            self.image_path = image_path
            image = Image.open(image_path)
        elif image:
            self.image = image
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.config(width=image.width, height=image.height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.update_button_states(image)

    def update_button_states(self, image):
        # 更新按钮状态
        mode = image.mode
        self.gray_button.config(state=tk.NORMAL if mode == "RGB" else tk.DISABLED)
        self.bw_button.config(state=tk.NORMAL if mode in ("L") else tk.DISABLED)
        self.threshold_entry.config(state=tk.NORMAL if mode == "L" else tk.DISABLED)
        self.threshold_label.config(state=tk.NORMAL if mode == "L" else tk.DISABLED)
        self.histogram_button.config(state=tk.NORMAL if mode in ("RGB", "L") else tk.DISABLED)
        self.encode_button.config(state=tk.NORMAL if mode == "L" else tk.DISABLED)
        self.decode_button.config(state=tk.NORMAL if mode == "L" else tk.DISABLED)
        self.predictor_order_entry.config(state=tk.NORMAL if mode == "L" else tk.DISABLED)
        self.predictor_order_label.config(state=tk.NORMAL if mode == "L" else tk.DISABLED)
        self.prediction_coefficients_entry.config(state=tk.NORMAL if mode == "L" else tk.DISABLED)
        self.prediction_coefficients_label.config(state=tk.NORMAL if mode == "L" else tk.DISABLED)

    def crop_image_dialog(self):
        # 弹出裁剪对话框
        crop_dialog = CropDialog(self)
        self.wait_window(crop_dialog)
        if crop_dialog.result:
            rows, cols, base_name, save_path = crop_dialog.result
            self.crop_image(rows, cols, base_name, save_path)

    def crop_image(self, rows, cols, base_name, save_path):
        # 裁剪图片
        image = self.load_image()
        width, height = image.size
        tile_width = math.ceil(width / cols)
        tile_height = math.ceil(height / rows)
        for row in range(rows):
            for col in range(cols):
                left = col * tile_width
                top = row * tile_height
                right = min(left + tile_width, width)
                bottom = min(top + tile_height, height)
                box = (left, top, right, bottom)
                cropped_image = image.crop(box)
                file_name = f"{base_name}_{row + 1}_{col + 1}.bmp"
                cropped_image.save(os.path.join(save_path, file_name))

    def save_image(self):
        # 保存图片
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP 文件", "*.bmp")])
        if save_path:
            self.load_image().save(save_path)

    def load_image(self):
        # 加载图片
        if self.image_path:
            return Image.open(self.image_path)
        elif self.image:
            return self.image

    def convert_to_grayscale(self):
        # 转换为灰度图像
        image = self.load_image()
        # 获取图像的宽度和高度
        width, height = image.size
        # 创建一个新的灰度图像
        grayscale_image = Image.new("L", (width, height))
        # 获取图像的像素数据
        pixels = image.load()
        grayscale_pixels = grayscale_image.load()
        # 计算灰度值并设置到新的灰度图像中
        for y in range(height):
            for x in range(width):
                # 获取像素的RGB值
                r, g, b = pixels[x, y]
                # 计算灰度值
                luminance = int(0.299 * r + 0.587 * g + 0.114 * b)
                # 设置灰度图像的像素值
                grayscale_pixels[x, y] = luminance
        self.show_new_image(grayscale_image)

    def convert_to_black_white(self):
        # 转换为黑白图像
        image = self.load_image()
        threshold = int(self.threshold_entry.get())
        bw_image = image.convert("L").point(lambda p: 0 if p < threshold else 255, mode='1')
        self.show_new_image(bw_image)

    def histogram_equalization(self):
        # 直方图均衡
        image = self.load_image()
        if image.mode == 'RGB':
            hsv_image = np.array(image.convert('HSV'))
            h, s, v = np.split(hsv_image, 3, axis=2)
            v_equalized = np.interp(v, (v.min(), v.max()), (0, 255)).astype(np.uint8)
            hsv_equalized = np.dstack((h, s, v_equalized))
            equalized_image = Image.fromarray(hsv_equalized, 'HSV').convert('RGB')
        elif image.mode == "L":
            equalized_image = ImageOps.equalize(image).convert('L')
        self.show_new_image(equalized_image)

    def encode_image(self):
        # 编码图片
        predictor_order = int(self.predictor_order_entry.get())
        prediction_coefficients_str = self.prediction_coefficients_entry.get()
        prediction_coefficients = [float(x.strip()) for x in prediction_coefficients_str.split(',')]
        
        image = self.load_image()
        lpc = LinearPredictiveCoder(predictor_order, prediction_coefficients)
        encoded_image = lpc.encode(image)
        
        self.show_new_image(encoded_image)
    
    def decode_image(self):
        # 解码图片
        predictor_order = int(self.predictor_order_entry.get())
        prediction_coefficients_str = self.prediction_coefficients_entry.get()
        prediction_coefficients = [float(x.strip()) for x in prediction_coefficients_str.split(',')]
        
        encoded_image = self.load_image()
        lpc = LinearPredictiveCoder(predictor_order, prediction_coefficients)
        decoded_image = lpc.decode(encoded_image)
        
        # 创建新的ImageWindow来显示解码后的数据
        self.show_new_image(decoded_image)

    def show_new_image(self, new_image):
        # 显示新的图片
        new_window = ImageWindow(self.master, image=new_image)
        new_window.show_image(image=new_image)
