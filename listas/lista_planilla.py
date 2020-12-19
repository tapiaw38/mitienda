from tkinter import *
from tkinter import messagebox, ttk
import os
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import webbrowser as wb
import itertools
from conexion import conexion_psql



def planillaList():
    root = Toplevel()
    root.title("Planillas")
    root.geometry("1050x410+100+130")
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
    consulta = StringVar()

    # Funcion pagar
    def pagar():
        idSelecionado = lista.item(lista.selection())['text']
        if idSelecionado == "":
            messagebox.showwarning("Atencion", "Debes seleccionar un registro para editarlo")
            root.deiconify()
        else:
            root2 = Toplevel()
            root2.title("Pagar")
            root2.geometry("300x200+450+250")
            root2.config(bg="white")
            root2.resizable(0, 0)
            root2.iconbitmap("img/mitienda.ico")
            # Variables
            abonar = IntVar()
            pago = IntVar()
            deuda = IntVar()
            abonar.set(0)

            # Funcion Actualiza
            def actualiza():
                pago_total = pago.get() + abonar.get()
                deuda_total = deuda.get() - abonar.get()
                if deuda_total < 0:
                    root2.destroy()
                    messagebox.showerror("ERROR", "Ingresaste un monto mayor a la deuda, intentalo de nuevo")
                else:
                    miConexion = conexion_psql()
                    miCursor = miConexion.cursor()
                    miCursor.execute("UPDATE venta SET pago='" + str(pago_total) +
                                     "', deuda='" + str(deuda_total) +
                                     "' WHERE id=" + str(idSelecionado))
                    miConexion.commit()
                    root2.destroy()
                    messagebox.showinfo("Felicidades!",
                                        "Pago realizado con exito")
                root.deiconify()

            img_pagar = PhotoImage(file="img/pagar.png")
            Label(root2, image=img_pagar, bg="white").place(x=35, y=5)
            Label(root2, text="Pago de cuenta", bg="white", font=16).place(x=90, y=15)

            cliente = Label(root2, fg="blue", bg="white", font=14)
            cliente.place(x=80, y=60)

            Label(root2, text="A abonar $", bg="white").place(x=80, y=100)
            entrada6 = Entry(root2, width=10, textvariable=abonar).place(x=150, y=100)

            ttk.Button(root2, text="Confirmar", command=actualiza).place(x=110, y=140)
            # Label(root2, text="* Compra exitosa ", fg="green", bg="white").place(x=10, y=160)

            # insertar datos
            miConexion = conexion_psql()
            miCursor = miConexion.cursor()
            miCursor.execute(
                "SELECT usuario.nombre, venta.pago, venta.deuda FROM venta INNER JOIN usuario ON "
                "venta.usuario = usuario.id WHERE venta.id=" + str(idSelecionado)
            )
            planillas = miCursor.fetchall()
            for planilla in planillas:
                pago.set(planilla[1])
                deuda.set(planilla[2])
                cliente.config(text="{}".format("** " + planilla[0] + " **"))
            miConexion.commit()

            root2.mainloop()

        # Funciones

    # Buscar Deudores
    def buscaDeudores():
        miConexion = conexion_psql()
        miCursor = miConexion.cursor()
        miCursor.execute(
            "SELECT venta.id, producto.codigo, usuario.nombre, usuario.dni, producto.descripcion, producto.color, producto.talla, producto.precio,"
            " to_char( venta.fecha , 'DD-MON-YYYY') AS fecha_formato, venta.pago, venta.deuda FROM venta INNER JOIN producto"
            " ON venta.producto = producto.id INNER JOIN usuario ON venta.usuario = usuario.id"
            " WHERE venta.venta=false AND venta.deuda > 0"
        )
        productos = miCursor.fetchall()
        x = lista.get_children()
        if x != "()":
            for i in x:
                lista.delete(i)

        data = [("COD", "DESCRIPCION", "PRECIO", "CLIENTE", "DEUDA", "FECHA")]
        suma = 0
        suma_deuda = 0
        suma_total = 0
        for producto in productos:
            suma += int(producto[7]) - int(producto[10])
            suma_deuda += int(producto[10])
            suma_total += int(producto[7])
            ventas.config(text="{}".format("** Ventas $" + str(suma) + " **"))
            deuda.config(text="{}".format("** Deuda $" + str(suma_deuda) + " **"))
            total.config(text="{}".format("** Total $" + str(suma_total) + " **"))
            lista.insert("", 0, text=str(producto[0]),
                         values=(
                             str(producto[1]), str(producto[2]), str(producto[3]), str(producto[4]),
                             str(producto[5]),
                             str(producto[6]),
                             str(producto[7]), str(producto[8]), str(producto[9]), str(producto[10])))

            data.append(
                (str(producto[1]), str(producto[4]), "$" + str(producto[7]), str(producto[2]),
                 "$" + str(producto[10]),
                 str(producto[8])))

            crear_pdf(data, suma, suma_deuda, suma_total)

    # Buscar por rango de fechas
    def busca_fechas():
        x = lista.get_children()
        if x != "()":
            for i in x:
                lista.delete(i)
        miConexion = conexion_psql()
        miCursor = miConexion.cursor()
        miCursor.execute(

            "SELECT venta.id, producto.codigo, usuario.nombre, usuario.dni, producto.descripcion, producto.color, producto.talla, producto.precio,"
            " to_char( venta.fecha , 'DD-MON-YYYY') AS fecha_formato, venta.pago, venta.deuda FROM venta INNER JOIN producto"
            " ON venta.producto = producto.id INNER JOIN usuario ON venta.usuario = usuario.id"
            " WHERE venta.venta=false AND venta.fecha BETWEEN " + "'" + f3.get() + "/" +
            f2.get() + "/" +
            f1.get() +
            "'" +
            " AND " +
            "'" +
            f6.get() + "/" +
            f5.get() + "/" +
            f4.get() +
            "'"
        )
        productos = miCursor.fetchall()
        data = [("COD", "DESCRIPCION", "PRECIO", "CLIENTE", "DEUDA", "FECHA")]
        suma = 0
        suma_deuda = 0
        suma_total = 0
        for producto in productos:
            suma += int(producto[7]) - int(producto[10])
            suma_deuda += int(producto[10])
            suma_total += int(producto[7])
            ventas.config(text="{}".format("** Ventas $" + str(suma) + " **"))
            deuda.config(text="{}".format("** Deuda $" + str(suma_deuda) + " **"))
            total.config(text="{}".format("** Total $" + str(suma_total) + " **"))
            lista.insert("", 0, text=str(producto[0]),
                         values=(
                             str(producto[1]), str(producto[2]), str(producto[3]), str(producto[4]),
                             str(producto[5]),
                             str(producto[6]),
                             str(producto[7]), str(producto[8]), str(producto[9]), str(producto[10])))

            data.append(
                (str(producto[1]), str(producto[4]), "$" + str(producto[7]), str(producto[2]),
                 "$" + str(producto[10]),
                 str(producto[8])))

            crear_pdf(data, suma, suma_deuda, suma_total)

    def grouper(iterable, n):
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args)

    def crear_pdf(data, suma, suma_deuda, suma_total):
        c = canvas.Canvas("Mi_Tienda.pdf", pagesize=A4)
        w, h = A4
        c.drawString(50, h - 30, "Mi Tienda, Reporte de Ventas")
        c.drawString(50, h - 50, "Ventas ${}".format(suma))
        c.drawString(150, h - 50, "Deudas ${}".format(suma_deuda))
        c.drawString(250, h - 50, "Total ${}".format(suma_total))
        max_rows_per_page = 45
        # Margin.
        x_offset = 50
        y_offset = 70
        # Space between rows.
        padding = 15

        xlist = [x + x_offset for x in [0, 40, 180, 230, 380, 430, 510]]
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
                "SELECT venta.id, producto.codigo, usuario.nombre, usuario.dni, producto.descripcion, producto.color, producto.talla, producto.precio,"
                " to_char( venta.fecha , 'DD-MON-YYYY') AS fecha_formato, venta.pago, venta.deuda FROM venta INNER JOIN producto"
                " ON venta.producto = producto.id INNER JOIN usuario ON venta.usuario = usuario.id"
                " WHERE venta.venta=false AND producto.codigo='" + consulta.get().upper() + "'"
            )
            if len(consulta.get()) < 4:
                messagebox.showwarning("ERROR", "Debes ingresar un articulo correcto")
                root.deiconify()
            else:
                productos = miCursor.fetchall()
                x = lista.get_children()
                if x != "()":
                    for i in x:
                        lista.delete(i)
                data = [("COD", "DESCRIPCION", "PRECIO", "CLIENTE", "DEUDA", "FECHA")]
                suma = 0
                suma_deuda = 0
                suma_total = 0
                for producto in productos:
                    suma += int(producto[7]) - int(producto[10])
                    suma_deuda += int(producto[10])
                    suma_total += int(producto[7])
                    ventas.config(text="{}".format("** Ventas $" + str(suma) + " **"))
                    deuda.config(text="{}".format("** Deuda $" + str(suma_deuda) + " **"))
                    total.config(text="{}".format("** Total $" + str(suma_total) + " **"))
                    lista.insert("", 0, text=str(producto[0]),
                                 values=(
                                     str(producto[1]), str(producto[2]), str(producto[3]), str(producto[4]),
                                     str(producto[5]),
                                     str(producto[6]),
                                     str(producto[7]), str(producto[8]), str(producto[9]), str(producto[10])))

                    data.append(
                        (str(producto[1]), str(producto[4]), "$" + str(producto[7]), str(producto[2]),
                         "$" + str(producto[10]),
                         str(producto[8])))

                    crear_pdf(data, suma, suma_deuda, suma_total)

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
    Label(root, text="Ingrese DNI", bg="white").place(x=15, y=30)
    entrada5 = Entry(root, width=15, textvariable=consulta).place(x=90, y=30)
    ttk.Button(root, text="Buscar", command=buscaDatos).place(x=190, y=30)

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
    # Boton Pagar
    img_pagar = PhotoImage(file="img/pagar.png")
    Button(root, image=img_pagar, bg="white", command=pagar).place(x=600, y=30)
    # Boton Actualiza
    img_actualiza = PhotoImage(file="img/actualizar.png")
    Button(root, image=img_actualiza, bg="white", command=actualizaLista).place(x=650, y=30)
    # Boton Deudores
    img_falta = PhotoImage(file="img/falta.png")
    Button(root, image=img_falta, bg="white", command=buscaDeudores).place(x=700, y=30)
    # Imagen pdf
    img_txt = PhotoImage(file="img/pdf_2.png")
    Button(root, image=img_txt, bg="white", command=abrir_pdf).place(x=750, y=30)
    # Label ventas
    ventas = Label(root, bg="white", fg="blue", font=12)
    ventas.place(x=10, y=385)
    # Label deuda
    deuda = Label(root, bg="white", fg="red", font=12)
    deuda.place(x=310, y=385)
    # Label Total
    total = Label(root, bg="white", fg="green", font=12)
    total.place(x=610, y=385)

    # Lista
    root.config(bg="white")
    root.config(cursor="hand2")
    lista = ttk.Treeview(root, columns=("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"), height=14)
    lista.place(x=18, y=80)
    lista.heading("#0", text="id")
    lista.column("#0", minwidth=0, width=0)
    lista.heading("A", text="Codigo")
    lista.column("A", minwidth=0, width=80)

    lista.heading("B", text="Nombre y Apellido")
    lista.column("B", minwidth=0, width=150)
    lista.heading("C", text="DNI")
    lista.column("C", minwidth=0, width=50)
    lista.heading("D", text="Descripción")
    lista.heading("E", text="Color")
    lista.column("E", minwidth=0, width=100)
    lista.heading("F", text="Talla")
    lista.column("F", minwidth=0, width=50)
    lista.heading("G", text="Precio")
    lista.column("G", minwidth=0, width=70)
    lista.heading("H", text="Fecha")
    lista.column("H", minwidth=0, width=100)
    lista.heading("I", text="Pago")
    lista.column("I", minwidth=0, width=70)
    lista.heading("J", text="Deuda")
    lista.column("J", minwidth=0, width=70)
    # Lista de productos vendidos
    def insertar_datos():
        miConexion = conexion_psql()
        miCursor = miConexion.cursor()
        miCursor.execute(
        "SELECT venta.id, producto.codigo, usuario.nombre, usuario.dni, producto.descripcion, producto.color, producto.talla, producto.precio,"
        " to_char( venta.fecha , 'DD-MON-YYYY') AS fecha_formato, venta.pago, venta.deuda FROM venta INNER JOIN producto"
        " ON venta.producto = producto.id INNER JOIN usuario ON venta.usuario = usuario.id"
        " WHERE venta.venta=false")
        productos = miCursor.fetchall()
        data = [("COD", "DESCRIPCION", "PRECIO", "CLIENTE", "DEUDA", "FECHA")]
        suma = 0
        suma_deuda = 0
        suma_total = 0
        for producto in productos:
            suma += int(producto[7]) - int(producto[10])
            suma_deuda += int(producto[10])
            suma_total += int(producto[7])
            ventas.config(text="{}".format("** Ventas $" + str(suma) + " **"))
            deuda.config(text="{}".format("** Deuda $" + str(suma_deuda) + " **"))
            total.config(text="{}".format("** Total $" + str(suma_total) + " **"))
            lista.insert("", 0, text=str(producto[0]),
                         values=(
                         str(producto[1]), str(producto[2]), str(producto[3]), str(producto[4]), str(producto[5]),
                         str(producto[6]),
                         str(producto[7]), str(producto[8]), str(producto[9]), str(producto[10])))

            data.append(
                (str(producto[1]), str(producto[4]), "$" + str(producto[7]), str(producto[2]), "$" + str(producto[10]),
                 str(producto[8])))
            crear_pdf(data, suma, suma_deuda, suma_total)

    insertar_datos()

    root.mainloop()

