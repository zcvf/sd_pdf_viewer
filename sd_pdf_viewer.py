#!/usr/bin/env python3
# This program allow select and view pdf files 
# for working program you may need install packages and python modules:
# sudo apt-get install python3-pip python3-tk blt-demo tcl8.6 tk8.6 tix python3-tk-dbg python3-pil python3-pil.imagetk
# pip3 install PyMuPDF frontend pillow matplotlib


# import modules
from cProfile import label
from fileinput import filename
from tkinter import TOP, W, dialog
from tkinter import ttk
from tkinter.constants import BOTH, BOTTOM, HORIZONTAL, LEFT, RIGHT, VERTICAL, X, Y
from turtle import delay, width
import fitz
from PIL import ImageTk,Image
import tkinter
import tkinter.filedialog
import os

class SdPdfViewer():

    def __init__(self, root):
        self.root = root
        self.img_ref = None
        self.but_ref = None
        self.but = None
        self.tkimg = None
        self.file_for_open = None
        self.frame = None
        self.canvas = None
        self.frame2 = None
        self.frame3 = None
        self.canvas2 = None
        self.doc = None
        self.hbar = None
        self.vbar = None

    def donothing(self):
        print("donothing")
        return

    def open_file(self):
        self.file_for_open = tkinter.filedialog.askopenfilename(title="Open file",initialdir=(os.path.expanduser("~/")), defaultextension='.pdf')
        self.load_pdf_page(0)
        self.load_pdf_preview(0)

        return


    def close_program(self):
        self.root.quit()
        return


    def add_menubar(self):
        menubar = tkinter.Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open...", command=self.open_file)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.close_program)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = tkinter.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help",command=self.donothing)
        menubar.add_cascade(label="About",menu=helpmenu)
        #print(file_for_open)
        return

    # function for scrolling pages of document on mouse scroll
    def mouse_wheel(self, event):
