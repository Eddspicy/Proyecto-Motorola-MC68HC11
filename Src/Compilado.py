import re

def acortador_mnemonicos(cadena):
    cadena_cut = ""
    if len(cadena) >= 4:
        if cadena[3] == ',':
            cadena_cut = cadena[:3]
        else:
            cadena_cut = cadena[:4]
    else:
        cadena_cut = cadena[:len(cadena)]
    return cadena_cut;

def acortador_bytes(cadena):
    byte = cadena.split(',')
    if len(byte) > 1:
        return byte[-1].strip()
    else:
        return print("Error al obtener los bytes de la instrucción")

def acortador_opcode(cadena):
    primera_coma = cadena.find(',')
    segunda_coma = cadena.find(',', primera_coma + 1)

    if primera_coma != -1 and segunda_coma != -1:
        opcode = cadena[primera_coma + 1:segunda_coma].strip()
        return opcode
    else:
        return print("Error al encontrar el opcode")


def compilado_REL (instruccion, mnemonicos, stack_compiler, stack_error, error_line, list_labels):
    print("relativo")
    for i in mnemonicos:
        if instruccion[1] == acortador_mnemonicos(i):
            stack_compiler.push(acortador_opcode(i))


def compilado_INH (instruccion, mnemonicos, stack_compiler, stack_error,error_line):
    print("inherente")


def compilado_ALL5 (instruccion, mnemonicos_dir, mnemonicos_ext, mnemonicos_imm, mnemonicos_indx, mnemonicos_indy, stack_compiler, stack_error, error_line, list_labels):
    print("ALL5")
    IMM = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?)(\s#)(\d{1,5}|\$[0-9A-F]{2,4}|’][A-Za-z]{1})(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    DIR = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?)(\s){1}(\d{1,3}|\$[0-9A-F]{2}|\$0[0-9A-F]|’[A-Za-z]{1})(\s\*[A-Z]*)?", flags= re.IGNORECASE) #Puede que la tercera condicion de operadores este de mas
    EXT = re.compile(r"([ABCDEIJLNORST][BDEILMNOPRSTU][ABCDGLMPRSTXY][ABD]?)(\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1})(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    INDX = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?)(\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1})(,X)(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    INDY = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?)(\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1})(,Y)(\s\*[A-Z]*)?", flags= re.IGNORECASE)