import re

def acortador_mnemonicos(cadena):
    cadena_cut = ""
    if len(cadena) >= 4:
        if cadena[3] == ',':
            cadena_cut = cadena[:3]
        else:
            cadena_cut = cadena[:4]
    else:
        cadena_cut = cadena[:len(cadena)]
    return cadena_cut;

def acortador_bytes(cadena):
    byte = cadena.split(',')
    if len(byte) > 1:
        return byte[-1].strip()
    else:
        return print("Error al obtener los bytes de la instrucción")

def acortador_opcode(cadena):
    primera_coma = cadena.find(',')
    segunda_coma = cadena.find(',', primera_coma + 1)

    if primera_coma != -1 and segunda_coma != -1:
        opcode = cadena[primera_coma + 1:segunda_coma].strip()
        return opcode
    else:
        return print("Error al encontrar el opcode")


def compilado_REL (instruccion, mnemonicos, stack_compiler, stack_error, error_line, list_labels):
    for i in mnemonicos:
        if instruccion[1] == acortador_mnemonicos(i):
            stack_compiler.push(acortador_opcode(i))
        #INTRODUCIR OPCODE DE LASA ETIQUETAS


def compilado_INH (instruccion, mnemonicos, stack_compiler, stack_error,error_line):
    print("inherente")
    for i in mnemonicos:
        if instruccion[1] == acortador_mnemonicos(i):
            stack_compiler.push(acortador_opcode(i))


def compilado_ALL5 (instruccion, mnemonicos_dir, mnemonicos_ext, mnemonicos_imm, mnemonicos_indx, mnemonicos_indy, stack_compiler, stack_error, error_line, list_labels):
    print("ALL5")
    IMM = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?)(\s#)(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1}|%[0-1]{1,16})(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    DIR = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?)(\s){1}(\d{1,3}|\$[0-9A-F]{2}|\$0[0-9A-F]|’[A-Za-z]{1})(\s\*[A-Z]*)?", flags= re.IGNORECASE) #Puede que la tercera condicion de operadores este de mas
    EXT = re.compile(r"([ABCDEIJLNORST][BDEILMNOPRSTU][ABCDGLMPRSTXY][ABD]?)(\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1}|%[0-1]{1,16})(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    INDX = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?)(\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1}|%[0-1]{1,16})(,X)(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    INDY = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?)(\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1}|%[0-1]{1,16})(,Y)(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    
    tostr = "".join(instruccion) #SIRVE PARA VERFIFICAR EL DIRECCIONAMIENTO COMO CADENA MEDIANTE REGEX

    if re.fullmatch(IMM, tostr):
        for i in mnemonicos_imm:
            #MNEMONICO
            if instruccion[1] == acortador_mnemonicos(i):
                if len(acortador_mnemonicos(i)) == 2:
                    stack_compiler.push(acortador_opcode(i))
                elif len(acortador_mnemonicos(i)) > 2:
                    stack_compiler.push(acortador_opcode(i[0:1]))
                    stack_compiler.push(acortador_opcode(i[2:3]))
            else:
                stack_error.push("El mnemonico no existe")

           #OPERANDOS DIFERENCIACION
            verificador = instruccion[3]
            if verificador[0] == "$":
                if acortador_bytes(i) == 2:
                    if len(instruccion[3][1:]) == 2:
                        stack_compiler.push(instruccion[3])
                else:
                    stack_error.push("Error en el operando ingresado")
            
                if acortador_bytes(i) > 2:
                    if len(instruccion[3][1:]) == 3:
                        stack_compiler.push(instruccion[3][1:2])
                        stack_compiler.push(instruccion[3][3])
                    elif len(instruccion[3][1:]) == 4:
                        stack_compiler.push(instruccion[3][1:2])
                        stack_compiler.push(instruccion[3][3:4])
                else:stack_error.push("Error en el operando ingresado")

            #CONVERSION ASCII
            elif verificador[0] == "’":
                conversion = hex(ord(instruccion[3[1:]]))
                if acortador_bytes(i) == 2:
                    if len(conversion) == 2:
                        stack_compiler.push(conversion)
                else:
                    stack_error.push("Error en el operando ingresado")
            
                if acortador_bytes(i) > 2:
                    if len(conversion) == 3:
                        stack_compiler.push(conversion[0:1]) #Empieza desde 0 porque en decimal no se utiliza ningun simbolo para especificarlo como en los demas operandos
                        stack_compiler.push(conversion[3][2])
                    elif len(conversion[3]) == 4:
                        stack_compiler.push(conversion[0:1])
                        stack_compiler.push(conversion[2:3])
                    else:
                        stack_error.push("Error en el operando ingresado")
            
            #CONVERSION BINARIO
            elif verificador[0] == "%":
                conversion = hex(int(instruccion[3][1:]),2)
                if acortador_bytes(i) == 2:
                    if len(conversion) == 2:
                        stack_compiler.push(conversion)
                else:
                    stack_error.push("Error en el operando ingresado")
            
                if acortador_bytes(i) > 2:
                    if len(conversion) == 3:
                        stack_compiler.push(conversion[0:1])
                        stack_compiler.push(conversion[3][2])
                    elif len(conversion[3]) == 4 and conversion < hex(65535):
                        stack_compiler.push(conversion[0:1])
                        stack_compiler.push(conversion[2:3])
                    else:
                        stack_error.push("Error en el operando ingresado")
                
            #CONVERSION DECIMAL
            else:
                conversion = hex(int(instruccion[3]))
                if acortador_bytes(i) == 2:
                    if len(conversion) == 2:
                        stack_compiler.push(conversion)
                else:
                    stack_error.push("Error en el operando ingresado")
            
                if acortador_bytes(i) > 2:
                    if len(conversion) == 3:
                        stack_compiler.push(conversion[0:1])
                        stack_compiler.push(conversion[3][2])
                    elif len(conversion[3]) == 4 and conversion < hex(65535):
                        stack_compiler.push(conversion[0:1])
                        stack_compiler.push(conversion[2:3])
                    else:
                        stack_error.push("Error en el operando ingresado")
            
            


    elif re.fullmatch(DIR, tostr):
        for i in mnemonicos_dir:
            if instruccion[1] == acortador_mnemonicos(i):
                stack_compiler.push(acortador_opcode(i))
            else:
                stack_error.push("El mnemonico no existe")
            if len(instruccion[3]) <= 2:
                stack_compiler.push(instruccion[3])
            else:
                 stack_error.push("El operando ingreso es incorrecto")

    elif re.fullmatch(EXT, tostr):
        for i in mnemonicos_ext:
            if instruccion[1] == acortador_mnemonicos(i):
                stack_compiler.push(acortador_opcode(i))
            else:
                stack_error.push("El mnemonico no existe")

    elif re.fullmatch(INDY, tostr):
        for i in mnemonicos_indy:
            if instruccion[1] == acortador_mnemonicos(i):
                stack_compiler.push(acortador_opcode(i))
            else:
                stack_error.push("El mnemonico no existe")

    elif re.fullmatch(INDX, tostr):
        for i in mnemonicos_indx:
            if instruccion[1] == acortador_mnemonicos(i):
                stack_compiler.push(acortador_opcode(i))
            else:
                stack_error.push("El mnemonico no existe")
            
