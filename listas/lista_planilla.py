from tkinter import *
from tkinter import messagebox, ttk
import os

def planillaList():
    root = Toplevel()
    root.title("Planillas")
    root.geometry("1050x400+100+130")
    root.resizable(0, 0)
    root.iconbitmap("img/mitienda.ico")
    # ventana_menu.state("zoomed")#mazimizar ventana

    # Funcion pagar
    def pagar():
        root2 = Toplevel()
        root2.title("Pagar")
        root2.geometry("300x200+450+250")
        root2.config(bg="white")
        root2.resizable(0, 0)
        root2.iconbitmap("img/mitienda.ico")
        # Variables
        abonar = StringVar()
        abonar.set(0)

        # update de pagos

        img_pagar = PhotoImage(file="img/pagar.png")
        Label(root2, image=img_pagar, bg="white").place(x=35, y=5)
        Label(root2, text="Pago de cuenta", bg="white", font=16).place(x=90, y=15)

        Label(root2, text="** Tapia Walter, 35153294 **", fg="blue", bg="white",font=14).place(x=40, y=60)

        Label(root2, text="A abonar $", bg="white").place(x=80, y=100)
        entrada6 = Entry(root2, width=10, textvariable=abonar).place(x=150, y=100)

        ttk.Button(root2, text="Confirmar").place(x=110, y=140)
        # Label(root2, text="* Compra exitosa ", fg="green", bg="white").place(x=10, y=160)

        root2.mainloop()






    # Busqueda
    Label(root, text="Ingrese DNI", bg="white").place(x=15, y=30)
    entrada5 = Entry(root, width=15).place(x=90, y=30)
    ttk.Button(root, text="Buscar").place(x=190, y=30)

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
    #Boton Pagar
    img_pagar = PhotoImage(file="img/pagar.png")
    Button(root, image=img_pagar, bg="white",command=pagar).place(x=600, y=30)
    #Boton Eliminar
    img_eliminar = PhotoImage(file="img/eliminar.png")
    Button(root, image=img_eliminar, bg="white").place(x=650, y=30)
    #Boton Deudores
    img_falta = PhotoImage(file="img/falta.png")
    Button(root, image=img_falta, bg="white").place(x=700, y=30)

    # Lista
    root.config(bg="white")
    root.config(cursor="hand2")
    lista =ttk.Treeview(root ,columns=("A" ,"B" ,"C" ,"D","E","F","G","H","I","J") ,height=14)
    lista.place(x=18 ,y=80)
    lista.heading("#0" ,text="Nombre y apellido")
    lista.column("#0" ,minwidth=0 ,width=150)
    lista.heading("A" ,text="DNI")
    lista.column("A" ,minwidth=0 ,width=50)
    lista.heading("B" ,text="Codigo")
    lista.column("B" ,minwidth=0 ,width=80)
    lista.heading("C" ,text="Descripción")
    lista.heading("D" ,text="Color")
    lista.column("D" ,minwidth=0 ,width=100)
    lista.heading("E" ,text="Talla")
    lista.column("E" ,minwidth=0 ,width=50)
    lista.heading("F" ,text="Precio")
    lista.column("F" ,minwidth=0 ,width=70)
    lista.heading("G" ,text="Fecha")
    lista.column("G" ,minwidth=0 ,width=100)
    lista.heading("H" ,text="Pago")
    lista.column("H" ,minwidth=0 ,width=70)
    lista.heading("I" ,text="Deuda")
    lista.column("I" ,minwidth=0 ,width=70)
    lista.heading("J" ,text="Total + i ")
    lista.column("J" ,minwidth=0 ,width=70)


    root.mainloop()