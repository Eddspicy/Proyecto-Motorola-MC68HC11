import re
from Funciones_apoyo import  *
from Precompilado import *
from Poscompilado import  *
from Archivos import  *

#DESCRIPCION
"""
    En este archivo se encuentra la función main del programa. Dicha función se encarga de abrir todos los archivos necesarios para la compilación: ya sea los mnemonicos y sus datos o el programa.
    También se encarga de declarar las variables o arreglos más importantes del programa y realizar un import sobre los demás archivos para llamar correctamente a todas las funciones necesarias para
    la compilación. Además en esta función existen algunos print de variables que permiten observar el flujo y correcta ejecución del compilador.
"""
#DESCRIPCION
"""
"""

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

    if ctrl == False:
        stack_error.append(CONS_010)
    else:
        borrar_linea("down.ASC", end)

    #DESCRIPCION
    """
        Los siguientes dos withopen se encargan del proceso principal de compilación mientras leen direcatamente del archivo el código ensamblador. El primer withopen con su ciclo for, se encarga de 
        reconocer algunas directivas, todas las constantes, variables y etiquetas del programa. Al reconocerlas las guarda en distintos arreglos para poder recurrir a ellas ordenadamente cuando sea
        necesario en la compilación. Se guardan algunas cosas adicionales como el numero de linea en que se encontraba cada cosa. Ignora la instrucciones, solo se dedica a lo mencionado para que todo eso}
        exista coherentemente cuando se procesen las instrucciones.

    """
            
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

    #DESCRIPCION
    """
    Este with open junto a su ciclo for se encarga de ignorar directivas, etiquetas, vaariables y constantes para dedicarse a reconocer las instriucciones y compilarlas ya con los datos de los elementos
    ignorados en este ciclo. Para las instrucciones primero se identifica que no caarezcan de un espacio relativo al margen y luego se procesan, para procesarlas se llama a la función de precompilado.
    """
    
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
    #DESCRIPCION
    """
    Se llaman a las funciones de poscompilado para compilar correctamente las intrucciones realtivas y las de saltos, pudiendo calcular el valor o dirección de memoria al que se debe realaizar el 
    salto cuando todas las dempas instrucciones ya fueron compiladas.
    """
    
    compilado_RELpt2("down.ASC", stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, list_labels)
    compilado_saltos("down.ASC", stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, list_labels)

#DESCRIPCION
    """
    Las siguientes lineas se encargan de depurar los arreglos de compilación, eliminan lineas reptidas, incompletas y elementos que ya no son necesarios luego de la compilación, además ordena todos
    los arreglos por número de linea y elimina de memoria todos los elementos inecesaarios.
    """
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
    
    #DESCRIPCION
    """
    Las siguientes lineas llaman a todas las funciones que crean los archivos de compilación del programa.
    """

    creacion_lst(list_comentarios, fostack_compiler_vls, list_labels, stack_error)
    creacion_HTML(list_comentarios, fostack_compiler_html, list_labels, stack_error)
    creacion_s19(fostack_compiler_s19)

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
"""
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
"""

main()