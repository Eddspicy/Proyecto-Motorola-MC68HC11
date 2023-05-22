import re

def evaluar_direccionamiento(cadena):
    REL = re.compile(r"(B[CEGHLMNPRSV][ACEILNOQRST])\s([A-ZA-Z]{0,256})?")
    INH = re.compile(r"([ACDFILMNPRSTWX][ABDEGLNOPSTUWXY][ABCDGHILMOPRSTVXY]([ABDPSVXY])?)")
    IMM = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY]([ABD])?)(\s)(#)(\d{1,5}|(\$)([0-9A-F]{2,4}|([’])[A-Za-z]{1}))")
    DIR = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY]([ABD])?)([\s]){1}(\d{1,3}|(\$)[0-9A-F]{2}|(\$)0[0-9A-F]|([’])[A-Za-z]{1})")
    EXT = re.compile(r"([ABCDEIJLNORST][BDEILMNOPRSTU][ABCDGLMPRSTXY]([ABD])?)([\s]){1}(\d{1,5}|(\$)([0-9A-F]{2,4}|([’])[A-Za-z]{1}))")
    INDX = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY]([ABDELRT])?)([\s]){1}(\d{1,5}|(\$)([0-9A-F]{2,4}|([’])[A-Za-z]{1}))(,X)")
    INDY = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY]([ABDELRT])?)([\s]){1}(\d{1,5}|(\$)([0-9A-F]{2,4}|([’])[A-Za-z]{1}))(,Y)")

    if re.fullmatch(REL, cadena):
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
