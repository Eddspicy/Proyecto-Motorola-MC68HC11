from io import open
from Precompilado import *

#Errores
CONS_001 = "001   CONSTANTE INEXISTENTE - Error en linea:"
CONS_002 = "002   VARIABLE INEXISTENTE - Error en linea:"
CONS_003 = "003   ETIQUETA INEXISTENTE - Error en linea:"
CONS_004 = "004   MNEMÓNICO INEXISTENTE - Error en linea:"
CONS_005 = "005   INSTRUCCIÓN CARECE DE  OPERANDO(S) - Error en linea:"
CONS_006 = "006   INSTRUCCIÓN NO LLEVA OPERANDO(S) - Error en linea:"
CONS_007 = "007   MAGNITUD DE  OPERANDO ERRONEA - Error en linea:"
CONS_008 = "008   SALTO RELATIVO MUY LEJANOE - Error en linea:"
CONS_009 = "009   INSTRUCCIÓN CARECE DE ALMENOS UN ESPACIO RELATIVO AL MARGENE - Error en linea:"
CONS_010 = "010   NO SE ENCUENTRA END - Error en linea:"

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
    stack_compiler_vls = [] #(codigo objeto, linea de codigo original, label, lb_cod, comentario, dir_mem)
    stack_compiler_s19 = [] #(codigo objeto en pila)
    stack_compiler_html = [] #(codigo objeto mne, color mne, codigo objeto op, color op, linea de codigo original, label, lb_cod,  comentario, dir_mem)
    var_cons = []
    stack_error = [] #(cadenas con los errores)
    list_labels = [] #(cadenas con las etiquetas)
    error_line = 0
    dir_mem = hex(8000)

    for linea in programa:
        if linea.startswith(" "):
            precompilado(linea.strip(), DIR, EXT, IMM, INDX, INDY, INH, REL, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error,error_line, list_labels,dir_mem)
        else:
            print(f"Es una etiqueta, directiva o end: {linea.strip()}\n") #FALTA TRATAMIENTO DE ETIQUETAS, VARIABLES, CONSTANTES Y DIRECTIVAS
            list_labels.append(linea.strip())
    programa.close()
    #---------------------------------------------
    
main()