import re
from Compilado import *



def precompilado(cadena, mnemonicos_dir,mnemonicos_ext,mnemonicos_imm, mnemonicos_indx, mnemonicos_indy, mnemonicos_inh, mnemonicos_rel, stack_compiler, stack_error,error_line, list_labels):
    REL = re.compile(r"(B[CEGHLMNPRSV][ACEILNOQRST])(\s[A-ZA-Z]{1,256})?(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    INH = re.compile(r"([ACDFILMNPRSTWX][ABDEGLNOPSTUWXY][ABCDGHILMOPRSTVXY][ABDPSVXY]?)(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    ALL5 = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?)(\s#|\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1})(,[XY])?(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    GP1 = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?)")
    GP2 = re.compile(r"(\s#|\s){1}")
    GP3 = re.compile(r"(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1})")
    
    if re.fullmatch(REL, cadena):
       Matcher = re.split(REL, cadena)
       # print(Matcher)
       compilado_REL(Matcher, mnemonicos_rel, stack_compiler, stack_error, error_line, list_labels)

    elif re.fullmatch(INH, cadena):
        Matcher = re.split(INH, cadena)
        compilado_INH(Matcher, mnemonicos_rel, stack_compiler, stack_error, error_line)

    elif re.fullmatch(r"([A-Z])*",cadena) == None and  re.fullmatch(INH, cadena) == None and  re.fullmatch(REL, cadena) == None:
        Matcher = re.split(ALL5, cadena)
        if re.fullmatch(GP1, Matcher[1]):
            print("El mnemonico existe dentro de los 5 modos")
            if re.fullmatch(GP2, Matcher[2]):
                print("La sintaxis es correcta para alguna de las 5")
                if re.fullmatch(GP3,  Matcher[3]):
                    print(Matcher)
                    print("El operando existe")
                    compilado_ALL5 (Matcher, mnemonicos_dir, mnemonicos_ext, mnemonicos_imm, mnemonicos_indx, mnemonicos_indy, stack_compiler, stack_error, error_line, list_labels)
                    Matcher.clear
                else:
                    print("No existe operadno")
            else:
                print("sintaxis incorrecta")
    #DEBE HABER UN ELIF MAS PARA LA INSTRUCCION JMP
        else:
            print("no existe el mnemonico")
    else:
        print("No se ajusta aningun caso conocido, error")