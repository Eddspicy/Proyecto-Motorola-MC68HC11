def imprimir_arreglos(arreglos, ruta_archivo):
    contador = 1
    var_eys = 8000

    with open(ruta_archivo, 'w') as archivo:
        for arreglo in arreglos:
            try:
                valor1, valor2, *valor3 = arreglo
            except ValueError:
                archivo.write("El arreglo no tiene la estructura adecuada")
                return

            valor3 = valor3[0] if valor3 else ""

            if valor3 and not valor3.startswith('*'):
                raise Exception("ERROR COMENTARIO")

            longitud_valor1 = len(valor1)
            var_eys = var_eys + (longitud_valor1 // 2)

            output = f"{contador}: \t{var_eys} ({valor1})\t\t: {valor2} {valor3}"
            archivo.write(output + '\n')

            contador += 1

        archivo.write("\nSymbol Table")

# Ejemplo de uso
EJ_ARRAY1 = ['hola', 'prueba', '*comentario']
EJ_ARRAY2 = ['buenas', 'test', '*comentario2']
EJ_ARRAY3 = ['adios1', 'fin']
EJ_ARRAY4 = ['hello2', 'world', '']
arreglos = [EJ_ARRAY1, EJ_ARRAY2, EJ_ARRAY3, EJ_ARRAY4]

ruta_archivo = r'C:\Users\minec\Desktop\Carpeta de pruebas\PRUEBASPY\numeros.txt'
imprimir_arreglos(arreglos, ruta_archivo)