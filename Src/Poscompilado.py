import re
from Funciones_apoyo import  *

#DESCRIPCION
"""
Este archivo esta destinado a terminar la compilación, calculando los saltos para las instrucciones con saltos.

"""


#DESCRIPCION
"""
Esta función recorre los arreglos de instrucciones compiladas para identificar las instrucciones relativas mediante su expresión regular y el indicador que se le puso en la parte de compilado "sc o second compile".
Cuando se identifica una instrucción relativa se divide en subgrupos según la expresión regular relativa, con la etiqueta, los arreglos de compilación y el archivo del programa se calcula la distancia entre la instruccion 
y a donde quiere ir, con ellos se identifica si la etiqueta esta despues o antes de donde se llamó. Luego de que la función identifica si la etiqueta esta antes o despues calcula el valor del salto realizando una resta de direciones de memoria
y obteniendo su complemento "A2", también verifica que el salto no vaya más alla de 127 o 128 bytes según la dirección del mismo, si el salto supera los bytes máximos se provoca el error "salto relativo muy lejano". De lo contrario
se agrega de nuevo a los arreglos de compilación la instrucción realtiva totalmente compilada con su operando de salto.
"""
def compilado_RELpt2(file_name, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, list_labels):
    for i in range (len(stack_compiler_vls)):
        if re.fullmatch(ER_REL, stack_compiler_vls[i][1]) and stack_compiler_vls[i][2] == "sc":
            grupos = re.split(ER_REL, stack_compiler_vls[i][1])
            diff = encuentra_linea(file_name, stack_compiler_vls[i][3], grupos[2].strip())
            find = int(stack_compiler_vls[i][3]) - diff

            if diff >= 1:
                for j in range (len(stack_compiler_vls)):
                    if stack_compiler_vls[j][3] == find:
                        rest =  int(stack_compiler_vls[i][4][2:],16) - int(stack_compiler_vls[j][4][2:],16)
                        opr = complemento_a_dos(rest)
                        if rest <= 128:
                            stack_compiler_vls.append((stack_compiler_vls[i][0]+opr, stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3] , stack_compiler_vls[i][4],  grupos[3]))
                            stack_compiler_s19.append((stack_compiler_vls[i][0]+opr, "ns",  stack_compiler_vls[i][3]))   
                            stack_compiler_html.append((stack_compiler_vls[i][0], "red", opr, "blue", stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3], stack_compiler_vls[i][4], grupos[3]))
                        else:
                            stack_error.append(CONS_008+str(stack_compiler_vls[i][3]))

            elif diff < 0:
                for j in range (len(stack_compiler_vls)):
                    if stack_compiler_vls[j][3] == find:
                        rest = int(stack_compiler_vls[j][4][2:],16) - int(stack_compiler_vls[i][4][2:],16)
                        opr = complemento_a_dos(rest)
                        if rest <= 127:
                            stack_compiler_vls.append((stack_compiler_vls[i][0]+opr, stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3] , stack_compiler_vls[i][4],  grupos[3]))
                            stack_compiler_s19.append((stack_compiler_vls[i][0]+opr, "ns", stack_compiler_vls[i][3]))   
                            stack_compiler_html.append((stack_compiler_vls[i][0], "red", opr, "blue", stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3], stack_compiler_vls[i][4], grupos[3]))
                        else:
                            stack_error.append(CONS_008+str(stack_compiler_vls[i][3]))

