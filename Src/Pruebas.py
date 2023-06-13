import re
from Precompilado import *
from Funciones_apoyo import  *

def pruebas():

    #ABRIR MNEMONICOS
    REL = []
    f_rel = open("REL.txt", "r")
    for line in f_rel :
        REL.append(line)
    f_rel.close()

    INH = []
    f_inh = open("INH.txt", "r")
    for line in f_inh :
        INH.append(line)
    f_inh.close()

    IMM = []
    f_imm = open("IMM.txt", "r")
    for line in f_imm :
        IMM.append(line)
    f_imm.close()

    DIR = []
    f_dir = open("DIR.txt", "r")
    for line in f_dir :
        DIR.append(line)
    f_dir.close()

    EXT = []
    f_ext = open("EXT.txt", "r")
    for line in f_ext :
        EXT.append(line)
    f_ext.close()

    INDX = []
    f_indx = open("INDX.txt", "r")
    for line in f_indx :
        INDX.append(line)
    f_indx.close()

    INDY = []
    f_indy = open("INDY.txt", "r")
    for line in f_indy :
        INDY.append(line)
    f_indy.close()
    #---------------------------------------------

    #EXPRESIONES REGULARES PARA CPSAS QUE NO SON INSTRUCCIONES

    variables = re.compile(r"(([A-Z0-9]|\_)+)((\s)+EQU(\s)+)(\$00[0-9A-F]{2})", flags=re.IGNORECASE) #acepta simbolos en los nombres
    constantes = re.compile(r"(([A-Z0-9]|\_)+)(\s)+(EQU)(\s)+(\$10[0-9A-F]{2})", flags=re.IGNORECASE) #acepta simbolos en los nombres
    comentarios = re.compile(r"(\*(\w|\W)*)")
    etiquetas = re.compile(r"(([A-Z]|[\_])*)", flags=re.IGNORECASE) #no debe detectar espacios ni lineas en blanco

    #ARREGLOS PARA EL COMPILADO

    stack_compiler_vls = [] #(codigo objeto, linea de codigo original, sc , dir_mem, comentario)
    stack_compiler_s19 = [] #(codigo objeto en pila)
    stack_compiler_html = [] #(codigo objeto mne, color mne, codigo objeto op, color op, linea de codigo original, sc , dir_mem, comentario)
    stack_error = [] #(cadenas con los errores)
    list_labels = [] #(cadenas con las etiquetas)
    list_variables = []
    list_constantes = []
    list_comentarios = []
    line = 0
    dir_mem = hex(8000)

    with open("down.ASC","r") as archivo:

        for linea in archivo:
            
            linea = linea.rstrip() #se uso porque de alguna manera se tienen espacios, tabulaciones saltos a final de las lineas y las ER no detectan bien por eso
            if re.fullmatch(r'', linea):
                line +=1
            elif re.fullmatch(variables, linea):
                line +=1
                #print("se detecto una variable: " +linea)
                Matcher = re.split(variables, linea)
                list_variables.append((Matcher[1],Matcher[6]))
            elif re.fullmatch(constantes, linea):
                line +=1
                #print("se detecto una constante: " +linea)
                Matcher = re.split(constantes, linea)
                list_constantes.append((Matcher[1],Matcher[6]))
            elif re.fullmatch(comentarios, linea):
                line +=1
                list_comentarios.append((linea, line))
            elif re.fullmatch(etiquetas, linea) and verificar_palabra_reservada(linea):
                line +=1
                #print("se detecto una etiqueta: " +linea)
                list_labels.append((linea.strip(), hex(0), line))
            elif re.match(r'\s+', linea):
                line +=1
            else:
                line +=1
                stack_error.append(CONS_009+str(line))
    
    line = 0
    
    with open("down.ASC","r") as archivo:

        for linea in archivo:
            
            linea = linea.rstrip() #se uso porque de alguna manera se tienen espacios, tabulaciones saltos a final de las lineas y las ER no detectan bien por eso
            if re.fullmatch(r'', linea):
                line +=1
            elif re.fullmatch(variables, linea):
                line +=1
            elif re.fullmatch(constantes, linea):
                line +=1
            elif re.fullmatch(comentarios, linea):
                line +=1
            elif re.fullmatch(etiquetas, linea) and verificar_palabra_reservada(linea):
                line +=1
            elif re.match(r'\s+', linea):
                line +=1
                precompilado(linea.strip(), REL, INH, IMM, DIR, EXT, INDX, INDY, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios)
            else:
                line +=1
    
    print("PRUEBA CONSTANTES")
    for i in list_constantes:
        print(i)

    print("PRUEBA VARIABLES")
    for i in list_variables:
        print(i)

    print("PRUEBA COMENTARIOS")
    for i in list_comentarios:
        print(i)

    print("PRUEBA ETIQUETAS")
    for i in list_labels:
        print(i)

    print("PRUEBA ERRORES")
    for i in stack_error:
        print(i)

    print("PRUEBA VLS")
    for i in stack_compiler_vls:
        print(i)
    
    print("PRUEBA HTML")
    for i in stack_compiler_html:
        print(i)

pruebas()

