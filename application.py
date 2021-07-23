import tkinter as tk
from tkinter.constants import ACTIVE, DISABLED

# import PIL
from PIL import Image
from PIL import ImageFilter, ImageTk, ImageDraw, ImageStat
import numpy as np

from tkinter.filedialog import *
from tensor import *
from PIL import Image

import cv2



def write_array_masck(p):
    tab = []

def alert():
    tk.messagebox.showinfo("alerte", "Bravo!")

def taille_canvas(h,w):
    return str(h)+ "x"+ str(w)


class masque(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("DeepLearning Segmentation")
        
        self.img = None
        self.type_masque = None

    def add(self, img, type_masque):
        self.img = img
        self.type_masque = type_masque
        self.master.title(type_masque)
        str = taille_canvas(256,256)
        self.master.geometry(str)



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.master.title("DeepLearning Segmentation")
        self.master.geometry('300x0')
        self.pack()
        self.monCanva = None
        self.creat_widget()
        self.add_menu()
        self.top = None


    def print_pred(self):
        print(self.top)
        self.top.master.destroy()
        self.top = None


    def creat_widget(self):
        print("creat")

    def add_menu(self):
        menubar = tk.Menu(self.master)

        menu1 = tk.Menu(menubar, tearoff=0)
        menu1.add_command(label="Ouvrir image", command=self.open_img)
       

        menu1.add_command(label="Quitter", command=self.master.quit)
        menubar.add_cascade(label="Fichier", menu=menu1)

        self.menu2 = tk.Menu(menubar, tearoff=0)
        self.menu2.add_command(label="U-net",state=DISABLED, command=self.print_prediction)
        self.menu2.add_separator()
        self.menu2.add_command(label="enregistrer prediction", command=self.register_pred)
        menubar.add_cascade(label="Segmentation", menu=self.menu2)

        menu3 = tk.Menu(menubar, tearoff=0)
        menu3.add_command(label="A propos", command=None)

        # .edit.entryconfig(0, state = ACTIVE)

        self.master.config(menu=menubar)

    def register_pred(self):
        name_mask ="./results/" + self.name + "_mask.tif"
        cv2.imwrite(name_mask, self.p)

    def open_img(self):
        self.filepath = askopenfilename(title = "Ouvrir une image", filetypes = [('png files','.png'),('tiff files','.tif')] )
    
        self.im = Image.open(self.filepath)
        self.width, self.height = self.im.size
        self.photo = ImageTk.PhotoImage(self.im)

        if self.monCanva is None:
            self.monCanva = tk.Canvas(self,width = 2000, height = 2000, bg = "blue")
            self.monCanva.pack()
        else:
            self.monCanva.delete("all")

        self.monCanva.create_image(0, 0, image = self.photo, anchor=tk.NW)

        self.monCanva.image = self.im
        
        self.master.geometry(taille_canvas(self.width, self.height))

        np_im = np.array(self.im)

        self.menu2.entryconfig(0, state = ACTIVE)


    
    def print_prediction(self):
        self.p = predition_img(self.filepath)

        self.p = self.p.astype(np.uint8)

        tab = self.filepath.split('/')
        self.name = tab[len(tab)-1].split('.')[0]
        name_mask = self.name + "_mask.tif"
        
        # cv2.imwrite(name_mask, self.p)
        # self.im = Image.open(name_mask)
        # self.photoMask = ImageTk.PhotoImage(self.im)
        # im.resize((width, height))
        new_im = Image.fromarray(self.p)
        new_im = new_im.resize((self.width, self.height))

        self.create_top(new_im)

    def create_top(self, new_im):
        if self.top is None:
            # self.top = tk.Toplevel(self.master)
            self.top = masque(tk.Toplevel(self.master))
            self.top.master.title("M_" + self.name)
        canvas = tk.Canvas(self.top.master, width = 2000, height = 2000)
        canvas.pack()

        self.photoM = ImageTk.PhotoImage(new_im)
        photo2 = ImageTk.PhotoImage(self.im)
        self.top.master.geometry(taille_canvas(self.width, self.height))
        
        canvas.create_image( 0,0, image = self.photoM, anchor=tk.NW)
        # canvas.image = new_im
        self.top.master.protocol("WM_DELETE_WINDOW", self.print_pred)

if __name__ == "__main__":
    root = tk.Tk()
    a = Application(master = root)
    root.mainloop()

