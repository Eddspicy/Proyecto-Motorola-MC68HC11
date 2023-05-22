cadena = input("Ingresa una cadena: ")
if len(cadena) >= 4:
    if cadena[3] == ',':
        cadena = cadena[:3]
    else:
        cadena = cadena[:4]
else:
    cadena = cadena[:len(cadena)]
    
print("Cadena resultante:", cadena)