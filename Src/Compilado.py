import re

#Errores
CONS_001 = "001   CONSTANTE INEXISTENTE - Error en linea:"
CONS_002 = "002   VARIABLE INEXISTENTE - Error en linea:"
CONS_003 = "003   ETIQUETA INEXISTENTE - Error en linea:"
CONS_004 = "004   MNEMÓNICO INEXISTENTE - Error en linea:"
CONS_005 = "005   INSTRUCCIÓN CARECE DE  OPERANDO(S) - Error en linea:"
CONS_006 = "006   INSTRUCCIÓN NO LLEVA OPERANDO(S) - Error en linea:"
CONS_007 = "007   MAGNITUD DE  OPERANDO ERRONEA - Error en linea:"
CONS_008 = "008   SALTO RELATIVO MUY LEJANOE - Error en linea:"
CONS_009 = "009   INSTRUCCIÓN CARECE DE ALMENOS UN ESPACIO RELATIVO AL MARGEN - Error en linea:"
CONS_010 = "010   NO SE ENCUENTRA END - Error en linea:"

def compilado_REL (instruccion, mnemonicos, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error,error_line, list_labels): #FALTA COMPILACION DE ESTE MODO, ES DIFERENTE A LOS OTROS
    for i in mnemonicos:
        if instruccion[1] == acortador_mnemonicos(i):
            stack_compiler.push(acortador_opcode(i))
        #INTRODUCIR OPCODE DE LASA ETIQUETAS


def compilado_INH (instruccion, mnemonicos, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error,error_line, list_labels): #FALTA COMPILACION DE ESTE MODO, ES DIFERENTE A LOS OTROS
    tostr = "".join(instruccion)
    for i in mnemonicos:
        if instruccion[1] == acortador_mnemonicos(i):
                stack_compiler_vls.append((acortador_opcode(i),tostr,"no label", 0, instruccion[4]))
                stack_compiler_s19.push(acortador_opcode(i))
                stack_compiler_html.append((acortador_opcode(i),"r","no operando","b",tostr,"no label", 0, instruccion[4]))

#FALTA TAMBIEN HACER BIEN TODO LO DE LOS ERRORES, AUNQUE YA PUEDE GUARDARLOS

