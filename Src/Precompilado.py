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
def verificar_palabra_reservada(texto):
    palabras = [
        'aba', 'abx', 'aby', 'adca', 'adcb', 'adda', 'addb', 'addd', 'anda', 'andb',
        'asl', 'asla', 'aslb', 'asld', 'asr', 'asra', 'asrb', 'bcc', 'bclr', 'bcs',
        'beq', 'bge', 'bgt', 'bhi', 'bhs', 'bita', 'bitb', 'ble', 'blo', 'bls', 'blt',
        'bmi', 'bne', 'bpl', 'bra', 'brclr', 'brn', 'brset', 'bset', 'bsr', 'bvc',
        'bvs', 'cba', 'clc', 'cli', 'clr', 'clra', 'clrb', 'clv', 'cmpa', 'cmpb', 'com',
        'coma', 'comb', 'cpd', 'cpx', 'cpy', 'daa', 'dec', 'deca', 'decb', 'des', 'dex',
        'dey', 'eora', 'eorb', 'fdiv', 'idiv', 'inc', 'inca', 'incb', 'ins', 'inx', 'iny',
        'jmp', 'jsr', 'ldaa', 'ldab', 'ldd', 'lds', 'ldx', 'ldy', 'lsl', 'lsla', 'lslb',
        'lsld', 'lsr', 'lsra', 'lsrb', 'lsrd', 'mul', 'neg', 'nega', 'negb', 'nop',
        'oraa', 'orab', 'psha', 'pshb', 'pshx', 'pshy', 'pula', 'pulb', 'pulx', 'puly',
        'rol', 'rola', 'rolb', 'ror', 'rora', 'rorb', 'rti', 'rts', 'sba', 'sbca', 'sbcb',
        'sec', 'sei', 'sev', 'staa', 'stab', 'std', 'stop', 'sts', 'stx', 'sty', 'suba',
        'subb', 'subd', 'swi', 'tab', 'tap', 'tba', 'tets', 'tpa', 'tst', 'tsta', 'tstb',
        'tsx', 'tsy', 'txs', 'tys', 'wai', 'xgdx', 'xgdy'
    ]

    control = False
    
    for palabra in palabras:
        if re.search(palabra, texto, flags=re.IGNORECASE ) :
            control = True
    
    return control

def precompilado(instruccion, REL, INH, IMM, DIR, EXT, INDX, INDY, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error, line, list_labels,list_variables, list_constantes, list_comentarios, dir_mem):
    ER_REL = re.compile(r"^(B[CEGHLMNPRSV][ACEILNOQRST])(\s*[\w]{1,256})?(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
    ER_INH = re.compile(r"^([ACDFILMNPRSTWX][ABDEGLNOPSTUWXY][ABCDGHILMOPRSTVXY][ABDPSVXY]?)(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
    ER_ALL5 = re.compile(r"^([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s*#|\s*){1}(\d{1,5}|\$[0-9A-F]{2,4}|'\S{1}|%[0-1]{1,16}|\w+)(,[XY])?(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
    ER_IMM = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?)(\s#)(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1}|%[0-1]{1,16})(\s\*[A-Z]*)?", flags= re.IGNORECASE) #se tiene que cambiar lo de los operandos
    ER_DIR = re.compile(r"^([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?[RT]?)(\s){1}(\d{1,3}|^\$[0-9A-F]{2}$|'\S{1}|%[0-1]{1,8}|\w+)(\s*\*\s[A-Z]*)?$", flags= re.IGNORECASE)
    ER_EXT = re.compile(r"^([ABCDEIJLNORST][BDEILMNOPRSTU][ABCDGLMPRSTXY][ABD]?)(\s){1}(\d{1,5}|^\$[0-9A-F]{2,4}$|'\S{1}|%[0-1]{1,16}|\w+)(\s*\*\s[A-Z]*)?$", flags=re.IGNORECASE)
    ER_INDX = re.compile(r"^([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s){1}(\d{1,5}|^\$[0-9A-F]{2,4}$|'\S{1}|%[0-1]{1,16}|\w+)(\s*\*\s[A-Z]*)?(,X)(\s\*[A-Z]*)?$", flags= re.IGNORECASE)
    ER_INDY = re.compile(r"^([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s){1}(\d{1,5}|^\$[0-9A-F]{2,4}$|'\S{1}|%[0-1]{1,16}|\w+)(\s*\*\s[A-Z]*)?(,Y)(\s\*[A-Z]*)?$", flags= re.IGNORECASE)
   

    
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
 
    elif re.fullmatch(ER_ALL5, instruccion):
        grupos = re.split(ER_ALL5, instruccion)
        if verificar_palabra_reservada(grupos[1]):
            print("Existe la palabra rservada:"+instruccion)
            if re.fullmatch(r"\w+", grupos[3]):
                nombre = grupos[3]
                for i in range (len(list_variables)):
                    if grupos[3] == list_variables[i][0]:
                        instruccion = instruccion.replace(grupos[3], list_variables[i][1])
                        nombre = nombre.replace(grupos[3], list_variables[i][1])
                if nombre == grupos[3]:
                    stack_error.append(CONS_002+str(line))
                
                for i in range (len(list_constantes)):
                    if grupos[3] == list_constantes[i][0]:
                        instruccion = instruccion.replace(grupos[3], list_constantes[i][1])
                        nombre = nombre.replace(grupos[3], list_constantes[i][1])
                if nombre == grupos[3]:
                    stack_error.append(CONS_001+str(line))

                print("Se asigno un valor:"+instruccion)
                

                """
                for i, j  in zip (list_variables, list_constantes):
                    if grupos[3] == list_variables[i][0]:
                        instruccion = instruccion.replace(grupos[3], list_variables[i][0])
                    else:
                        stack_error.append(CONS_002+str(line))
                    if grupos[3] == list_constantes[j][0]:
                        instruccion = instruccion.replace(grupos[3], list_variables[i][0])
                    else:
                        stack_error.append(CONS_001+str(line))
                """

        else:
            stack_error.append(CONS_004+str(line))

        """
        #PRINTS DE CONTROL DE GRUPOS
        print("instruccion original:",instruccion)
        print("Grupos subdivididos:")
        print("grupo1:")
        print(grupos[1])
        print("grupo2:")
        print(grupos[2])
        print("grupo3:")
        print(grupos[3])
        print("grupo4:")
        print(grupos[4])
        print("grupo5:")
        print(grupos[5])
        #for i, grupo in enumerate(grupos.groups(), start=1):
           # print("grupo:"+str(i)+ grupo[i])
            #print(f"Grupo {i}: {grupo}")
        print("----------------------------------------")
    else:
        print("instruccinstruccion no coincide con el patrón:"+instruccion)
        print("----------------------------------------")
        """