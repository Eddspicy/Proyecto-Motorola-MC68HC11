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
Mediante una expresión regular especializaada, se compruba que efectivamente la instrucción sea inhenrente, luego se compara contra una lista de mnemonicos inherentes. Al hacer macth con algun mnemonico
inherente, el op code, la dirección de memoria generada, la linea de la instrucción y algunos elemento más se guardan en los arreglos de compilación, indicando que estas instrucciones por su naturaleza
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
Esta función se encarga de identificar explicitamente el modo de direccionamiento entre los modos inmediato, directo, extendido e indexado. Laa función identifica mediante expresiones regulares especializadas
para cada modo de direccionamiento y haciendo uso de la api de regex (expresiones regulares en python). Cuando la función identifica el modo de la instrucción, luego identiifca si es una instrucción de salto o no,
si es de salto se realiza un proceso similar al compilado de las instrucciones relativas para terminar de compilar con los saltos después. Para las instrucciones que no son de saltos, se verifica que el mnemonico de la
instrucción exista dentro del modo de direccionamiento, al realizarlo se identifica también el op code, los bytes de la instrucción y su operando; para compilar el operando se llama a la función "compilando operandos",
dicha función se encarga de identificar el sistema numerico del operando o el codigo ascii de un caracter para guardarlo de forma hexadecimal el dato del operando. Con todos los datos obtenidos se llama a la función
compilando operandos para continuaar con la compilación de una instrucción.
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
Con el op code, los bytes de instruccion, el operando procesado y algunos otros datos como el numero de linea se guarda en todos los arreglos de compilación los datos de la instruicción totlmente compilada para que 
a la hora de crear los archivos puedan mostrarse correctamente los bytes en hexadecimal de la compilación y el formato de cada archivo. Taabién se genera la dirección de memoria para la instrucción en conjunta, esta además
de ser guardada en los arrreglos de compilación, será util para calcular los saltos y poder obtrener la compilación completa de instrucciones de salto como las relativas.
"""
def compilado(instruccion, operando, comentario, mnemonico, insbytes, oprbytes, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, dir_mem):
    temporal = int(dir_mem[0][2:], 16) + incremento_memoria(len(mnemonico+operando))
    dir_mem[0] = dir_mem[0].replace(dir_mem[0], hex(temporal))
    stack_compiler_vls.append((mnemonico+operando, instruccion, "ns", line,dir_mem[0],  comentario))
    stack_compiler_s19.append((mnemonico+operando, "ns", line))   
    stack_compiler_html.append((mnemonico, "red", operando, "blue", instruccion, "ns", line, dir_mem[0], comentario)) 

#DESCRIPCION
"""
Esta función se asegura que el operando de la instrucción sea compatible con la misma y su modo, según la cantidad de bytes que puede tener la instrucción en el direccionamiento en que se identifico.
Si los bytes del op code la instruccion y el operando son compatibles segun la cantidad de bytes posibles entonces se llama ala función final de compilado. Si los bytes llegarán a no ser compatibles, se genera
el error de "magnitud de operando incorrecta"
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
Según el simbolo que tenga el operando antes de el, la función identifica su sistema numerico, o si es la obtención del codigo ascii de un caracter. Luego de identificar, la función trata al operando
para convertir sus datos en un dato hexadecimal que será parte de la instrucción.
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