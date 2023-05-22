def obtener_primeras_letras_sin_repetir_desde_archivo(nombre_archivo):
    letras = set()
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            cadena = linea.strip()  # Eliminar espacios en blanco al inicio y final de la línea
            primera_letra = cadena[1]
            letras.add(primera_letra)

    letras_ordenadas = sorted(letras)
    return letras_ordenadas


# Ejemplo de uso:
nombre_archivo = 'D:\Facultad\Semestre 2023-2\EyPC\Proyecto\Proyecto-Motorola-MC68HC11\EXT.txt'  # Reemplaza con la ruta y nombre de tu archivo de texto
primeras_letras_sin_repetir_ordenadas = obtener_primeras_letras_sin_repetir_desde_archivo(nombre_archivo)
#print(primeras_letras_sin_repetir_ordenadas)

def limpiar_texto(texto):
    cadena = ''.join(texto)
    
    cadena = cadena.replace("'", "").replace("[", "").replace("]", "")
    
    return cadena

texto = primeras_letras_sin_repetir_ordenadas
texto_limpiado = "[" + limpiar_texto(texto) + "]"
print(texto_limpiado)


