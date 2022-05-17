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


'''
def message_box(counter):
    if alert.exist():
        pass
    else:
        alert = tkinter.Tk()
    label=tkinter.Label(alert, text = "страница: %d" % counter)
    label.pack()
'''

def donothing():
    print("donothing")
    return

def open_file():
    global file_for_open 
    global root
    file_for_open = tkinter.filedialog.askopenfilename(title="Open file",initialdir=(os.path.expanduser("~/")), defaultextension='.pdf')
    load_pdf_page(root, 0)
    load_pdf_preview(root, 0)

    return


def close_program():
    global root
    root.quit()
    return


def add_menubar(root):
    menubar = tkinter.Menu(root)
    root.config(menu=menubar)
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open...", command=open_file)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=close_program)
    menubar.add_cascade(label="File", menu=filemenu)
    helpmenu = tkinter.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help",command=donothing)
    menubar.add_cascade(label="About",menu=helpmenu)
    #print(file_for_open)
    return

# function for scrolling pages of document on mouse scroll
def mouse_wheel(event):
    global canvas
    global vbar, cur_page_num
#    print("top position: %f, bottom position: %f, event.delta: %f" % (vbar.get()[0], vbar.get()[1], event.delta))
    print("cur_page_num = %f" % cur_page_num)

    # if scroll down
    if event.num == 5 or event.delta < 0:
        print("scroll down")
        canvas.yview("scroll",1,"units")
#        '''
        if vbar.get()[1] >= 1:
            if cur_page_num < doc.page_count:
                new_page = cur_page_num+1
                cur_page_num = new_page
                load_pdf_page(root,new_page)
                root.after(100)
                canvas.yview("moveto","0.0")
#                vbar.set(0.01,0.02)
                canvas.config(yscrollcommand=vbar.set(0.01,0.02))
#        '''
    # if scroll up
    elif event.num == 4 or event.delta > 0:
        print("scroll up")
        canvas.yview("scroll",-1,"units")
#        '''
        if vbar.get()[0] <= 0:
            if cur_page_num > 0:
                new_page = cur_page_num-1
                cur_page_num = new_page
                load_pdf_page(root,new_page)
                root.after(100)
                canvas.yview("moveto","1.0")
#                vbar.set(0.99,0.98)
                canvas.config(yscrollcommand=vbar.set(0.99,0.98))
#        '''

def mouse_wheel_preview(event):
    global canvas2
    if event.num == 5 or event.delta < 0 :
        canvas2.yview("scroll",1,"units")
    elif event.num == 4 or event.delta > 0:
        canvas2.yview("scroll",-1,"units")


def load_pdf_page(root, page_num = 2, dpi = 120):
    global cur_page_num
    global frame
    global canvas
    global doc
    global file_for_open, hbar, vbar
    cur_page_num = page_num
    rw = root.winfo_screenwidth()
    rh = root.winfo_screenheight()



    if frame != None:
        print("frame in globals")

    else:
        print("frame not in globals")
        frame = tkinter.Frame(root)
        frame.pack(side=LEFT, expand=True, fill=BOTH, pady=0, padx = 0)

    if canvas != None:
        print("canvas in globals")
#        canvas.destroy()
#        hbar.destroy()
#       vbar.destroy()
#       canvas = None
        '''
        canvas.destroy()
        canvas = tkinter.Canvas(frame, width = rw, height = rh)
        hbar = ttk.Scrollbar(frame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,expand=False,fill=X)
        hbar.config(command=canvas.xview)
        vbar = ttk.Scrollbar(frame,orient=VERTICAL)
        vbar.pack(side=RIGHT,expand=False,fill=Y)
        vbar.config(command=canvas.yview)
        '''
    else:
        canvas = tkinter.Canvas(frame, height = rh)
        hbar = ttk.Scrollbar(frame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,expand=False,fill=X)
        hbar.config(command=canvas.xview)
        global vbar
        vbar = ttk.Scrollbar(frame,orient=VERTICAL)
        vbar.pack(side=RIGHT,expand=False,fill=Y)
        vbar.config(command=canvas.yview)


    doc = fitz.Document(file_for_open)

    page = doc.load_page(page_num)

    pix = page.get_pixmap(dpi=dpi)

    mode = "RGBA" if pix.alpha else "RGB"
    pw = pix.width
    ph = pix.height
    img = Image.frombytes(mode, [pw, ph], pix.samples)
    global tkimg
    tkimg = ImageTk.PhotoImage(img)


    rw = root.winfo_width()
    rh = root.winfo_height()
    w = int(root.winfo_width()) - 300
    h = int(root.winfo_height()) - 300

#    print( pw )
#    print((lambda pw: w if pw >= w else pw)(pw))

    if canvas != None:
        canvas.config(scrollregion = (0,0,pw,ph))
#        canvas.config(scrollregion = (0,0,(lambda pw: w if pw >= w else pw)(pw),(lambda ph: h if ph>=h else ph)(ph)))
        canvas.config(height=h)
