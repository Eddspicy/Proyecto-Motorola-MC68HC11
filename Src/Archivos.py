#DESCRIPCION
"""
"""

#------------------------------------------------FUNCIONES PARA LST Y HTML-----------------------------------------------------------------------------------#
def insertar_texterr(texto_error):
    return f"{texto_error}\n"

def insertar_comentario(tupla):
    comentario, linea = tupla
    return f"{linea}:\t{comentario}\n"

def insertar_etiquetas(tupla):
    etiqueta = tupla[0]
    return f"{etiqueta}\n"

def insertar_etiquetas_modificado(tupla, lineas):
    etiqueta, _, linea = tupla
    lineas[linea] = f"{linea}: {etiqueta}\n"

#___________________________________________________________________________________________________________________________________________________________#

#------------------------------------------------CREACION DE ARCHIVO LST-----------------------------------------------------------------------------------#

def insertar_lst(tupla):
    cod_op, instruccion, _, linea, dir_mem, _ = tupla
    dir_mem = dir_mem[2:].ljust(6)  # Asegura que dir_mem siempre tenga 6 caracteres
    return f"{linea}:\t{dir_mem.upper()}({cod_op})\t\t:\t{instruccion}\n"

def creacion_lst(tuplas_comentario, tuplas_lst, tuplas_etiquetas, errores, nombre_archivo="Compilado.lst"):
    max_linea = max([tupla[1] for tupla in tuplas_comentario] + [tupla[3] for tupla in tuplas_lst] + [tupla[2] for tupla in tuplas_etiquetas])
    lineas = [''] * (max_linea + 1)

    for tupla in tuplas_comentario:
        lineas[tupla[1]] = insertar_comentario(tupla)

    for tupla in tuplas_lst:
        lineas[tupla[3]] = insertar_lst(tupla)

    for i in range(1, len(lineas)):
        if lineas[i] == '':
            lineas[i] = f"{i}:\n"

    for tupla in tuplas_etiquetas:
        insertar_etiquetas_modificado(tupla, lineas)

    lineas.append('SYMBOLTABLE'.center(80) + '\n')

    for tupla in tuplas_etiquetas:
        lineas.append(insertar_etiquetas(tupla))

    lineas.append('ERRORES'.center(80) + '\n')

    for error in errores:
        lineas.append(insertar_texterr(error))

    with open(nombre_archivo, 'w') as f:
        f.write("0:"+"\t"+"ORG $8000"+"\n")
        f.writelines(lineas)

#___________________________________________________________________________________________________________________________________________________________#

#------------------------------------------------CREACION DE ARCHIVO S19------------------------------------------------------------------------------------#
def contador_s19(index):
    sequence = []  # Arreglo principal

    # El bucle más externo recorre los números 8 y 9 para el primer dígito
    for first_digit in range(8, 10):
        # El bucle externo recorre desde 0 hasta 15 para el segundo dígito
        for second_digit in range(16):
            # Convierte el dígito a hexadecimal, elimina el prefijo '0x' y lo convierte a mayúsculas
            second_hex = hex(second_digit)[2:].upper()
            
            # El bucle interno recorre desde 0 hasta 15 para el tercer dígito
            for third_digit in range(16):
                # Convierte el dígito a hexadecimal, elimina el prefijo '0x' y lo convierte a mayúsculas
                third_hex = hex(third_digit)[2:].upper()
                
                # Genera el valor y lo agrega directamente a la secuencia
                sequence.append(f"{first_digit}{second_hex}{third_hex}0")

    # Verifica si el índice es válido
    if index < 1 or index > len(sequence):
        return "Índice inválido"
    else:
        return sequence[index - 1]  # Ajusta para el índice basado en 1

def dividir_cadenas_s19(tuples):
    hex_strings = [t[0] for t in tuples]  # Recoge todos los strings hexadecimales.
    all_hex = ''.join(hex_strings)  # Une todos los strings.
    split_hex = [all_hex[i:i+2] for i in range(0, len(all_hex), 2)]  # Divide en grupos de dos.

    # Divide en listas de 16 elementos.
    split_hex_arrays = [split_hex[i:i+16] for i in range(0, len(split_hex), 16)]
    # Une los elementos en cada lista con un espacio y luego las convierte en strings.
    result = [' '.join(array) for array in split_hex_arrays]
    
    return tuple(result)  # Convierte la lista en una tupla


def creacion_s19(tuplas):
    result = dividir_cadenas_s19(tuplas)
    filename = "Compilado.s19"  # Define el nombre del archivo.

    # Abre el archivo para escribir.
    with open(filename, 'w') as file:
        for i, array in enumerate(result, start=1):
            file.write(f"<{contador_s19(i)}> {array}\n")  # Escribe en el archivo.

#___________________________________________________________________________________________________________________________________________________________#

#------------------------------------------------CREACION DE ARCHIVO HTML-----------------------------------------------------------------------------------#

def insertar_HTML(tupla):
    cod_mne, color_mne,cod_op, color_op, linea, _, nline, dir_mem, _ = tupla
    dir_mem = dir_mem[2:].ljust(6)
    #(codigo objeto mne, color mne, codigo objeto op, color op, linea de codigo original, sc , line, dir_mem, comentario)
    if cod_op == "inherente":
        return f"{nline}:\t{dir_mem.upper()}\t(<span style='color: {color_mne};'>{cod_mne}</span>)\t:\t{linea.upper()}\n"
    else:
        return f"{nline}:\t{dir_mem.upper()}\t(<span style='color: {color_mne};'>{cod_mne}</span><span style='color: {color_op};'>{cod_op}</span>)\t:\t{linea.upper()}\n"

def creacion_HTML(tuplas_comentario, tuplas_html, tuplas_etiquetas, errores, nombre_archivo="Compilado.html"):
    max_linea = max([tupla[1] for tupla in tuplas_comentario] + [tupla[6] for tupla in tuplas_html] + [tupla[2] for tupla in tuplas_etiquetas])
    lineas = [''] * (max_linea + 1)

    for tupla in tuplas_comentario:
        lineas[tupla[1]] = insertar_comentario(tupla)

    for tupla in tuplas_html:
        lineas[tupla[6]] = insertar_HTML(tupla)

    for i in range(1, len(lineas)):
        if lineas[i] == '':
            lineas[i] = f"{i}:\n"

    for tupla in tuplas_etiquetas:
        insertar_etiquetas_modificado(tupla, lineas)

    lineas.append('SYMBOLTABLE'.center(80) + '\n')

    for tupla in tuplas_etiquetas:
        lineas.append(insertar_etiquetas(tupla))

    lineas.append('ERRORES'.center(80) + '\n')

    for error in errores:
        lineas.append(insertar_texterr(error))

    with open(nombre_archivo, 'w') as f:
        f.write("<html>\n<body>\n<pre>\n")
        f.write("0:"+"\t"+"ORG $8000"+"\n")
        f.writelines(lineas)
#___________________________________________________________________________________________________________________________________________________________#