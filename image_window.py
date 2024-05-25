import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import math

class ImageWindow(tk.Toplevel):
    def __init__(self, master=None, image_path=None):
        super().__init__(master)
        self.title("Image Viewer")
        self.canvas = tk.Canvas(self)
        self.canvas.pack()
        self.image_path = image_path
        self.photo = None
        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.save_button = tk.Button(self, text="Save Image", command=self.save_image)
        self.save_button.pack()
        self.crop_button = tk.Button(self, text="Crop Image", command=self.crop_image_dialog)
        self.crop_button.pack()

    def show_image(self, image_path):
        self.image_path = image_path
        image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.config(width=image.width, height=image.height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    def crop_image_dialog(self):
        crop_dialog = CropDialog(self)
        self.wait_window(crop_dialog)
        if crop_dialog.result:
            rows, cols, base_name, save_path = crop_dialog.result
            self.crop_image(rows, cols, base_name, save_path)

    def crop_image(self, rows, cols, base_name, save_path):
        if self.image_path:
            image = Image.open(self.image_path)
            width, height = image.size
            tile_width = math.ceil(width / cols)
            tile_height = math.ceil(height / rows)
            count = 1
            for y in range(0, height, tile_height):
                for x in range(0, width, tile_width):
                    box = (x, y, x + tile_width, y + tile_height)
                    cropped_image = image.crop(box)
                    file_name = f"{base_name}_{count}.bmp"
                    cropped_image.save(os.path.join(save_path, file_name))
                    count += 1

    def save_image(self):
        if self.image_path:
            save_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP Files", "*.bmp")])
            if save_path:
                image = Image.open(self.image_path)
                image.save(save_path)

class CropDialog(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Crop Image")
        self.result = None
        self.create_widgets()

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