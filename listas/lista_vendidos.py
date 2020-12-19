import datetime
from datetime import datetime
from tkinter import *
from tkinter import messagebox, ttk
import os
import sqlite3
import itertools
from random import randint
from statistics import mean
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import webbrowser as wb
from conexion import conexion_psql



def vendidosList():
    root = Toplevel()
    root.title("Ventas")
    root.geometry("820x415+300+130")
    root.resizable(0, 0)
    root.iconbitmap("img/mitienda.ico")
    # ventana_menu.state("zoomed")#mazimizar ventana
    # Variables
    f1 = StringVar()
    f2 = StringVar()
    f3 = StringVar()
    f4 = StringVar()
    f5 = StringVar()
    f6 = StringVar()
    consulta_codigo = StringVar()

    # Funciones

    # Buscar por rango de fechas
    def busca_fechas():
        x = lista.get_children()
        if x != "()":
            for i in x:
                lista.delete(i)
        miConexion = conexion_psql()
        miCursor = miConexion.cursor()
        miCursor.execute(
            "SELECT venta.id, producto.codigo, producto.descripcion, producto.precio, producto.color, producto.talla,"
            " to_char( venta.fecha , 'DD-MON-YYYY') AS fecha_formato FROM venta INNER JOIN producto"
            " ON venta.producto = producto.id WHERE venta.venta=true"
            " AND venta.fecha BETWEEN " + "'" + f3.get() + "/" +
            f2.get() + "/" +
            f1.get() +
            "'" +
            " AND " +
            "'" +
            f6.get() + "/" +
            f5.get() + "/" +
            f4.get() +
            "'")
        productos = miCursor.fetchall()
        data = [("COD", "DESCRIPCION", "PRECIO", "COLOR", "TALLA", "FECHA")]
        suma = 0
        for producto in productos:
            suma += int(producto[3])
            ventas.config(text="{}".format("** Dinero en ventas $" + str(suma) + " **"))
            lista.insert("", 0, text=str(producto[0]),
                         values=(
                             str(producto[1]), str(producto[2]), str(producto[3]), str(producto[4]),
                             str(producto[5]), str(producto[6])))

            data.append((str(producto[1]), str(producto[2]), str(producto[3]), str(producto[4]), str(producto[5]),
                         str(producto[6])))
            crear_pdf(data, suma)

    def grouper(iterable, n):
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args)

    def crear_pdf(data, suma):
        c = canvas.Canvas("Mi_Tienda.pdf", pagesize=A4)
        w, h = A4
        c.drawString(50, h - 30, "Mi Tienda, Reporte de Ventas")
        c.drawString(50, h - 50, "Dinero en ventas ${}".format(suma))
        max_rows_per_page = 45
        # Margin.
        x_offset = 50
        y_offset = 70
        # Space between rows.
        padding = 15

        xlist = [x + x_offset for x in [0, 50, 180, 230, 360, 430, 510]]
        ylist = [h - y_offset - i * padding for i in range(max_rows_per_page + 1)]

        for rows in grouper(data, max_rows_per_page):
            rows = tuple(filter(bool, rows))
            c.grid(xlist, ylist[:len(rows) + 1])
            for y, row in zip(ylist[:-1], rows):
                for x, cell in zip(xlist, row):
                    c.drawString(x + 2, y - padding + 3, str(cell))
            c.showPage()
        c.save()

    def abrir_pdf():
        wb.open_new("Mi_tienda.pdf")


    # Funcion Buscar Producto
    def buscaDatos():
        try:
            miConexion = conexion_psql()
            miCursor = miConexion.cursor()
            miCursor.execute(
                "SELECT venta.id, producto.codigo, producto.descripcion, producto.precio, producto.color, producto.talla,"
                " to_char( venta.fecha , 'DD-MON-YYYY') AS fecha_formato FROM venta INNER JOIN producto"
                " ON venta.producto = producto.id WHERE venta.venta=true AND producto.codigo='" + consulta_codigo.get().upper() + "'")
            if len(consulta_codigo.get()) < 4:
                messagebox.showwarning("ERROR", "Debes ingresar un articulo correcto")
                root.deiconify()
            else:
                productos = miCursor.fetchall()
                x = lista.get_children()
                if x != "()":
                    for i in x:
                        lista.delete(i)
                data = [("COD", "DESCRIPCION", "PRECIO", "COLOR", "TALLA", "FECHA")]
                suma = 0
                for producto in productos:
                    suma += int(producto[3])
                    ventas.config(text="{}".format("** Dinero en ventas $" + str(suma) + " **"))
                    lista.insert("", 0, text=str(producto[0]),
                                 values=(
                                     str(producto[1]), str(producto[2]), str(producto[3]), str(producto[4]),
                                     str(producto[5]), str(producto[6])))
                    data.append(
                        (str(producto[1]), str(producto[2]), str(producto[3]), str(producto[4]), str(producto[5]),
                         str(producto[6])))
                    crear_pdf(data, suma)

        except:
            messagebox.showwarning("ERROR", "Busqueda invalida, intentalo de nuevo")
            root.deiconify()

    # Funcion Actualiza
    def actualizaLista():
        x = lista.get_children()
        if x != "()":
            for i in x:
                lista.delete(i)
        insertar_datos()

    # Busqueda
    Label(root, text="Ingrese codigo", bg="white").place(x=15, y=30)
    entrada5 = Entry(root, width=15, textvariable=consulta_codigo).place(x=100, y=30)
    ttk.Button(root, text="Buscar", command=buscaDatos).place(x=200, y=30)

    # Busqueda por fechas
    Label(root, text="* Busqueda por fechas *", bg="white", fg="blue").place(x=340, y=0)

    # Desde
    Label(root, text="Desde", bg="white").place(x=310, y=30)
    fecha1 = Entry(root, width=3, textvariable=f1)
    fecha1.place(x=350, y=30)
    Label(root, text="-", bg="white").place(x=370, y=30)
    fecha2 = Entry(root, width=3, textvariable=f2)
    fecha2.place(x=380, y=30)
    Label(root, text="-", bg="white").place(x=400, y=30)
    fecha3 = Entry(root, width=5, textvariable=f3)
    fecha3.place(x=410, y=30)

    # Hasta
    Label(root, text="Hasta", bg="white").place(x=310, y=50)
    fecha4 = Entry(root, width=3, textvariable=f4)
    fecha4.place(x=350, y=50)
    Label(root, text="-", bg="white").place(x=370, y=50)
    fecha5 = Entry(root, width=3, textvariable=f5)
    fecha5.place(x=380, y=50)
    Label(root, text="-", bg="white").place(x=400, y=50)
    fecha6 = Entry(root, width=5, textvariable=f6)
    fecha6.place(x=410, y=50)

    # Boron buscar fecha
    img_buscar = PhotoImage(file="img/deuda.png")
    Button(root, image=img_buscar, bg="white", command=busca_fechas).place(x=450, y=30)
    img_actualiza = PhotoImage(file="img/actualizar.png")
    Button(root, image=img_actualiza, bg="white", command=actualizaLista).place(x=500, y=30)
    img_txt = PhotoImage(file="img/pdf_2.png")
    Button(root, image=img_txt, bg="white", command=abrir_pdf).place(x=550, y=30)
    # Muestra cantidad de dinero
    ventas = Label(root, bg="white", fg="blue", font=12)
    ventas.place(x=10, y=385)

    # Lista
    root.config(bg="white")
    root.config(cursor="hand2")
    lista = ttk.Treeview(root, columns=("A", "B", "C", "D", "E", "F"), height=14)
    lista.place(x=18, y=80)
    lista.heading("#0", text="id")
    lista.column("#0", minwidth=0, width=0)
    lista.heading("A", text="Codigo")
    lista.column("A", minwidth=0, width=100)
    lista.heading("B", text="Descripción")
    lista.column("B", minwidth=0, width=230)
    lista.heading("C", text="Precio")
    lista.column("C", minwidth=0, width=80)
    lista.heading("D", text="Color")
    lista.heading("E", text="Talla")
    lista.column("E", minwidth=0, width=50)
    lista.heading("F", text="Fecha")
    lista.column("F", minwidth=0, width=120)
    # Lista de productos vendidos
    def insertar_datos():
        miConexion = conexion_psql()
        miCursor = miConexion.cursor()
        miCursor.execute(
            "SELECT venta.id, producto.codigo, producto.descripcion, producto.precio, producto.color, producto.talla,"
            " to_char( venta.fecha , 'DD-MON-YYYY') AS fecha_formato FROM venta INNER JOIN producto"
            " ON venta.producto = producto.id WHERE venta.venta=true")
        productos = miCursor.fetchall()

        data = [("COD", "DESCRIPCION", "PRECIO", "COLOR", "TALLA", "FECHA")]
        suma = 0
        for producto in productos:
            suma += int(producto[3])
            ventas.config(text="{}".format("** Dinero en ventas $" + str(suma) + " **"))
            lista.insert("", 0, text=str(producto[0]),
                         values=(
                             str(producto[1]), str(producto[2]), str(producto[3]), str(producto[4]),
                             str(producto[5]),
                             str(producto[6])))
            data.append((str(producto[1]), str(producto[2]), "$"+str(producto[3]), str(producto[4]), str(producto[5]),
                         (producto[6])))

            crear_pdf(data, suma)
    insertar_datos()

    root.mainloop()
