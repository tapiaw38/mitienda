from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
# Importaciones de paquetes
from formulario.venta_form import ventaForm
from formulario.producto_form import productoForm
from formulario.usuario_form import usuarioForm
from listas.lista_usuario import usuariosList
from listas.lista_stock import stockList
from listas.lista_vendidos import vendidosList
from listas.lista_planilla import planillaList
from calc import calc
from conexion import conexion_psql

# configuracion de la raiz de la ventana
ventana_menu = Tk()
ventana_menu.title("Mi Tienda")
ventana_menu.geometry("620x750+250+30")
ventana_menu.resizable(0, 0)
ventana_menu.iconbitmap("img/mitienda.ico")
# ventana_menu.state("zoomed")#mazimizar ventana
ventana_menu.config(bg="white")
ventana_menu.config(cursor="hand2")

# introducimos una imagen y titulo
miImagen = PhotoImage(file="img/mitienda.png")
Label(ventana_menu, image=miImagen, bg="white").place(x=0, y=50)

# Integro Frame
frame = Frame(ventana_menu)
frame.config(width=620,height=60)
frame.config(bg="black")
frame.place(x=0,y=670)
#Label(frame, text="Tienda de Ropa Nombre Tienda \nDe Nombre Persona - Direción del Local", fg="white", bg="black", font=("Monotype Corsiva", 14)).place(
#    x=160, y=0)

# funciones internas


def clave():
    root2 = Toplevel()
    root2.title("Ingresar clave de producto")
    root2.geometry("300x180+450+250")
    root2.config(bg="white")
    root2.resizable(0, 0)
    root2.iconbitmap("img/mitienda.ico")
    #variables

    ingresar = StringVar()
    def abrir():
        global contador
        miConexion = sqlite3.connect("data.db")
        miCursor = miConexion.cursor()
        miCursor.execute("SELECT * FROM pass")
        clave = miCursor.fetchall()
        for i in clave:
            if i[0] == ingresar.get() and 0 == i[1]:
                messagebox.showinfo("Mi Tienda","Bienvenido a Mi Tienda!")
                crear_db(root2)
                miConexion = sqlite3.connect("data.db")
                miCursor = miConexion.cursor()
                miCursor.execute("UPDATE pass SET cont=1")
                miConexion.commit()

            elif i[0] == ingresar.get() and i[1] > 0:
                messagebox.showerror("Error", "Esta clave ya esta en uso\nConsigue una bitcode@gmail.com")
            else:
                messagebox.showerror("Error","Introduce una clave valida")
                root2.deiconify()

    img_pagar = PhotoImage(file="img/candado.png")
    Label(root2, image=img_pagar, bg="white").place(x=35, y=5)
    Label(root2, text="Clave de Producto", bg="white", font=16).place(x=90, y=15)
    entrada6 = Entry(root2, width=30, show="*",justify="center",textvariable=ingresar)
    entrada6.place(x=60, y=60)
    entrada6.focus()

    ttk.Button(root2, text="Confirmar",command=abrir).place(x=110, y=100)
    root2.mainloop()


# Crear tabla producto
def crear_db(root2):
    try:
        bd = conexion_psql()
        cursor = bd.cursor()
        tablas = [

            "CREATE TABLE IF NOT EXISTS producto("
                "id integer NOT NULL DEFAULT nextval('producto_id_seq'::regclass),"
                "codigo character varying(100) COLLATE pg_catalog.'default' NOT NULL,"
                "descripcion character varying(150) COLLATE pg_catalog.'default',"
                "precio real NOT NULL,"
                "color character varying(50) COLLATE pg_catalog.'default',"
                "talla character varying(20) COLLATE pg_catalog.'default',"
                "existe boolean NOT NULL,"
                "CONSTRAINT producto_pkey PRIMARY KEY (id))"
                " WITCH (OIDS = FALSE) TABLESPACE pg_default;",
            "ALTER TABLE public.producto OWNER to postgres;",

            "CREATE TABLE IF NOT EXISTS usuario("
                "id integer NOT NULL DEFAULT nextval('usuario_id_seq'::regclass),"
                "nombre character varying(100) COLLATE pg_catalog.'default' NOT NULL,"
                "dni character varying(8) COLLATE pg_catalog.'default' NOT NULL,"
                "dir character varying(100) COLLATE pg_catalog.'default',"
                "tel character varying(10) COLLATE pg_catalog.'default',"
                "CONSTRAINT usuario_pkey PRIMARY KEY (id))"
                " WITCH (OIDS = FALSE) TABLESPACE pg_default;",
            "ALTER TABLE public.usuario OWNER to postgres;",

            "CREATE TABLE IF NOT EXISTS venta("
                "id integer NOT NULL DEFAULT nextval('venta_id_seq'::regclass),"
                "producto integer NOT NULL"
                "venta boolean NOT NULL,"
                "pago real,"
                "interes real,"
                "deuda real,"
                "fecha date NOT NULL,"
                "usuario integer,"
                "CONSTRAINT venta_pkey PRIMARY KEY (id),"
                "CONSTRAINT venta_producto_fkey FOREIGN KEY (producto)"
                " REFERENCES public.producto (id) MATCH SIMPLE"
                " ON UPDATE CASCADE"
                " ON DELETE CASCADE,"
                " CONSTRAINT venta_usuario_fkey FOREIGN KEY (usuario)"
                " REFERENCES public.usuario (id) MATCH SIMPLE"
                " ON UPDATE CASCADE"
                " ON DELETE SET NULL)"
                " WITCH (OIDS = FALSE) TABLESPACE pg_default;",
            "ALTER TABLE public.venta OWNER to postgres;",

        ]
        for tabla in tablas:
            cursor.execute(tabla);
        messagebox.showinfo("Crear DB","Tablas creadas correctamente")
        root2.destroy()
    except sqlite3.OperationalError as error:
        messagebox.showinfo("Error al crear tablas:", error)



