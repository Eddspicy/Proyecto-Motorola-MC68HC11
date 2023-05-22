import re
from io import open

REL = re.compile(r"(b[ceghlmnprsv][aceilnoqrst])(\s[a-zA-Z]{0,256})?")
INH = re.compile(r"([acdfilmnprstwx][abdeglnopstuwxy][abcdghilmoprstvxy]([abdpsvxy])?)")
#REST = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY]([ABDELRT])?)([#\s]){1}([\$’])?([0-9A-F]{2,4}|[A-Za-z]{1})(,[XY])?")
IMM = re.compile(r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY]([ABD])?)(#)([\$’])?([0-9A-F]{2,4}|[A-Za-z]{1})")
DIR = re.compile (r"([ABCELOS][BDIMNOPRU][ABCDPRSTXY]([ABD])?)([\s]){1}([\$’])?(([0-9A-F]{2}|(0[0-9A-F]))|[A-Za-z]{1})")
EXT = re.compile (r"([ABCDEIJLNORST][BDEILMNOPRSTU][ABCDGLMPRSTXY]([ABD])?)([\s]){1}([\$’])?([0-9A-F]{2,4}|[A-Za-z]{1})")
INDX = re.compile (r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY]([ABDELRT])?)([\s]){1}([\$’])?(([0-9A-F]{2}|(0[0-9A-F]))|[A-Za-z]{1})(,X)")
INDY = re.compile (r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY]([ABDELRT])?)([\s]){1}([\$’])?(([0-9A-F]{2}|(0[0-9A-F]))|[A-Za-z]{1})(,Y)")

test_str = "bgt HOLA"

match = re.search(INDY, "LDY $AB,Y")
if match:
    print("Direccionamiento INDY")

##match = REL.match(test_str)

#print(match)

#print(match.groups())

#def reconocimiento_modos(match_modos):
#    if (match_modos.group(4) == "#" or match_modos.group(5) == "#") :
#        print("MODO DE DIRECCIONAMIENTO INMEDIATO")
#   elif (match_modos.group(4) == " " or match_modos.group(5) == " ") : 
#        print("MODO DE DIRECCIONAMIENTO DIRECTO, EXTENDIDO E INDEXADO.")
#    else:
#        # Acciones para cualquier otra opción
#       print("Opción inválida")

# Ejemplo de uso
#opcion_seleccionada = 2
#ejecutar_opcion(opcion_seleccionada)

#if (match.group(1) == "bgt" and  match.group(2) == " HOLA"):
#    print("EL modo de direccionamiento es relativo")

#Instrucciones_relativas = open("D:\Facultad\Semestre 2023-2\EyPC\Proyecto\Proyecto-Motorola-MC68HC11\REL.txt", "r")
#Irel=[]
#for line in Instrucciones_relativas:
#    Irel.append(line)

#Primer_programa = open("/home/eddspicy/Documents/Compilador Motorola MC68HC11/Proyecto-Motorola-MC68HC11/prueba.asc", "r")
#Programa=[]
#for line in Primer_programa:
#    Programa.append(line)
#
#print(Programa)