import cv2 
import tkinter as tk
from tkinter import ttk, simpledialog
from tkinter import messagebox
from PIL import Image, ImageTk
import threading

from menu_fct import *
from drawing_app.hands_painter import start_draw


root = tk.Tk()
root.title("DrawItium")
root.minsize(600, 380)
root.maxsize(600, 420)
center_window(root, 600, 420)

# Loading image for background
image = Image.open("ressources/background.png")
background_image = ImageTk.PhotoImage(image)

# Creating a canvas for the background
canvas = tk.Canvas(root)
canvas.place(relwidth=1, relheight=1)
canvas.create_image(300, 240, image=background_image)

def start():
    root = tk.Toplevel()
    app_theme(root)
    root.withdraw()  
    
    num_cam = simpledialog.askinteger("Cam", "Enter camera number:")
    width_cam = simpledialog.askinteger("Width Cam", "Enter camera width:")
    height_cam = simpledialog.askinteger("Height Cam", "Enter camera height:")
    superpos = messagebox.askquestion("Superposition", "Do you want to superimpose the 2 screens into one ?")
    if superpos == 'yes':
        superpos = True
    else: 
        superpos = False
        
    if num_cam is not None and width_cam is not None and height_cam is not None:
        # Executing start_draw in a separate thread
        draw_thread = threading.Thread(target=start_draw, args=(num_cam, width_cam, height_cam, superpos))
        draw_thread.start()
    else: 
        messagebox.showerror("Error", "You must enter values")

def cam_info():
    root = tk.Toplevel()
    app_theme(root)
    root.withdraw()  
    
    num_cam = simpledialog.askinteger("Cam", "Enter camera number:")
    # Open video capture from camera
    cap = cv2.VideoCapture(num_cam)

    # Check if video capture is open
    if not cap.isOpened():
        messagebox.showerror("Error", "Unable to open video capture.")
    else:
        # Get width and height of video capture
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        messagebox.showinfo("Video information", f"Video width: {width}\nVideo height: {height}")

        # Release video capture
        cap.release()

# Creating a style for the buttons
style = ttk.Style()
style.configure('TButton', font=('Times New Roman', 18, 'bold'), foreground='black', background='gray', padding=(10, 4, 10, 4))

# Creation of buttons with custom style
button1 = ttk.Button(root, text="Start", command=start, style='TButton')
button2 = ttk.Button(root, text="Cam Info", command=cam_info, style='TButton')

# Placement of buttons in absolute center position
button1.place(relx=0.5, rely=0.45, anchor="center")
button2.place(relx=0.5, rely=0.57, anchor="center")

root.mainloop()