#DESCRIPCION
"""
Similar a las instrucciones relativas, se identifica con un marcador y su mnemonico las instrucciones de salto para el resto de modos que la usan. Al igual que en la función anterior, se identifica la dirección del salto
y se calcula su valor con la resta de direcciones de memoria y su complemento "A2" (parte de eso se realiza en la función "asigna operandos", implementarlo en una función ahorro reescribir el mismo codigo varias veces para cada direcionamiento), 
en este caso no importa la distancia del sato por lo cual no se toma en cuenta en comparación a las instrucciones relativas.
Finalmente se agregan a los arreglos de compilación las instrucciones totalmente compiladas y con el indicador de que no necesitan volver a ser procesadas "nc o no compile"
"""
def compilado_saltos(file_name, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, list_labels):
    for i in range (len(stack_compiler_vls)):
       # if (stack_compiler_vls[i][2] == "sc" and re.match(r"JSR", stack_compiler_vls[i][1], flags= re.IGNORECASE)) or  (stack_compiler_vls[i][2] == "sc" and  re.match(r"JSR", stack_compiler_vls[i][1], flags= re.IGNORECASE)):
        if stack_compiler_vls[i][2] == "sc" and re.match(r"JSR", stack_compiler_vls[i][1], flags= re.IGNORECASE):

            if re.fullmatch(ER_DIR, stack_compiler_vls[i][1]):
                grupos = re.split(ER_DIR, stack_compiler_vls[i][1])
                asigna_operandos(i, stack_compiler_vls,stack_compiler_s19,stack_compiler_html, file_name, grupos, grupos[4])
            elif re.fullmatch(ER_EXT, stack_compiler_vls[i][1]):
                grupos = re.split(ER_EXT, stack_compiler_vls[i][1])
                asigna_operandos(i, stack_compiler_vls,stack_compiler_s19,stack_compiler_html, file_name, grupos, grupos[4])
            elif re.fullmatch(ER_INDX, stack_compiler_vls[i][1]):
                grupos = re.split(ER_DIR, stack_compiler_vls[i][1])
                asigna_operandos(i, stack_compiler_vls,stack_compiler_s19,stack_compiler_html, file_name, grupos, grupos[5])
            elif re.fullmatch(ER_INDY, stack_compiler_vls[i][1]):
                grupos = re.split(ER_DIR, stack_compiler_vls[i][1])
                asigna_operandos(i, stack_compiler_vls,stack_compiler_s19,stack_compiler_html, file_name, grupos, grupos[5])
            
            
        elif stack_compiler_vls[i][2] == "sc" and  re.match(r"JMP", stack_compiler_vls[i][1], flags= re.IGNORECASE):
            
            if re.fullmatch(ER_EXT, stack_compiler_vls[i][1]):
                grupos = re.split(ER_EXT, stack_compiler_vls[i][1])
                asigna_operandos(i, stack_compiler_vls,stack_compiler_s19,stack_compiler_html, file_name, grupos, grupos[4])
            elif re.fullmatch(ER_INDX, stack_compiler_vls[i][1]):
                grupos = re.split(ER_DIR, stack_compiler_vls[i][1])
                asigna_operandos(i, stack_compiler_vls,stack_compiler_s19,stack_compiler_html, file_name, grupos, grupos[5])
            elif re.fullmatch(ER_INDY, stack_compiler_vls[i][1]):
                grupos = re.split(ER_DIR, stack_compiler_vls[i][1])
                asigna_operandos(i, stack_compiler_vls,stack_compiler_s19,stack_compiler_html, file_name, grupos, grupos[5])
            
 
def asigna_operandos(i, stack_compiler_vls,stack_compiler_s19,stack_compiler_html, file_name, grupos, comentario):
    
    if re.fullmatch(r"\$[0-9A-F]{2,4}", grupos[3], flags= re.IGNORECASE):
        stack_compiler_vls.append((stack_compiler_vls[i][0]+grupos[3][1:], stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3] , stack_compiler_vls[i][4],  comentario))
        stack_compiler_s19.append((stack_compiler_vls[i][0]+grupos[3][1:], "ns",  stack_compiler_vls[i][3]))   
        stack_compiler_html.append((stack_compiler_vls[i][0], "red", grupos[3][1:], "blue", stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3], stack_compiler_vls[i][4], comentario))
    else:
        diff = encuentra_linea(file_name, stack_compiler_vls[i][3], grupos[3].strip())

        find = int(stack_compiler_vls[i][3]) - diff

        if diff >= 1:
            for j in range (len(stack_compiler_vls)):
                if stack_compiler_vls[j][3] == find:
                    rest =  int(stack_compiler_vls[i][4][2:],16) - int(stack_compiler_vls[j][4][2:],16)
                    opr = complemento_a_dos(rest)
                    stack_compiler_vls.append((stack_compiler_vls[i][0]+opr, stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3] , stack_compiler_vls[i][4],  comentario))
                    stack_compiler_s19.append((stack_compiler_vls[i][0]+opr, "ns",  stack_compiler_vls[i][3]))   
                    stack_compiler_html.append((stack_compiler_vls[i][0], "red", opr, "blue", stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3], stack_compiler_vls[i][4], comentario))

        elif diff < 0:
            for j in range (len(stack_compiler_vls)):
                if stack_compiler_vls[j][3] == find:
                    rest = int(stack_compiler_vls[j][4][2:],16) - int(stack_compiler_vls[i][4][2:],16)
                    opr = complemento_a_dos(rest)
                    stack_compiler_vls.append((stack_compiler_vls[i][0]+opr, stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3] , stack_compiler_vls[i][4],  comentario))
                    stack_compiler_s19.append((stack_compiler_vls[i][0]+opr, "ns", stack_compiler_vls[i][3]))   
                    stack_compiler_html.append((stack_compiler_vls[i][0], "red", opr, "blue", stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3], stack_compiler_vls[i][4], comentario))