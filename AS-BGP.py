#!/usr/bin/env python3
# Validador de AS BGP 16-bit y 32-bit usando if/elif/else

asn = int(input("Ingrese número de AS: "))

if 1 <= asn <= 64511:
    print(f"El AS {asn} es un AS público de 16 bits.")
elif 64512 <= asn <= 65534:
    print(f"El AS {asn} es un AS privado de 16 bits.")
elif 65536 <= asn <= 4199999999:
    print(f"El AS {asn} es un AS público de 32 bits.")
elif 4200000000 <= asn <= 4294967294:
    print(f"El AS {asn} es un AS privado de 32 bits.")
else:
    print(f"{asn} no es un número de AS válido de 16 o 32 bits.")
