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
    f_arel = open("/home/eddspicy/Documents/Compilador Motorola MC68HC11/Proyecto-Motorola-MC68HC11/REL.txt", "r")
    for line in f_arel :
        AREL.append(line)
    for i in range (len(AREL)) :
        if instruccion == acortador_cadenas(AREL[i]):
            print("Si matchearon")
def compilado_INH(instruccion):
    AINH = []
    f_inh = open("/home/eddspicy/Documents/Compilador Motorola MC68HC11/Proyecto-Motorola-MC68HC11/INH.txt", "r")
    for line in f_inh :
        AINH.append(line)
    #for i in range (len(AINH)) :
    #    print(AINH[i])
def compilado_IMM(instruccion):
    AIMM = []
    f_aimm = open("/home/eddspicy/Documents/Compilador Motorola MC68HC11/Proyecto-Motorola-MC68HC11/IMM.txt", "r")
    for line in f_aimm :
        AIMM.append(line)
    #for i in range (len(AIMM)) :
    #    print(AIMM[i])
def compilado_DIR(instruccion) :
    ADIR = []
    f_adir = open("/home/eddspicy/Documents/Compilador Motorola MC68HC11/Proyecto-Motorola-MC68HC11/DIR.txt", "r")
    for line in f_adir :
        ADIR.append(line)
    #for i in range (len(ADIR)) :
    #    print(ADIR[i])   
def compilado_EXT(instruccion) :
    AEXT = []
    f_aext = open("/home/eddspicy/Documents/Compilador Motorola MC68HC11/Proyecto-Motorola-MC68HC11/EXT.txt", "r")
    for line in f_aext :
        AEXT.append(line)
    #for i in range (len(AEXT)) :
    #    print(AEXT[i])
def compilado_INDX(instruccion) :
    AINDX = []
    f_aindx = open("/home/eddspicy/Documents/Compilador Motorola MC68HC11/Proyecto-Motorola-MC68HC11/INDX.txt", "r")
    for line in f_aindx :
        AINDX.append(line)
    #for i in range (len(AINDX)) :
    #    print(AINDX[i])
def compilado_INDY(instruccion) :
    AINDY = []
    f_aindy = open("/home/eddspicy/Documents/Compilador Motorola MC68HC11/Proyecto-Motorola-MC68HC11/INDY.txt", "r")
    for line in f_aindy :
        AINDY.append(line)
    #for i in range (len(AINDY)) :
    #    print(AINDY[i])