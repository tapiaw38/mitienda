from tkinter import *
from tkinter import messagebox, ttk
import os
import sqlite3
from listas.lista_stock import stockList

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
        desc = StringVar()
        color = StringVar()
        talle = StringVar()
        precio = StringVar()



        # Guardar Producto
        def guardarProducto():
            miConexion = sqlite3.connect("database.db")
            miCursor = miConexion.cursor()
            if desc.get() == "":
                messagebox.showerror("ERROR", "Debes completar todos lo campos")
                root.deiconify()
            elif color.get() == "":
                messagebox.showerror("ERROR", "Debes completar todos lo campos")
                root.deiconify()
            elif talle.get() == "":
                messagebox.showerror("ERROR", "Debes completar todos lo campos")
                root.deiconify()
            elif precio.get() == "":
                messagebox.showerror("ERROR", "Debes completar todos lo campos")
                root.deiconify()
            elif not precio.get().isdigit():
                messagebox.showerror("ERROR", "Ingresaste un monto invalido")
                root.deiconify()
            else:
                miCursor.execute("INSERT INTO productos VALUES(NULL, "
                                 "'" + desc.get().upper() +
                                 "','" + precio.get() +
                                 "','" + color.get().upper() +
                                 "','" + talle.get().upper() +
                                 "','" + "1" +
                                 "')")
                miConexion.commit()
                opcion = messagebox.askquestion("Felicidades!", " Registro Guardado\n¿Deseas ingresar uno nuevo?")
                if opcion == "yes":
                    root.destroy()
                    productoForm()
                else:
                    root.destroy()
                    stockList()



        # Titulo de ventana
        img_producto = PhotoImage(file="img/producto_nuevo.png")
        Label(root, image=img_producto, bg="white").place(x=30, y=10)
        Label(root, text="Ingreso de Productos", bg="white", font=16).place(x=85, y=10)

        Label(root,text="** Anota este codigo a tu producto **", bg="white", fg="blue",font=12).place(x=20,y=50)
        codigo_producto=Label(root,text="ART1",fg="green", bg="white",font=12)
        codigo_producto.place(x=120,y=90)

        # Leer id y codigo de producto
        miConexion = sqlite3.connect("database.db")
        miCursor = miConexion.cursor()
        miCursor.execute("SELECT * FROM productos")
        productos = miCursor.fetchall()
        for producto in productos:
            codigo_producto.config(text="{}".format("ART-"+str(producto[0] + 1)))
            codigo = "ART"+str(producto[0] + 1)
        miConexion.commit()

        # Campos de formulario
        Label(root, text="Descripción", bg="white").place(x=10, y=130)
        entrada2 = Entry(root, width=30, textvariable=desc).place(x=80, y=130)

        Label(root, text="Color", bg="white").place(x=10, y=170)
        entrada3 = Entry(root, width=15, textvariable=color).place(x=80, y=170)

        Label(root, text="Talle", bg="white").place(x=10, y=210)
        entrada4 = Entry(root, width=10,textvariable=talle).place(x=80, y=210)

        Label(root, text="Precio en $", bg="white").place(x=10, y=250)
        entrada5 = Entry(root, width=10,textvariable=precio).place(x=80, y=250)

        # Boton Guardar
        img_caja = PhotoImage(file="img/caja-abierta.png")
        Button(root, image=img_caja, bg="white", command=guardarProducto).place(x=114, y=300)

        root.mainloop()
