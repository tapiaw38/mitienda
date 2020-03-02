import os
from tkinter import *
from tkinter import messagebox

# Importaciones de paquetes
from formulario.venta_form import ventaForm
from formulario.producto_form import productoForm
from formulario.usuario_form import usuarioForm
from listas.lista_usuario import usuariosList
from listas.lista_stock import stockList
from listas.lista_vendidos import vendidosList
from listas.lista_planilla import planillaList

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
Label(frame, text="Tienda de Ropa Nombre Tienda \nDe Nombre Persona - Direción del Local", fg="white", bg="black", font=("Monotype Corsiva", 14)).place(
    x=160, y=0)

# funciones internas
def licencia():
    messagebox.showinfo("Mi Tienda", "Version 1.0 \n2020 all rights reserved.")

def salir():
    valor = messagebox.askquestion("Salir", "¿Deseas salir de la aplicacion?")
    if valor == "yes":
        ventana_menu.destroy()
def calculadora():
    os.system("calc")
def notas():
    os.system("notepad")

# funicones de los paquetes


# configura el menu y submenu
barramenu = Menu(ventana_menu)
ventana_menu.config(menu=barramenu)

img_calculadora=PhotoImage(file="img/calculadora.png")
img_notas=PhotoImage(file="img/notas.png")
img_salida=PhotoImage(file="img/salida.png")
archivo = Menu(barramenu, tearoff=0, font=20)
archivo.add_command(label="Calculadora",underline=0,image=img_calculadora,compound=LEFT,command=calculadora)
archivo.add_command(label="Block de notas",underline=0,image=img_notas,compound=LEFT,command=notas)
archivo.add_separator()
archivo.add_command(label="Salir", command=salir,underline=0,image=img_salida,compound=LEFT)

img_producto=PhotoImage(file="img/camiseta.png")
img_stock=PhotoImage(file="img/caja.png")
#img_ventas=PhotoImage(file="img/vendido.png")
productos = Menu(barramenu, tearoff=0, font=20)
productos.add_command(label="Ingreso",underline=0,image=img_stock,compound=LEFT,command=productoForm)
productos.add_separator()  # separador de menu
productos.add_command(label="En Stock",underline=0,image=img_producto,compound=LEFT,command=stockList)
#productos.add_command(label="Vendidos",underline=0,image=img_ventas,compound=LEFT,command=vendidosList)

img_pdf=PhotoImage(file="img/pdf.png")
informes = Menu(barramenu, tearoff=0, font=20)
informes.add_command(label="Ventas hoy",underline=0,image=img_pdf,compound=LEFT)
informes.add_command(labe="Stock",underline=0,image=img_pdf,compound=LEFT)
informes.add_command(labe="Deudores",underline=0,image=img_pdf,compound=LEFT)

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

barramenu.add_cascade(label="Informes", menu=informes)

barramenu.add_cascade(label="Clientes", menu=clientes)

barramenu.add_cascade(label="Ayuda", menu=ayuda)

ventana_menu.mainloop()
