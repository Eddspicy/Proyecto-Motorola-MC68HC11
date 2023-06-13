import re

#Errores
CONS_001 = "001   CONSTANTE INEXISTENTE - Error en linea:" #YA SE USO
CONS_002 = "002   VARIABLE INEXISTENTE - Error en linea:" #YA SE USO
CONS_003 = "003   ETIQUETA INEXISTENTE - Error en linea:" #YA SE USO
CONS_004 = "004   MNEMÓNICO INEXISTENTE - Error en linea:" #YA SE USO
CONS_005 = "005   INSTRUCCIÓN CARECE DE  OPERANDO(S) - Error en linea:" #YA SE USO
CONS_006 = "006   INSTRUCCIÓN NO LLEVA OPERANDO(S) - Error en linea:" #YA SE USO
CONS_007 = "007   MAGNITUD DE  OPERANDO ERRONEA - Error en linea:" #YA SE USO
CONS_008 = "008   SALTO RELATIVO MUY LEJANO - Error en linea:"
CONS_009 = "009   INSTRUCCIÓN CARECE DE ALMENOS UN ESPACIO RELATIVO AL MARGENE - Error en linea:" #YA SE USO
CONS_010 = "010   NO SE ENCUENTRA END - Error en linea:"

ER_REL = re.compile(r"^(B[CEGHLMNPRSV][ACEILNOQRST])(\s+[\w]{1,256})?(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
ER_INH = re.compile(r"^([ACDFILMNPRSTWX][ABDEGLNOPSTUWXY][ABCDGHILMOPRSTVXY][ABDPSVXY]?)(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
ER_IMM = re.compile(r"^([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?)(\s*#)(\d{1,5}|\$[0-9A-F]{2,4}||\'\S{1}|\%[0-1]{1,16})(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE) #se tiene que cambiar lo de los operandos
ER_DIR = re.compile(r"^([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?[RT]?)(\s+){1}(\d{1,3}|\$[0-9A-F]{2}|'\S{1}|%[0-1]{1,8}|\w+)(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
ER_EXT = re.compile(r"^([ABCDEIJLNORST][BDEILMNOPRSTU][ABCDGLMPRSTXY][ABD]?)(\s+){1}(\d{1,5}|\$[0-9A-F]{4}|'\S{1}|%[0-1]{1,16}|\w+)(\s*\\s?[\w|\W])?$", flags=re.IGNORECASE)
ER_INDX = re.compile(r"^([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s+){1}(\d{1,3}|\$[0-9A-F]{2}|'\S{1}|%[0-1]{1,8}|\w+)(\s*\\s[A-Z])?(,X)(\s*\\s?[\w|\W])?$", flags= re.IGNORECASE)
ER_INDY = re.compile(r"^([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s+){1}(\d{1,3}|\$[0-9A-F]{2}|'\S{1}|%[0-1]{1,8}|\w+)(\s*\\s[A-Z])?(,Y)(\s*\\s?[\w|\W])?$", flags= re.IGNORECASE)

"""
ER_DIR = re.compile(r"^([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?[RT]?)(\s+){1}(\d{1,3}|\$[0-9A-F]{2}|'\S{1}|%[0-1]{1,8}|\w+)(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
ER_EXT = re.compile(r"^([ABCDEIJLNORST][BDEILMNOPRSTU][ABCDGLMPRSTXY][ABD]?)(\s+){1}(\d{1,5}|\$[0-9A-F]{2,4}|'\S{1}|%[0-1]{1,16}|\w+)(\s*\\s?[\w|\W])?$", flags=re.IGNORECASE)
ER_INDX = re.compile(r"^([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s){1}(\d{1,5}|^\$[0-9A-F]{2,4}$|'\S{1}|%[0-1]{1,16}|\w+)(\s*\*\s[A-Z]*)?(,X)(\s\*[A-Z]*)?$", flags= re.IGNORECASE)
ER_INDY = re.compile(r"^([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s){1}(\d{1,5}|^\$[0-9A-F]{2,4}$|'\S{1}|%[0-1]{1,16}|\w+)(\s*\*\s[A-Z]*)?(,Y)(\s\*[A-Z]*)?$", flags= re.IGNORECASE)
"""
def compilado_ALL5(instruccion, IMM, DIR, EXT, INDX, INDY, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios, dir_mem):
    
    if re.fullmatch(ER_IMM, instruccion):
        grupos = re.split(ER_IMM, instruccion)
        for i in range (len(IMM)):
            if re.fullmatch(acortador_mnemonicos(IMM[i]), grupos[1],  flags= re.IGNORECASE):
                instruccion = conversor_operandos(instruccion, grupos[3])
                hex_act = re.split(ER_IMM, instruccion)
                mnemonico = acortador_opcode(IMM[i])
                mnemonico = eliminar_espacios(mnemonico)
                insbytes = acortador_bytes(IMM[i])
                oprbytes = (len(hex_act[3][1:]) / 2)
                compilado_operandos(instruccion, hex_act[3][1:], grupos[5], mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)
    
    elif re.fullmatch(ER_DIR, instruccion):
        grupos = re.split(ER_DIR, instruccion)
        for i in range (len(DIR)):
            if re.fullmatch(acortador_mnemonicos(DIR[i]), grupos[1],  flags= re.IGNORECASE):
                instruccion = conversor_operandos(instruccion, grupos[3])
                hex_act = re.split(ER_DIR, instruccion)
                mnemonico = acortador_opcode(DIR[i])
                mnemonico = eliminar_espacios(mnemonico)
                insbytes = acortador_bytes(DIR[i])
                oprbytes = (len(hex_act[3][1:]) / 2)
                compilado_operandos(instruccion, hex_act[3][1:], grupos[5], mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)

    elif re.fullmatch(ER_EXT, instruccion):
        grupos = re.split(ER_EXT, instruccion)
        for i in range (len(EXT)):
            if re.fullmatch(acortador_mnemonicos(EXT[i]), grupos[1],  flags= re.IGNORECASE):
                instruccion = conversor_operandos(instruccion, grupos[3])
                hex_act = re.split(ER_EXT, instruccion)
                mnemonico = acortador_opcode(EXT[i])
                mnemonico = eliminar_espacios(mnemonico)
                insbytes = acortador_bytes(EXT[i])
                oprbytes = (len(hex_act[3][1:]) / 2)
                compilado_operandos(instruccion, hex_act[3][1:], grupos[5], mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)

    elif re.fullmatch(ER_INDX, instruccion):
        grupos = re.split(ER_INDX, instruccion)
        for i in range (len(INDX)):
            if re.fullmatch(acortador_mnemonicos(INDX[i]), grupos[1],  flags= re.IGNORECASE):
                instruccion = conversor_operandos(instruccion, grupos[3])
                hex_act = re.split(ER_INDX, instruccion)
                mnemonico = acortador_opcode(INDX[i])
                mnemonico = eliminar_espacios(mnemonico)
                insbytes = acortador_bytes(INDX[i])
                oprbytes = (len(hex_act[3][1:]) / 2)
                compilado_operandos(instruccion, hex_act[3][1:], grupos[5], mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)

    elif re.fullmatch(ER_INDY, instruccion):
        grupos = re.split(ER_INDY, instruccion)
        for i in range (len(INDY)):
            if re.fullmatch(acortador_mnemonicos(INDY[i]), grupos[1],  flags= re.IGNORECASE):
                instruccion = conversor_operandos(instruccion, grupos[3])
                hex_act = re.split(ER_INDY, instruccion)
                mnemonico = acortador_opcode(INDY[i])
                mnemonico = eliminar_espacios(mnemonico)
                insbytes = acortador_bytes(INDY[i])
                oprbytes = (len(hex_act[3][1:]) / 2)
                compilado_operandos(instruccion, hex_act[3][1:], grupos[5], mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)

def compilado_operandos(instruccion, operando, comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem):
    if insbytes == 2:
        if len(mnemonico) == 2 and oprbytes == 1:
            compilado(instruccion, operando, comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)
        else:
            stack_error.append(CONS_007+str(line))
    elif insbytes == 3:
        if len(mnemonico) == 2 and oprbytes == 2:
            compilado(instruccion, operando, comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)
        elif len(mnemonico) == 4 and oprbytes == 1:
            compilado(instruccion, operando, comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)
        else:
            stack_error.append(CONS_007+str(line))
    elif insbytes == 4:
        if len(mnemonico) == 4  and oprbytes == 2:
            compilado(instruccion, operando, comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)        
        else:
            stack_error.append(CONS_007+str(line))

def compilado(instruccion, operando, comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem):
    stack_compiler_vls.append((mnemonico+operando, instruccion, "ns", dir_mem, comentario))
    stack_compiler_s19.append(mnemonico+operando)   
    stack_compiler_html.append((mnemonico, "r", operando, "b", instruccion, "ns", dir_mem, comentario)) 

def conversor_operandos(instruccion, operando):
    if operando[0] == "$":
        return instruccion
    elif operando[0] == "'":
        conversion = hex(ord(operando[1]))
        instruccion = instruccion.replace(operando, "$"+str(conversion[2:]))
        return instruccion
    elif operando[0] == "%":
        conversion = hex(int(operando[1:], 2))
        instruccion = instruccion.replace(operando, "$"+str(conversion[2:]))
        return instruccion
    else:
        conversion = hex(int(operando, 10))
        instruccion = instruccion.replace(operando, "$"+str(conversion[2:]))
        return instruccion

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