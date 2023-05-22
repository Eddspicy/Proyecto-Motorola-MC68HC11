from io import open
from Precompilado import *
import Compilado

def main(): 
    archivo = open("/home/eddspicy/Documents/Compilador Motorola MC68HC11/Proyecto-Motorola-MC68HC11/pruebaAZ.asc", "r")
    for linea in archivo:
        direccionamiento = precompilado(linea.strip())
        print(f"Cadena: {linea.strip()}\nTipo de direccionamiento: {direccionamiento}\n")
    archivo.close()
()
