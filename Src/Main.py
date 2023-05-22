from io import open
import Precompilado
import Compilado

def main(): 
    archivo = open("D:\Facultad\Semestre 2023-2\EyPC\Proyecto\Proyecto-Motorola-MC68HC11\pruebaAZ.asc", "r")
    for linea in archivo:
        direccionamiento = Precompilado.precompilado(linea.strip())
        print(f"Cadena: {linea.strip()}\nTipo de direccionamiento: {direccionamiento}\n")
    archivo.close()
()
