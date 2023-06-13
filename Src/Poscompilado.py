import re
from Funciones_apoyo import  *

def compilado_RELpt2(file_name, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, list_labels):
    for i in range (len(stack_compiler_vls)):
        if re.fullmatch(ER_REL, stack_compiler_vls[i][1]) and stack_compiler_vls[i][2] == "sc":
            grupos = re.split(ER_REL, stack_compiler_vls[i][1])
            diff = encuentra_linea(file_name, stack_compiler_vls[i][3], grupos[2].strip())

            find = int(stack_compiler_vls[i][3]) - diff + 1

            if diff >= 1:
                for j in range (len(stack_compiler_vls)):
                    if stack_compiler_vls[j][3] == find:
                        rest =  int(stack_compiler_vls[i][4][2:],16) - int(stack_compiler_vls[j][4][2:],16)
                        opr = complemento_a_dos(rest)
                        if rest <= 128:
                            stack_compiler_vls.append((stack_compiler_vls[i][0]+opr, stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3] , stack_compiler_vls[i][4],  grupos[3]))
                            stack_compiler_s19.append(stack_compiler_vls[i][0]+opr)   
                            stack_compiler_html.append((stack_compiler_vls[i][0], "r", opr, "b", stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3], stack_compiler_vls[i][4], grupos[3]))
                        else:
                            stack_error.append(CONS_008+str(stack_compiler_vls[i][3]))

            elif diff < 0:
                find = find - 2
                for j in range (len(stack_compiler_vls)):
                    if stack_compiler_vls[j][3] == find:
                        rest = int(stack_compiler_vls[j][4][2:],16) - int(stack_compiler_vls[i][4][2:],16)
                        opr = complemento_a_dos(rest)
                        if rest <= 127:
                            stack_compiler_vls.append((stack_compiler_vls[i][0]+opr, stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3] , stack_compiler_vls[i][4],  grupos[3]))
                            stack_compiler_s19.append(stack_compiler_vls[i][0]+opr)   
                            stack_compiler_html.append((stack_compiler_vls[i][0], "r", opr, "b", stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3], stack_compiler_vls[i][4], grupos[3]))
                        else:
                            stack_error.append(CONS_008+str(stack_compiler_vls[i][3]))

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
        stack_compiler_s19.append(stack_compiler_vls[i][0]+grupos[3][1:])   
        stack_compiler_html.append((stack_compiler_vls[i][0], "r", grupos[3][1:], "b", stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3], stack_compiler_vls[i][4], comentario))
    else:
        diff = encuentra_linea(file_name, stack_compiler_vls[i][3], grupos[3].strip())

        find = int(stack_compiler_vls[i][3]) - diff + 1

        if diff >= 1:
            for j in range (len(stack_compiler_vls)):
                if stack_compiler_vls[j][3] == find:
                    rest =  int(stack_compiler_vls[i][4][2:],16) - int(stack_compiler_vls[j][4][2:],16)
                    opr = complemento_a_dos(rest)
                    stack_compiler_vls.append((stack_compiler_vls[i][0]+opr, stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3] , stack_compiler_vls[i][4],  comentario))
                    stack_compiler_s19.append(stack_compiler_vls[i][0]+opr)   
                    stack_compiler_html.append((stack_compiler_vls[i][0], "r", opr, "b", stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3], stack_compiler_vls[i][4], comentario))

        elif diff < 0:
            find = find - 2
            for j in range (len(stack_compiler_vls)):
                if stack_compiler_vls[j][3] == find:
                    rest = int(stack_compiler_vls[j][4][2:],16) - int(stack_compiler_vls[i][4][2:],16)
                    opr = complemento_a_dos(rest)
                    stack_compiler_vls.append((stack_compiler_vls[i][0]+opr, stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3] , stack_compiler_vls[i][4],  comentario))
                    stack_compiler_s19.append(stack_compiler_vls[i][0]+opr)   
                    stack_compiler_html.append((stack_compiler_vls[i][0], "r", opr, "b", stack_compiler_vls[i][1], "ns", stack_compiler_vls[i][3], stack_compiler_vls[i][4], comentario))