import tkinter as tk
from tkinter import filedialog

class CropDialog(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("裁剪")
        self.result = None
        self.create_widgets()
        self.minsize(300, 100)

    def create_widgets(self):
        # 添加空白间距
        tk.Label(self, text="Rows:").pack(pady=5)
        self.rows_entry = tk.Entry(self)
        self.rows_entry.pack(pady=5)
        tk.Label(self, text="Columns:").pack(pady=5)
        self.cols_entry = tk.Entry(self)
        self.cols_entry.pack(pady=5)
        tk.Label(self, text="Base Name:").pack(pady=5)
        self.base_name_entry = tk.Entry(self)
        self.base_name_entry.pack(pady=5)
        tk.Label(self, text="保存路径").pack(pady=5)
        self.save_path_entry = tk.Entry(self)
        self.save_path_entry.pack(pady=5)
        self.save_path_button = tk.Button(self, text="选择保存位置", command=self.select_save_path)
        self.save_path_button.pack(pady=5)
        # 添加更多空白间距
        tk.Button(self, text="确定", command=self.crop).pack(pady=10)

    def select_save_path(self):
        save_path = filedialog.askdirectory()
        self.save_path_entry.delete(0, tk.END)
        self.save_path_entry.insert(0, save_path)

    def crop(self):
        rows = int(self.rows_entry.get())
        cols = int(self.cols_entry.get())
        base_name = self.base_name_entry.get()
        save_path = self.save_path_entry.get()
        self.result = (rows, cols, base_name, save_path)
        self.destroy()