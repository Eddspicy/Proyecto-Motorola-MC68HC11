import re
from Funciones_apoyo import  *

#DESCRIPCION
"""
Esta función se encarga de preprocesar las instrucciones relativas, mediante una expresión regulas especializada vuelve a comprobar que la instrucción si sea relativa. Después compara su mnemonico
con una lista de mnemonicos relativos, si hace match con alguno toma su op code y lo guarda. En los arreglos de compilación se guarda el opcode de la instrucción, su dirección de memoria e idnicadores
para que el programa rccuerde que estas instrucciones deben volverse a compilar por la parte de los saltos.
"""

def compilado_RELpt1(instruccion, REL, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios, dir_mem):
    if re.fullmatch(ER_REL, instruccion):
        grupos = re.split(ER_REL, instruccion)
        for i in range (len(REL)):
            if re.fullmatch(acortador_mnemonicos(REL[i]), grupos[1],  flags= re.IGNORECASE):
                mnemonico = acortador_opcode(REL[i])
                mnemonico = eliminar_espacios(mnemonico)
                temporal = int(dir_mem[0][2:], 16) + incremento_memoria(len(mnemonico)) + 1
                dir_mem[0] = dir_mem[0].replace(dir_mem[0], hex(temporal))
                stack_compiler_vls.append((mnemonico.upper(), instruccion, "sc", line, dir_mem[0], grupos[3]))
                stack_compiler_s19.append((mnemonico.upper(), "sc", line))   
                stack_compiler_html.append((mnemonico.upper(), "red", "relativo", "blue", instruccion, "sc", line, dir_mem[0], grupos[3]))

#DESCRIPCION
"""
Mediante una expresión regular especializaada, se compruba que efectivamente la isntrucción sea inhenrente, luego se compara contra una lista de mnemonicos inherentes. Al hacer macth con algun mnemonico
inherente, el op code, la dirección de memoria generada, la linea de la isntrucción y algunos elemento más se guardan en los arreglos de compilación, indicando que estas isntrucciones por su naturaleza
ya estan totalmente compiladas.
"""
def compilado_INH(instruccion, INH, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios, dir_mem):
    if re.fullmatch(ER_INH, instruccion):
        grupos = re.split(ER_INH, instruccion)
        for i in range (len(INH)):
            if re.fullmatch(acortador_mnemonicos(INH[i]), grupos[1],  flags= re.IGNORECASE):
                mnemonico = acortador_opcode(INH[i])
                mnemonico = eliminar_espacios(mnemonico)
                temporal = int(dir_mem[0][2:], 16) + incremento_memoria(len(mnemonico))
                dir_mem[0] = dir_mem[0].replace(dir_mem[0], hex(temporal))
                stack_compiler_vls.append((mnemonico.upper(), instruccion, "ns", line, dir_mem[0], grupos[2]))
                stack_compiler_s19.append((mnemonico.upper(), "ns", line))   
                stack_compiler_html.append((mnemonico.upper(), "red", "inherente", "black", instruccion, "ns", line, dir_mem[0], grupos[2])) 

