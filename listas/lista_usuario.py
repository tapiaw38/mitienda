from tkinter import *
from tkinter import messagebox, ttk
from formulario.usuario_form import usuarioForm
import os
import sqlite3
def usuariosList():
    root = Toplevel()
    root.title("Usuarios")
    root.geometry("750x400+300+130")
    root.resizable(0, 0)
    root.iconbitmap("img/mitienda.ico")
    # ventana_menu.state("zoomed")#mazimizar ventana

    # Variables
    consulta = StringVar()


    # Funcion Actualiza Datos
    def actualizaLista():
        x=lista.get_children()
        if x !="()":
            for i in x:
                lista.delete(i)
        miConexion = sqlite3.connect("database.db")
        miCursor = miConexion.cursor()
        miCursor.execute("SELECT ID, nombre, dni, dir, tel FROM usuario")
        usuarios = miCursor.fetchall()
        for usuario in usuarios:
            lista.insert("", 0, text=usuario[0],
                         values=(str(usuario[1]), str(usuario[2]), str(usuario[3]), str(usuario[4])))

    # Funcion Buscar Usuarios
    def buscaDatos():
        try:
            miConexion = sqlite3.connect("database.db")
            miCursor = miConexion.cursor()
            miCursor.execute("SELECT ID, nombre, dni, dir, tel FROM usuario WHERE dni=" + consulta.get())
            if len(consulta.get())>8 or len(consulta.get())<8:
                messagebox.showwarning("ERROR", "Debes ingresar el DNI sin puntos")
                root.deiconify()
            elif not consulta.get().isdigit():
                messagebox.showerror("ERROR", "Ingresaste un DNI invalido")
                root.deiconify()
            elif consulta.get() == "":
                messagebox.showerror("ERROR", "No ingresaste una busqueda")
                root.deiconify()
            else:
                usuarios = miCursor.fetchall()
                x=lista.get_children()
                if x !="()":
                    for i in x:
                        lista.delete(i)
                for usuario in usuarios:
                    lista.insert("", 0, text=usuario[0],
                                 values=(str(usuario[1]), str(usuario[2]), str(usuario[3]), str(usuario[4])))
        except:
            messagebox.showwarning("ERROR", "Busqueda invalida, intentalo de nuevo")
            root.deiconify()


    # Funcion Eliminar Datos
    def eliminUsuario():
        idSelecionado = lista.item(lista.selection())['text']
        if idSelecionado == "":
            messagebox.showwarning("Atencion", "Debes seleccionar un registro para eliminar")
            root.deiconify()
        else:
            opcion = messagebox.askquestion("Eliminar", "Estas seguro?")
            if opcion == "yes":
                miConexion = sqlite3.connect("database.db")
                miCursor = miConexion.cursor()
                miCursor.execute("DELETE FROM usuario WHERE ID=" + str(idSelecionado))
                miCursor.fetchall()
                miConexion.commit()
                messagebox.showinfo("Eliminar",
                                       " Registro Eliminado")
                root.deiconify()
            else:
                root.deiconify()

    # Funcion Editar datos
    def editarUsuario():
        idSelecionado = lista.item(lista.selection())['text']
        if idSelecionado == "":
            messagebox.showwarning("Atencion", "Debes seleccionar un registro para editarlo")
            root.deiconify()
        else:
            root2 = Toplevel()
            root2.title("Editar")
            root2.geometry("300x400+300+130")
            root2.resizable(0, 0)
            root2.iconbitmap("img/mitienda.ico")
            # ventana_menu.state("zoomed")#mazimizar ventana
            root2.config(bg="white")
            root2.config(cursor="hand2")
            # Variables
            nombre = StringVar()
            dni = StringVar()
            dir = StringVar()
            tel = StringVar()

            miConexion = sqlite3.connect("database.db")
            miCursor = miConexion.cursor()
            miCursor.execute("SELECT ID, nombre, dni, dir, tel FROM usuario WHERE ID=" + str(idSelecionado))
            usuarios = miCursor.fetchall()
            for usuario in usuarios:
                nombre.set(usuario[1])
                dni.set(usuario[2])
                dir.set(usuario[3])
                tel.set(usuario[4])
            miConexion.commit()

            # Funcion Actualiza
            def actualiza():
                miConexion = sqlite3.connect("database.db")
                miCursor = miConexion.cursor()
                miCursor.execute("UPDATE usuario SET nombre='" + nombre.get() +
                                 "', dni='" + dni.get() +
                                 "', dir='" + dir.get() +
                                 "', tel='" + tel.get() +
                                 "' WHERE ID=" + str(idSelecionado))
                miConexion.commit()
                root2.destroy()
                opcion = messagebox.askquestion("Felicidades!",
                                                " Registro Modificado\n¿Deseas volver a editar?")
                if opcion == "yes":
                    root2.destroy()
                    root.deiconify()
                    editarUsuario()
                else:
                    root2.destroy()
                    root.deiconify()


            # Titulo de ventana
            img_usuario = PhotoImage(file="img/equipo.png")
            Label(root2, image=img_usuario, bg="white").place(x=30, y=10)
            Label(root2, text="Edición de clientes", bg="white", font=16).place(x=85, y=10)

            # Campos de formulario
            Label(root2, text="Nombre y Apellido", bg="white").place(x=10, y=80)
            entrada2 = Entry(root2, width=25, textvariable=nombre).place(x=120, y=80)

            Label(root2, text="DNI", bg="white").place(x=50, y=120)
            entrada3 = Entry(root2, width=15, textvariable=dni).place(x=120, y=120)

            Label(root2, text="Dirección", bg="white").place(x=30, y=160)
            entrada4 = Entry(root2, width=25, textvariable=dir).place(x=120, y=160)

            Label(root2, text="Telefono", bg="white").place(x=30, y=200)
            entrada5 = Entry(root2, width=15, textvariable=tel).place(x=120, y=200)

            # Boton Guardar
            img_salvar = PhotoImage(file="img/actualiza.png")
            Button(root2, image=img_salvar, bg="white", command=actualiza).place(x=114, y=270)

            root2.mainloop()

    # Busqueda
    Label(root, text="Ingrese DNI", bg="white").place(x=15, y=30)
    entrada5 = Entry(root, width=15, textvariable=consulta).place(x=90, y=30)
    ttk.Button(root, text="Buscar", command=buscaDatos).place(x=190, y=30)
    # Botones
    img_editar = PhotoImage(file="img/editar.png")
    Button(root, image=img_editar, bg="white",command=editarUsuario).place(x=300, y=25)

    img_eliminar = PhotoImage(file="img/eliminar.png")
    Button(root, image=img_eliminar, bg="white",command=eliminUsuario).place(x=350, y=25)

    img_actualiza = PhotoImage(file="img/actualizar.png")
    Button(root, image=img_actualiza, bg="white", command=actualizaLista).place(x=400, y=25)

    img_agregar = PhotoImage(file="img/agregar-usuario.png")
    Button(root, image=img_agregar, bg="white", command=usuarioForm).place(x=450, y=25)

    # Lista
    root.config(bg="white")
    root.config(cursor="hand2")
    lista =ttk.Treeview(root ,columns=("A" ,"B" ,"C" ,"D") ,height=14)
    lista.place(x=18 ,y=80)
    lista.heading("#0" ,text="#")
    lista.column("#0" ,minwidth=0 ,width=50)
    lista.heading("A" ,text="Cliente")
    lista.heading("B" ,text="DNI")
    lista.column("B" ,minwidth=0 ,width=130)
    lista.heading("C" ,text="Dirección")
    lista.heading("D" ,text="Teléfono")
    lista.column("D" ,minwidth=0 ,width=130)

    # Lista de Usuarios Cargar datos en lista
    miConexion = sqlite3.connect("database.db")
    miCursor = miConexion.cursor()
    miCursor.execute("SELECT ID, nombre, dni, dir, tel FROM usuario")
    usuarios = miCursor.fetchall()
    for usuario in usuarios:
        lista.insert("", 0, text=usuario[0],
                     values=(str(usuario[1]), str(usuario[2]), str(usuario[3]), str(usuario[4])))


    root.mainloop()