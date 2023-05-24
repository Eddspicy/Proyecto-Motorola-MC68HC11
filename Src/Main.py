from io import open
from Precompilado import *

def main(): 

    #ABRIR MNEMONICOS
    REL = []
    f_rel = open("REL.txt", "r")
    for line in f_rel :
        REL.append(line)
    f_rel.close()

    INH = []
    f_inh = open("INH.txt", "r")
    for line in f_inh :
        INH.append(line)
    f_inh.close()

    IMM = []
    f_imm = open("IMM.txt", "r")
    for line in f_imm :
        IMM.append(line)
    f_imm.close()

    DIR = []
    f_dir = open("DIR.txt", "r")
    for line in f_dir :
        DIR.append(line)
    f_dir.close()

    EXT = []
    f_ext = open("EXT.txt", "r")
    for line in f_ext :
        EXT.append(line)
    f_ext.close()

    INDX = []
    f_indx = open("INDX.txt", "r")
    for line in f_indx :
        INDX.append(line)
    f_indx.close()

    INDY = []
    f_indy = open("INDY.txt", "r")
    for line in f_indy :
        INDY.append(line)
    f_indy.close()
    #---------------------------------------------
    #ABRIR PROGRAMA PARA PRECOMPILADO Y COMPILADO
    programa = open("pruebaTotal.asc", "r")
    stack_compiler = []
    stack_error = []
    list_labels = []
    error_line = 0
    for linea in programa:
        if linea.startswith(" "):
            precompilado(linea.strip(), DIR, EXT, IMM, INDX, INDY, INH, REL, stack_compiler, stack_error,error_line, list_labels)
        else:
            print(f"Es una etiqueta, directiva o end: {linea.strip()}\n") #FALTA TRATAMIENTO DE ETIQUETAS, VARIABLES, CONSTANTES Y DIRECTIVAS
            list_labels.append(linea.strip())
    programa.close()
    #---------------------------------------------
    
main()