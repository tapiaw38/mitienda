import psycopg2
import json

def conexion_psql():
    with open("credenciales.json") as archivo_credenciales:
        credenciales = json.load(archivo_credenciales)

    try:
        conexion = psycopg2.connect(**credenciales)
        print("conexion establecida")
        return conexion
    except:
        print("Ocurrio un error al conectarse a la base de datos")


