from tkinter import *
from tkinter import messagebox, ttk
import os
import sqlite3

def stockList():
    root = Toplevel()
    root.title("Stock")
    root.geometry("750x400+300+130")
    root.resizable(0, 0)
    root.iconbitmap("img/mitienda.ico")
    # ventana_menu.state("zoomed")#mazimizar ventana
    # Variable
    consulta = StringVar()

    # Funcion Buscar Producto
    def buscaDatos():
        try:
            texto = consulta.get().upper()
            consulta_id = texto.lstrip("ART-")
            print(consulta_id)
            miConexion = sqlite3.connect("database.db")
            miCursor = miConexion.cursor()
            miCursor.execute("SELECT * FROM productos WHERE ID=" + consulta_id + " AND existe=1 ")
            if len(consulta.get()) < 4:
                messagebox.showwarning("ERROR", "Debes ingresar un articulo correcto")
                root.deiconify()

            else:
                productos = miCursor.fetchall()
                x = lista.get_children()
                if x != "()":
                    for i in x:
                        lista.delete(i)
                for producto in productos:
                    lista.insert("", 0, text=str(producto[0]),
                                 values=(
                                 "ART-" + str(producto[0]), str(producto[1]), str(producto[2]), str(producto[3]),
                                 str(producto[4])))
        except:
            messagebox.showwarning("ERROR", "Busqueda invalida, intentalo de nuevo")
            root.deiconify()

    # Funcion Actualiza
    def actualizaLista():
        x = lista.get_children()
        if x != "()":
            for i in x:
                lista.delete(i)
        miConexion = sqlite3.connect("database.db")
        miCursor = miConexion.cursor()
        miCursor.execute("SELECT * FROM productos  WHERE existe=1")
        productos = miCursor.fetchall()
        for producto in productos:
            lista.insert("", 0, text=str(producto[0]),
                         values=("ART-" + str(producto[0]), str(producto[1]), str(producto[2]), str(producto[3]),
                                 str(producto[4])))

    # Funcion Eliminar Datos

    def eliminaProducto():
        idSelecionado = lista.item(lista.selection())['text']
        if idSelecionado == "":
            messagebox.showwarning("Atencion", "Debes seleccionar un registro para eliminar")
            root.deiconify()
        else:
            opcion = messagebox.askquestion("Eliminar", "Estas seguro de eliminar este registro?")
            if opcion == "yes":
                miCursor.execute("UPDATE productos SET existe=0 WHERE ID=" + str(idSelecionado))
                miConexion.commit()
                messagebox.showinfo("Eliminar",
                                    " Registro Eliminado")
                root.deiconify()
            else:
                root.deiconify()

    """
    def eliminaProducto():
        idSelecionado = lista.item(lista.selection())['text']
        if idSelecionado == "":
            messagebox.showwarning("Atencion", "Debes seleccionar un registro para eliminar")
            root.deiconify()
        else:
            opcion = messagebox.askquestion("Eliminar", "Estas seguro de eliminar este registro?")
            if opcion == "yes":
                miConexion = sqlite3.connect("database.db")
                miCursor = miConexion.cursor()
                miCursor.execute("DELETE FROM productos WHERE ID=" + str(idSelecionado))
                miCursor.fetchall()
                miConexion.commit()
                messagebox.showinfo("Eliminar",
                                    " Registro Eliminado")
                root.deiconify()
            else:
                root.deiconify()
    
    """
    # Editar Producto
    def editarProducto():
        idSelecionado = lista.item(lista.selection())['text']
        if idSelecionado == "":
            messagebox.showwarning("Atencion", "Debes seleccionar un registro para editarlo")
            root.deiconify()
        else:
            root2 = Toplevel()
            root2.title("Productos")
            root2.geometry("300x400+300+130")
            root2.resizable(0, 0)
            root2.iconbitmap("img/mitienda.ico")
            # ventana_menu.state("zoomed")#mazimizar ventana
            root2.config(bg="white")
            root2.config(cursor="hand2")
            # Variables

            desc = StringVar()
            color = StringVar()
            talle = StringVar()
            precio = StringVar()

            # Insertar Datos
            miConexion = sqlite3.connect("database.db")
            miCursor = miConexion.cursor()
            miCursor.execute("SELECT * FROM productos WHERE ID=" + str(idSelecionado))
            productos = miCursor.fetchall()
            for producto in productos:
                desc.set(producto[1])
                precio.set(producto[2])
                color.set(producto[3])
                talle.set(producto[4])
            miConexion.commit()

            # Funcion Actualiza
            def actualiza():
                miConexion = sqlite3.connect("database.db")
                miCursor = miConexion.cursor()
                if desc.get() == "":
                    messagebox.showerror("ERROR", "Debes completar todos lo campos")
                    root2.deiconify()
                elif color.get() == "":
                    messagebox.showerror("ERROR", "Debes completar todos lo campos")
                    root2.deiconify()
                elif talle.get() == "":
                    messagebox.showerror("ERROR", "Debes completar todos lo campos")
                    root2.deiconify()
                elif precio.get() == "":
                    messagebox.showerror("ERROR", "Debes completar todos lo campos")
                    root2.deiconify()
                else:
                    miCursor.execute("UPDATE productos SET descripcion='" + desc.get().upper() +
                                     "', precio='" + precio.get() +
                                     "', color='" + color.get().upper() +
                                     "', talla='" + talle.get().upper() +
                                     "' WHERE ID=" + str(idSelecionado))
                    miConexion.commit()
                    root2.destroy()
                    messagebox.showinfo("Felicidades!"," Registro Modificado")
                    root.deiconify()

            # Titulo de ventana
            img_producto = PhotoImage(file="img/producto_nuevo.png")
            Label(root2, image=img_producto, bg="white").place(x=30, y=10)
            Label(root2, text="Editar un Producto", bg="white", font=16).place(x=85, y=10)

            Label(root2, text="** Este es el codigo de tu producto **", bg="white", fg="green", font=12).place(x=15,
                                                                                                               y=50)
            codigo_producto = Label(root2, text="ART1", fg="green", bg="white", font=12)
            codigo_producto.place(x=120, y=90)

            # Leer id y codigo de producto
            miConexion = sqlite3.connect("database.db")
            miCursor = miConexion.cursor()
            miCursor.execute("SELECT * FROM productos WHERE ID=" + str(idSelecionado))
            productos = miCursor.fetchall()
            for producto in productos:
                codigo_producto.config(text="{}".format("ART-" + str(producto[0])))


            # Campos de formulario
            Label(root2, text="Descripción", bg="white").place(x=10, y=130)
            entrada2 = Entry(root2, width=30, textvariable=desc).place(x=80, y=130)

            Label(root2, text="Color", bg="white").place(x=10, y=170)
            entrada3 = Entry(root2, width=15, textvariable=color).place(x=80, y=170)

            Label(root2, text="Talle", bg="white").place(x=10, y=210)
            entrada4 = Entry(root2, width=10, textvariable=talle).place(x=80, y=210)

            Label(root2, text="Precio en $", bg="white").place(x=10, y=250)
            entrada5 = Entry(root2, width=10, textvariable=precio).place(x=80, y=250)

            # Boton Guardar
            img_caja = PhotoImage(file="img/actualiza.png")
            Button(root2, image=img_caja, bg="white", command=actualiza).place(x=114, y=300)

            root.mainloop()

    # Busqueda
    Label(root, text="Ingrese codigo", bg="white").place(x=15, y=30)
    entrada5 = Entry(root, width=15, textvariable=consulta).place(x=100, y=30)
    ttk.Button(root, text="Buscar", command=buscaDatos).place(x=200, y=30)
    # Botones
    img_editar = PhotoImage(file="img/editar.png")
    Button(root, image=img_editar, bg="white", command=editarProducto).place(x=300, y=25)

    img_actualiza = PhotoImage(file="img/actualizar.png")
    Button(root, image=img_actualiza, bg="white", command=actualizaLista).place(x=350, y=25)

    img_eliminar = PhotoImage(file="img/eliminar.png")
    Button(root, image=img_eliminar, bg="white",command=eliminaProducto).place(x=400, y=25)

    img_pdf = PhotoImage(file="img/pdf_2.png")
    Button(root, image=img_pdf, bg="white").place(x=450, y=25)

    # Lista
    root.config(bg="white")
    root.config(cursor="hand2")
    lista = ttk.Treeview(root, columns=("A", "B", "C", "D", "E"), height=14)
    lista.place(x=18, y=80)
    lista.heading("#0", text="#")
    lista.column("#0", minwidth=0, width=0)
    lista.heading("A", text="codigo")
    lista.column("A", minwidth=0, width=70)
    lista.heading("B", text="Descripción")
    lista.column("B", minwidth=0, width=260)
    lista.heading("C", text="Precio")
    lista.column("C", minwidth=0, width=130)
    lista.heading("D", text="Color")
    lista.heading("E", text="Talla")
    lista.column("E", minwidth=0, width=50)

    # Lista de Stock
    miConexion = sqlite3.connect("database.db")
    miCursor = miConexion.cursor()
    miCursor.execute("SELECT * FROM productos  WHERE existe=1")
    productos = miCursor.fetchall()
    for producto in productos:
        lista.insert("", 0, text=str(producto[0]),
                     values=(
                     "ART-" + str(producto[0]), str(producto[1]), str(producto[2]), str(producto[3]), str(producto[4])))

    root.mainloop()