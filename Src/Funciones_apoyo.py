import re

#Errores
CONS_001 = "001   CONSTANTE INEXISTENTE - Error en linea:" 
CONS_002 = "002   VARIABLE INEXISTENTE - Error en linea:" 
CONS_003 = "003   ETIQUETA INEXISTENTE - Error en linea:" 
CONS_004 = "004   MNEMONICO INEXISTENTE - Error en linea:" 
CONS_005 = "005   INSTRUCCION CARECE DE  OPERANDO(S) - Error en linea:" 
CONS_006 = "006   INSTRUCCION NO LLEVA OPERANDO(S) - Error en linea:" 
CONS_007 = "007   MAGNITUD DE  OPERANDO ERRONEA - Error en linea:" 
CONS_008 = "008   SALTO RELATIVO MUY LEJANO - Error en linea:"
CONS_009 = "009   INSTRUCCION CARECE DE ALMENOS UN ESPACIO RELATIVO AL MARGEN - Error en linea:" 
CONS_010 = "010   NO SE ENCUENTRA END"

#Saltos NO RELATIVOS
SALTOS  = ['jmp', 'jsr']

#Mnemonicos en arreglo
palabras = [
        'aba', 'abx', 'aby', 'adca', 'adcb', 'adda', 'addb', 'addd', 'anda', 'andb',
        'asl', 'asla', 'aslb', 'asld', 'asr', 'asra', 'asrb', 'bcc', 'bclr', 'bcs',
        'beq', 'bge', 'bgt', 'bhi', 'bhs', 'bita', 'bitb', 'ble', 'blo', 'bls', 'blt',
        'bmi', 'bne', 'bpl', 'bra', 'brclr', 'brn', 'brset', 'bset', 'bsr', 'bvc',
        'bvs', 'cba', 'clc', 'cli', 'clr', 'clra', 'clrb', 'clv', 'cmpa', 'cmpb', 'com',
        'coma', 'comb', 'cpd', 'cpx', 'cpy', 'daa', 'dec', 'deca', 'decb', 'des', 'dex',
        'dey', 'eora', 'eorb', 'fdiv', 'idiv', 'inc', 'inca', 'incb', 'ins', 'inx', 'iny',
        'jmp', 'jsr', 'ldaa', 'ldab', 'ldd', 'lds', 'ldx', 'ldy', 'lsl', 'lsla', 'lslb',
        'lsld', 'lsr', 'lsra', 'lsrb', 'lsrd', 'mul', 'neg', 'nega', 'negb', 'nop',
        'oraa', 'orab', 'psha', 'pshb', 'pshx', 'pshy', 'pula', 'pulb', 'pulx', 'puly',
        'rol', 'rola', 'rolb', 'ror', 'rora', 'rorb', 'rti', 'rts', 'sba', 'sbca', 'sbcb',
        'sec', 'sei', 'sev', 'staa', 'stab', 'std', 'stop', 'sts', 'stx', 'sty', 'suba',
        'subb', 'subd', 'swi', 'tab', 'tap', 'tba', 'tets', 'tpa', 'tst', 'tsta', 'tstb',
        'tsx', 'tsy', 'txs', 'tys', 'wai', 'xgdx', 'xgdy'
    ]

#Variable direccion de memoria en lista para pasarla como "apuntador" y que pueda ser modificada dentro de todas las funciones
dir_mem = [hex(32768)]

def incremento_memoria(len_cmp):
    inc = (len_cmp / 2)
    return int(inc)

#EXPRESIONES REGULARES
variables = re.compile(r"(([A-Z0-9]|\_)+)((\s)+EQU(\s)+)(\$00[0-9A-F]{2})", flags=re.IGNORECASE) #acepta simbolos en los nombres
constantes = re.compile(r"(([A-Z0-9]|\_)+)(\s)+(EQU)(\s)+(\$10[0-9A-F]{2})", flags=re.IGNORECASE) #acepta simbolos en los nombres
comentarios = re.compile(r"(\*(\w|\W)*)")
etiquetas = re.compile(r"(([A-Z]|[\_])*)", flags=re.IGNORECASE) #no debe detectar espacios ni lineas en blanco

