import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageEnhance

class BMPFileHandler:
    def __init__(self, master):
        self.master = master
        self.master.title("BMP 文件处理器")
        self.image_list = []  # 存储导入的图片
        self.thumbnail_list = []  # 存储缩略图
        
        self.open_button = tk.Button(master, text="导入文件", command=self.import_files)
        self.open_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        self.save_button = tk.Button(master, text="保存文件", command=self.save_file)
        self.save_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        self.clear_button = tk.Button(master, text="清除画布", command=self.clear_canvas)
        self.clear_button.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        self.draw_button = tk.Button(master, text="开启画笔", command=self.toggle_drawing)
        self.draw_button.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        
        self.color_button = tk.Button(master, text="选择颜色", command=self.choose_color)
        self.color_button.grid(row=1, column=4, padx=10, pady=5, sticky="ew")
        
        self.canvas = tk.Canvas(master, bg="gray")
        self.canvas.grid(row=2, column=0, columnspan=5, pady=10, sticky="nsew")
        
        self.thumbnail_frame = tk.Frame(master)
        self.thumbnail_frame.grid(row=3, column=0, columnspan=5, pady=10)
        
        self.image = None
        self.original_image = None
        self.filepath = ""
        self.draw_color = "black"
        self.drawing = False
        self.prev_x = None
        self.prev_y = None
        self.drawing_strokes = []  # 初始化绘制痕迹列表
        self.brightness = 1.0
        self.saturation = 1.0
        self.contrast = 1.0
        self.apply_adjustments = False  # 是否应用调整
        
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=1)
        self.master.grid_columnconfigure(4, weight=1)
        
        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.master.bind("<Configure>", self.on_window_resize)

    def import_files(self):
        filetypes = [("BMP files", "*.bmp"), ("All files", "*.*")]
        filepaths = filedialog.askopenfilenames(title="选择 BMP 文件", filetypes=filetypes)
        
        if filepaths:
            for filepath in filepaths:
                try:
                    image = Image.open(filepath)
                    self.image_list.append((image, filepath))
                    thumbnail = image.copy()
                    thumbnail.thumbnail((50, 50))  # 调整缩略图大小
                    self.thumbnail_list.append(thumbnail)
                except Exception as e:
                    messagebox.showerror("导入文件错误", f"无法导入文件：{e}")
            self.display_thumbnails()
            self.switch_image(0)  # 默认显示第一张图片

    def display_thumbnails(self):
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()
        
        for idx, thumbnail in enumerate(self.thumbnail_list):
            img_tk = ImageTk.PhotoImage(thumbnail)
            button = tk.Button(self.thumbnail_frame, image=img_tk, command=lambda idx=idx: self.switch_image(idx))
            button.image = img_tk
            button.grid(row=0, column=idx, padx=5, pady=5)

    def switch_image(self, idx):
        self.image, self.filepath = self.image_list[idx]
        self.original_image = self.image.copy()
        self.clear_canvas()

    def save_file(self):
        if self.image:
            filetypes = [("BMP files", "*.bmp")]
            save_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=filetypes)
            
            if save_path:
                try:
                    save_image = self.apply_image_adjustments(self.image.copy()) if self.apply_adjustments else self.image
                    save_image.save(save_path, format="BMP")
                    messagebox.showinfo("保存成功", f"文件已保存到: {save_path}")
                except Exception as e:
                    messagebox.showerror("保存文件错误", f"无法保存文件：{e}")
        else:
            messagebox.showwarning("未加载图像", "请先导入一个 BMP 文件。")

    def clear_canvas(self):
        # 清除画布上的所有绘制痕迹
        self.canvas.delete("all")
        self.drawing_strokes = []  # 清空绘制痕迹列表

        # 清除 self.image 中的绘制痕迹
        self.image = self.original_image.copy()  # 重置 self.image 为原始图像
        self.display_image()  # 更新画布显示

    def display_image(self):
        self.canvas.delete("all")  # 清空画布

        if self.image:
            image = self.image

            # 如果需要，应用亮度、饱和度和对比度的调整
            if self.apply_adjustments:
                image = self.apply_image_adjustments(image)

            img_width, img_height = image.size
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # 计算缩放比例，使图像适应画布
            x_scale = canvas_width / img_width
            y_scale = canvas_height / img_height
            scale = min(x_scale, y_scale)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            img = image.resize((new_width, new_height), Image.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(img)
            
            # 计算图像在画布上的位置使其居中显示
            x_offset = (canvas_width - new_width) // 2
            y_offset = (canvas_height - new_height) // 2

            self.canvas.create_image(x_offset, y_offset, anchor="nw", image=self.img_tk)
            self.canvas.image = self.img_tk

            self.image_x_offset = x_offset
            self.image_y_offset = y_offset
            self.image_display_width = new_width
            self.image_display_height = new_height

    def apply_image_adjustments(self, image):
        # 调整亮度、饱和度和对比度
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(self.brightness)
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(self.saturation)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(self.contrast)
        return image

    def start_drawing(self, event):
        if self.drawing:
            self.prev_x = event.x
            self.prev_y = event.y

    def draw(self, event):
        if self.drawing and self.prev_x is not None and self.prev_y is not None:
            x = event.x
            y = event.y
            
            # 在画布上绘制
            self.canvas.create_line(self.prev_x, self.prev_y, x, y, fill=self.draw_color, width=2)

            # 检查绘制点是否在图像显示区域内
            if (self.image_x_offset <= self.prev_x <= self.image_x_offset + self.image_display_width and
                self.image_y_offset <= self.prev_y <= self.image_y_offset + self.image_display_height and
                self.image_x_offset <= x <= self.image_x_offset + self.image_display_width and
                self.image_y_offset <= y <= self.image_y_offset + self.image_display_height):
                
                # 将画布上的坐标转换为图像上的坐标
                draw_x1 = int((self.prev_x - self.image_x_offset) * self.image.size[0] / self.image_display_width)
                draw_y1 = int((self.prev_y - self.image_y_offset) * self.image.size[1] / self.image_display_height)
                draw_x2 = int((x - self.image_x_offset) * self.image.size[0] / self.image_display_width)
                draw_y2 = int((y - self.image_y_offset) * self.image.size[1] / self.image_display_height)
                
                # 直接在图像上绘制
                draw_image = ImageDraw.Draw(self.image)
                draw_image.line((draw_x1, draw_y1, draw_x2, draw_y2), fill=self.draw_color, width=2)

            self.prev_x = x
            self.prev_y = y



    def toggle_drawing(self):
        self.drawing = not self.drawing
        if self.drawing:
            self.draw_button.config(text="关闭画笔")
        else:
            self.draw_button.config(text="开启画笔")

    def choose_color(self):
        color = colorchooser.askcolor(title="选择画笔颜色")
        if color[1]:
            self.draw_color = color[1]
    
    def on_window_resize(self, event):
        # 窗口大小变化时调用该方法
        self.display_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMPFileHandler(root)
    root.mainloop()