def compilado_ALL5 (instruccion, mnemonicos_dir, mnemonicos_ext, mnemonicos_imm, mnemonicos_indx, mnemonicos_indy, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error, error_line, list_labels):
    print("ALL5")
    IMM = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?)(\s#)(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1}|%[0-1]{1,16})(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    DIR = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?[RT]?)(\s){1}(\d{1,3}|\$[0-9A-F]{2}|\$0[0-9A-F]|’[A-Za-z]{1})(\s\*[A-Z]*)?", flags= re.IGNORECASE) #Puede que la tercera condicion de operadores este de mas
    EXT = re.compile(r"([ABCDEIJLNORST][BDEILMNOPRSTU][ABCDGLMPRSTXY][ABD]?)(\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1}|%[0-1]{1,16})(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    INDX = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1}|%[0-1]{1,16})(,X)(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    INDY = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?[RT]?)(\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1}|%[0-1]{1,16})(,Y)(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    
    tostr = "".join(instruccion) #SIRVE PARA VERFIFICAR EL DIRECCIONAMIENTO COMO CADENA MEDIANTE REGEX

    #Instruccion =[ ,mnemonico, espaacio_gato_ect, operando, comentario, ] [0,1,2,3,4,5,6]

    #COMPILADO IMM
    if re.fullmatch(IMM, tostr):
        comparacion_menemonicos(instruccion, mnemonicos_imm, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error, error_line, list_labels, tostr)
    #COMPILADO DIR
    if re.fullmatch(DIR, tostr):
        comparacion_menemonicos(instruccion, mnemonicos_dir, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error, error_line, list_labels, tostr)
    #COMPILADRO EXT
    if re.fullmatch(EXT, tostr):
        comparacion_menemonicos(instruccion, mnemonicos_ext, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error, error_line, list_labels, tostr) #FALTA VER QUE PASA CUANDO LLEGAN ETIQUETAS
    #COMPILADO INDX
    if re.fullmatch(INDX, tostr):
        comparacion_menemonicos(instruccion, mnemonicos_indx, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error, error_line, list_labels, tostr)
    #COMPILADO INDY
    if re.fullmatch(INDY, tostr):
        comparacion_menemonicos(instruccion, mnemonicos_indy, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error, error_line, list_labels, tostr)


def comparacion_menemonicos(instruccion, mnemonicos, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error, error_line, list_label, tostr):
    for i in mnemonicos:
    #MNEMONICO
        if instruccion[1] == acortador_mnemonicos(i):
             compilacion_ALL5(instruccion, i, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error, error_line, list_label, tostr, acortador_opcode(i))
        else:
            stack_error.push(CONS_004+error_line)
            

def compilacion_ALL5(instruccion, cline, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error, error_line, list_label, tostr, op_code):
    #OPERANDOS DIFERENCIACION
    verificador = instruccion[3]

    #stack_compiler_vls = [] #(codigo objeto, linea de codigo original, label, lb_cod, comentario)
    #stack_compiler_s19 = [] #(codigo objeto en pila)
    #stack_compiler_html = [] #(codigo objeto mne, color mne, codigo objeto op, color op, linea de codigo original, label, lb_cod,  comentario, 
    #if len(instruccion[3][1:] Si la instruccion es su campo operando apartir del segundo digito, que ya no identifica el tipo de operando si no que es el operando,  es de tal longitud

    if verificador[0] == "$":
        if acortador_bytes(cline) == 1:
            if len(instruccion[3][1:]) == 2 and int(instruccion[3][1:],16) <= 255:
                stack_compiler_vls.append((op_code+instruccion[3][1:2],tostr,"no label", 0, instruccion[4]))
                stack_compiler_s19.push(op_code+instruccion[3][1:2])
                stack_compiler_html.append((op_code,"r",instruccion[3][1:2],"b",tostr,"no label", 0, instruccion[4]))
        elif acortador_bytes(cline) == 2:
            if len(instruccion[3][1:]) == 4  and int(instruccion[3][1:],16) <= 255:
                stack_compiler_vls.append((op_code+instruccion[3][1:4],tostr,"no label", 0, instruccion[4]))
                stack_compiler_s19.push(op_code+instruccion[3][1:4])
                stack_compiler_html.append((op_code,"r",instruccion[3][1:4],"b",tostr,"no label", 0, instruccion[4]))
        elif acortador_bytes(cline) == 3:
            if len(instruccion[3][1:]) == 6  and int(instruccion[3][1:],16) <= 4095:
                stack_compiler_vls.append((op_code+instruccion[3][1:6],tostr,"no label", 0, instruccion[4]))
                stack_compiler_s19.push(op_code+instruccion[3][1:6])
                stack_compiler_html.append((op_code,"r",instruccion[3][1:6],"b",tostr,"no label", 0, instruccion[4]))
        elif acortador_bytes(cline) == 4 or acortador_bytes(cline) == 5:
            if len(instruccion[3][1:]) >= 8  and int(instruccion[3][1:],16) <= 65535:
                stack_compiler_vls.append((op_code+instruccion[3][1:],tostr,"no label", 0, instruccion[4]))
                stack_compiler_s19.push(op_code+instruccion[3][1:])
                stack_compiler_html.append((op_code,"r",instruccion[3][1:],"b",tostr,"no label", 0, instruccion[4]))
        else:
            stack_error.push(CONS_007+error_line)

    #CONVERSION ASCII
    elif verificador[0] == "’":
        conversion = hex(ord(instruccion[3][1:]))
        comp_conv(conversion, cline, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error, error_line, list_label, tostr, op_code)
            
    #CONVERSION BINARIO
    elif verificador[0] == "%":
        conversion = hex(int(instruccion[3][1:]),2)
        comp_conv(conversion, cline, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error, error_line, list_label, tostr, op_code)

                
    #CONVERSION DECIMAL
    else:
        conversion = hex(int(instruccion[3]))
        comp_conv(conversion, cline, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error, error_line, list_label, tostr, op_code)

def comp_conv(conversion, cline, stack_compiler_vls, stack_compiler_s19, stack_compiler_html,  stack_error, error_line, list_label, tostr, op_code):
        if acortador_bytes(cline) == 1:
        #Se empieza de dos en adelante porque se descuenta el 0x de el formato hex
            if len(conversion[2:]) == 2 and int(conversion,16) <= 255:
                stack_compiler_vls.append((op_code+conversion[2:3],tostr,"no label", 0, conversion[4]))
                stack_compiler_s19.push(op_code+conversion[2:3])
                stack_compiler_html.append((op_code,"r",conversion[2:3],"b",tostr,"no label", 0, conversion[4]))
        elif acortador_bytes(cline) == 2:
            if len(conversion[2:]) == 4  and int(conversion,16) <= 255:
                stack_compiler_vls.append((op_code+conversion[2:5],tostr,"no label", 0, conversion[4]))
                stack_compiler_s19.push(op_code+conversion[2:5])
                stack_compiler_html.append((op_code,"r",conversion[2:5],"b",tostr,"no label", 0, conversion[4]))
        elif acortador_bytes(cline) == 3:
            if len(conversion[2:]) == 6  and int(conversion,16) <= 4095:
                stack_compiler_vls.append((op_code+conversion[2:7],tostr,"no label", 0, conversion[4]))
                stack_compiler_s19.push(op_code+conversion[2:7])
                stack_compiler_html.append((op_code,"r",conversion[2:7],"b",tostr,"no label", 0, conversion[4]))
        elif acortador_bytes(cline) == 4 or acortador_bytes(cline) == 5:
            if len(conversion[2:]) >= 8  and int(conversion,16) <= 65535:
                stack_compiler_vls.append((op_code+conversion[2:],tostr,"no label", 0, conversion[4]))
                stack_compiler_s19.push(op_code+conversion[2:])
                stack_compiler_html.append((op_code,"r",conversion[2:],"b",tostr,"no label", 0, conversion[4]))
        else:
            stack_error.push(CONS_007+error_line)

def acortador_mnemonicos(cadena):
    cadena_cut = cadena.split(',')
    if len(cadena_cut) > 0:
        return cadena_cut[0]
    else:
        return ""

def acortador_bytes(cadena):
    cadena_cut = cadena.split(',')
    if len(cadena_cut) > 0:
        bytes_op = int(cadena_cut[3])
        return bytes_op
    else:
        return 0

def acortador_opcode(cadena):
    cadena_cut = cadena.split(',')
    if len(cadena_cut) > 0:
        op_code = cadena_cut[1]
        return op_code
    else:
        return 0