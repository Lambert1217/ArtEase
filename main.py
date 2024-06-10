import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from bmp_handler import BMPFileHandler  # 导入自定义BMP处理类
from crop_handler import BMPCropHandler  # 导入自定义裁剪处理类
from histogram_equalization_gray import histogram_equalization_gray  # 导入灰度直方图均衡化方法
from histogram_equalization_color import histogram_equalization_color  # 导入彩色直方图均衡化方法
from color_to_gray import color_to_gray  # 导入彩色转灰度方法
from gray_to_binary import gray_to_binary  # 导入灰度转二进制方法
from PIL import Image, ImageTk, ImageFilter, ImageOps, ImageEnhance
import numpy as np
from gaussian_blur import apply_gaussian_blur
from linear_predictive_coder import LinearPredictiveCoder


class BMPApp:
    def __init__(self, root):
        self.root = root
        self.predictor_order = None
        self.predictor_coefficient = None
        self.encode_data = None

        self.bmp_handler = BMPFileHandler(root)

        # 创建菜单栏
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # 创建文件菜单
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)
        self.file_menu.add_command(label="打开 BMP", command=self.bmp_handler.import_files)
        self.file_menu.add_command(label="保存 BMP", command=self.bmp_handler.save_file)

        # 创建编辑菜单
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="编辑", menu=self.edit_menu)
        self.edit_menu.add_command(label="裁剪并保存", command=self.crop_image)
        self.edit_menu.add_command(label="灰度图像增强", command=self.enhance_gray_image)
        self.edit_menu.add_command(label="彩色图像增强", command=self.enhance_color_image)
        self.edit_menu.add_command(label="灰转二进制", command=self.convert_to_binary)
        self.edit_menu.add_command(label="彩转灰", command=self.convert_to_gray)
        self.edit_menu.add_command(label="高斯模糊", command=self.apply_gaussian_blur)
        self.edit_menu.add_command(label="锐化", command=self.apply_sharpen)
        self.edit_menu.add_command(label="上下翻转", command=self.flip_vertical)
        self.edit_menu.add_command(label="左右翻转", command=self.flip_horizontal)
        self.edit_menu.add_command(label="反相", command=self.invert_colors)

        # 创建编码菜单
        self.encode_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="编码", menu=self.encode_menu)
        self.encode_menu.add_command(label="编码图像", command=self.encode_image)
        self.encode_menu.add_command(label="解码图像", command=self.decode_image)

        # 创建调节亮度、饱和度、对比度的滑块
        self.brightness_scale = tk.Scale(root, from_=0, to=2, resolution=0.01, label="亮度",
                                         orient="horizontal", command=self.scale_changed)
        self.brightness_scale.set(1)
        self.brightness_scale.grid(row=0, column=0, padx=10, pady=5)

        self.saturation_scale = tk.Scale(root, from_=0, to=2, resolution=0.01, label="饱和度",
                                         orient="horizontal", command=self.scale_changed)
        self.saturation_scale.set(1)
        self.saturation_scale.grid(row=0, column=1, padx=10, pady=5)

        self.contrast_scale = tk.Scale(root, from_=0, to=2, resolution=0.01, label="对比度",
                                       orient="horizontal", command=self.scale_changed)
        self.contrast_scale.set(1)
        self.contrast_scale.grid(row=0, column=2, padx=10, pady=5)

        self.apply_adjustments_var = tk.BooleanVar()
        self.apply_adjustments_checkbox = tk.Checkbutton(root, text="应用调整", variable=self.apply_adjustments_var,
                                                           command=self.apply_adjustments_changed)
        self.apply_adjustments_checkbox.grid(row=0, column=3, padx=10, pady=5)

        self.original_image = None
        self.bmp_crop_handler = None

    def display_image(self, image):
        self.bmp_handler.image = image
        # 使用现有的显示方法显示图片
        self.bmp_handler.display_image()

    def crop_image(self):
        if not self.bmp_handler.image:
            tk.messagebox.showwarning("未加载图像", "请先打开一个 BMP 文件。")
            return

        if not self.bmp_crop_handler:
            self.bmp_crop_handler = BMPCropHandler(self.root, self.bmp_handler.canvas, self.bmp_handler.image)

        self.bmp_crop_handler.crop_image()

    def enhance_gray_image(self):
        if not self.bmp_handler.image:
            tk.messagebox.showwarning("未加载图像", "请先打开一个 BMP 文件。")
            return

        enhanced_image = histogram_equalization_gray(self.bmp_handler.image)

        if enhanced_image:
            self.display_image(enhanced_image)
            messagebox.showinfo("增强成功", "灰度图像增强已完成并显示。")

    def enhance_color_image(self):
        if not self.bmp_handler.image:
            tk.messagebox.showwarning("未加载图像", "请先打开一个 BMP 文件。")
            return

        enhanced_image = histogram_equalization_color(self.bmp_handler.image)

        if enhanced_image:
            self.display_image(enhanced_image)
            messagebox.showinfo("增强成功", "彩色图像增强已完成并显示。")

    def convert_to_binary(self):
        if not self.bmp_handler.image:
            tk.messagebox.showwarning("未加载图像", "请先打开一个 BMP 文件。")
            return

        if self.bmp_handler.image.mode != 'L':
            tk.messagebox.showwarning("图像类型错误", "请先加载一个灰度图像。")
            return

        threshold = simpledialog.askinteger("输入阈值", "请输入阈值 (0-255):", minvalue=0, maxvalue=255)

        if threshold is None:
            tk.messagebox.showwarning("无效输入", "请输入一个有效的值。")
            return

        binary_image = gray_to_binary(self.bmp_handler.image, threshold)

        if binary_image:
            self.display_image(binary_image)
            messagebox.showinfo("转换成功", "灰转二进制图像已完成并显示。")

    def convert_to_gray(self):
        if not self.bmp_handler.image:
            tk.messagebox.showwarning("未加载图像", "请先打开一个 BMP 文件。")
            return

        if self.bmp_handler.image.mode != 'RGB':
            tk.messagebox.showwarning("图像类型错误", "请先加载一个彩色图像。")
            return

        gray_image = color_to_gray(self.bmp_handler.image)

        if gray_image:
            self.display_image(gray_image)
            messagebox.showinfo("转换成功", "彩转灰图像已完成并显示。")

    def encode_image(self):
        if not self.bmp_handler.image:
            tk.messagebox.showwarning("未加载图像", "请先打开一个 BMP 文件。")
            return

        self.predictor_order = simpledialog.askinteger("输入预测器阶数", "请输入预测器阶数 (1-3):", minvalue=1, maxvalue=3)
        if self.predictor_order is None:
            tk.messagebox.showwarning("无效输入", "请输入一个有效的阶数。")
            return

        self.predictor_coefficient = simpledialog.askstring("输入预测系数", "请输入预测系数 (逗号分隔):")
        if self.predictor_coefficient is None:
            tk.messagebox.showwarning("无效输入", "请输入有效的预测系数。")
            return

        self.predictor_coefficient = [float(coeff) for coeff in self.predictor_coefficient.split(',')]

        coder = LinearPredictiveCoder(self.predictor_order, self.predictor_coefficient)
        self.encode_data = coder.encode(self.bmp_handler.image)
        encoded_image = Image.fromarray(self.encode_data.astype(np.uint8))

        if encoded_image is not None:
            self.display_image(encoded_image)
            messagebox.showinfo("编码成功", "图像编码已完成并显示。")

    def decode_image(self):
        coder = LinearPredictiveCoder(self.predictor_order, self.predictor_coefficient)
        decoded_image = coder.decode(self.encode_data, self.bmp_handler.image)

        if decoded_image is not None:
            self.display_image(decoded_image)
            messagebox.showinfo("解码成功", "图像解码已完成并显示。")

    def apply_gaussian_blur(self):
        if not self.bmp_handler.image:
            tk.messagebox.showwarning("未加载图像", "请先打开一个 BMP 文件。")
            return

        sigma = 1  # 设置高斯模糊的标准差

        blurred_image = apply_gaussian_blur(self.bmp_handler.image, sigma)

        if blurred_image:
            self.display_image(blurred_image)
            messagebox.showinfo("模糊成功", "高斯模糊已完成并显示。")

    def apply_sharpen(self):
        if not self.bmp_handler.image:
            tk.messagebox.showwarning("未加载图像", "请先打开一个 BMP 文件。")
            return

        sharpened_image = self.bmp_handler.image.filter(ImageFilter.SHARPEN)
        self.display_image(sharpened_image)
        messagebox.showinfo("锐化成功", "图像锐化已完成并显示。")

    def flip_vertical(self):
        if not self.bmp_handler.image:
            tk.messagebox.showwarning("未加载图像", "请先打开一个 BMP 文件。")
            return

        flipped_image = self.bmp_handler.image.transpose(Image.FLIP_TOP_BOTTOM)
        self.display_image(flipped_image)
        messagebox.showinfo("翻转成功", "图像上下翻转已完成并显示。")

    def flip_horizontal(self):
        if not self.bmp_handler.image:
            tk.messagebox.showwarning("未加载图像", "请先打开一个 BMP 文件。")
            return

        flipped_image = self.bmp_handler.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.display_image(flipped_image)
        messagebox.showinfo("翻转成功", "图像左右翻转已完成并显示。")

    def invert_colors(self):
        if not self.bmp_handler.image:
            tk.messagebox.showwarning("未加载图像", "请先打开一个 BMP 文件。")
            return

        inverted_image = ImageOps.invert(self.bmp_handler.image)
        self.display_image(inverted_image)
        messagebox.showinfo("反相成功", "图像反相已完成并显示。")

    def scale_changed(self, event=None):
        self.bmp_handler.brightness = self.brightness_scale.get()
        self.bmp_handler.saturation = self.saturation_scale.get()
        self.bmp_handler.contrast = self.contrast_scale.get()
        self.bmp_handler.display_image()

    def apply_adjustments_changed(self):
        self.bmp_handler.apply_adjustments = self.apply_adjustments_var.get()
        self.bmp_handler.display_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = BMPApp(root)
    root.mainloop()
