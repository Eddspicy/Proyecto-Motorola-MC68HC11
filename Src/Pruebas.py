import re
from Precompilado import *

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

    control = True
    
    for palabra in palabras:
        if re.search(palabra, texto, flags=re.IGNORECASE ) :
            control = False
    
    return control

def pruebas():

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

    #EXPRESIONES REGULARES PARA CPSAS QUE NO SON INSTRUCCIONES

    variables = re.compile(r"(([A-Z0-9]|\_)+)((\s)+EQU(\s)+)(\$00[0-9A-F]{2})", flags=re.IGNORECASE) #acepta simbolos en los nombres
    constantes = re.compile(r"(([A-Z0-9]|\_)+)(\s)+(EQU)(\s)+(\$10[0-9A-F]{2})", flags=re.IGNORECASE) #acepta simbolos en los nombres
    comentarios = re.compile(r"(\*(\w|\W)*)")
    etiquetas = re.compile(r"(([A-Z]|[\W]|[\_])*)", flags=re.IGNORECASE) #no debe detectar espacios ni lineas en blanco

    #ARREGLOS PARA EL COMPILADO

    stack_compiler_vls = [] #(codigo objeto, linea de codigo original, label, lb_cod, dir_mem)
    stack_compiler_s19 = [] #(codigo objeto en pila)
    stack_compiler_html = [] #(codigo objeto mne, color mne, codigo objeto op, color op, linea de codigo original, label, lb_cod,  comentario, dir_mem)
    stack_error = [] #(cadenas con los errores)
    list_labels = [] #(cadenas con las etiquetas)
    list_variables = []
    list_constantes = []
    line = 0
    dir_mem = hex(8000)

    with open("down.ASC","r") as archivo:

        for linea in archivo:
            
            linea = linea.rstrip() #se uso porque de alguna manera se tienen espacios, tabulaciones saltos a final de las lineas y las ER no detectan bien por eso
            if re.fullmatch(r'', linea):
                print("se detecto una linea en blanco: " +linea)
            elif re.fullmatch(variables, linea):
                #print("se detecto una variable: " +linea)
                Matcher = re.split(variables, linea)
                print("Prueba:"+Matcher[1])
            elif re.fullmatch(constantes, linea):
                print("se detecto una constante: " +linea)
            elif re.fullmatch(comentarios, linea):
                print("se detecto un comentario: " +linea)
            elif re.fullmatch(etiquetas, linea) and verificar_palabra_reservada(linea):
                print("se detecto una etiqueta: " +linea)
            elif re.match(r'\s+', linea):
                print("se detecto una instruccion: " +linea)
                #precompilado(linea.strip(), DIR, EXT, IMM, INDX, INDY, INH, REL, stack_compiler_vls, stack_compiler_s19, stack_compiler_html, stack_error,error_line, list_labels,dir_mem
            else:
                stack_error.append(CONS_009+str(line))

pruebas()

