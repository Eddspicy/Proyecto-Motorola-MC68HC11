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
CONS_012 = "012   SE INGRESO ALGO QUE NADA QUE VER  - Error en linea:"

# PROCESAR VARIABLES Y CONSTANTES DESDE AQUI PARA MANDARLAS CON SU VALOR DE OPERANDO O GENERAR LOS ERRORES, VER QUE HACER CON JMP SI AQUI O ALLA

def precompilado(instruccion, REL, INH, IMM, DIR, EXT, INDX, INDY, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios, dir_mem):
    ER_REL = re.compile(r"\b((B[CEGHLMNPRSV][ACEILNOQRST])(\s[A-ZA-Z]{1,256})?(\s\*[A-Z]*)?)\b", flags= re.IGNORECASE)
    ER_INH = re.compile(r"([ACDFILMNPRSTWX][ABDEGLNOPSTUWXY][ABCDGHILMOPRSTVXY][ABDPSVXY]?)(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    ER_ALL5 = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s#|\s){1}(\d{1,5}|\$[0-9A-F]{2,4}||'\S{1}|%[0-1]{1,16}|(([A-Z0-9]|\_)+))(,[XY])?(\s*\*[A-Z]*)?", flags= re.IGNORECASE)
    #GP1 = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)")
    #GP2 = re.compile(r"(\s#|\s){1}")
    #GP3 = re.compile(r"(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1}|%[0-1]{1,16})")
    GP1 = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)", flags= re.IGNORECASE)
    GP2 = re.compile(r"(\s#|\s)")
    GP3 = re.compile(r"(\d{1,5}|\$[0-9A-F]{2,4}|'\S{1}|%[0-1]{1,16}|(([A-Z0-9]|\_)+))", flags= re.IGNORECASE)
    GP4 = re.compile(r"(,[XY])?", flags= re.IGNORECASE)
    GP5 = re.compile(r"(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    
    #Matcher =[ ,mnemonico, espaacio_gato_ect, operando, comentario, ] [0,1,2,3,4,5,6]
    if re.fullmatch(ER_REL, instruccion):
       #Matcher = re.split(REL, instruccion)
       # print(Matcher)
       #compilado_REL_p1(Matcher, mnemonicos_rel, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error,error_line, list_labels, dir_mem)
       print("instruccion relativa:"+instruccion)

    elif re.fullmatch(ER_INH, instruccion):
        #Matcher = re.split(INH, instruccion)
        #compilado_INH(Matcher, mnemonicos_inh, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error,error_line, list_labels, dir_mem)
        print("instruccion inherente:"+instruccion)
    else:
        Matcher = re.split(ER_ALL5, instruccion, maxsplit=2)
        print(Matcher)

    """
        print("Grupos de instruccion:"+str(line))
        if re.search(GP1, instruccion):
            Matcher = re.findall(GP1, instruccion)
            print(Matcher)
        if re.search(GP2, instruccion):
            Matcher = re.findall(GP2, instruccion)
            print(Matcher)
        if re.search(GP3, instruccion):
            Matcher = re.findall(GP3, instruccion)
            print(Matcher)
        if re.search(GP4, instruccion):
            Matcher = re.findall(GP4, instruccion)
            print(Matcher)
        if re.search(GP5, instruccion):
            Matcher = re.findall(GP5, instruccion)
            print(Matcher)
        print("fin del grupo")
    """


"""
    elif re.fullmatch(r"([A-Z])*",instruccion) == None and  re.fullmatch(ER_INH, instruccion) == None and  re.fullmatch(ER_REL, instruccion) == None:
        Matcher = re.split(ER_ALL5, instruccion)
        if re.fullmatch(GP1, Matcher[1]):
            #El mnemonico existe dentro de alguno de los 5 modos o es una subinstruccion de la ER valida
            if re.fullmatch(GP2, Matcher[2]):
                #La sintaxis es correcta para alguna de las 5
                if re.fullmatch(GP3,  Matcher[3]):
                    #El operando existe
                    #compilado_ALL5 (Matcher, mnemonicos_dir, mnemonicos_ext, mnemonicos_imm, mnemonicos_indx, mnemonicos_indy, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error,error_line, list_labels, dir_mem)
                    print("instruccion de cualquiera de los otros 4 modos:"+instruccion)
                    Matcher.clear
                else:
                    stack_error.append(CONS_005+str(line))
            else:
                stack_error.append(CONS_011+str(line))
    #DEBE HABER UN ELIF MAS PARA LA INSTRUCCION JMP
        else:
           stack_error.append(CONS_004+str(line))
    else:
        stack_error.append(CONS_012+str(line))
"""