ER_ALL5 = re.compile(r"^([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s*#|\s*){1}(\d{1,5}|\$[0-9A-F]{2,4}|'\S{1}|%[0-1]{1,16}|\w+)(,[XY])?(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
ER_OP = re.compile(r"^(\d{1,5}|\$[0-9A-F]{2,4}|'\S{1}|%[0-1]{1,16}|\w+)(,[XY])?(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)

ER_REL = re.compile(r"^(B[CEGHLMNPRSV][ACEILNOQRST])(\s+[\w]{1,256})?(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
ER_INH = re.compile(r"^([ACDFILMNPRSTWX][ABDEGLNOPSTUWXY][ABCDGHILMOPRSTVXY][ABDPSVXY]?)(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
ER_IMM = re.compile(r"^([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?)(\s*#)(\d{1,5}|\$[0-9A-F]{2,4}||\'\S{1}|\%[0-1]{1,16})(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE) #se tiene que cambiar lo de los operandos
ER_DIR = re.compile(r"^([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?[RT]?)(\s+){1}(\d{1,3}|\$[0-9A-F]{2}|'\S{1}|%[0-1]{1,8}|\w+)(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
ER_EXT = re.compile(r"^([ABCDEIJLNORST][BDEILMNOPRSTU][ABCDGLMPRSTXY][ABD]?)(\s+){1}(\d{1,5}|\$[0-9A-F]{4}|'\S{1}|%[0-1]{1,16}|\w+)(\s*\\s?[\w|\W])?$", flags=re.IGNORECASE)
ER_INDX = re.compile(r"^([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s+){1}(\d{1,3}|\$[0-9A-F]{2}|'\S{1}|%[0-1]{1,8}|\w+)(\s*\\s[A-Z])?(,X)(\s*\\s?[\w|\W])?$", flags= re.IGNORECASE)
ER_INDY = re.compile(r"^([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s+){1}(\d{1,3}|\$[0-9A-F]{2}|'\S{1}|%[0-1]{1,8}|\w+)(\s*\\s[A-Z])?(,Y)(\s*\\s?[\w|\W])?$", flags= re.IGNORECASE)

#FUNCIONES PARA MANIPULACION DE CADENAS O DEL ARCHIVO
def verificar_palabra_reservada(texto):
    control = True  
    for palabra in palabras:
        if re.search(palabra, texto, flags=re.IGNORECASE ) :
            control = False
    
    return control

def verificar_palabra_reservadainv(texto):
    control = False   
    for palabra in palabras:
        if re.search(palabra, texto, flags=re.IGNORECASE ) :
            control = True
    
    return control

def calcular_dirmem(cobj, old_dir_mem):  
    return old_dir_mem + hex(len(cobj) / 2)

def acortador_mnemonicos(cadena):
    cadena_cut = cadena.split(',')
    if len(cadena_cut) > 0:
        return cadena_cut[0]
    else:
        return ""

def acortador_bytes(cadena):
    cadena_cut = cadena.split(',')
    if len(cadena_cut) > 0:
        bytes_op = int(cadena_cut[3])
        return bytes_op
    else:
        return 0

def acortador_opcode(cadena):
    cadena_cut = cadena.split(',')
    if len(cadena_cut) > 0:
        op_code = cadena_cut[1]
        return op_code
    else:
        return 0

def eliminar_espacios(cadena):
    # Dividir la cadena en palabras individuales
    palabras = cadena.split()
    # Unir las palabras sin espacios
    resultado = "".join(palabras)
    
    return resultado

def borrar_linea(archivo, cadena):
    with open(archivo, "r") as file:
        lineas = file.readlines()

    with open(archivo, "w") as file:
        for linea in lineas:
            if cadena not in linea:
                file.write(linea)

#FUNCIONES PARA REALIZAR SALTOS
def complemento_a_dos(numero):
    # Convertir el número a binario
    binario = bin(numero)[2:]  # Quitamos el prefijo '0b' del número binario

    # Rellenar con ceros a la izquierda para mantener la longitud
    binario = binario.zfill(8)  # Suponiendo que trabajamos con números de 8 bits

    # Tomar el complemento a uno del número binario
    complemento_uno = ''.join('1' if bit == '0' else '0' for bit in binario)

    # Sumar 1 al complemento a uno
    complemento_dos = bin(int(complemento_uno, 2) + 1)[2:]

    # Convertir el complemento a dos a hexadecimal y mostrar en mayúsculas
    hexadecimal = hex(int(complemento_dos, 2))[2:].upper()  # Quitamos el prefijo '0x' del número hexadecimal y lo convertimos a mayúsculas

    return hexadecimal

def encuentra_linea(nombre_archivo, linea_codigo, palabra_buscar):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()  # Leer todas las líneas del archivo

    contador_lineas = 0  # Inicializar el contador de líneas
    encontrada = False
    hacia_abajo = False  # Bandera para rastrear si la búsqueda fue hacia abajo

    # Buscar la primera aparición de la palabra en la línea especificada hacia arriba
    for i, linea in reversed(list(enumerate(lineas[:linea_codigo]))):
        linea = linea.rstrip('\n')
        palabras = linea.split()
        if palabras and palabras[0] == palabra_buscar:
            encontrada = True
            break
        contador_lineas += 1

    # Corregir el conteo, dado que contamos una línea adicional al encontrar la palabra
    if encontrada:
        contador_lineas -= 1
    else:
        # Si no se encuentra la palabra, busca hacia abajo
        contador_lineas = 2  # Iniciar el contador en 2
        hacia_abajo = True  # Establecer la bandera hacia_abajo en verdadero
        for i, linea in enumerate(lineas[linea_codigo:], start=linea_codigo):
            linea = linea.rstrip('\n')
            palabras = linea.split()
            if palabras and palabras[0] == palabra_buscar:
                break
            contador_lineas += 1  # Incrementar el contador de líneas
        # Continuar contando hasta encontrar una línea que no sea vacía ni inicie con "*"
        while i+1 < len(lineas):
            siguiente_linea = lineas[i+1].rstrip('\n')
            if siguiente_linea != '' and siguiente_linea[0] != '*':
                break
            i += 1
            contador_lineas += 1

    return -contador_lineas if hacia_abajo else contador_lineas

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

#50: 8028  (<span style="color: red;">7F0002</span>)  :  CLR $0002

#___________________________________________________________________________________________________________________________________________________________#