import tkinter as tk
from tkinter import filedialog
from image_window import ImageWindow

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ArtEase")
        self.geometry("300x100")
        self.import_button = tk.Button(self, text="Import Image", command=self.import_image)
        self.import_button.pack(fill=tk.BOTH, expand=True)
        self.image_windows = []

        # 获取屏幕的宽度和高度
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 将屏幕分为四等份，计算窗口的位置
        window_width = 300
        window_height = 100
        x_position = int(screen_width * (3/4) - window_width)
        y_position = int(screen_height // 4 - window_height)

        # 将窗口的位置设置为屏幕右上角的中心位置
        self.geometry(f"+{x_position}+{y_position}")

    def import_image(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("BMP Files", "*.bmp")])
        if file_paths:
            for file_path in file_paths:
                image_window = ImageWindow(self, file_path)
                image_window.show_image(file_path)
                self.image_windows.append(image_window)
