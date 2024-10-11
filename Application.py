import json
from tkinter import font
from screeninfo import get_monitors
import tkinter as tk
from tkinter import *
from tkinter import messagebox, Menu, Toplevel, Listbox, END
import cv2
from typing import Any, Callable
import os
from PIL import ImageTk, Image
from ioioo import TkinterFactory
from deposition import gradually_increase_v, analogout, digitalout
from logview import debug, info, warning, error

class Application:

    def __init__(self):
        self.root = tk.Tk()
        self.elements = []
        self.pref = None
        self.file_path = 'selected_values.json'
        self.d = "Dsim" ##"SimDev1" #"Dev3" #self.daqdev()
        self.a0dev = "Dsim/ao0" ##"SimDev1/ao0" #"Dev3/ao0" #"Dev"+str(self.d)+"/ao0"
        self.a1dev = "Dsim/ao1" ##"SimDev1/ao1" #"Dev3/ao1" #"Dev"+str(self.d)+"/ao1"
        self.pzt = 3
        self.electrophoresis = 2
        self.deptime = 20
        self.youu()
        self.camera_on = False
        self.shutter_on = False
        self.deposition_on = False
        self.global_var = "CCD Camera"
        custom_font = font.Font(size=12)
        self.root.option_add("*Font", custom_font)
        self.root.title("LAEPD")
        self.var1 = IntVar()
        self.cap = None
        self.on=False
        self.seek_value = 0
        self.is_capturing = False
        mi = get_monitors()[0]
        h = round(mi.height * 0.85)
        w = round(mi.width * 0.85)
        self.root.geometry(f"{w}x{h}+0+0")
        self.root.configure(bg="white")
        self.root.resizable(False, False)
        self.img_pathy = r"C:/Users/kouki-15/Pictures/Screenshots/Screenshot 2024-10-07 161949.png"
        self.logo = PhotoImage(file=r"C:/Users/kouki-15/Pictures/Screenshots/Screenshot 2024-10-07 161949.png", height=round(self.mgh(0.4)*0.5), width=round(self.mgw(0.4)*0.5))
        self.root.iconphoto(False, self.logo)
        self.fa = TkinterFactory(self.root)
        self.create_elements()
        self.root.protocol("WM_DELETE_WINDOW", self.xitt)
        self.root.mainloop()

    def on_scale_changed(self, value):
        self.seek_value = value

    def xitt(self):
        analogout(v=0, d=self.a0dev)
        analogout(v=0, d=self.a1dev)
        self.root.destroy()

    def ehandl(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(self, *args, **kwargs) -> Any:
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                error_message = str(e)
                messagebox.showerror("Error Message", error_message)
        return wrapper


    def mgh(self,ma):
        mi = self.root.winfo_height()
        h = mi* ma
        return round(h)

    def mgw(self,ma):
        mi = self.root.winfo_width()
        w = mi* ma
        return round(w)

    def get_vfj(self, key):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        if key in data:
            return data[key]
        else:
            return None  # Key not found in JSON file

    def daqdev(self):
        de = self.get_vfj("Daqd")
        return str(de)
    # value = get_value_from_json(file_path, key_to_retrieve)
    # print(f"Value of '{key_to_retrieve}': {value}")

    def save(self, var, key):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        data[key] = var
        with open(self.file_path, 'w') as file:
            json.dump(data, file)

    @ehandl
    def youu(self):
        # hh= analogout(d=self.a1dev)
        # print(hh)
        analogout(v=0, d=self.a1dev)
        analogout(v=0, d=self.a0dev)
        self.bindings()
        if not os.path.isfile(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({'Camera': 'CCD Camera', 'int': 1, 'maya': 'm', 'Daqd': 1}, file)
        with open(self.file_path, 'r') as file:
            self.pref = json.load(file)

    def bindings(self):
        self.root.bind("m", lambda event: self.onof(event))
        self.root.bind("c", lambda event: self.start_capture(event))
        self.root.bind("z", lambda event: self.xitt(event))
        #self.root.bind("m", lambda event: self.onof(event))
        #self.root.bind("m", lambda event: self.onof(event))
        
        
        
    def restart(self):
        self.root.destroy()
        app = Application()

    def shutteronoff(self,event):
        if self.get_vfj('shut') == 0:
            digitalout(True)
            self.ck.config(text="Shutter On")
        elif self.get_vfj('shut') == 1:
            digitalout(False)
            self.ck.config(text="Shutter Off")
            
    def onof(self,event):
        if self.on == False:
            digitalout(True)
            self.ck.config(text="Shutter On")
            self.on = True
        elif self.on == True:
            digitalout(False)
            self.ck.config(text="Shutter Off")
            self.on = False
            

    def handle_keyboard_event(self,event):
            print("kk")
            
    @ehandl
    def create_elements(self):
        self.menu()
        self.CCD_l = self.fa.clbl(self.root, text="CCD Camera", row=0, column=0, img=self.img_pathy, width=self.mgw(0.4), height=self.mgh(0.4))
        self.CCD_label = self.fa.clbl(self.CCD_l, text="CCD Camera", anchor="center", row=0, column=0)
        self.dgraph = self.fa.clbl(self.root, text="Graph", row=0, column=self.mgw(0.4) + 1, img=self.img_pathy, width=self.mgw(0.4), height=self.mgw(0.4))
        self.opf= self.fa.cfrm(self.root, row=0, column=self.mgw(0.8)+3, height=self.mgh(1), width=self.mgw(0.1))
        Lb1 = self.fa.clbl(self.opf, text="Choose Camera", row=0, column=0)
        self.opt = self.fa.cbbox(self.opf, values=("CCD Camera", "Laptop Webcam"), row=40, column=0, lofa=self.pref['Camera'])
        Lb2 = self.fa.clbl(self.opf, text="Choose Deposition time(ms)", row=90, column=0)
        self.daqd = self.fa.cbbox(self.opf, values=("1", "2", "3"), row=130, column=0, lofa=self.pref['Daqd'])
        self.ck = self.fa.ckbtn(self.opf, text="Shutter", row=170, column=0, variable=self.var1, vari=self.pref['int'])
        self.ck.bind("<Button-1>", lambda event: [self.save(var=self.var1.get(), key='shut'), self.shutteronoff(event)])
        self.opt.bind("<<ComboboxSelected>>", lambda event: self.save(var=self.opt.get(), key='Camera'))
        self.daqd.bind("<<ComboboxSelected>>", lambda event: self.save(var=self.daqd.get(), key='Daqd'))
        self.cb = self.fa.ctggle(self.opf, text="Camera", w=round(self.mgh(0.4)*0.5 * 0.02),row=210, column=0, func1=self.start_capture, func2=self.stop_capture)
        self.sb = self.fa.ckbtn(self.opf, text="Shutter", row=270, column=0, variable=3, vari=self.pref['maya'])
        self.dp = self.fa.cbtn(self.opf, text="Deposition", w=round(self.mgh(0.4)*0.5 * 0.02), row=330, column=0, command=lambda: gradually_increase_v(pzt_port=self.a1dev, label=self.dgraph, pzt_volt=self.pzt, tim=self.deptime, electro_port=self.a0dev, electro_volt=self.electrophoresis))
        self.elp = self.fa.ctggle(self.opf, text="Electro", w=round(self.mgh(0.4)*0.5 * 0.02), row=390, column=0, func1=lambda: analogout(v=2, d=self.a0dev), func2= analogout(v=0, d=self.a0dev))
        self.zbtn = self.fa.cbtn(self.opf, text="Zero", w=round(self.mgh(0.4)*0.5 * 0.02), row=470, column=0, command=lambda: analogout(v=0, d=self.a0dev))
        exit = self.fa.cbtn(self.opf, text="Restart Program", w=round(self.mgh(0.4) * 0.5 * 0.02), command=self.restart, row=530, column=0)
        scale = tk.Scale(self.opf, from_=0, to=5, resolution=0.5, orient=tk.HORIZONTAL, command=self.on_scale_changed)
        scale.place(y=570, x=0, relwidth=1)

    @ehandl
    def menu(self):
        menu_items = {
            "Help": {
                "Key": lambda:messagebox.showinfo("Shortcut Keys", "1. m-> toggle shutter.\n2. c->camera"),
                "About": lambda:messagebox.showinfo("About Designer", "Naresh"),
                "Exit": lambda:self.xitt(),
            }
        }
        menu = Menu(self.root)
        for label, items in menu_items.items():
            submenu = Menu(menu, tearoff=0)
            for item_label, command in items.items():
                submenu.add_command(label=item_label, command=command)
            menu.add_cascade(label=label, menu=submenu, underline=0)
        self.root.config(menu=menu)


    @ehandl
    def start_capture(self,event=None):
        if event is None or self.is_capturing == False:
            if self.get_vfj('Camera') == 'CCD Camera':
                cam = 1
            elif self.get_vfj('Camera') == 'Laptop Webcam':
                cam = 0
            if not self.is_capturing:
                self.cap = cv2.VideoCapture(cam)
                self.is_capturing = True
                self.zoom_level = 1.0
                self.CCD_label.bind("<MouseWheel>", self.handle_zoom)
                self.update_frame()
                
        else:
            self.stop_capture()

    @ehandl
    def update_frame(self):
        if self.is_capturing:
            ret, frame = self.cap.read()
            if ret:
                frame = self.apply_zoom(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # frame = cv2.resize(frame, (self.mgw(0.36), self.mgw(0.36)))
                frame = cv2.flip(frame, 1)
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.CCD_label.config(image=img)
                self.CCD_label.image = img
        if self.is_capturing:  # Add this check to continue updating frames only if capturing
            self.CCD_label.after(10, self.update_frame)

    def apply_zoom(self, frame):
        height, width, _ = frame.shape
        zoomed_width = int(width * self.zoom_level)
        zoomed_height = int(height * self.zoom_level)
        frame = cv2.resize(frame, (zoomed_width, zoomed_height))
        return frame

    def handle_zoom(self, event):
        delta = event.delta
        if delta > 0:
            self.zoom_level *= 1.1  # Zoom in
        else:
            self.zoom_level /= 1.1  # Zoom out
        self.zoom_level = max(1.0, min(self.zoom_level, 5.0))

    @ehandl
    def stop_capture(self):
        if self.is_capturing:
            self.is_capturing = False
            if self.cap:
                self.cap.release()
                self.cap = None
            original_image = Image.open(self.img_pathy)
            w,h= self.CCD_label.winfo_height(),self.CCD_label.winfo_width()
            resized_image = original_image.resize((w, h))
            photo_image = ImageTk.PhotoImage(resized_image)
            self.CCD_label.configure(image=photo_image)
            self.CCD_label.image = photo_image



if __name__ == "__main__":
    app = Application()
