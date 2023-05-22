def dividir_cadena(cadena):
    grupos = []
    for i in range(0, len(cadena), 3):
        grupo = cadena[i:i+3]
        grupos.append(grupo)
    resultado = ' '.join(grupos)
    return resultado

cadena = input("Ingresa una cadena: ")
resultado = dividir_cadena(cadena)
print("Resultado:", resultado)