import re

def acortador_cadenas (cadena):
    cadena_cut = ""
    if len(cadena) >= 4:
        if cadena[3] == ',':
            cadena_cut = cadena[:3]
        else:
            cadena_cut = cadena[:4]
    else:
        cadena_cut = cadena[:len(cadena)]
    return cadena_cut;

def compilado_REL(instruccion) :
    AREL = []
    f_arel = open("D:\Facultad\Semestre 2023-2\EyPC\Proyecto\Proyecto-Motorola-MC68HC11\REL.txt", "r")
    for line in f_arel :
        AREL.append(line)
    for i in range (len(AREL)) :
        if instruccion == acortador_cadenas(AREL[i]):
            print("Si matchearon")
def compilado_INH(instruccion):
    AINH = []
    f_inh = open("D:\Facultad\Semestre 2023-2\EyPC\Proyecto\Proyecto-Motorola-MC68HC11\INH.txt", "r")
    for line in f_inh :
        AINH.append(line)
    #for i in range (len(AINH)) :
    #    print(AINH[i])
def compilado_IMM(instruccion):
    AIMM = []
    f_aimm = open("D:\Facultad\Semestre 2023-2\EyPC\Proyecto\Proyecto-Motorola-MC68HC11\IMM.txt", "r")
    for line in f_aimm :
        AIMM.append(line)
    #for i in range (len(AIMM)) :
    #    print(AIMM[i])
def compilado_DIR(instruccion) :
    ADIR = []
    f_adir = open("D:\Facultad\Semestre 2023-2\EyPC\Proyecto\Proyecto-Motorola-MC68HC11\DIR.txt", "r")
    for line in f_adir :
        ADIR.append(line)
    #for i in range (len(ADIR)) :
    #    print(ADIR[i])   
def compilado_EXT(instruccion) :
    AEXT = []
    f_aext = open("D:\Facultad\Semestre 2023-2\EyPC\Proyecto\Proyecto-Motorola-MC68HC11\EXT.txt", "r")
    for line in f_aext :
        AEXT.append(line)
    #for i in range (len(AEXT)) :
    #    print(AEXT[i])
def compilado_INX(instruccion) :
    AINDX = []
    f_aindx = open("D:\Facultad\Semestre 2023-2\EyPC\Proyecto\Proyecto-Motorola-MC68HC11\INDX.txt", "r")
    for line in f_aindx :
        AINDX.append(line)
    #for i in range (len(AINDX)) :
    #    print(AINDX[i])
def compilado_INDY(instruccion) :
    AINDY = []
    f_aindy = open("D:\Facultad\Semestre 2023-2\EyPC\Proyecto\Proyecto-Motorola-MC68HC11\INDY.txt", "r")
    for line in f_aindy :
        AINDY.append(line)
    #for i in range (len(AINDY)) :
    #    print(AINDY[i])

def evaluar_direccionamiento(cadena):
    REL = re.compile(r"(B[CEGHLMNPRSV][ACEILNOQRST])\s([A-ZA-Z]{0,256})?")
    INH = re.compile(r"([ACDFILMNPRSTWX][ABDEGLNOPSTUWXY][ABCDGHILMOPRSTVXY]([ABDPSVXY])?)")
    IMM = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY]([ABD])?)(\s)(#)(\d{1,5}|(\$)([0-9A-F]{2,4}|([’])[A-Za-z]{1}))")
    DIR = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY]([ABD])?)([\s]){1}(\d{1,3}|(\$)[0-9A-F]{2}|(\$)0[0-9A-F]|([’])[A-Za-z]{1})")
    EXT = re.compile(r"([ABCDEIJLNORST][BDEILMNOPRSTU][ABCDGLMPRSTXY]([ABD])?)([\s]){1}(\d{1,5}|(\$)([0-9A-F]{2,4}|([’])[A-Za-z]{1}))")
    INDX = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY]([ABDELRT])?)([\s]){1}(\d{1,5}|(\$)([0-9A-F]{2,4}|([’])[A-Za-z]{1}))(,X)")
    INDY = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY]([ABDELRT])?)([\s]){1}(\d{1,5}|(\$)([0-9A-F]{2,4}|([’])[A-Za-z]{1}))(,Y)")

    if re.fullmatch(REL, cadena):
#        compilado_REL(re.fullmatch(REL, cadena).group(1))
        return "Direccionamiento relativo"
    elif re.fullmatch(INH, cadena):
        return "Direccionamiento inherente"
    elif re.fullmatch(IMM, cadena):
        return "Direccionamiento inmediato"
    elif re.fullmatch(DIR, cadena):
        return "Direccionamiento directo"
    elif re.fullmatch(EXT, cadena):
        return "Direccionamiento EXTENDIDO"
    elif re.fullmatch(INDX, cadena):
        return "Direccionamiento indexado en X"
    elif re.fullmatch(INDY, cadena):
        return "Direccionamiento indexado en Y"
    else:
        return "No se ajusta a ningún caso conocido"

# Ejemplo de uso
archivo = open("D:\Facultad\Semestre 2023-2\EyPC\Proyecto\Proyecto-Motorola-MC68HC11\pruebaAZ.asc", "r")
for linea in archivo:
    direccionamiento = evaluar_direccionamiento(linea.strip())
    print(f"Cadena: {linea.strip()}\nTipo de direccionamiento: {direccionamiento}\n")
archivo.close()

