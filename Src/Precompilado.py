import re
from Compilado import  *

#Errores
CONS_001 = "001   CONSTANTE INEXISTENTE - Error en linea:" #YA SE USO
CONS_002 = "002   VARIABLE INEXISTENTE - Error en linea:" #YA SE USO
CONS_003 = "003   ETIQUETA INEXISTENTE - Error en linea:" #YA SE USO
CONS_004 = "004   MNEMÓNICO INEXISTENTE - Error en linea:" #YA SE USO
CONS_005 = "005   INSTRUCCIÓN CARECE DE  OPERANDO(S) - Error en linea:" #YA SE USO
CONS_006 = "006   INSTRUCCIÓN NO LLEVA OPERANDO(S) - Error en linea:" #YA SE USO
CONS_007 = "007   MAGNITUD DE  OPERANDO ERRONEA - Error en linea:" 
CONS_008 = "008   SALTO RELATIVO MUY LEJANO - Error en linea:"
CONS_009 = "009   INSTRUCCIÓN CARECE DE ALMENOS UN ESPACIO RELATIVO AL MARGENE - Error en linea:" #YA SE USO
CONS_010 = "010   NO SE ENCUENTRA END - Error en linea:"

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
    ER_REL = re.compile(r"^(B[CEGHLMNPRSV][ACEILNOQRST])(\s+[\w]{1,256})?(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
    ER_INH = re.compile(r"^([ACDFILMNPRSTWX][ABDEGLNOPSTUWXY][ABCDGHILMOPRSTVXY][ABDPSVXY]?)(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
    ER_ALL5 = re.compile(r"^([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s*#|\s*){1}(\d{1,5}|\$[0-9A-F]{2,4}|'\S{1}|%[0-1]{1,16}|\w+)(,[XY])?(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
    ER_OP = re.compile(r"^(\d{1,5}|\$[0-9A-F]{2,4}|'\S{1}|%[0-1]{1,16}|\w+)(,[XY])?(\s*\*\s?[\w|\W]*)?$", flags= re.IGNORECASE)
    
    #Matcher =[ ,mnemonico, espaacio_gato_ect, operando, comentario, ] [0,1,2,3,4,5,6]
    if re.match(ER_REL, instruccion):
        grupos = re.split(ER_REL, instruccion)
        
        nombre = grupos[2]
        if re.fullmatch(r"(\s+[\w]{1,256})?", grupos[2], flags= re.IGNORECASE):
            for i in range (len(list_labels)):
                if nombre.strip() == list_labels[i][0]:
                    instruccion = instruccion.replace(grupos[2], " "+list_labels[i][0])
                    nombre = nombre.replace(nombre, "etiqueta")
        if nombre == grupos[2].strip():
            stack_error.append(CONS_003+str(line))
        print("instruccion relativa:"+instruccion)

    elif re.fullmatch(ER_INH, instruccion): #Aqui va el error de instrucción no lleva operando, pero lo puse abajo
        print("instruccion inherente:"+instruccion)
 
    elif re.match(ER_ALL5, instruccion):
        grupos = re.split(ER_ALL5, instruccion)
        
        if verificar_palabra_reservada(grupos[1]):
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
