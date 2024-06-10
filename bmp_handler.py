import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk,ImageDraw
import functools

class BMPFileHandler:
    def __init__(self, master):
        self.master = master
        self.master.title("BMP 文件处理器")
        self.image_list = []  # 存储导入的图片
        self.thumbnail_list = []  # 存储缩略图
        
        self.label = tk.Label(master, text="选择一个 BMP 文件")
        self.label.grid(row=0, column=0, columnspan=4, pady=10)
        
        self.open_button = tk.Button(master, text="打开文件", command=self.open_file)
        self.open_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        self.save_button = tk.Button(master, text="保存文件", command=self.save_file)
        self.save_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        self.clear_button = tk.Button(master, text="清除画布", command=self.clear_canvas)
        self.clear_button.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        self.draw_button = tk.Button(master, text="开启画笔", command=self.toggle_drawing)
        self.draw_button.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

        
        self.canvas = tk.Canvas(master, bg="gray")
        self.canvas.grid(row=2, column=0, columnspan=4, pady=10, sticky="nsew")

   

        
        self.image = None
        self.original_image = None
        self.temp_image = None
        self.filepath = ""
        self.draw_color = "black"
        self.drawing = False
        self.prev_x = None
        self.prev_y = None
        self.drawing_strokes = []  # 初始化绘制痕迹列表
        
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=1)
        
        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)



    def open_file(self):
        filetypes = [("BMP files", "*.bmp"), ("All files", "*.*")]
        self.filepath = filedialog.askopenfilename(title="选择一个 BMP 文件", filetypes=filetypes)
        
        if self.filepath:
            try:
                self.image = Image.open(self.filepath)
                self.original_image = self.image.copy()  # 复制原始图像以便保存
                self.temp_image = self.image.copy()
                self.display_image()
            except Exception as e:
                messagebox.showerror("打开文件错误", f"无法打开文件：{e}")

    def save_file(self):
     if self.image:
        filetypes = [("BMP files", "*.bmp")]
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=filetypes)
        
        if save_path:
            try:
                # Convert original image and current image to RGBA mode to preserve alpha channel
                original_image_rgba = self.original_image.convert("RGBA")
                current_image_rgba = self.image.convert("RGBA")
                
                # Adjust canvas size to match the size of the original image
                canvas_width, canvas_height = self.original_image.size
                self.canvas.config(width=canvas_width, height=canvas_height)
                
                # Create a new image object and merge the content of the canvas with the original image
                merged_image = Image.alpha_composite(original_image_rgba, current_image_rgba)
                
                # Convert the merged image to BMP format
                merged_image.save(save_path, format="BMP")
                messagebox.showinfo("保存成功", f"文件已保存到: {save_path}")
            except Exception as e:
                messagebox.showerror("保存文件错误", f"无法保存文件：{e}")
        else:
            messagebox.showwarning("未加载图像", "请先打开一个 BMP 文件。")


    def clear_canvas(self):
     # 清除画布上的所有绘制痕迹
     for stroke in self.drawing_strokes:
        self.canvas.delete(stroke)
     self.drawing_strokes = []  # 清空绘制痕迹列表
    
     # 清除 self.image 中的绘制痕迹
     self.image = self.original_image.copy()  # 重置 self.image 为原始图像
     self.temp_image = self.original_image.copy()
     self.display_image()  # 更新画布显示

    def display_image(self):
        self.canvas.delete("all")  # 清空画布

        if self.image:
            img_width, img_height = self.image.size
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # 计算缩放比例，使图像适应画布
            x_scale = canvas_width / img_width
            y_scale = canvas_height / img_height
            scale = min(x_scale, y_scale)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            img = self.image.resize((new_width, new_height), Image.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(img)
            
            # 计算图像在画布上的位置使其居中显示
            x_offset = (canvas_width - new_width) // 2
            y_offset = (canvas_height - new_height) // 2

            self.canvas.create_image(x_offset, y_offset, anchor="nw", image=self.img_tk)
            self.canvas.image = self.img_tk

    def start_drawing(self, event):
        if self.drawing:
            self.prev_x = event.x
            self.prev_y = event.y

    def draw(self, event):
     if self.drawing and self.prev_x is not None and self.prev_y is not None:
        x = event.x
        y = event.y
        
        # 计算绘制时的坐标和显示时的坐标之间的缩放比例
        img_width, img_height = self.image.size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        x_scale = img_width / canvas_width
        y_scale = img_height / canvas_height
        
        # 将绘制时的坐标缩放到显示时的坐标范围内
        draw_x1 = int(self.prev_x * x_scale)
        draw_y1 = int(self.prev_y * y_scale)
        draw_x2 = int(x * x_scale)
        draw_y2 = int(y * y_scale)
        
        # 创建临时图像对象并进行绘制
        draw_image = Image.new("RGBA", self.original_image.size, (0, 0, 0, 0))
        draw_canvas = ImageDraw.Draw(draw_image)
        draw_canvas.line((draw_x1, draw_y1, draw_x2, draw_y2), fill=self.draw_color, width=2)
        
        # 将绘制结果合并到 self.image 中
        self.image = Image.alpha_composite(self.image.convert("RGBA"), draw_image.convert("RGBA"))
        
        # 更新画布显示
        self.display_image()
        
        # 更新前一个坐标
        self.prev_x = x
        self.prev_y = y



    def toggle_drawing(self):
        self.drawing = not self.drawing
        if self.drawing:
            self.draw_button.config(text="关闭画笔")
        else:
            self.draw_button.config(text="开启画笔")

if __name__ == "__main__":
    root = tk.Tk()
    app = BMPFileHandler(root)
    root.mainloop()



       



