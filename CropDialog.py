import tkinter as tk
from tkinter import filedialog

class CropDialog(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Crop Image")
        self.result = None
        self.create_widgets()
        self.minsize(300, 100)

    def create_widgets(self):
        tk.Label(self, text="Rows:").pack()
        self.rows_entry = tk.Entry(self)
        self.rows_entry.pack()
        tk.Label(self, text="Columns:").pack()
        self.cols_entry = tk.Entry(self)
        self.cols_entry.pack()
        tk.Label(self, text="Base Name:").pack()
        self.base_name_entry = tk.Entry(self)
        self.base_name_entry.pack()
        tk.Label(self, text="Save Path:").pack()
        self.save_path_entry = tk.Entry(self)
        self.save_path_entry.pack()
        self.save_path_button = tk.Button(self, text="Select Save Path", command=self.select_save_path)
        self.save_path_button.pack()
        tk.Button(self, text="Crop", command=self.crop).pack()

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