#        canvas.config(width=(lambda pw: w if pw >= w else pw)(pw),height=rh)
        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        canvas.create_image(int(pw/2), int(ph/2), image = tkimg)
        canvas.bind("<Button-4>",mouse_wheel)
        canvas.bind("<Button-5>",mouse_wheel)
        canvas.bind("<MouseWheel>",mouse_wheel)
        canvas.pack(side=LEFT,expand=True,fill=BOTH)



def load_pdf_preview(root, page_num = 2, dpi = 16):

    global frame2, frame3, canvas2, doc, file_for_open
    
    doc = fitz.Document(file_for_open)

    rw = root.winfo_screenwidth()
    rh = root.winfo_screenheight()

    if frame2 != None:
        print("frame2 in globals")
    #    frame2.pack_forget()
    #    frame2.destroy()
        frame2.pack_forget()
        frame2.destroy()
        frame2=ttk.Frame(root)
        frame2.config(width=200,height=frame2.winfo_height())
#        frame2.pack(side=RIGHT, expand=True, fill=Y)

    else:
        frame2=ttk.Frame(root)
        frame2.config(width=500,height=frame2.winfo_height())
#        frame2.pack(side=RIGHT, expand=True, fill=Y)

#    '''
    if canvas2 != None:
        print("canvas2 in globals")
        canvas2.destroy()
        canvas2 = tkinter.Canvas(frame2, bg="#dedede")
    else:
        canvas2 = tkinter.Canvas(frame2, bg="#dedede")


    #tkinter.Label(canvas2, text='Label', bg='green').pack(expand=None, fill=tkinter.Y)

    
    
    print(" :: %d" % int(frame2.winfo_height()))
    canvas2.config(width = 300, height = rh)

    if frame3 != None:
        frame3.pack_forget()
        frame3.destroy()
        frame3 = ttk.Frame(canvas2)
        frame3.bind(
            "<Configure>",
            lambda e: canvas2.configure(
                scrollregion=canvas2.bbox("all")
            )
        )
    else:
        frame3 = ttk.Frame(canvas2)
        frame3.bind(
            "<Configure>",
            lambda e: canvas2.configure(
                scrollregion=canvas2.bbox("all")
            )
        )



#    '''



    preview = []
    preview.clear()

#    print(doc.page_count)


    for i in range(0,doc.page_count):
        prev_page = doc.load_page(i)
        preview.append(prev_page.get_pixmap(dpi=dpi)) 


    counter = 0
    global img_ref
#    global but_ref

    img_ref = []
#    but_ref = []


    for prev_img in preview:
        prev_w = prev_img.width
        prev_h = prev_img.height
        mode = "RGBA" if prev_img.alpha else "RGB"

        preview_img = Image.frombytes(mode, [prev_w, prev_h], prev_img.samples)
        preview_tkimg = ImageTk.PhotoImage(preview_img)
        img_ref.append(preview_tkimg)
        but = ttk.Button(frame3,image=img_ref[counter], command=lambda root=root, counter=counter: load_pdf_page(root, page_num = counter)) #, relief = 'flat'
#        but.bind("<Button-4>",mouse_wheel_preview)
#        but.bind("<Button-5>",mouse_wheel_preview)
#        but.bind("<MouseWheel>",mouse_wheel_preview)
        but.pack()
#        but_ref.append(but)
        counter += 1

    frame3.update_idletasks()
    canvas2.update_idletasks()
    frame2.update_idletasks()

    canvas2.bind("<Button-4>", mouse_wheel_preview)
    canvas2.bind("<Button-5>", mouse_wheel_preview)
    canvas2.bind("<MouseWheel>", mouse_wheel_preview)
#    frame3.bind("<Button-4>", mouse_wheel_preview)
#    frame3.bind("<Button-5>", mouse_wheel_preview)


    frame3.pack(side=RIGHT, expand=True, fill=Y)

    canvas2.pack(side=LEFT, expand=True, fill=Y)

    canvas2.create_window((1,1), window=frame3,anchor="nw")

    frame2.pack(side=RIGHT, expand=False, fill=Y)

    vbar2 = ttk.Scrollbar(frame2,orient=VERTICAL,command=canvas2.yview)
    canvas2.config(yscrollcommand=vbar2.set)
    vbar2.pack(side=RIGHT, expand=True, fill="y")



img_ref = None
but_ref = None
but = None
tkimg = None
file_for_open = None
frame = None
canvas = None
frame2 = None
frame3 = None
canvas2 = None
doc = None
hbar = None
vbar = None

root = tkinter.Tk()
rw = root.winfo_screenwidth()
rh = root.winfo_screenheight()

root.geometry(f"{rw}x{rh}")
root.title("PDF viewer by sd")
add_menubar(root)
#root.bind("<Configure>",root.on_resize)

root.mainloop()
