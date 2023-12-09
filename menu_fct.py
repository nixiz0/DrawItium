import tkinter as tk


# Design for the simpledialog (user input)
def app_theme(root):
    root.tk_setPalette(background='#2b2d42', foreground='#ffffff')

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width / 2)
    y_coordinate = (screen_height / 2) - (height / 2)
    window.geometry(f"{width}x{height}+{int(x_coordinate)}+{int(y_coordinate)-80}")