#DESCRIPCION
"""
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

        if re.fullmatch(r"JSR", grupos[1], flags= re.IGNORECASE):
            temporal = int(dir_mem[0][2:], 16) + incremento_memoria(2) + 1
            dir_mem[0] = dir_mem[0].replace(dir_mem[0], hex(temporal))
            stack_compiler_vls.append(("9D", instruccion, "sc", line, dir_mem[0], grupos[2]))
            stack_compiler_s19.append(("9D", "sc", line))   
            stack_compiler_html.append(("9D", "red", "salto", "blue", instruccion, "sc", line, dir_mem[0], grupos[2]))
        else:
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

        if re.fullmatch(r"JSR", grupos[1], flags= re.IGNORECASE):
            temporal = int(dir_mem[0][2:], 16) + incremento_memoria(2) + 1
            dir_mem[0] = dir_mem[0].replace(dir_mem[0], hex(temporal))
            stack_compiler_vls.append(("BD", instruccion, "sc", line, dir_mem[0], grupos[2]))
            stack_compiler_s19.append(("BD", "sc", line))   
            stack_compiler_html.append(("BD", "red", "salto", "blue", instruccion, "sc", line, dir_mem[0], grupos[2]))
        elif re.fullmatch(r"JMP", grupos[1], flags= re.IGNORECASE):
            temporal = int(dir_mem[0][2:], 16) + incremento_memoria(2) + 1
            dir_mem[0] = dir_mem[0].replace(dir_mem[0], hex(temporal))
            stack_compiler_vls.append(("7E", instruccion, "sc", line,dir_mem[0], grupos[2]))
            stack_compiler_s19.append(("7E", "sc",line))   
            stack_compiler_html.append(("7E", "red", "salto", "blue", instruccion, "sc", line, dir_mem[0], grupos[2]))
        else:
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

        if re.fullmatch(r"JSR", grupos[1], flags= re.IGNORECASE):
            temporal = int(dir_mem[0][2:], 16) + incremento_memoria(2) + 1
            dir_mem[0] = dir_mem[0].replace(dir_mem[0], hex(temporal))
            stack_compiler_vls.append(("AD", instruccion, "sc", line, dir_mem[0], grupos[2]))
            stack_compiler_s19.append(("AD", "sc", line))   
            stack_compiler_html.append(("AD", "red", "salto", "blue", instruccion, "sc", line,dir_mem[0], grupos[2]))
        elif re.fullmatch(r"JMP", grupos[1], flags= re.IGNORECASE):
            temporal = int(dir_mem[0][2:], 16) + incremento_memoria(2) + 1
            dir_mem[0] = dir_mem[0].replace(dir_mem[0], hex(temporal))
            stack_compiler_vls.append(("6E", instruccion, "sc", line,dir_mem[0], grupos[2]))
            stack_compiler_s19.append(("6E", "sc", line))   
            stack_compiler_html.append(("6E", "red", "salto", "blue", instruccion, "sc", line,dir_mem[0], grupos[2]))
        else:
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
        if re.fullmatch(r"JSR", grupos[1], flags= re.IGNORECASE):
            temporal = int(dir_mem[0][2:], 16) + incremento_memoria(2) + 1
            dir_mem[0] = dir_mem[0].replace(dir_mem[0], hex(temporal))
            stack_compiler_vls.append(("18AD", instruccion, "sc", line, dir_mem[0], grupos[2]))
            stack_compiler_s19.append(("18AD", "sc", line))   
            stack_compiler_html.append(("18AD", "red", "salto", "blue", instruccion, "sc", line, dir_mem[0], grupos[2]))
        elif re.fullmatch(r"JMP", grupos[1], flags= re.IGNORECASE):
            temporal = int(dir_mem[0][2:], 16) + incremento_memoria(2) + 1
            dir_mem[0] = dir_mem[0].replace(dir_mem[0], hex(temporal))
            stack_compiler_vls.append(("186E", instruccion, "sc", line, dir_mem[0],  grupos[2]))
            stack_compiler_s19.append(("186E", "sc", line))   
            stack_compiler_html.append(("186E", "red", "salto", "blue", instruccion, "sc", line, dir_mem[0], grupos[2]))
        else:
            for i in range (len(INDY)):
                if re.fullmatch(acortador_mnemonicos(INDY[i]), grupos[1],  flags= re.IGNORECASE):
                    instruccion = conversor_operandos(instruccion, grupos[3])
                    hex_act = re.split(ER_INDY, instruccion)
                    mnemonico = acortador_opcode(INDY[i])
                    mnemonico = eliminar_espacios(mnemonico)
                    insbytes = acortador_bytes(INDY[i])
                    oprbytes = (len(hex_act[3][1:]) / 2)
                    compilado_operandos(instruccion, hex_act[3][1:], grupos[5], mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)
#DESCRIPCION
"""
"""
def compilado(instruccion, operando, comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem):
    temporal = int(dir_mem[0][2:], 16) + incremento_memoria(len(mnemonico+operando))
    dir_mem[0] = dir_mem[0].replace(dir_mem[0], hex(temporal))
    stack_compiler_vls.append((mnemonico+operando, instruccion, "ns", line,dir_mem[0],  comentario))
    stack_compiler_s19.append((mnemonico+operando, "ns", line))   
    stack_compiler_html.append((mnemonico, "red", operando, "blue", instruccion, "ns", line, dir_mem[0], comentario)) 

#DESCRIPCION
"""
"""
def compilado_operandos(instruccion, operando, comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem):
    if insbytes == 2:
        if len(mnemonico) == 2 and oprbytes == 1:
            compilado(instruccion, operando.upper(), comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)
        else:
            stack_error.append(CONS_007+str(line))
    elif insbytes == 3:
        if len(mnemonico) == 2 and oprbytes == 2:
            compilado(instruccion, operando.upper(), comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)
        elif len(mnemonico) == 4 and oprbytes == 1:
            compilado(instruccion, operando.upper(), comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)
        else:
            stack_error.append(CONS_007+str(line))
    elif insbytes == 4:
        if len(mnemonico) == 4  and oprbytes == 2:
            compilado(instruccion, operando.upper(), comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem)        
        else:
            stack_error.append(CONS_007+str(line))
#DESCRIPCION
"""
"""            
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