def licencia():
    messagebox.showinfo("Mi Tienda", "Version 1.0 \n2020 all rights reserved.")

def salir():
    valor = messagebox.askquestion("Salir", "¿Deseas salir de la aplicacion?")
    if valor == "yes":
        ventana_menu.destroy()
def calculadora():
    calc()


# funicones de los paquetes


# configura el menu y submenu
barramenu = Menu(ventana_menu)
ventana_menu.config(menu=barramenu)

img_calculadora=PhotoImage(file="img/calculadora.png")
img_notas=PhotoImage(file="img/notas.png")
img_salida=PhotoImage(file="img/salida.png")
img_datos=PhotoImage(file="img/llave.png")
archivo = Menu(barramenu, tearoff=0, font=20)
archivo.add_command(label="Calculadora",underline=0,image=img_calculadora,compound=LEFT,command=calculadora)
archivo.add_separator()
archivo.add_command(label="Ingresa clave",underline=0,image=img_datos,compound=LEFT,command=clave)
archivo.add_command(label="Salir", command=salir,underline=0,image=img_salida,compound=LEFT)

img_producto=PhotoImage(file="img/camiseta.png")
img_stock=PhotoImage(file="img/caja.png")
#img_ventas=PhotoImage(file="img/vendido.png")
productos = Menu(barramenu, tearoff=0, font=20)
productos.add_command(label="Ingreso",underline=0,image=img_stock,compound=LEFT,command=productoForm)
productos.add_separator()  # separador de menu
productos.add_command(label="En Stock",underline=0,image=img_producto,compound=LEFT,command=stockList)
#productos.add_command(label="Vendidos",underline=0,image=img_ventas,compound=LEFT,command=vendidosList)


img_portapapeles=PhotoImage(file="img/portapapeles.png")
img_cliente=PhotoImage(file="img/chica.png")
clientes = Menu(barramenu,tearoff=0, font=20)
clientes.add_command(label="Agregar",underline=0,image=img_cliente,compound=LEFT,command=usuarioForm)
clientes.add_command(label="Lista de Clientes",underline=0,image=img_portapapeles,compound=LEFT, command=usuariosList)

img_vender=PhotoImage(file="img/venta.png")
acciones = Menu(barramenu, tearoff=0, font=20)
acciones.add_command(label="Vender",command=ventaForm,underline=0,image=img_vender,compound=LEFT)

img_cartera=PhotoImage(file="img/cartera.png")
img_planillas=PhotoImage(file="img/planillas.png")
ventas = Menu(barramenu, tearoff=0, font=20)
ventas.add_command(label="Contado",underline=0,image=img_cartera,compound=LEFT,command=vendidosList)
ventas.add_command(label="Planillas",underline=0,image=img_planillas,compound=LEFT,command=planillaList)

img_info=PhotoImage(file="img/informacion.png")
ayuda = Menu(barramenu, tearoff=0, font=20)
ayuda.add_command(label="Acerca de...", command=licencia,underline=0,image=img_info,compound=LEFT)
# -------------------------ingresar en menu-------------------------------
barramenu.add_cascade(label="Archivo", menu=archivo)

barramenu.add_cascade(label="Acciones", menu=acciones)

barramenu.add_cascade(label="Productos", menu=productos)

barramenu.add_cascade(label="Ventas", menu=ventas)

barramenu.add_cascade(label="Clientes", menu=clientes)

barramenu.add_cascade(label="Ayuda", menu=ayuda)

ventana_menu.mainloop()
