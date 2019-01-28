from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import filedialog
from tkinter import StringVar
from tkinter import END
from tkinter import E
from tkinter import W
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import messagebox
from tkinter import INSERT
from tkinter import Menu
from tkinter import BooleanVar
import base64
import binascii
import imghdr


def select_file():
    filename = filedialog.askopenfilename()
    if filename is "": return
    filepath_txt.configure(state="normal")
    filepath_txt.delete(0, END)
    filepath_txt.insert(0, filename)
    filepath_txt.configure(state="readonly")
    convert_btn.configure(state="normal")
    savefile_btn.configure(state="disabled")


def convert():
    filename = filepath_txt.get()
    try:
        with open(filename, "rb") as targetFile:
            encodedFile = base64.b64encode(targetFile.read())
            output_panel.configure(state="normal")
            output_panel.delete(1.0, END)
            output_panel.insert(INSERT, encodedFile)
            output_panel.configure(state="disabled")
    except:
        messagebox.showerror("Error", "No file exists")
    convert_btn.configure(state="disabled")
    savefile_btn.configure(state="normal")


def save_file():
    f = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
    if f is None: return
    try:
        f.write(output_panel.get(1.0, END))
        f.close()
    except:
        messagebox.showerror("Error", "Error during file write")
        f.close()


def show_decode():
    if not decode_button.get(): 
        decode_button.set(True)
        return
    encode_button.set(False)
    toolbar.pack_forget()
    treeframe.pack_forget()
    decode_toolbar.pack(side="top", fill="x")
    decode_treeframe.pack(side="bottom", fill="both", expand=True)


def show_encode():
    if not encode_button.get(): 
        encode_button.set(True)
        return
    decode_button.set(False)
    decode_toolbar.pack_forget()
    decode_treeframe.pack_forget()
    toolbar.pack(side="top", fill="x")
    treeframe.pack(side="bottom", fill="both", expand=True)


def load_file():
    filepath = filedialog.askopenfilename()
    if filepath is "": return
    try:
        with open(filepath, "r") as targetFile:
            encodedFile = targetFile.read()
            filepreview_panel.configure(state="normal")
            filepreview_panel.delete(1.0, END)
            filepreview_panel.insert(INSERT, encodedFile)
            filepreview_panel.configure(state="disabled")  
            decodeto_btn.configure(state="normal")
    except UnicodeDecodeError:
        messagebox.showerror("Error", "System expects a text file containing base64 string")
    except:
        messagebox.showerror("Error", "No file exists")
 
    
def decode_and_save_file():
    fileContent = filepreview_panel.get(1.0, END)

    try:
        decoded_fileContent = base64.b64decode(fileContent)
    except binascii.Error:
        messagebox.showerror("Error", "Not a valid base64 input")

    # TODO: automatically find out what is the extension

    f = filedialog.asksaveasfile(mode="wb")
    if f is None: return
    try:
        f.write(decoded_fileContent)
        f.close()
    except:
        messagebox.showerror("Error", "Error during file write")
        f.close()


window = Tk()
window.title("Base64 File Converter")
window.geometry("480x300")

# ---------- Sample Menu code
menu = Menu(window)
encodeDecodeMenu = Menu(menu, tearoff=0)
encode_button = BooleanVar()
encode_button.set(True)
decode_button = BooleanVar()
encodeDecodeMenu.add_checkbutton(label="Encode Base64", variable=encode_button, command=show_encode)
encodeDecodeMenu.add_checkbutton(label="Decode Base64", variable=decode_button, command=show_decode)
menu.add_cascade(label="File", menu=encodeDecodeMenu)
window.config(menu=menu)

#----------- Define Tabs
# tab_control = ttk.Notebook(window)
# encode_tab = ttk.Frame(tab_control)
# decode_tab = ttk.Frame(tab_control)
# tab_control.add(encode_tab, text="Encode Base64")
# tab_control.add(decode_tab, text="Decode Base64")

# lbl1 = Label(encode_tab, text="label1")
# lbl1.grid(column=0, row=0)
# lbl2 = Label(decode_tab, text="label2")
# lbl2.grid(column=0, row=0)

# tab_control.pack(expand=1, fill="both")

#------------ Encode Frame
toolbar = ttk.Frame(window)
treeframe = ttk.Frame(window)

toolbar.pack(side="top", fill="x")
treeframe.pack(side="bottom", fill="both", expand=True)

default_txt = StringVar(toolbar, value="Select the file to convert to base64..")
filepath_txt = Entry(toolbar, width=30, state="readonly", textvariable=default_txt)

selectfile_btn = Button(toolbar, text="Select File", command=select_file)
convert_btn = Button(toolbar, text="Convert", state="disabled", command=convert)
savefile_btn = Button(toolbar, text="Save File", state="disabled", command=save_file)
filepath_txt.pack(side="left")
selectfile_btn.pack(side="left")
convert_btn.pack(side="left")
savefile_btn.pack(side="left")

output_panel = scrolledtext.ScrolledText(treeframe, width=55, height=10, state="disabled")
output_panel.pack(side="top", fill="both", expand=True)

#------------ Decode Frame
decode_toolbar = ttk.Frame(window)
decode_treeframe = ttk.Frame(window)

load_btn = Button(decode_toolbar, text="Load File", command=load_file)
load_btn.pack(side="left")
decodeto_btn = Button(decode_toolbar, text="Decode as", state="disabled", command=decode_and_save_file)
decodeto_btn.pack(side="left")
filepreview_panel = scrolledtext.ScrolledText(decode_treeframe, width=55, height=10, state="disabled")
filepreview_panel.pack(side="top", fill="both", expand=True)

window.mainloop()