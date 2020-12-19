import datetime
from tkinter import *
from tkinter import messagebox, ttk
import os
import sqlite3
from conexion import conexion_psql


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

    art = IntVar()
    art_E = Entry(root, textvariable=art)
    compra = BooleanVar()
    compra.set(True)
    consulta = StringVar()
    desc = StringVar()
    color = StringVar()
    talle = StringVar()
    precio = StringVar()
    fecha_hoy = StringVar()
    usuario_id = IntVar()

    # Funciones
    def buscar_product():
        try:

            global consulta_codigo
            consulta_codigo = consulta.get().upper()
            miConexion = conexion_psql()
            miCursor = miConexion.cursor()
            miCursor.execute("SELECT * FROM producto WHERE codigo=" + "'" + consulta_codigo + "'" + " AND existe=true ")
            productos = miCursor.fetchall()
            for producto in productos:
                art.set(producto[0])
                desc.set(producto[2])
                precio.set(producto[3])
                color.set(producto[4])
                talle.set(producto[5])
            miConexion.commit()
        except:
            messagebox.showwarning("ERROR", "Busqueda invalida, intentalo de nuevo")
            root.deiconify()

    def guardarVenta():
        if compra.get() == True:
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
                miConexion = conexion_psql()
                miCursor = miConexion.cursor()
                miCursor.execute("UPDATE producto SET existe='" + "false" +
                                 "' WHERE codigo=" + "'" +consulta_codigo + "'")
                #miConexion.commit()

                # Guardar en ventas
                hoy = datetime.datetime.today()
                fecha_hoy.set(hoy.strftime('%Y/%m/%d'))
                print(art.get())

                miCursor.execute("INSERT INTO venta(producto, venta, fecha) VALUES(" +
                                 "'" + str(art.get()) +
                                 "','" + str(compra.get()) +
                                 "','" + fecha_hoy.get() +
                                 "')")
                miConexion.commit()
                opcion = messagebox.askquestion("Mis ventas", " Producto vendido!\n¿Quieres seguir vendiendo?")
                if opcion == "yes":
                    root.destroy()
                    ventaForm()
                else:
                    root.destroy()


        elif compra.get() == False and desc.get() != "":
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
                    miConexion = conexion_psql()
                    miCursor = miConexion.cursor()
                    miCursor.execute("SELECT ID, nombre, dni, dir, tel FROM usuario WHERE dni=" + "'" + consulta_dni.get() + "'")
                    if len(consulta_dni.get()) > 8 or len(consulta_dni.get()) < 8:
                        messagebox.showwarning("ERROR", "Debes ingresar el DNI sin puntos")
                        root.deiconify()
                    else:
                        usuarios = miCursor.fetchall()
                        for usuario in usuarios:
                            nombre.set(usuario[1])
                            usuario_id.set(usuario[0])
                        miConexion.commit()

                except:
                    messagebox.showwarning("ERROR", "Busqueda invalida, intentalo de nuevo")
                    root.deiconify()

            def vender_planilla():

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
                    miConexion = conexion_psql()
                    miCursor = miConexion.cursor()
                    miCursor.execute("UPDATE producto SET existe='" + "false" +
                                     "' WHERE codigo=" + "'" +consulta_codigo + "'")

                    # Guardar en ventas
                    hoy = datetime.datetime.today()
                    fecha_hoy.set(hoy.strftime('%Y/%m/%d'))
                    deuda = float(precio.get()) - float(abonar.get())
                    interes = 1
                    miCursor.execute("INSERT INTO venta(producto, venta, pago, interes, deuda, fecha, usuario) VALUES("
                                     "'" + str(art.get()) +
                                     "','" + str(compra.get()) +
                                     "','" + str(abonar.get()) +
                                     "','" + str(interes) +
                                     "','" + str(deuda) +
                                     "','" + fecha_hoy.get() +
                                     "','" + str(usuario_id.get()) +
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

    Radiobutton(root, text='Planilla', bg="white", variable=compra, value=False).place(x=80, y=290)
    Radiobutton(root, text='Contado', bg="white", variable=compra, value=True).place(x=160, y=290)

    # Boton Vender
    img_venta = PhotoImage(file="img/bolsa-compra.png")
    Button(root, image=img_venta, bg="white", command=guardarVenta).place(x=114, y=355)

    root.mainloop()

