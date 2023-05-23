import re

def acortador_cadenas(cadena):
    cadena_cut = ""
    if len(cadena) >= 4:
        if cadena[3] == ',':
            cadena_cut = cadena[:3]
        else:
            cadena_cut = cadena[:4]
    else:
        cadena_cut = cadena[:len(cadena)]
    return cadena_cut;

def compilado_REL (instruccion, mnemonicos, stack_compiler, stack_error, error_line, list_labels):
    print("relativo")


def compilado_INH (instruccion, mnemonicos, stack_compiler, stack_error,error_line):
    print("inherente")


def compilado_ALL5 (instruccion, mnemonicos_dir, mnemonicos_ext, mnemonicos_imm, mnemonicos_indx, mnemonicos_indy, stack_compiler, stack_error, error_line, list_labels):
    print("ALL5")
    IMM = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?)(\s#)(\d{1,5}|\$[0-9A-F]{2,4}|’][A-Za-z]{1})(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    DIR = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY][ABD]?)(\s){1}(\d{1,3}|\$[0-9A-F]{2}|\$0[0-9A-F]|’[A-Za-z]{1})(\s\*[A-Z]*)?", flags= re.IGNORECASE) #Puede que la tercera condicion de operadores este de mas
    EXT = re.compile(r"([ABCDEIJLNORST][BDEILMNOPRSTU][ABCDGLMPRSTXY][ABD]?)(\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1})(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    INDX = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?)(\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1})(,X)(\s\*[A-Z]*)?", flags= re.IGNORECASE)
    INDY = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY][ABDELRT]?)(\s){1}(\d{1,5}|\$[0-9A-F]{2,4}|’[A-Za-z]{1})(,Y)(\s\*[A-Z]*)?", flags= re.IGNORECASE)