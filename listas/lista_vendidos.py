from tkinter import *
from tkinter import messagebox, ttk
import os

def vendidosList():
    root = Toplevel()
    root.title("Ventas")
    root.geometry("820x400+300+130")
    root.resizable(0, 0)
    root.iconbitmap("img/mitienda.ico")
    # ventana_menu.state("zoomed")#mazimizar ventana

    # Busqueda
    Label(root, text="Ingrese codigo", bg="white").place(x=15, y=30)
    entrada5 = Entry(root, width=15).place(x=100, y=30)
    ttk.Button(root, text="Buscar").place(x=200, y=30)

    # Busqueda por fechas
    Label(root, text="* Busqueda por fechas *",bg="white",fg="blue").place(x=340, y=0)

    # Desde
    Label(root,text="Desde",bg="white").place(x=310,y=30)
    fecha1 = Entry(root, width=3)
    fecha1.place(x=350, y=30)
    Label(root,text="-",bg="white").place(x=370,y=30)
    fecha2 = Entry(root, width=3)
    fecha2.place(x=380, y=30)
    Label(root, text="-",bg="white").place(x=400, y=30)
    fecha3 = Entry(root, width=5)
    fecha3.place(x=410, y=30)

    # Hasta
    Label(root,text="Hasta",bg="white").place(x=310,y=50)
    fecha4 = Entry(root, width=3)
    fecha4.place(x=350, y=50)
    Label(root,text="-",bg="white").place(x=370,y=50)
    fecha5 = Entry(root, width=3)
    fecha5.place(x=380, y=50)
    Label(root, text="-",bg="white").place(x=400, y=50)
    fecha6 = Entry(root, width=5)
    fecha6.place(x=410, y=50)

    #Boron buscar fecha
    img_buscar = PhotoImage(file="img/deuda.png")
    Button(root, image=img_buscar, bg="white").place(x=450, y=30)

    # Lista
    root.config(bg="white")
    root.config(cursor="hand2")
    lista =ttk.Treeview(root ,columns=("A" ,"B" ,"C" ,"D","E") ,height=14)
    lista.place(x=18 ,y=80)
    lista.heading("#0" ,text="Codigo")
    lista.column("#0" ,minwidth=0 ,width=100)
    lista.heading("A" ,text="Descripción")
    lista.heading("B" ,text="Precio")
    lista.column("B" ,minwidth=0 ,width=130)
    lista.heading("C" ,text="Color")
    lista.heading("D" ,text="Talla")
    lista.column("D" ,minwidth=0 ,width=50)
    lista.heading("E" ,text="Fecha")
    lista.column("E" ,minwidth=0 ,width=100)




    root.mainloop()