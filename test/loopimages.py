from tkinter import *
from PIL import ImageTk, Image
import os

root = Tk()

f = open("ids.txt")
ids = []
apps = []
imgs = []
for line in f:
    line = line.rstrip("\n")
    line = line.split('-')
    ids.append(line[0])
    apps.append(line[1])
print(ids, apps)
f.close()

imgs = []
for i in range(7):
    ids.append(i+1)
    #Resize the Image using resize method
    img = Image.open(f"./icones/{ids[i]}.png")
    resized_image= img.resize((100,100), Image.Resampling.LANCZOS)

    imgs.append(ImageTk.PhotoImage(resized_image))
    lbl = Label(root, image=imgs[-1], background="#282c34", width=100, height=100)
    lbl.pack(fill = None, expand = 1, side=LEFT)


root.mainloop()
