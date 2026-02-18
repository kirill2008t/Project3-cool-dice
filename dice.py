import random
from tkinter import *

root = Tk()
root.title("cooldice")

def roll_dice():
    dice_value = random.randint(1, 6)
    label.config(text=f"Выпало {dice_value}")


label = Label(root, text="Нажмите 'бросить', чтобы кинуть кубик", font=('Helvetica', 18))
label.pack(pady=20)


button = Button(root, text='Бросить!', command=roll_dice, bg="#4CAF50", fg="white", font=('Helvetica', 14), width=15)
button.pack(pady=10)


root.mainloop()