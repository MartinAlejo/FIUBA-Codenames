from random import *
import difflib

def generar_nombres_clave(ruta, cantidad):
	"""
	Dada una ruta y una cantidad (siendo la cantidad, el numeros de nombres en clave a obtener), devuelve una lista de nombres en clave seleccionados de forma aleatoria (y sin repetir) entre los existentes
	"""
	nombres_en_clave = []
	nombres_en_clave_seleccionados = []
	pos_x = 0
	pos_y = 0

	# Lee y completa la lista de nombres en clave existentes 
	with open(ruta) as nombres:
		for nombre in nombres:
			nombres_en_clave.append(nombre.strip())

	# Genera una nueva lista de nombres en clave, seleccionados de forma aleatoria
	for _ in range(cantidad):
		if pos_x == 5:
			pos_x = 0
			pos_y += 1
		nombre = choice(nombres_en_clave)
		nombres_en_clave.remove(nombre)
		nombres_en_clave_seleccionados.append((nombre, pos_x, pos_y))
		pos_x += 1

	return nombres_en_clave_seleccionados

def generar_posiciones():
	"""
	Devuelve un diccionario, donde cada clave es una categoria, y el valor es una lista son las posiciones ocupadas por dicha categoria
	"""
	pos_disponibles = []
	cat_pos = {"Azul": [], "Rojo": [], "Civil": [], "Doble": [], "Asesino": []}

	# Genero una lista de posiciones
	for _ in range(25):
		pos = (randint(0, 4), randint(0, 4))
		while pos in pos_disponibles:
			pos = (randint(0, 4), randint(0, 4))
		pos_disponibles.append(pos)

	# Asigno las posiciones disponibles a las categorias pertinentes
	for i in range(25):
		pos = choice(pos_disponibles)
		if i <= 7:
			cat_pos["Azul"].append(pos)
		elif 7 < i <= 15:
			cat_pos["Rojo"].append(pos)
		elif 16 <= i < 23:
			cat_pos["Civil"].append(pos)
		elif i == 23:
			cat_pos["Doble"].append(pos)
		elif i == 24:
			cat_pos["Asesino"].append(pos)
		pos_disponibles.remove(pos)

	return cat_pos

