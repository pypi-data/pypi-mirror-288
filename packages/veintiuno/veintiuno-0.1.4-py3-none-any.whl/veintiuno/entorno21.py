"""Entorno para el juego de 21,
contiene metodos p1ara retornar el estado inicial, estado siguiente, 
recompensa/penalidad, si termina el juego; y un metodo para ejecutar
una accion (para añadir una carta o detener el juego)."""

import random

class VeintiUno(object):
	"""docstring for veinitiuno"""
	def __init__(self):
		self.estado = (0,0)  # Tupla (suma_cartas_de_mesa, suma_mis_cartas)
		self.recompensa = 0  # Entero entre 0 y 1.
		self.accion = 0		 # Entero entre 0 y 1.
		self.fin = False
		self.volo = [False, False]

	def inicializar_estado(self):
		carta_mesa = random.randint(1, 10)
		carta_mia = random.randint(1, 10)
		self.estado = (carta_mesa, carta_mia)
		return self.estado

	def ejecutar_accion(self, accion):
		ganador = 0
		if accion != 0 and accion != 1:
			raise ValueError("Solo 0 y 1")

		## Pido cartas
		cartas = self.repartir_carta(accion, 1)
		self.estado = (self.estado[0], cartas)
		if self.volo[1]:
			self.recompensa = 0
			return self.estado, self.recompensa, self.fin
		
		## Mesa pide carta
		cartas = self.repartir_carta(1, 0)
		self.estado = (cartas, self.estado[1])
		if self.volo[0]:
			self.recompensa = 1
			return self.estado, self.recompensa, self.fin

		ganador = self.estado[1] > self.estado[0]
		self.recompensa = ganador
		return self.estado, self.recompensa, self.fin

	def repartir_carta(self, accion, jugador):
		"""jugador: 0 -> mesa, 1 -> yo"""
		carta = accion*random.randint(1, 10)
		carta_jugador = self.estado[jugador] + carta
		self.fin = 1 - accion + self.fin
		if carta_jugador > 21:
			self.recompensa = 1 - jugador
			self.volo[jugador] = True
			self.fin = True
		return carta_jugador