#        print("cur_page_num = %f" % self.cur_page_num)
        if event.num == 5 or event.delta < 0:
            print("scroll down")
            self.canvas.yview("scroll",1,"units")
            if self.vbar.get()[1] >= 1:
                if self.cur_page_num < self.doc.page_count:
                    new_page = self.cur_page_num+1
                    self.cur_page_num = new_page
                    self.load_pdf_page(new_page)
                    self.root.after(100)
                    self.canvas.yview("moveto","0.0")
                    self.canvas.config(yscrollcommand=self.vbar.set(0.01,0.02))
        elif event.num == 4 or event.delta > 0:
            print("scroll up")
            self.canvas.yview("scroll",-1,"units")
            if self.vbar.get()[0] <= 0:
                if self.cur_page_num > 0:
                    new_page = self.cur_page_num-1
                    self.cur_page_num = new_page
                    self.load_pdf_page(new_page)
                    self.root.after(100)
                    self.canvas.yview("moveto","1.0")
                    self.canvas.config(yscrollcommand=self.vbar.set(0.99,0.98))

    def mouse_wheel_preview(self, event):
        if event.num == 5 or event.delta < 0 :
            self.canvas2.yview("scroll",1,"units")
        elif event.num == 4 or event.delta > 0:
            self.canvas2.yview("scroll",-1,"units")


    def load_pdf_page(self, page_num = 2, dpi = 120):
        self.cur_page_num = page_num
        rw = self.root.winfo_screenwidth()
        rh = self.root.winfo_screenheight()
        if self.frame != None:
            print("frame in globals")
        else:
            print("frame not in globals")
            self.frame = tkinter.Frame(self.root)
            self.frame.pack(side=LEFT, expand=True, fill=BOTH, pady=0, padx = 0)

        if self.canvas != None:
            print("canvas in globals")
        else:
            self.canvas = tkinter.Canvas(self.frame, height = rh)
            self.hbar = ttk.Scrollbar(self.frame,orient=HORIZONTAL)
            self.hbar.pack(side=BOTTOM,expand=False,fill=X)
            self.hbar.config(command=self.canvas.xview)
            self.vbar = ttk.Scrollbar(self.frame,orient=VERTICAL)
            self.vbar.pack(side=RIGHT,expand=False,fill=Y)
            self.vbar.config(command=self.canvas.yview)

        self.doc = fitz.Document(self.file_for_open)

        page = self.doc.load_page(page_num)

        pix = page.get_pixmap(dpi=dpi)

        mode = "RGBA" if pix.alpha else "RGB"
        pw = pix.width
        ph = pix.height
        img = Image.frombytes(mode, [pw, ph], pix.samples)
        self.tkimg = ImageTk.PhotoImage(img)


        rw = self.root.winfo_width()
        rh = self.root.winfo_height()
        w = int(self.root.winfo_width()) - 300
        h = int(self.root.winfo_height()) - 300

        if self.canvas != None:
            self.canvas.config(scrollregion = (0,0,pw,ph))
            self.canvas.config(height=h)
            self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
            self.canvas.create_image(int(pw/2), int(ph/2), image = self.tkimg)
            self.canvas.bind("<Button-4>",self.mouse_wheel)
            self.canvas.bind("<Button-5>",self.mouse_wheel)
            self.canvas.bind("<MouseWheel>",self.mouse_wheel)
            self.canvas.pack(side=LEFT,expand=True,fill=BOTH)


    def load_pdf_preview(self, page_num = 2, dpi = 16):
        self.doc = fitz.Document(self.file_for_open)
        rw = self.root.winfo_screenwidth()
        rh = self.root.winfo_screenheight()
        if self.frame2 != None:
            print("self.frame2 in globals")
            self.frame2.pack_forget()
            self.frame2.destroy()
            self.frame2=ttk.Frame(self.root)
            self.frame2.config(width=200,height=self.frame2.winfo_height())

        else:
            self.frame2=ttk.Frame(self.root)
            self.frame2.config(width=500,height=self.frame2.winfo_height())
        if self.canvas2 != None:
            print("self.canvas2 in globals")
            self.canvas2.destroy()
            self.canvas2 = tkinter.Canvas(self.frame2, bg="#dedede")
        else:
            self.canvas2 = tkinter.Canvas(self.frame2, bg="#dedede")
        
        print(" :: %d" % int(self.frame2.winfo_height()))
        self.canvas2.config(width = 300, height = rh)

        if self.frame3 != None:
            self.frame3.pack_forget()
            self.frame3.destroy()
            self.frame3 = ttk.Frame(self.canvas2)
            self.frame3.bind(
                "<Configure>",
                lambda e: self.canvas2.configure(
                    scrollregion=self.canvas2.bbox("all")
                )
            )
        else:
            self.frame3 = ttk.Frame(self.canvas2)
            self.frame3.bind(
                "<Configure>",
                lambda e: self.canvas2.configure(
                    scrollregion=self.canvas2.bbox("all")
                )
            )


        preview = []
        preview.clear()

        for i in range(0,self.doc.page_count):
            prev_page = self.doc.load_page(i)
            preview.append(prev_page.get_pixmap(dpi=dpi)) 


        counter = 0
        self.img_ref = []
        for prev_img in preview:
            prev_w = prev_img.width
            prev_h = prev_img.height
            mode = "RGBA" if prev_img.alpha else "RGB"
            preview_img = Image.frombytes(mode, [prev_w, prev_h], prev_img.samples)
            preview_tkimg = ImageTk.PhotoImage(preview_img)
            self.img_ref.append(preview_tkimg)
            but = ttk.Button(self.frame3,image=self.img_ref[counter], command=lambda counter=counter: self.load_pdf_page(page_num = counter)) #, relief = 'flat'
            but.pack()
            counter += 1

        self.frame3.update_idletasks()
        self.canvas2.update_idletasks()
        self.frame2.update_idletasks()

        self.canvas2.bind("<Button-4>", self.mouse_wheel_preview)
        self.canvas2.bind("<Button-5>", self.mouse_wheel_preview)
        self.canvas2.bind("<MouseWheel>", self.mouse_wheel_preview)

        self.frame3.pack(side=RIGHT, expand=True, fill=Y)

        self.canvas2.pack(side=LEFT, expand=True, fill=Y)

        self.canvas2.create_window((1,1), window=self.frame3,anchor="nw")

        self.frame2.pack(side=RIGHT, expand=False, fill=Y)

        self.vbar2 = ttk.Scrollbar(self.frame2,orient=VERTICAL,command=self.canvas2.yview)
        self.canvas2.config(yscrollcommand=self.vbar2.set)
        self.vbar2.pack(side=RIGHT, expand=True, fill="y")




if __name__ == "__main__":
    root = tkinter.Tk()
    rw = root.winfo_screenwidth()
    rh = root.winfo_screenheight()

    root.geometry(f"{rw}x{rh}")
    root.title("PDF viewer by sd")

    pdf_viewer = SdPdfViewer(root)
    pdf_viewer.add_menubar()

    root.mainloop()
