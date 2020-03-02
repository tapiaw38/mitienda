from tkinter import *
from tkinter import messagebox, ttk
import os

def stockList():
    root = Toplevel()
    root.title("Stock")
    root.geometry("750x400+300+130")
    root.resizable(0, 0)
    root.iconbitmap("img/mitienda.ico")
    # ventana_menu.state("zoomed")#mazimizar ventana

    # Busqueda
    Label(root, text="Ingrese codigo", bg="white").place(x=15, y=30)
    entrada5 = Entry(root, width=15).place(x=100, y=30)
    ttk.Button(root, text="Buscar").place(x=200, y=30)
    # Botones
    img_editar = PhotoImage(file="img/editar.png")
    Button(root, image=img_editar, bg="white").place(x=300, y=25)

    img_eliminar = PhotoImage(file="img/eliminar.png")
    Button(root, image=img_eliminar, bg="white").place(x=350, y=25)

    # Lista
    root.config(bg="white")
    root.config(cursor="hand2")
    lista =ttk.Treeview(root ,columns=("A" ,"B" ,"C" ,"D") ,height=14)
    lista.place(x=18 ,y=80)
    lista.heading("#0" ,text="Codigo")
    lista.column("#0" ,minwidth=0 ,width=100)
    lista.heading("A" ,text="Descripción")
    lista.heading("B" ,text="Precio")
    lista.column("B" ,minwidth=0 ,width=130)
    lista.heading("C" ,text="Color")
    lista.heading("D" ,text="Talla")
    lista.column("D" ,minwidth=0 ,width=50)



    root.mainloop()