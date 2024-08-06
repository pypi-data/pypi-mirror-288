# veintiuno
veintinuno is a package for create and interact with a blackjack envieronment.
**business projects** in Python.

You can find out more about this package
on [MyPortfolio](https://lequispep.com)

## Installation
You can install this package using

```
pip install veintiuno
```
## Usage
```
from veintiuno import VeintiUno

v21 = VeintiUno()
estado0 = v21.inicializar_estado()
print("\n")
print("Cartas mesa: ", estado0[0])
print("Mis cartas: ", estado0[1])
fin = False

while not fin:
	accion = int(input("¿Pedir Cartas? [0 -> NO, 1 -> SI]: "))
	estado, recompensa, fin = v21.ejecutar_accion(accion)
	print("\n")
	print("Cartas mesa: ", estado[0])
	print("Mis cartas: ", estado[1])

if recompensa == 1:
	print("Ganaste")
else:
	print("Perdiste")
```