class Juego:
	def __init__(self, equipo_azul, equipo_rojo):
		"""
		Se inicializa el estado de juego, se debera pasar 2 listas donde cada una seran los jugadores de cada equipo
		"""
		# En el caso de que no se haya pasado quien sera el primer espia de cada equipo, se eligira de forma aleatoria
		self.nombres_clave = "" # Se crean en el metodo "generar_tablero"
		self.turno_equipo = choice(["Azul", "Rojo"])
		self.equipo_azul = equipo_azul
		self.equipo_rojo = equipo_rojo
		self.spymaster_azul = None # Se elige en el metodo "seleccionar_spymaster"
		self.spymaster_rojo = None # Se elige en el metodo "seleccionar_spymaster"
		self.pista_actual = ""
		self.cant_pista = "" # La cantidad de agentes a los que se aplica la pista actual
		self.tablero = "" # Se crea en el metodo "generar_tablero"
		self.posiciones = "" # Se crean en el metodo "generar_tablero"
		self.punt_azul = 0
		self.punt_rojo = 0
		self.ronda = 1
		self.cartas_azules = 8 # Las cartas azules que existen al principio de la ronda
		self.cartas_rojas = 8 # Las cartas rojas que existen al principio de la ronda
		self.carta_asesino = 1
		self.casillas_descubiertas = [] # Las casillas que se descubrieron en la ronda

		if self.turno_equipo == "Azul":
			self.turno = "Spymaster Azul"
		else:
			self.turno = "Spymaster Rojo"

	def obtener_llave(self):
		"""
		Devuelve una llave (solo los spymasters tienen acceso a la llave), que muestra que y donde esta en el tablero
		"""
		return self.posiciones

	def obtener_codenames(self):
		"""
		Devuelve los nombres clave en forma de lista
		"""
		return self.nombres_clave

	def obtener_puntuaciones(self):
		"""
		Devuelve la puntuacion del equipo azul y la puntuacion del equipo rojo
		"""
		return self.punt_azul, self.punt_rojo

	def obtener_turno(self):
		"""
		Devuelve el turno actual
		"""
		return self.turno

	def obtener_ronda(self):
		"""
		Devuelve la ronda actual
		"""
		return self.ronda

	def obtener_pista(self):
		"""
		Devuelve la pista actual
		"""
		return self.pista_actual

	def obtener_cant_pista(self):
		"""
		Devuelve la cantidad de agentes los que se aplica la pista actual
		"""
		return self.cant_pista

	def obtener_casillas_descubiertas(self):
		"""
		Devuelve las casillas descubiertas (x, y) en forma de lista
		"""
		return self.casillas_descubiertas

	def obtener_ganador(self):
		if self.punt_azul > self.punt_rojo:
			ganador = "Equipo Azul"
		elif self.punt_azul < self.punt_rojo:
			ganador = "Equipo Rojo"
		else:
			ganador = "Empate"
		return ganador


	def seleccionar_spymaster(self):
		"""
		Cambia de spymaster al siguiente, dependiendo del equipo
		"""
		if self.spymaster_azul == None or self.spymaster_rojo == None:
			self.spymaster_azul = self.equipo_azul[0]
			self.spymaster_rojo = self.equipo_rojo[0]

		# Cambiamos de spymaster para el equipo azul
		nro_jug = self.equipo_azul.index(self.spymaster_azul)
		self.spymaster_azul = self.equipo_azul[(nro_jug + 1) % len(self.equipo_azul)]

		# Cambiamos de spymaster para el equipo rojo
		nro_jug = self.equipo_rojo.index(self.spymaster_rojo)
		self.spymaster_rojo = self.equipo_rojo[(nro_jug + 1) % len(self.equipo_rojo)]

	def actualizar_pista(self, pista):
		"""
		Actualiza la pista actual
		"""
		self.pista_actual = pista

	def actualizar_cant_pista(self, cant):
		"""
		Actualiza la cantidad de agentes a los que se aplica la pista actual
		"""
		self.cant_pista = cant

	def avanzar_turno(self):
		"""
		Avanza al siguiente turno
		"""
		if self.turno == "Spymaster Azul":
			self.turno = "Equipo Azul"

		elif self.turno == "Spymaster Rojo":
			self.turno = "Equipo Rojo"

		elif self.turno == "Equipo Azul":
			self.turno = "Spymaster Rojo"

		elif self.turno == "Equipo Rojo":
			self.turno = "Spymaster Azul"

	def pista_es_valida(self, pista):
		"""
		Devuelve True si la pista es valida, False si es invalida
		"""
		# Para verificar si la pista es valida, usamos "SequenceMatcher", que nos devuelve un "ratio" (que va desde 0.0 a 1.0) en funcion de que tanto se parecen 2 strings... Siendo 0.0 totalmente diferentes y 1.0 iguales
		# Si se quiere ser mas estricto, se puede reducir el valor maximo de ratio (ya que entre mas se parecen dos strings, mayor es el ratio)
		for nombre, _, _ in self.nombres_clave:
			if difflib.SequenceMatcher(None, nombre, pista).ratio() > 0.7:
				return False
		return True

	def penalizar(self):
		"""
		Resta un punto al equipo penalizado
		"""
		if self.turno == "Spymaster Azul":
			self.punt_azul -= 1
		if self.turno == "Spymaster Rojo":
			self.punt_rojo -= 1

	def descubrir_posicion(self, celda):
		"""
		Agrega la celda a las posiciones descubiertas
		"""
		self.casillas_descubiertas.append(celda)

	def actualizar_puntuacion(self, juego, tipo):
		"""
		Actualiza la puntuacion, las cartas restantes, y devuelve True si se debe avanzar el turno
		"""
		if self.turno == "Equipo Rojo":
			if tipo == "Azul":
				self.punt_azul += 1
				self.cartas_azules -= 1
				avanzar = True
			if tipo == "Rojo":
				self.punt_rojo += 1
				self.cartas_rojas -= 1
				avanzar = False
			if tipo == "Civil":
				self.punt_rojo -= 1
				avanzar = True
			if tipo == "Doble":
				self.punt_rojo += 1
				avanzar = True
			if tipo == "Asesino":
				self.punt_rojo -= 5
				self.carta_asesino -= 1
				avanzar = False

		if self.turno == "Equipo Azul":
			if tipo == "Azul":
				self.punt_azul += 1
				self.cartas_azules -= 1
				avanzar = False
			if tipo == "Rojo":
				self.punt_rojo += 1
				self.cartas_rojas -= 1
				avanzar = True
			if tipo == "Civil":
				self.punt_azul -= 1
				avanzar = True
			if tipo == "Doble":
				self.punt_azul += 1
				avanzar = True
			if tipo == "Asesino":
				self.punt_azul -= 5
				self.carta_asesino -= 1
				avanzar = False

		return avanzar

	def generar_tablero(self):
		"""
		Empieza una nueva ronda, y por lo tanto se genera un nuevo tablero y se decide/cambia al jugador que sera el spymaster
		"""
		# Se inicializa una grilla vacia (de 25 casilleros) que se llenara mas abajo
		# Se eligen 25 nombres claves de forma aleatoria
		# Se generan las posiciones de todas las "categorias" (Siendo las categorias los equipos, civil, agente doble y asesino)
		# Se selecciona un nuevo spymaster

		tablero = [["", "", "", "", ""] for _ in range(5)] 
		# Definimos/Actualizamos los atributos
		self.nombres_clave = generar_nombres_clave("nombres_clave.txt", 25)
		self.posiciones = generar_posiciones()
		self.cartas_azules = 8
		self.cartas_rojas = 8
		self.carta_asesino = 1 
		self.casillas_descubiertas = []

		# Construimos el tablero
		ind = 0
		for ind_fila, fila in enumerate(tablero):
			for ind_col in range(len(fila)):
				tablero[ind_fila][ind_col] = self.nombres_clave[ind]
				ind += 1

		self.tablero = tablero

	def ronda_terminada(self):
		"""
		Devuelve "True" si se termino la ronda (no quedan mas cartas azules/rojas o se toco la carta del asesino)
		"""
		if self.cartas_azules == 0 or self.cartas_rojas == 0 or self.carta_asesino == 0:
			return True
		return False

	def avanzar_ronda(self):
		"""
		Avanza a la siguiente ronda
		"""
		self.ronda += 1

	def terminado(self):
		"""
		Devuelve "True" si el juego se termino (pasaron las "x" rondas, donde "x" es el numero de jugadores de un equipo)
		"""
		if self.ronda > len(self.equipo_azul) or self.ronda > len(self.equipo_rojo):
			return True
		return False

	def __str__(self):
		"""
		Printea el estado de juego en la consola
		"""
		return f"El equipo azul es: {self.equipo_azul}\nEl equipo rojo es: {self.equipo_rojo}\nEl spymaster azul es: {self.spymaster_azul}\nEl spymaster rojo es: {self.spymaster_rojo}\nLa pista actual es: {self.pista_actual}\nLas puntuaciones son: Azul: {self.punt_azul} Azul: {self.punt_rojo}"

