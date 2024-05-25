import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import os
import math
from CropDialog import CropDialog
import numpy as np

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
        self.save_button = tk.Button(self, text="Save Image", command=self.save_image)
        self.save_button.pack()
        self.crop_button = tk.Button(self, text="Crop Image", command=self.crop_image_dialog)
        self.crop_button.pack()
        self.gray_button = tk.Button(self, text="Convert to Grayscale", command=self.convert_to_grayscale)
        self.gray_button.pack()
        self.bw_button = tk.Button(self, text="Convert to Black & White", command=self.convert_to_black_white)
        self.bw_button.pack()
        self.histogram_button = tk.Button(self, text="Histogram Equalization", command=self.histogram_equalization)
        self.histogram_button.pack()
        self.threshold_entry = tk.Entry(self)
        self.threshold_entry.pack()
        self.threshold_label = tk.Label(self, text="Threshold:")
        self.threshold_label.pack()

    def show_image(self, image_path=None, image=None):
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
        if image.mode == "RGB":
            self.gray_button.config(state=tk.NORMAL)
            self.bw_button.config(state=tk.DISABLED)
            self.threshold_entry.config(state=tk.DISABLED)
            self.threshold_label.config(state=tk.DISABLED)
            self.histogram_button.config(state=tk.NORMAL)
        elif image.mode == "L":
            self.gray_button.config(state=tk.DISABLED)
            self.bw_button.config(state=tk.NORMAL)
            self.threshold_entry.config(state=tk.NORMAL)
            self.threshold_label.config(state=tk.NORMAL)
            self.histogram_button.config(state=tk.NORMAL)
        elif image.mode == "1":
            self.gray_button.config(state=tk.DISABLED)
            self.bw_button.config(state=tk.DISABLED)
            self.threshold_entry.config(state=tk.DISABLED)
            self.threshold_label.config(state=tk.DISABLED)
            self.histogram_button.config(state=tk.DISABLED)

    def crop_image_dialog(self):
        crop_dialog = CropDialog(self)
        self.wait_window(crop_dialog)
        if crop_dialog.result:
            rows, cols, base_name, save_path = crop_dialog.result
            self.crop_image(rows, cols, base_name, save_path)

    def crop_image(self, rows, cols, base_name, save_path):
        if self.image_path or self.image:
            if self.image_path:
                image = Image.open(self.image_path)
            elif self.image:
                image = self.image
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
        if self.image_path or self.image:
            save_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP Files", "*.bmp")])
            if save_path:
                if self.image_path:
                    image = Image.open(self.image_path)
                elif self.image:
                    image = self.image
                image.save(save_path)

    def convert_to_grayscale(self):
        if self.image_path or self.image:
            if self.image_path:
                image = Image.open(self.image_path)
            elif self.image:
                image = self.image
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
            # 创建一个新的图像窗口来显示灰度图像
            gray_window = ImageWindow(self.master, image=grayscale_image)
            gray_window.show_image(image=grayscale_image)

    def convert_to_black_white(self):
        if self.image_path or self.image:
            if self.image_path:
                image = Image.open(self.image_path)
            elif self.image:
                image = self.image
            threshold = int(self.threshold_entry.get())
            # 获取图像的宽度和高度
            width, height = image.size
            # 创建一个新的黑白图像
            bw_image = Image.new("1", (width, height))
            # 获取图像的像素数据
            pixels = image.load()
            bw_pixels = bw_image.load()
            # 将灰度值根据阈值转换为黑白值
            for y in range(height):
                for x in range(width):
                    # 获取像素的灰度值
                    luminance = pixels[x, y]
                    # 根据阈值判断黑白值
                    bw_value = 0 if luminance < threshold else 255
                    # 设置黑白图像的像素值
                    bw_pixels[x, y] = bw_value
            # 创建一个新的图像窗口来显示黑白图像
            bw_window = ImageWindow(self.master, image=bw_image)
            bw_window.show_image(image=bw_image)
        
    def histogram_equalization(self):
        if self.image_path or self.image:
            if self.image_path:
                image = Image.open(self.image_path)
            elif self.image:
                image = self.image
                
            if image.mode == 'RGB':
                # 转换为 HSV 色彩空间
                hsv_image = np.array(image.convert('HSV'))

                # 分离 H, S, V 分量
                h, s, v = np.split(hsv_image, 3, axis=2)
                h = h.reshape(-1)
                s = s.reshape(-1)
                v = v.reshape(-1)

                # 对 V 分量进行直方图均衡
                v_equalized = np.array(np.interp(v, (v.min(), v.max()), (0, 255)), dtype=np.uint8)

                # 合并 H, S, V 分量
                hsv_equalized = np.dstack((h.reshape(hsv_image.shape[0], hsv_image.shape[1]),
                                        s.reshape(hsv_image.shape[0], hsv_image.shape[1]),
                                        v_equalized.reshape(hsv_image.shape[0], hsv_image.shape[1])))

                # 转换回 RGB 色彩空间
                equalized_image = Image.fromarray(hsv_equalized, 'HSV').convert('RGB')
            elif image.mode == "L":
                equalized_image = ImageOps.equalize(image).convert('L')

            # 创建一个新的图像窗口来显示直方图均衡后的图像
            equalized_window = ImageWindow(self.master, image=equalized_image)
            equalized_window.show_image(image=equalized_image)
