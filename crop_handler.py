import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

class BMPCropHandler:
    def __init__(self, master, canvas, image):
        self.master = master
        self.canvas = canvas
        self.image = image
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
    
    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')
    
    def on_mouse_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)
    
    def on_button_release(self, event):
        self.end_x, self.end_y = (event.x, event.y)
    
    def crop_image(self):
        if not self.image:
            messagebox.showwarning("未加载图像", "请先打开一个 BMP 文件。")
            return

        # 检查是否已经选择了裁剪区域
        if self.start_x is None or self.start_y is None:
            messagebox.showwarning("未选择裁剪区域", "请在图像上点击并拖动鼠标来选择裁剪区域。")
            return
        
        # 计算在原始图像上的裁剪区域
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        orig_width, orig_height = self.image.size
        
        ratio_x = orig_width / canvas_width
        ratio_y = orig_height / canvas_height
        
        left = int(self.start_x * ratio_x)
        upper = int(self.start_y * ratio_y)
        right = int(self.end_x * ratio_x)
        lower = int(self.end_y * ratio_y)
        
        cropped_image = self.image.crop((left, upper, right, lower))
        
        # 保存裁剪后的图像
        filetypes = [("BMP files", "*.bmp")]
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=filetypes)
        
        if save_path:
            try:
                cropped_image.save(save_path)
                messagebox.showinfo("保存成功", f"裁剪后的文件已保存到: {save_path}")
            except Exception as e:
                messagebox.showerror("保存文件错误", f"无法保存文件：{e}")
