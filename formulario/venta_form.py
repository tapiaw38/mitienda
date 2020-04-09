import datetime
from tkinter import *
from tkinter import messagebox, ttk
import os
import sqlite3


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

    art = StringVar()
    art_E = Entry(root, textvariable=art)
    compra = StringVar()
    compra.set(0)
    consulta = StringVar()
    desc = StringVar()
    color = StringVar()
    talle = StringVar()
    precio = StringVar()

    # Funciones
    def buscar_product():
        try:
            texto = consulta.get().upper()
            global consulta_id
            consulta_id = texto.lstrip("ART-")
            miConexion = sqlite3.connect("database.db")
            miCursor = miConexion.cursor()
            miCursor.execute("SELECT * FROM productos WHERE ID=" + consulta_id + " AND existe=1 ")
            productos = miCursor.fetchall()
            for producto in productos:
                art.set(producto[0])
                desc.set(producto[1])
                precio.set(producto[2])
                color.set(producto[3])
                talle.set(producto[4])
            miConexion.commit()
        except:
            messagebox.showwarning("ERROR", "Busqueda invalida, intentalo de nuevo")
            root.deiconify()

    def guardarVenta():
        if compra.get() == "0":
            miConexion = sqlite3.connect("database.db")
            miCursor = miConexion.cursor()
            if desc.get() == "":
                messagebox.showerror("ERROR", "Debes ingresar el cofigo de un producto")
                root.deiconify()
            elif color.get() == "":
                messagebox.showerror("ERROR", "Debes ingresar el cofigo de un producto")
                root.deiconify()
            elif talle.get() == "":
                messagebox.showerror("ERROR", "Debes ingresar el cofigo de un productos")
                root.deiconify()
            elif precio.get() == "":
                messagebox.showerror("ERROR", "Debes ingresar el cofigo de un producto")
                root.deiconify()
            else:
                # Actualiza el estado de producto
                miConexion = sqlite3.connect("database.db")
                miCursor = miConexion.cursor()
                miCursor.execute("UPDATE productos SET existe='" + "0" +
                                 "' WHERE ID=" + str(consulta_id))
                miConexion.commit()

                # Guardar en ventas
                hoy = datetime.datetime.today()
                fecha_hoy = hoy.strftime("%Y-%m-%d")
                articulo = "ART-" + art.get()
                miCursor.execute("INSERT INTO venta VALUES(NULL, "
                                 "'" + str(articulo) +
                                 "','" + desc.get().upper() +
                                 "','" + precio.get() +
                                 "','" + color.get().upper() +
                                 "','" + talle.get().upper() +
                                 "','" + compra.get() +
                                 "','" + "" +
                                 "','" + "" +
                                 "','" + "" +
                                 "','" + "" +
                                 "','" + "" +
                                 "','" + fecha_hoy +
                                 "')")
                miConexion.commit()
                opcion = messagebox.askquestion("Mis ventas", " Producto vendido!\n¿Quieres seguir vendiendo?")
                if opcion == "yes":
                    root.destroy()
                    ventaForm()
                else:
                    root.destroy()


        elif compra.get() == "1" and desc.get() != "":
            root2 = Toplevel()
            root2.title("Venta por planilla")
            root2.geometry("300x200+600+430")
            root2.config(bg="white")
            root2.resizable(0, 0)
            root2.iconbitmap("img/mitienda.ico")
            # Variables
            consulta_dni = StringVar()
            nombre = StringVar()
            dni = StringVar()
            abonar = StringVar()
            abonar.set(0)

            # Buscar persona
            def buscar_persona():
                try:
                    miConexion = sqlite3.connect("database.db")
                    miCursor = miConexion.cursor()
                    miCursor.execute("SELECT ID, nombre, dni, dir, tel FROM usuario WHERE dni=" + consulta_dni.get())
                    if len(consulta_dni.get()) > 8 or len(consulta_dni.get()) < 8:
                        messagebox.showwarning("ERROR", "Debes ingresar el DNI sin puntos")
                        root.deiconify()
                    else:
                        usuarios = miCursor.fetchall()
                        for usuario in usuarios:
                            nombre.set(usuario[1])
                        miConexion.commit()

                except:
                    messagebox.showwarning("ERROR", "Busqueda invalida, intentalo de nuevo")
                    root.deiconify()

            def vender_planilla():
                miConexion = sqlite3.connect("database.db")
                miCursor = miConexion.cursor()
                if nombre.get() == "":
                    messagebox.showerror("ERROR", "Debes ingresar un cliente")
                    root2.deiconify()
                elif abonar.get() == "":
                    messagebox.showerror("ERROR", "Debes ingresar un monto ejem: '0'")
                    root2.deiconify()
                elif not abonar.get().isdigit():
                    messagebox.showerror("ERROR", "Ingresaste un monto invalido")
                    root2.deiconify()
                else:
                    # Actualiza el estado de producto
                    miConexion = sqlite3.connect("database.db")
                    miCursor = miConexion.cursor()
                    miCursor.execute("UPDATE productos SET existe='" + "0" +
                                     "' WHERE ID=" + str(consulta_id))
                    miConexion.commit()

                    # Guardar en ventas
                    hoy = str(datetime.datetime.now())
                    articulo = "ART-" + art.get()
                    deuda = float(precio.get()) - float(abonar.get())
                    interes = 1
                    miCursor.execute("INSERT INTO venta VALUES(NULL, "
                                     "'" + str(articulo) +
                                     "','" + desc.get().upper() +
                                     "','" + precio.get() +
                                     "','" + color.get().upper() +
                                     "','" + talle.get().upper() +
                                     "','" + compra.get() +
                                     "','" + nombre.get() +
                                     "','" + consulta_dni.get() +
                                     "','" + abonar.get() +
                                     "','" + str(interes) +
                                     "','" + str(deuda) +
                                     "','" + hoy +
                                     "')")
                    miConexion.commit()
                    root2.destroy()
                    opcion = messagebox.askquestion("Mis ventas", " Producto vendido!\n¿Quieres seguir vendiendo?")
                    if opcion == "yes":
                        root.destroy()
                        ventaForm()
                    else:
                        root.destroy()

            # update de datos
            img_planilla = PhotoImage(file="img/planilla.png")
            Label(root2, image=img_planilla, bg="white").place(x=35, y=5)
            Label(root2, text="Venta por planilla", bg="white", font=16).place(x=90, y=15)

            Label(root2, text="Ingrese DNI", bg="white").place(x=10, y=60)
            entrada5 = Entry(root2, width=15, textvariable=consulta_dni).place(x=90, y=60)
            ttk.Button(root2, text="Buscar", command=buscar_persona).place(x=190, y=60)

            entrada6 = Entry(root2, textvariable=nombre).place(x=90, y=90)

            Label(root2, text="A abonar $", bg="white").place(x=20, y=120)
            entrada6 = Entry(root2, width=10, textvariable=abonar).place(x=90, y=120)

            ttk.Button(root2, text="Confirmar", command=vender_planilla).place(x=110, y=160)
            # Label(root2, text="* Compra exitosa ", fg="green", bg="white").place(x=10, y=160)

            root2.mainloop()
        elif desc.get() == "":
            messagebox.showerror("Error", "Debes ingresar el cofigo de un producto")
            root.deiconify()

    # Busqueda
    Label(root, text="Ingresar Codigo", bg="white").place(x=10, y=30)
    entrada1 = Entry(root, width=15, textvariable=consulta).place(x=120, y=30)
    img_busqueda = PhotoImage(file="img/buscar.png")
    Button(root, image=img_busqueda, bg="white", command=buscar_product).place(x=220, y=15)

    # Titulo de ventana
    img_rebaja = PhotoImage(file="img/rebaja.png")
    Label(root, image=img_rebaja, bg="white").place(x=30, y=80)
    Label(root, text="Producto a vender", bg="white", font=16).place(x=85, y=80)

    # Campos de formulario
    Label(root, text="Descripción", bg="white").place(x=10, y=130)
    entrada2 = Entry(root, width=30, textvariable=desc).place(x=80, y=130)

    Label(root, text="Color", bg="white").place(x=10, y=170)
    entrada3 = Entry(root, width=15, textvariable=color).place(x=80, y=170)

    Label(root, text="Talle", bg="white").place(x=10, y=210)
    entrada4 = Entry(root, width=10, textvariable=talle).place(x=80, y=210)

    Label(root, text="Precio en $", bg="white").place(x=10, y=250)
    entrada5 = Entry(root, width=10, textvariable=precio).place(x=80, y=250)

    Label(root, text="Pago", bg="white").place(x=10, y=290)

    Radiobutton(root, text='Planilla', bg="white", variable=compra, value=1).place(x=80, y=290)
    Radiobutton(root, text='Contado', bg="white", variable=compra, value=0).place(x=160, y=290)

    # Boton Vender
    img_venta = PhotoImage(file="img/bolsa-compra.png")
    Button(root, image=img_venta, bg="white", command=guardarVenta).place(x=114, y=355)

    root.mainloop()

