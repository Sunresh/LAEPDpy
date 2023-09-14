import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image


class TkinterFactory:
    def __init__(self, master):
        self.elements = []

    def clbl(self, master, text=None, row=None, column=None, img=None, image=None, height=None, width=None,
             anchor=None):
        label = tk.Label(master, text=text, image=image, height=height, width=width, anchor=anchor)
        label.place(x=column, y=row)
        if img is not None:
            original_image = Image.open(img)
            resized_image = original_image.resize((width, height))
            photo_image = ImageTk.PhotoImage(resized_image)
            label.configure(image=photo_image)
            label.image = photo_image
        self.elements.append(label)
        return label

    def ccanv(self, master, text=None, row=None, column=None, image=None):
        label = tk.Canvas(master, text=text, image=image)
        label.place(x=column, y=row)
        self.elements.append(label)
        return label

    def cfrm(self, master, row, column, columnspan=None, width=None, height=None):
        fram = tk.Frame(master, height=height, width=width)
        fram.place(x=column, y=row, relwidth=1)
        self.elements.append(fram)
        return fram

    def clblfr(self, master, text, row, column, columnspan=None):
        labelframe = tk.LabelFrame(master, text=text)
        labelframe.place(x=column, y=row, )
        self.elements.append(labelframe)
        return labelframe

    def cbtn(self, master, text, row, column, command=None, w=None):
        button = tk.Button(master, text=text, command=command, width=w, padx=15, pady=15)
        button.place(x=column, y=row)
        self.elements.append(button)
        return button

    def ckbtn(self, master, text, row, column, variable, vari, command=None):
        button = tk.Checkbutton(master, text=text, variable=variable, command=command)
        button.place(x=column, y=row)
        if vari == 0:
            button.select()
        else:
            button.deselect()
        self.elements.append(button)
        return button

    def centry(self, master, row, column):
        entry = tk.Entry(master)
        entry.place(x=column, y=row)
        self.elements.append(entry)
        return entry

    def ctxt(self, master, row, column):
        text = tk.Text(master)
        text.place(x=column, y=row)
        self.elements.append(text)
        return text

    def ctggle(self, master, text, row, func1, func2, column, w=None):
        toggle_button = tk.Button(master, text=text, background="red", width=w, padx=15, pady=15)
        toggle_button.place(x=column, y=row)
        toggle_button.is_toggled = False
        toggle_button.config(relief="raised")

        def toggle():
            if toggle_button.is_toggled:
                toggle_button.is_toggled = False
                toggle_button.config(relief="raised", background="red", text=text + " off")
                func2()
            else:
                toggle_button.is_toggled = True
                toggle_button.config(relief="sunken", background="green", text=text + " on")
                func1()

        toggle_button.config(command=toggle)
        self.elements.append(toggle_button)
        return toggle_button

    def cbbox(self, master, values, row, column, lofa):
        combobox = ttk.Combobox(master, values=values)
        combobox.place(x=column, y=row)
        combobox.set(lofa)
        self.elements.append(combobox)
        return combobox

    def matplot2tk(self, master, xname, yname, title, data):
        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.get_tk_widget().place(x=0, y=0, anchor="nw")
        ax = fig.add_subplot(111)
        ax.plot(data)
        ax.set_xlabel(xlabel=xname)
        ax.set_ylabel(ylabel=yname)
        ax.set_title(title)
        canvas.draw()
        self.elements.append(canvas)

    def destroy_elements(self):
        for element in self.elements:
            element.destroy()
        self.elements = []


    def create_listview(container, label):
        scrollbar = ttk.Scrollbar(container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox = tk.Listbox(container, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=listbox.yview)
        listbox.insert(tk.END, label)

