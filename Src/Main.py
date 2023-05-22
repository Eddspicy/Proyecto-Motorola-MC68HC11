import re
from io import open

REL = re.compile(r"(b[ceghlmnprsv][aceilnoqrst])(\s)?([a-zA-Z]{0,256})")
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