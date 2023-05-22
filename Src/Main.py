import re
from io import open

#ALL5 = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY]([ABDELRT])?)([#\s]){1}([\$’])?([0-9A-F]{2,4}|[A-Za-z]{1})(,[XY])?")

REL = re.compile(r"(b[ceghlmnprsv][aceilnoqrst])(\s[a-zA-Z]{0,256})?")
INH = re.compile(r"([acdfilmnprstwx][abdeglnopstuwxy][abcdghilmoprstvxy]([abdpsvxy])?)")
IMM = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY]([ABD])?)(#)([\$’])?([0-9A-F]{2,4}|[A-Za-z]{1})")
DIR = re.compile (r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY]([ABD])?)([\s]){1}([\$’])?(([0-9A-F]{2}|(0[0-9A-F]))|[A-Za-z]{1})")
EXT = re.compile (r"([ABCDEIJLNORST][BDEILMNOPRSTU][ABCDGLMPRSTXY]([ABD])?)([\s]){1}([\$’])?([0-9A-F]{2,4}|[A-Za-z]{1})")
INDX = re.compile (r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY]([ABDELRT])?)([\s]){1}([\$’])?(([0-9A-F]{2}|(0[0-9A-F]))|[A-Za-z]{1})(,X)")
INDY = re.compile (r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY]([ABDELRT])?)([\s]){1}([\$’])?(([0-9A-F]{2}|(0[0-9A-F]))|[A-Za-z]{1})(,Y)")

def reconocimiento_modos(match_modos):
    Primer_programa = open("/home/eddspicy/Documents/Compilador Motorola MC68HC11/Proyecto-Motorola-MC68HC11/prueba.asc", "r")
    Programa=[]
    match = True
    for line in Primer_programa:
        Programa.push(line)
        if(match == re.fullmatch(REL, line)):
            print("Direccionamiento relativo")
        elif(match == re.fullmatch(INH, line)):
            print("Direccionamiento inherente")
        elif(match == re.fullmatch(IMM, line)):
            print("Direccionamiento inmediato")
        elif(match == re.fullmatch(DIR, line)):
            print("Direccionamiento directo")
        elif(match == re.fullmatch(EXT, line)):
            print("Direccionamiento EXTENDIDO")
        elif(match == re.fullmatch(INDX, line)):
            print("Direccionamiento indexado en X")
        elif(match == re.fullmatch(INDY, line)):
            print("Direccionamiento indexado en Y")
()
