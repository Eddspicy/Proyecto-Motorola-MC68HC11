import re
from Compilado import  *
from Funciones_apoyo import  *

def precompilado(instruccion, REL, INH, IMM, DIR, EXT, INDX, INDY, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios, dir_mem):
    #Matcher =[ ,mnemonico, espaacio_gato_ect, operando, comentario, ] [0,1,2,3,4,5,6]
    if re.match(ER_REL, instruccion):
        grupos = re.split(ER_REL, instruccion)
        
        nombre = grupos[2]
        if re.fullmatch(r"(\s+[\w]{1,256})?", grupos[2], flags= re.IGNORECASE):
            for i in range (len(list_labels)):
                if nombre.strip() == list_labels[i][0]:
                    instruccion = instruccion.replace(grupos[2], " "+list_labels[i][0])
                    nombre = nombre.replace(nombre, "etiqueta")
            compilado_RELpt1(instruccion, REL, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios, dir_mem)
        if nombre == grupos[2].strip():
            stack_error.append(CONS_003+str(line))
        print("instruccion relativa:"+instruccion)

    elif re.fullmatch(ER_INH, instruccion): #Aqui va el error de instrucción no lleva operando, pero lo puse abajo
        print("instruccion inherente:"+instruccion)
        compilado_INH(instruccion, INH, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios, dir_mem)
 
    elif re.match(ER_ALL5, instruccion):
        grupos = re.split(ER_ALL5, instruccion)
        
        if verificar_palabra_reservadainv(grupos[1]):
            print("Existe la palabra rservada:"+instruccion)
            
            if re.fullmatch(ER_OP, grupos[3]) != None:
                if re.fullmatch(r"[0-9]+", grupos[3]):
                    print("No se requiere hacer cambio de variable:"+instruccion)
            
                elif re.fullmatch(r"\w+", grupos[3], flags= re.IGNORECASE):
                
                    nombre = grupos[3]
                    #COMPROBACION DE VARIABLES
                    for i in range (len(list_variables)):
                        if grupos[3] == list_variables[i][0]:
                            instruccion = instruccion.replace(grupos[3], list_variables[i][1])
                            nombre = nombre.replace(grupos[3], "variable")
                
                    #COMPROBACION DE CONSTANTES
                    for i in range (len(list_constantes)):
                        if grupos[3] == list_constantes[i][0]:
                            instruccion = instruccion.replace(grupos[3], list_constantes[i][1])
                            nombre = nombre.replace(grupos[3], "constante")
                
                    #COMPROBACION DE ETIQUETAS
                    for i in range (len(list_labels)):
                        if nombre.strip() == list_labels[i][0]:
                            instruccion = instruccion.replace(grupos[3], " "+list_labels[i][0])
                            nombre = nombre.replace(nombre, "etiqueta")

                    if nombre == grupos[3]:
                        stack_error.append(CONS_001+str(line))
                    if nombre == grupos[3]:
                        stack_error.append(CONS_002+str(line))
                    if nombre == grupos[3].strip():
                        stack_error.append(CONS_003+str(line))

                    print("Se asigno un valor:"+instruccion) #LLAMAR A COMPILADO AQUÍ SI ES VARIABLE, CONSTANTE O ETIQUETA
                    compilado_ALL5(instruccion, IMM, DIR, EXT, INDX, INDY, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios, dir_mem)

                else:# PARA CASOS DONDE NO ES VARIABLE, CONSTANTE O ETIQUETA
                    compilado_ALL5(instruccion, IMM, DIR, EXT, INDX, INDY, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios, dir_mem)
            else:
                stack_error.append(CONS_005+str(line))
        else:
            stack_error.append(CONS_004+str(line))
    else:
        stack_error.append(CONS_006+str(line)) #falta tratar directiva fcb para que no llegue aqui