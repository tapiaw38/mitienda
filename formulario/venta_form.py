from tkinter import *
from tkinter import messagebox, ttk
import os


def ventaForm():
    root = Toplevel()
    root.title("Ventas")
    root.geometry("300x500+300+130")
    root.resizable(0, 0)
    root.iconbitmap("img/mitienda.ico")
    # ventana_menu.state("zoomed")#mazimizar ventana
    root.config(bg="white")
    root.config(cursor="hand2")
    # Variables
    compra = StringVar()
    compra.set(0)

    # Funciones
    def guardar():
        if compra.get() == "1":
            root2 = Toplevel()
            root2.title("Venta por planilla")
            root2.geometry("300x200+600+430")
            root2.config(bg="white")
            root2.resizable(0, 0)
            root2.iconbitmap("img/mitienda.ico")
            # Variables
            abonar = StringVar()
            abonar.set(0)


            # update de datos

            img_planilla = PhotoImage(file="img/planilla.png")
            Label(root2, image=img_planilla, bg="white").place(x=35, y=5)
            Label(root2, text="Venta por planilla", bg="white", font=16).place(x=90, y=15)

            Label(root2, text="Ingrese DNI", bg="white").place(x=10, y=60)
            entrada5 = Entry(root2, width=15).place(x=90, y=60)
            ttk.Button(root2,text="Buscar").place(x=190,y=60)

            Label(root2,text="* Tapia Walter, Barrio Proreso",fg="blue",bg="white").place(x=20,y=90)

            Label(root2, text="A abonar $", bg="white").place(x=10, y=120)
            entrada6 = Entry(root2, width=10, textvariable=abonar).place(x=80, y=120)

            ttk.Button(root2, text="Confirmar").place(x=110,y=160)
            #Label(root2, text="* Compra exitosa ", fg="green", bg="white").place(x=10, y=160)

            root2.mainloop()


    # Busqueda
    Label(root,text="Ingresar Codigo",bg="white").place(x=10,y=30)
    entrada1 = Entry(root,width=15).place(x=120,y=30)
    img_busqueda = PhotoImage(file="img/buscar.png")
    Button(root,image=img_busqueda,bg="white").place(x=220,y=15)

    # Titulo de ventana
    img_rebaja = PhotoImage(file="img/rebaja.png")
    Label(root,image=img_rebaja,bg="white").place(x=30,y=80)
    Label(root,text="Producto a vender",bg="white",font=16).place(x=85,y=80)

    # Campos de formulario
    Label(root,text="Descripción",bg="white").place(x=10,y=130)
    entrada2 = Entry(root,width=30).place(x=80,y=130)

    Label(root,text="Color",bg="white").place(x=10,y=170)
    entrada3 = Entry(root,width=15).place(x=80,y=170)

    Label(root,text="Talle",bg="white").place(x=10,y=210)
    entrada4 = Entry(root,width=10).place(x=80,y=210)

    Label(root,text="Precio en $",bg="white").place(x=10,y=250)
    entrada5 = Entry(root,width=10).place(x=80,y=250)

    Label(root, text="Pago",bg="white").place(x=10,y=290)

    Radiobutton(root,text='Planilla',bg="white",variable=compra, value=1).place(x=80,y=290)
    Radiobutton(root,text='Contado',bg="white",variable=compra, value=0).place(x=160,y=290)

    # Boton Vender
    img_venta = PhotoImage(file="img/bolsa-compra.png")
    Button(root,image=img_venta,bg="white",command=guardar).place(x=114,y=355)


    root.mainloop()