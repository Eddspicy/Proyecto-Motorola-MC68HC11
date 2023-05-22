import re
from io import open

REL = re.compile(r"(b[ceghlmnprsv][aceilnoqrst])(\s[a-zA-Z]{0,256})?")
INH = re.compile(r"([acdfilmnprstwx][abdeglnopstuwxy][abcdghilmoprstvxy]([abdpsvxy])?)")
REST = re.compile(r"([ABCDEIJLNORST][BCDEILMNOPRSTU][ABCDEGLMPRSTXY]([ABDELRT])?)([#\s]){1}([\$’])?([0-9A-F]{2,4}|[A-Za-z]{1})(,[XY])?")
test_str = "bgt HOLA"

match = REL.match(test_str)

print(match)

print(match.groups())

if (match.group(2) == " " and  match.group(3) == "HOLA"):
    print("EL modo de direccionamiento es relativo")

Instrucciones_relativas = open("/home/eddspicy/Documents/Compilador Motorola MC68HC11/Proyecto-Motorola-MC68HC11/REL.txt", "r")
Irel=[]
for line in Instrucciones_relativas:
    Irel.append(line)

Primer_programa = open("/home/eddspicy/Documents/Compilador Motorola MC68HC11/Proyecto-Motorola-MC68HC11/prueba.asc", "r")
Programa=[]
for line in Primer_programa:
    Programa.append(line)

print(Programa)