import re
from Compilado import *

#Errores
CONS_001 = "001   CONSTANTE INEXISTENTE - Error en linea:"
CONS_002 = "002   VARIABLE INEXISTENTE - Error en linea:"
CONS_003 = "003   ETIQUETA INEXISTENTE - Error en linea:"
CONS_004 = "004   MNEMÓNICO INEXISTENTE - Error en linea:" #YA SE USO
CONS_005 = "005   INSTRUCCIÓN CARECE DE  OPERANDO(S) - Error en linea:" #YA SE USO
CONS_006 = "006   INSTRUCCIÓN NO LLEVA OPERANDO(S) - Error en linea:"
CONS_007 = "007   MAGNITUD DE  OPERANDO ERRONEA - Error en linea:" #YA SE USO
CONS_008 = "008   SALTO RELATIVO MUY LEJANOE - Error en linea:"
CONS_009 = "009   INSTRUCCIÓN CARECE DE ALMENOS UN ESPACIO RELATIVO AL MARGENE - Error en linea:"
CONS_010 = "010   NO SE ENCUENTRA END - Error en linea:"
CONS_011 = "011   ERROR DE SINTAXIS  - Error en linea:" #YA SE USO

# PROCESAR VARIABLES Y CONSTANTES DESDE AQUI PARA MANDARLAS CON SU VALOR DE OPERANDO O GENERAR LOS ERRORES, VER QUE HACER CON JMP SI AQUI O ALLA

def precompilado(cadena, mnemonicos_dir,mnemonicos_ext,mnemonicos_imm, mnemonicos_indx, mnemonicos_indy, mnemonicos_inh, mnemonicos_rel, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error,error_line, list_labels, dir_mem):
    REL = re.compile(r"(B[CEGHLMNPRSV][ACEILNOQRST])(\s[A-ZA-Z]{1,256})?(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    INH = re.compile(r"([ACDFILMNPRSTWX][ABDEGLNOPSTUWXY][ABCDGHILMOPRSTVXY][ABDPSVXY]?)(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    ALL5 = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s#|\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1}|%[0-1]{1,16})(,[XY])?(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    GP1 = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)")
    GP2 = re.compile(r"(\s#|\s){1}")
    GP3 = re.compile(r"(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1}|%[0-1]{1,16})")
    
    #Matcher =[ ,mnemonico, espaacio_gato_ect, operando, comentario, ] [0,1,2,3,4,5,6]
    if re.fullmatch(REL, cadena):
       Matcher = re.split(REL, cadena)
       # print(Matcher)
       compilado_REL_p1(Matcher, mnemonicos_rel, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error,error_line, list_labels, dir_mem)

    elif re.fullmatch(INH, cadena):
        Matcher = re.split(INH, cadena)
        compilado_INH(Matcher, mnemonicos_inh, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error,error_line, list_labels, dir_mem)

    elif re.fullmatch(r"([A-Z])*",cadena) == None and  re.fullmatch(INH, cadena) == None and  re.fullmatch(REL, cadena) == None:
        Matcher = re.split(ALL5, cadena)
        if re.fullmatch(GP1, Matcher[1]):
            #El mnemonico existe dentro de alguno de los 5 modos o es una subcadena de la ER valida
            if re.fullmatch(GP2, Matcher[2]):
                #La sintaxis es correcta para alguna de las 5
                if re.fullmatch(GP3,  Matcher[3]):
                    #El operando existe
                    compilado_ALL5 (Matcher, mnemonicos_dir, mnemonicos_ext, mnemonicos_imm, mnemonicos_indx, mnemonicos_indy, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error,error_line, list_labels, dir_mem)
                    Matcher.clear
                else:
                    print("No existe operando")
                    stack_error.push(CONS_005+error_line)
            else:
                stack_error.push(CONS_011+error_line)
    #DEBE HABER UN ELIF MAS PARA LA INSTRUCCION JMP
        else:
           stack_error.push(CONS_004+error_line)
    else:
        stack_error.push("no se que poner aqui")