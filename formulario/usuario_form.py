from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
import os

def usuarioForm():
    root = Toplevel()
    root.title("Usuarios")
    root.geometry("300x400+300+130")
    root.resizable(0, 0)
    root.iconbitmap("img/mitienda.ico")
    # ventana_menu.state("zoomed")#mazimizar ventana
    root.config(bg="white")
    root.config(cursor="hand2")
    # Variables
    nombre = StringVar()
    dni = StringVar()
    dir = StringVar()
    tel = StringVar()


    # Funcion Guardar
    def guardarUsuario():
        miConexion = sqlite3.connect("database.db")
        miCursor = miConexion.cursor()
        if nombre.get() == "":
            messagebox.showerror("ERROR", "Debes completar todos lo campos")
            root.deiconify()
        elif dni.get() == "":
            messagebox.showerror("ERROR", "Debes completar todos lo campos")
            root.deiconify()
        elif len(dni.get()) > 8 or len(dni.get()) < 8:
            messagebox.showerror("ERROR", "Debes ingresar un DNI sin puntos \nDebe tener 8 caracteres")
            root.deiconify()
        elif not dni.get().isdigit():
            messagebox.showerror("ERROR", "Ingresaste un DNI invalido")
            root.deiconify()
        elif dir.get() == "":
            messagebox.showerror("ERROR", "Debes completar todos lo campos")
            root.deiconify()
        elif tel.get() == "":
            messagebox.showerror("ERROR", "Debes completar todos lo campos")
            root.deiconify()
        elif not tel.get().isdigit():
            messagebox.showerror("ERROR", "Ingresaste un celular invalido")
            root.deiconify()
        elif len(tel.get()) > 10 or len(tel.get()) < 10:
            messagebox.showerror("ERROR", "Debes ingresar un número sin 0 y 15")
            root.deiconify()

        else:
            miCursor.execute("INSERT INTO usuario VALUES(NULL, '" + nombre.get() +
                             "','" + dni.get() +
                             "','" + dir.get() +
                             "','" + tel.get() +
                             "')")
            miConexion.commit()
            opcion = messagebox.askquestion("Felicidades!", " Registro Guardado\n¿Deseas ingresar uno nuevo?")
            if opcion == "yes":
                root.destroy()
                usuarioForm()
            else:
                root.destroy()
    # Fin funcion guardar

    # Titulo de ventana
    img_usuario = PhotoImage(file="img/equipo.png")
    Label(root, image=img_usuario, bg="white").place(x=30, y=10)
    Label(root, text="Registro de clientes", bg="white", font=16).place(x=85, y=10)

    # Campos de formulario
    Label(root, text="Nombre y Apellido", bg="white").place(x=10, y=80)
    entrada2 = Entry(root, width=25, textvariable=nombre).place(x=120, y=80)

    Label(root, text="DNI", bg="white").place(x=50, y=120)
    entrada3 = Entry(root, width=15, textvariable=dni).place(x=120, y=120)

    Label(root, text="Dirección", bg="white").place(x=30, y=160)
    entrada4 = Entry(root, width=25,textvariable=dir).place(x=120, y=160)

    Label(root, text="Telefono", bg="white").place(x=30, y=200)
    entrada5 = Entry(root, width=15,textvariable=tel).place(x=120, y=200)

    # Boton Guardar
    img_salvar = PhotoImage(file="img/salvar.png")
    Button(root, image=img_salvar, bg="white",command=guardarUsuario).place(x=114, y=270)

    root.mainloop()