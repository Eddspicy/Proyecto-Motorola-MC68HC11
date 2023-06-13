import re
from Funciones_apoyo import  *

ER_REL = re.compile(r"^(B[CEGHLMNPRSV][ACEILNOQRST])(\s+[\w]{1,256})?(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
ER_INH = re.compile(r"^([ACDFILMNPRSTWX][ABDEGLNOPSTUWXY][ABCDGHILMOPRSTVXY][ABDPSVXY]?)(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
ER_IMM = re.compile(r"^([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?)(\s*#)(\d{1,5}|\$[0-9A-F]{2,4}||\'\S{1}|\%[0-1]{1,16})(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE) #se tiene que cambiar lo de los operandos
ER_DIR = re.compile(r"^([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?[RT]?)(\s+){1}(\d{1,3}|\$[0-9A-F]{2}|'\S{1}|%[0-1]{1,8}|\w+)(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
ER_EXT = re.compile(r"^([ABCDEIJLNORST][BDEILMNOPRSTU][ABCDGLMPRSTXY][ABD]?)(\s+){1}(\d{1,5}|\$[0-9A-F]{4}|'\S{1}|%[0-1]{1,16}|\w+)(\s*\\s?[\w|\W])?$", flags=re.IGNORECASE)
ER_INDX = re.compile(r"^([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s+){1}(\d{1,3}|\$[0-9A-F]{2}|'\S{1}|%[0-1]{1,8}|\w+)(\s*\\s[A-Z])?(,X)(\s*\\s?[\w|\W])?$", flags= re.IGNORECASE)
ER_INDY = re.compile(r"^([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s+){1}(\d{1,3}|\$[0-9A-F]{2}|'\S{1}|%[0-1]{1,8}|\w+)(\s*\\s[A-Z])?(,Y)(\s*\\s?[\w|\W])?$", flags= re.IGNORECASE)

def compilado_RELpt1(instruccion, REL, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios):
    if re.fullmatch(ER_REL, instruccion):
        grupos = re.split(ER_REL, instruccion)
        for i in range (len(REL)):
            if re.fullmatch(acortador_mnemonicos(REL[i]), grupos[1],  flags= re.IGNORECASE):
                mnemonico = acortador_opcode(REL[i])
                mnemonico = eliminar_espacios(mnemonico)
                stack_compiler_vls.append((mnemonico.upper(), instruccion, "sc", line, grupos[2]))
                stack_compiler_s19.append(mnemonico.upper())   
                stack_compiler_html.append((mnemonico.upper(), "r", "relativo", "b", instruccion, "sc", line, grupos[2]))

def compilado_INH(instruccion, INH, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios):
    if re.fullmatch(ER_INH, instruccion):
        grupos = re.split(ER_INH, instruccion)
        for i in range (len(INH)):
            if re.fullmatch(acortador_mnemonicos(INH[i]), grupos[1],  flags= re.IGNORECASE):
                mnemonico = acortador_opcode(INH[i])
                mnemonico = eliminar_espacios(mnemonico)
                stack_compiler_vls.append((mnemonico.upper(), instruccion, "ns", line, grupos[2]))
                stack_compiler_s19.append(mnemonico.upper())   
                stack_compiler_html.append((mnemonico.upper(), "r", "inherente", "n", instruccion, "ns", line,  grupos[2])) 

def compilado_ALL5(instruccion, IMM, DIR, EXT, INDX, INDY, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios):
    
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
                compilado_operandos(instruccion, hex_act[3][1:], grupos[5], mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line)
    
    elif re.fullmatch(ER_DIR, instruccion):
        grupos = re.split(ER_DIR, instruccion)

        if re.fullmatch(r"JSR", grupos[1], flags= re.IGNORECASE):
            stack_compiler_vls.append(("9D", instruccion, "sc", line, grupos[2]))
            stack_compiler_s19.append("9D")   
            stack_compiler_html.append(("9D", "r", "salto", "b", instruccion, "sc", line, grupos[2]))
        else:
            for i in range (len(DIR)):
                if re.fullmatch(acortador_mnemonicos(DIR[i]), grupos[1],  flags= re.IGNORECASE):
                    instruccion = conversor_operandos(instruccion, grupos[3])
                    hex_act = re.split(ER_DIR, instruccion)
                    mnemonico = acortador_opcode(DIR[i])
                    mnemonico = eliminar_espacios(mnemonico)
                    insbytes = acortador_bytes(DIR[i])
                    oprbytes = (len(hex_act[3][1:]) / 2)
                    compilado_operandos(instruccion, hex_act[3][1:], grupos[5], mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line)

    elif re.fullmatch(ER_EXT, instruccion):
        grupos = re.split(ER_EXT, instruccion)

        if re.fullmatch(r"JSR", grupos[1], flags= re.IGNORECASE):
            stack_compiler_vls.append(("BD", instruccion, "sc", line, grupos[2]))
            stack_compiler_s19.append("BD")   
            stack_compiler_html.append(("BD", "r", "salto", "b", instruccion, "sc", line, grupos[2]))
        elif re.fullmatch(r"JMP", grupos[1], flags= re.IGNORECASE):
            stack_compiler_vls.append(("7E", instruccion, "sc", line, grupos[2]))
            stack_compiler_s19.append("7E")   
            stack_compiler_html.append(("7E", "r", "salto", "b", instruccion, "sc", line, grupos[2]))
        else:
            for i in range (len(EXT)):
                if re.fullmatch(acortador_mnemonicos(EXT[i]), grupos[1],  flags= re.IGNORECASE):
                    instruccion = conversor_operandos(instruccion, grupos[3])
                    hex_act = re.split(ER_EXT, instruccion)
                    mnemonico = acortador_opcode(EXT[i])
                    mnemonico = eliminar_espacios(mnemonico)
                    insbytes = acortador_bytes(EXT[i])
                    oprbytes = (len(hex_act[3][1:]) / 2)
                    compilado_operandos(instruccion, hex_act[3][1:], grupos[5], mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line)

    elif re.fullmatch(ER_INDX, instruccion):
        grupos = re.split(ER_INDX, instruccion)

        if re.fullmatch(r"JSR", grupos[1], flags= re.IGNORECASE):
            stack_compiler_vls.append(("AD", instruccion, "sc", line, grupos[2]))
            stack_compiler_s19.append("AD")   
            stack_compiler_html.append(("AD", "r", "salto", "b", instruccion, "sc", line, grupos[2]))
        elif re.fullmatch(r"JMP", grupos[1], flags= re.IGNORECASE):
            stack_compiler_vls.append(("6E", instruccion, "sc", line, grupos[2]))
            stack_compiler_s19.append("6E")   
            stack_compiler_html.append(("6E", "r", "salto", "b", instruccion, "sc", line, grupos[2]))
        else:
            for i in range (len(INDX)):
                if re.fullmatch(acortador_mnemonicos(INDX[i]), grupos[1],  flags= re.IGNORECASE):
                    instruccion = conversor_operandos(instruccion, grupos[3])
                    hex_act = re.split(ER_INDX, instruccion)
                    mnemonico = acortador_opcode(INDX[i])
                    mnemonico = eliminar_espacios(mnemonico)
                    insbytes = acortador_bytes(INDX[i])
                    oprbytes = (len(hex_act[3][1:]) / 2)
                    compilado_operandos(instruccion, hex_act[3][1:], grupos[5], mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line)

    elif re.fullmatch(ER_INDY, instruccion):
        grupos = re.split(ER_INDY, instruccion)
        if re.fullmatch(r"JSR", grupos[1], flags= re.IGNORECASE):
            stack_compiler_vls.append(("18AD", instruccion, "sc", line, grupos[2]))
            stack_compiler_s19.append("18AD")   
            stack_compiler_html.append(("18AD", "r", "salto", "b", instruccion, "sc", line, grupos[2]))
        elif re.fullmatch(r"JMP", grupos[1], flags= re.IGNORECASE):
            stack_compiler_vls.append(("186E", instruccion, "sc", line, grupos[2]))
            stack_compiler_s19.append("186E")   
            stack_compiler_html.append(("186E", "r", "salto", "b", instruccion, "sc", line, grupos[2]))
        else:
            for i in range (len(INDY)):
                if re.fullmatch(acortador_mnemonicos(INDY[i]), grupos[1],  flags= re.IGNORECASE):
                    instruccion = conversor_operandos(instruccion, grupos[3])
                    hex_act = re.split(ER_INDY, instruccion)
                    mnemonico = acortador_opcode(INDY[i])
                    mnemonico = eliminar_espacios(mnemonico)
                    insbytes = acortador_bytes(INDY[i])
                    oprbytes = (len(hex_act[3][1:]) / 2)
                    compilado_operandos(instruccion, hex_act[3][1:], grupos[5], mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line)

def compilado(instruccion, operando, comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line):
    stack_compiler_vls.append((mnemonico+operando, instruccion, "ns", line, comentario))
    stack_compiler_s19.append(mnemonico+operando)   
    stack_compiler_html.append((mnemonico, "r", operando, "b", instruccion, "ns", line, comentario)) 

def compilado_operandos(instruccion, operando, comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line):
    if insbytes == 2:
        if len(mnemonico) == 2 and oprbytes == 1:
            compilado(instruccion, operando.upper(), comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line)
        else:
            stack_error.append(CONS_007+str(line))
    elif insbytes == 3:
        if len(mnemonico) == 2 and oprbytes == 2:
            compilado(instruccion, operando.upper(), comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line)
        elif len(mnemonico) == 4 and oprbytes == 1:
            compilado(instruccion, operando.upper(), comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line)
        else:
            stack_error.append(CONS_007+str(line))
    elif insbytes == 4:
        if len(mnemonico) == 4  and oprbytes == 2:
            compilado(instruccion, operando.upper(), comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line)        
        else:
            stack_error.append(CONS_007+str(line))
            
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