import re
from Precompilado import *
from Funciones_apoyo import  *
from Poscompilado import  *

def main():
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
    #ARREGLOS PARA EL COMPILADO

    stack_compiler_vls = [] #(codigo objeto, linea de codigo original, sc , line, dir_mem,  comentario)
    stack_compiler_s19 = [] #(codigo objeto en pila)
    stack_compiler_html = [] #(codigo objeto mne, color mne, codigo objeto op, color op, linea de codigo original, sc , line, dir_mem, comentario)
    stack_error = [] #(cadenas con los errores)
    list_labels = [] #(cadenas con las etiquetas)
    list_variables = []
    list_constantes = []
    list_comentarios = []
    line = 0
    ctrl = False
    end = ""
    org = []
    
    with open("down.ASC","r") as archivo:
        for linea in archivo:
            if re.fullmatch(r"^((END(\s)+\$8000?)|(END))$", linea.strip(), flags= re.IGNORECASE):
                ctrl = True
                end = linea.strip()
            if re.match(r"^((0RG)(\s+)(\$[A-F0-9)]{4}))$", linea.strip(), flags= re.IGNORECASE):
                org.append(linea.strip())

    for i in range (len(org)):
        borrar_linea("down.ASC", org[i]) 
    
    #SOLO EJECUTAR SI YA SE PRESENTARA O SE ESTA SEGURO DE LA COMPILACION

    if ctrl == False:
        stack_error.append(CONS_010)
    else:
        borrar_linea("down.ASC", end)
            
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
                precompilado(linea.strip(), REL, INH, IMM, DIR, EXT, INDX, INDY, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios, dir_mem)
            else:
                line +=1
    
    compilado_RELpt2("down.ASC", stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, list_labels)
    compilado_saltos("down.ASC", stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, list_labels)

    fstack_compiler_vls = []
    fstack_compiler_html = []
    fstack_compiler_s19 = []

    #linea en 3
    for i in range (len(stack_compiler_vls)):
        if stack_compiler_vls[i][2] == "ns":
            fstack_compiler_vls.append((stack_compiler_vls[i][0],stack_compiler_vls[i][1],stack_compiler_vls[i][2],stack_compiler_vls[i][3],stack_compiler_vls[i][4], stack_compiler_vls[i][5]))
    
    #linea en 6
    for i in range (len(stack_compiler_html)):
        if stack_compiler_html[i][5] == "ns":
            fstack_compiler_html.append((stack_compiler_html[i][0],stack_compiler_html[i][1],stack_compiler_html[i][2],stack_compiler_html[i][3],stack_compiler_html[i][4], stack_compiler_html[i][5],stack_compiler_html[i][6],stack_compiler_html[i][7],stack_compiler_html[i][8]))

    for i in range (len(stack_compiler_s19)):
        if stack_compiler_s19[i][1] == "ns":
            fstack_compiler_s19.append((stack_compiler_s19[i][0], stack_compiler_s19[i][2]))
    
    stack_compiler_vls.clear()
    stack_compiler_html.clear()
    stack_compiler_s19.clear()

    fostack_compiler_vls = sorted(fstack_compiler_vls, key=lambda x: x[3])
    fostack_compiler_html = sorted(fstack_compiler_html, key=lambda x: x[6])
    fostack_compiler_s19 = sorted(fstack_compiler_s19, key=lambda x: x[1])

    fstack_compiler_vls.clear()
    fstack_compiler_html.clear()
    fstack_compiler_s19.clear()

    creacion_lst(list_comentarios, fostack_compiler_vls, list_labels, stack_error)

#PRINTS DE CONTROL DE FLUJO
    print("-------------------------------------------------")
    print("PRUEBA CONSTANTES")
    for i in list_constantes:
        print(i)

    print("-------------------------------------------------")
    print("PRUEBA VARIABLES")
    for i in list_variables:
        print(i)

    print("-------------------------------------------------")
    print("PRUEBA COMENTARIOS")
    for i in list_comentarios:
        print(i)

    print("-------------------------------------------------")
    print("PRUEBA ETIQUETAS")
    for i in list_labels:
        print(i)

    print("-------------------------------------------------")
    print("PRUEBA ERRORES")
    for i in stack_error:
        print(i)

    print("-------------------------------------------------")
    print("PRUEBA VLS")
    for i in fostack_compiler_vls:
        print(i)

    print("-------------------------------------------------")    
    print("PRUEBA HTML")
    for i in fostack_compiler_html:
        print(i)
    
    print("-------------------------------------------------")
    print("PRUEBA S19")
    for i in fostack_compiler_s19:
        print(i)
    print("-------------------------------------------------")

main()

