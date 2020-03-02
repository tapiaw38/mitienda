from tkinter import *
from tkinter import messagebox, ttk
import os

def productoForm():
    root = Toplevel()
    root.title("Productos")
    root.geometry("300x400+300+130")
    root.resizable(0, 0)
    root.iconbitmap("img/mitienda.ico")
    # ventana_menu.state("zoomed")#mazimizar ventana
    root.config(bg="white")
    root.config(cursor="hand2")
    # Variables
    compra = StringVar()
    compra.set(0)

    # Titulo de ventana
    img_producto = PhotoImage(file="img/producto_nuevo.png")
    Label(root, image=img_producto, bg="white").place(x=30, y=10)
    Label(root, text="Ingreso de Productos", bg="white", font=16).place(x=85, y=10)

    Label(root,text="** Anota este codigo a tu producto **", bg="white", fg="blue",font=12).place(x=20,y=50)
    Label(root,text="ART000",fg="green", bg="white",font=12).place(x=120,y=90)

    # Campos de formulario
    Label(root, text="Descripción", bg="white").place(x=10, y=130)
    entrada2 = Entry(root, width=30).place(x=80, y=130)

    Label(root, text="Color", bg="white").place(x=10, y=170)
    entrada3 = Entry(root, width=15).place(x=80, y=170)

    Label(root, text="Talle", bg="white").place(x=10, y=210)
    entrada4 = Entry(root, width=10).place(x=80, y=210)

    Label(root, text="Precio en $", bg="white").place(x=10, y=250)
    entrada5 = Entry(root, width=10).place(x=80, y=250)

    # Boton Guardar
    img_caja = PhotoImage(file="img/caja-abierta.png")
    Button(root, image=img_caja, bg="white").place(x=114, y=300)

    root.mainloop()