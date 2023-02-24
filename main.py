from juego import *
import gamelib

ANCHO_PANTALLA = 1280

ALTO_PANTALLA = 680

ALTO_CASILLA = 80

ANCHO_CASILLA = 120 

FILAS = 5

CASILLAS_FILA = 5

MARGEN_IZQUIERDO = 50 # Es el margen que se deja (en pixeles) desde el borde izquierdo de la pantalla

MARGEN_SUPERIOR = 50 # Es el margen que se deja (en pixeles) desde el borde superior de la pantalla

MARGEN_DERECHO = 250 # Es el margen que se deja (en pixeles) desde el borde derecho de la pantalla

TAMAÑO_LETRA_CODENAMES = 12

TAMAÑO_LETRA_MENU = 16

def dibujar_grilla():
    """
    Dibuja la grilla en la pantalla
    """
    y = MARGEN_SUPERIOR
    x = MARGEN_IZQUIERDO
    y_fin = ALTO_CASILLA * FILAS + y
    x_fin = ANCHO_CASILLA * CASILLAS_FILA + x


    # El siguiente bloque, dibuja las lineas horizontales
    for _ in range(FILAS + 1):
        gamelib.draw_line(MARGEN_IZQUIERDO, y, x_fin, y)
        y += ALTO_CASILLA

    # El siguiente bloque, dibuja las lineas verticales
    for _ in range(CASILLAS_FILA + 1):
        gamelib.draw_line(x, MARGEN_SUPERIOR, x, y_fin)
        x += ANCHO_CASILLA

def crear_diccionario_celdas():
    """
    Crea un diccionario en donde las 'keys' son tuplas, las cuales contienen la posicion de la celda en la grilla, y los 'values'
    son son una tupla de tuplas, donde cada tupla contiene la posicion de la celda, pero dada en rangos de pixeles 
    """
    dic_celdas = {}

    ran_pix_y1 = MARGEN_SUPERIOR
    ran_pix_y2 = ALTO_CASILLA + MARGEN_SUPERIOR

    ran_pix_x1 = MARGEN_IZQUIERDO
    ran_pix_x2 = ANCHO_CASILLA + MARGEN_IZQUIERDO

    for fil in range(FILAS):
        for col in range(CASILLAS_FILA):
            dic_celdas[(fil, col)] = (ran_pix_x1, ran_pix_x2), (ran_pix_y1, ran_pix_y2)
            ran_pix_x1 += ANCHO_CASILLA
            ran_pix_x2 += ANCHO_CASILLA

        ran_pix_y1 += ALTO_CASILLA
        ran_pix_y2 += ALTO_CASILLA

        ran_pix_x1 = MARGEN_IZQUIERDO
        ran_pix_x2 = ANCHO_CASILLA + MARGEN_IZQUIERDO

    return dic_celdas

def obtener_celda(x, y):
    """
    Devuelve la celda/casillero de la grilla, a partir de las coordenadas "x" e "y" obtenidas al hacer click el usuario
    """
    diccionario_celdas = crear_diccionario_celdas()
    columna = None
    fila = None
    #El siguiente bloque, busca para los parametros "x", "y", a que posicion de la grilla se refieren
    for cor_grilla in diccionario_celdas:
        ran_x1 = diccionario_celdas[cor_grilla][0][0]
        ran_x2 = diccionario_celdas[cor_grilla][0][1]

        ran_y1 = diccionario_celdas[cor_grilla][1][0]
        ran_y2 = diccionario_celdas[cor_grilla][1][1]

        if (ran_x1 < x < ran_x2) and (ran_y1 < y < ran_y2):
            fila = cor_grilla[0]
            columna = cor_grilla[1]

    if columna == None or fila == None:
        return None

    return (columna, fila)

def dibujar_codenames(juego):
    """
    Dibuja en la grilla los codenames de la ronda
    """
    nombres = juego.obtener_codenames()
    cont_casilla = 0
    x = MARGEN_IZQUIERDO + ANCHO_CASILLA // 2
    y = MARGEN_SUPERIOR + ALTO_CASILLA // 2

    for nombre, _, _ in nombres:
        gamelib.draw_text(nombre, x, y, size = TAMAÑO_LETRA_CODENAMES)
        cont_casilla += 1
        if cont_casilla >= CASILLAS_FILA:
            x = MARGEN_IZQUIERDO + ANCHO_CASILLA // 2
            y += ALTO_CASILLA
            cont_casilla = 0
            continue
        x += ANCHO_CASILLA

def dibujar_puntuaciones(juego):
    """
    Dibuja en la pantalla las puntuaciones
    """
    x_texto = ANCHO_PANTALLA - MARGEN_DERECHO
    punt_azul, punt_rojo = juego.obtener_puntuaciones()

    # Dibujo la puntuacion del equipo azul
    gamelib.draw_rectangle(x_texto - ANCHO_CASILLA // 2, MARGEN_SUPERIOR + ALTO_CASILLA // 4, x_texto + ANCHO_CASILLA // 2, MARGEN_SUPERIOR + ALTO_CASILLA, outline='white', fill='black')
    gamelib.draw_text("Puntuación del equipo azul:", x_texto, MARGEN_SUPERIOR, size = TAMAÑO_LETRA_MENU)
    gamelib.draw_text(punt_azul, x_texto, MARGEN_SUPERIOR + ALTO_CASILLA // 1.5, size = TAMAÑO_LETRA_MENU)

    # Dibujo la puntuacion del equipo rojo
    gamelib.draw_rectangle(x_texto - ANCHO_CASILLA // 2, MARGEN_SUPERIOR * 3 + ALTO_CASILLA // 4, x_texto + ANCHO_CASILLA // 2, MARGEN_SUPERIOR * 3 + ALTO_CASILLA, outline='white', fill='black')
    gamelib.draw_text("Puntuación del equipo rojo:", x_texto, MARGEN_SUPERIOR * 3, size = TAMAÑO_LETRA_MENU)
    gamelib.draw_text(punt_rojo, x_texto, MARGEN_SUPERIOR * 3 + ALTO_CASILLA // 1.5, size = TAMAÑO_LETRA_MENU)

def dibujar_turno(juego):
    """
    Dibuja en la pantalla el turno actual
    """
    x_texto = ANCHO_PANTALLA - MARGEN_DERECHO
    turno = juego.obtener_turno()
    color = "white"
    if turno == "Spymaster Azul" or turno == "Azules":
        color = "blue"
    elif turno == "Spymaster Rojo" or turno == "Rojos":
        color = "red"

    # Dibujo el turno
    gamelib.draw_rectangle(x_texto - ANCHO_CASILLA // 2, MARGEN_SUPERIOR * 6 + ALTO_CASILLA // 4, x_texto + ANCHO_CASILLA // 2, MARGEN_SUPERIOR * 6 + ALTO_CASILLA, outline='white', fill='black')
    gamelib.draw_text("Turno:", x_texto, MARGEN_SUPERIOR * 6, size = TAMAÑO_LETRA_MENU)
    gamelib.draw_text(turno, x_texto, MARGEN_SUPERIOR * 6 + ALTO_CASILLA // 1.5, size = 12, fill = color)

def dibujar_ronda(juego):
    """
    Dibuja la ronda actual en la pantalla
    """
    x_texto = ANCHO_PANTALLA - MARGEN_DERECHO
    ronda = juego.obtener_ronda()

    # Dibujo la ronda
    gamelib.draw_rectangle(x_texto - ANCHO_CASILLA // 2, MARGEN_SUPERIOR * 8 + ALTO_CASILLA // 4, x_texto + ANCHO_CASILLA // 2, MARGEN_SUPERIOR * 8 + ALTO_CASILLA, outline='white', fill='black')
    gamelib.draw_text("Ronda:", x_texto, MARGEN_SUPERIOR * 8, size = TAMAÑO_LETRA_MENU)
    gamelib.draw_text(ronda, x_texto, MARGEN_SUPERIOR * 8 + ALTO_CASILLA // 1.5, size = 12)

def dibujar_pista(juego): 
    """
    Dibuja la pista en la pantalla junto a la cantidad de agentes a los que se aplica
    """
    x_texto = ANCHO_PANTALLA - MARGEN_DERECHO
    pista = juego.obtener_pista()
    cant = juego.obtener_cant_pista()  

    # Dibujamos la pista
    gamelib.draw_rectangle(x_texto - ANCHO_CASILLA // 2, MARGEN_SUPERIOR * 10 + ALTO_CASILLA // 4, x_texto + ANCHO_CASILLA // 2, MARGEN_SUPERIOR * 10 + ALTO_CASILLA, outline='white', fill='black')
    gamelib.draw_text("Pista:", x_texto, MARGEN_SUPERIOR * 10, size = TAMAÑO_LETRA_MENU)
    gamelib.draw_text(f"{pista} - {cant}", x_texto, MARGEN_SUPERIOR * 10 + ALTO_CASILLA // 1.5, size = 12)
    
def inicializar_juego(jug_azules, jug_rojos):
    """
    Inicializa el estado de juego, a partir de una lista de jugadores para cada equipo
    """
    return Juego(jug_azules, jug_rojos)

def mostrar_estado_juego(juego):
    """
    Dibuja el juego en la pantalla
    """
    gamelib.draw_begin()
    dibujar_grilla()
    dibujar_codenames(juego)
    dibujar_puntuaciones(juego)
    dibujar_turno(juego)
    dibujar_ronda(juego)
    dibujar_pista(juego)
    dibujar_descubiertas(juego)
    gamelib.draw_end()

def mostrar_juego_y_llave(juego):
    gamelib.draw_begin()
    dibujar_grilla()
    dibujar_codenames(juego)
    dibujar_puntuaciones(juego)
    dibujar_turno(juego)
    dibujar_ronda(juego)
    dibujar_pista(juego)
    dibujar_llave(juego)
    dibujar_descubiertas(juego)
    gamelib.draw_end()

def dibujar_llave(juego):
    """
    Dibuja la "llave" en la pantalla (Solo en el turno del spymaster)
    """
    # La "llave" es una grilla con las ubicaciones de todas las cartas de la partida
    # "A" quiere decir que ahi hay una carta "Azul"
    # "R" quiere decir que ahi hay una carta "Roja"
    # "C" quiere decir que ahi hay una carta "Civil"
    # "D" quiere decir que ahi hay una carta "Doble" (El doble funciona como un comodin, le suma un punto al primer equipo que lo encuentra)
    # "K" quiere decir que ahi hay una carta "Asesino"
    llave = juego.obtener_llave()
    x = MARGEN_IZQUIERDO * 4
    y = ALTO_CASILLA * FILAS + MARGEN_SUPERIOR * 2
    y_fin = ALTO_CASILLA // 3 * FILAS + y
    x_fin = ANCHO_CASILLA // 5 * CASILLAS_FILA + x


    # Primero dibujamos el texto
    gamelib.draw_text("Llave: ", MARGEN_IZQUIERDO * 3, y_fin - 70, size = 12)

    # El siguiente bloque, dibuja las lineas horizontales
    for _ in range(FILAS + 1):
        gamelib.draw_line(x, y, x_fin, y)
        y += ALTO_CASILLA // 3

    # El siguiente bloque, dibuja las lineas verticales
    for _ in range(CASILLAS_FILA + 1):
        gamelib.draw_line(x, ALTO_CASILLA * FILAS + MARGEN_SUPERIOR * 2, x, y_fin)
        x += ANCHO_CASILLA // 5

    # Lo siguiente es para dibujar el caracter correspondendiente a cada casillero de la llave
    pos_x = 0
    pos_y = 0
    x = MARGEN_IZQUIERDO * 4 + ANCHO_CASILLA // 10
    y = ALTO_CASILLA * FILAS + MARGEN_SUPERIOR * 2 + ALTO_CASILLA // 6
    while pos_y < FILAS:
        if (pos_x, pos_y) in llave["Azul"]:
            car = "A"
        elif (pos_x, pos_y) in llave["Rojo"]:
            car = "R"   
        elif (pos_x, pos_y) in llave["Civil"]:
            car = "C"
        elif (pos_x, pos_y) in llave["Doble"]:
            car = "D"
        elif (pos_x, pos_y) in llave["Asesino"]:
            car = "K"

        gamelib.draw_text(car, x, y, size = 8)
        pos_x += 1
        if pos_x >= CASILLAS_FILA:
            pos_x = 0
            pos_y += 1

        x += ANCHO_CASILLA // 5
        if x >= x_fin:
            y += ALTO_CASILLA // 3
            x = MARGEN_IZQUIERDO * 4 + ANCHO_CASILLA // 10

def encontrar_tipo(juego, celda):
    """
    A partir de una celda (Que representa la posicion de la grilla, en la lista), obtenidos por el usuario al hacer click,
    devuelve el "tipo" que se encontraba en dicha casilla
    """
    # Con "tipo" se refiere a: Azul, Rojo, Civil, Doble, Asesino
    tipo_celda = juego.obtener_llave()
    for tipo in tipo_celda:
        if celda in tipo_celda[tipo]:
            return tipo

def dibujar_descubiertas(juego):
    """
    Dibuja en pantalla que habia detras del nombre clave de cada casilla que fue descubierta
    """
    tipo_celda = juego.obtener_llave()
    descubiertas = juego.obtener_casillas_descubiertas()

    # Iteramos las celdas descubiertas, y dibujamos la imagen en pantalla en funcion de que tipo era la celda
    for celda in descubiertas:
        for tipo in tipo_celda:
            if celda in tipo_celda[tipo]:
                if tipo == "Azul":
                    ruta = 'img/agente_azul.gif'
                if tipo == "Rojo":
                    ruta = 'img/agente_rojo.gif'
                if tipo == "Civil":
                    ruta = 'img/civil.gif'
                if tipo == "Doble":
                    ruta = 'img/doble.gif'
                if tipo == "Asesino":
                    ruta = 'img/asesino.gif'

        pos_x = MARGEN_IZQUIERDO + ANCHO_CASILLA * celda[0]
        pos_y = MARGEN_SUPERIOR + ALTO_CASILLA * celda[1]
        gamelib.draw_image(ruta, pos_x + 2, pos_y + 2) # El "+2" es para encuadrar la imagen mejor

def dibujar_ganador(ganador):
    """
    Dibuja el ganador en pantalla
    """
    x = 960
    y = 370
    gamelib.draw_text("Ganador: ", x, y, size = 20)
    gamelib.draw_text(ganador, x + 135, y, size = 20)

def mostrar_ganador(juego, ganador):
    """
    Dado el ganador (que se obtiene por el metodo obtener ganador), lo muestra en pantalla (junto a la grilla, la llave y las puntuaciones)
    """
    gamelib.draw_begin()
    dibujar_grilla()
    dibujar_codenames(juego)
    dibujar_puntuaciones(juego)
    dibujar_descubiertas(juego)
    dibujar_llave(juego)
    dibujar_ganador(ganador)
    gamelib.draw_end()

def generar_equipos(cant_jug, jugadores):
    """
    Dada una lista de nombres y la cantidad de jugadores, se dividiran en 2 equipos de forma aleatoria y se devolveran como lista
    """
    equipo_azul = []
    equipo_rojo = []

    for i in range(cant_jug):
        nro_azar = randint(0, len(jugadores) - 1)
        jugador = jugadores.pop(nro_azar)
        if i % 2 == 0:
            equipo_azul.append(jugador)
        else:
            equipo_rojo.append(jugador)

    return equipo_azul, equipo_rojo

def main():
    gamelib.resize(ANCHO_PANTALLA, ALTO_PANTALLA)
    gamelib.title("Codenames")
    # Como pide la consigna: "Se ingresará la cantidad de jugadores y sus nombres al juego y se dividirán aleatoriamente en 2 equipos de igual cantidad de jugadores"
    cant_jug = int(input("Ingrese la cantidad de jugadores: ")) 
    jugadores = input("Ingrese el nombre de los jugadores, separados por un espacio: ").split()
    while not(len(jugadores) == cant_jug):
        print("Error, el numero de jugadores no es igual a la cantidad ingresada")
        cant_jug = int(input("Ingrese nuevamente la cantidad de jugadores: ")) 
        jugadores = input("Ingrese nuevamente el nombre de los jugadores, separados por un espacio: ").split()
    equipo_azul, equipo_rojo = generar_equipos(cant_jug, jugadores)
    # Inicializamos el estado de juego
    juego = inicializar_juego(equipo_azul, equipo_rojo)
    juego.generar_tablero()
    dic_celdas = crear_diccionario_celdas()
    mostrar_estado_juego(juego)
    while gamelib.loop(fps=30):
        # Este loop sucede siempre que gamelib este abierto
        while not juego.terminado():
            # Este loop sucede mientras continua la partida
            juego.seleccionar_spymaster()
            # Verificamos que el turno inicial al principio de la ronda sea de un spymaster, en caso contrario pasamos turno
            turno_inic = juego.obtener_turno()
            if not turno_inic in ("Spymaster Rojo", "Spymaster Azul"):
                juego.avanzar_turno()
            while not juego.ronda_terminada():
                # Este loop sucede mientras continua la ronda
                if juego.obtener_turno() == "Spymaster Rojo" or juego.obtener_turno() == "Spymaster Azul":
                    # El siguiente bloque, modifica el estado de juego en funcion del spymaster del equipo
                    mostrar_juego_y_llave(juego)
                    # Pedimos la pista
                    pista = gamelib.input("Ingrese una pista: ")
                    while not pista:
                        pista = gamelib.input("Hubo un error. Ingrese nuevamente la pista: ")
                    # Verificamos la pista y actuamos en consecuencia
                    while not juego.pista_es_valida(pista):
                        juego.penalizar()
                        mostrar_juego_y_llave(juego)
                        pista = gamelib.input("Pista invalida, se penalizara al equipo. Ingrese otra pista: ")
                    # Pedimos la cantidad de agentes a los cuales se aplica la pista
                    cant = gamelib.input("Ingrese la cantidad de agentes a los cuales se aplica la pista: ")
                    while not cant or not cant.isdigit() or int(cant) < 1:
                        cant = gamelib.input("Hubo un error. Ingrese nuevamente la cantidad: ")
                    # Definimos tambien el limite de intentos en funcion de la cantidad, e inicializamos el numero de intento
                    limite_intentos = int(cant) + 1
                    intento = 0
                    juego.actualizar_pista(pista)
                    juego.actualizar_cant_pista(cant)
                    juego.avanzar_turno()
                else:
                    # El siguiente bloque, modifica el estado de juego en funcion de los jugadores de los equipos
                    avanzar = False
                    terminar_ronda = False
                    mostrar_estado_juego(juego)
                    # Primero verificamos si se alcanzo el limite de intentos, en cuyo caso se avanza el turno luego de un aviso
                    if intento >= limite_intentos:
                        gamelib.say("Límite de intentos alcanzado. Se avanzará el turno")
                        juego.avanzar_turno()
                    # Esperamos a que suceda un evento
                    ev = gamelib.wait()
                    if not ev:
                        # El usuario cerró la ventana.
                        exit()
                    if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
                        # El usuario presionó la tecla Escape, cerrar la aplicación.
                        exit()
                    if ev.type == gamelib.EventType.ButtonPress:
                        # El usuario presionó un botón del mouse
                        x, y = ev.x, ev.y # Averiguamos la posición donde se hizo click
                        celda = obtener_celda(x, y)
                        # Vemos que se clickeo una celda que pertenece a la grilla y no haya sido descubierta
                        if celda != None and not celda in juego.obtener_casillas_descubiertas():
                            intento += 1
                            juego.descubrir_posicion(celda)
                            tipo = encontrar_tipo(juego, celda)
                            avanzar = juego.actualizar_puntuacion(juego, tipo)
                    if avanzar:
                        juego.avanzar_turno()
                # En el caso de que se termine la ronda, se pide confirmacion para continuar
                if juego.ronda_terminada():
                    mostrar_estado_juego(juego)
                    confirmacion = gamelib.input("Ronda finalizada, escriba 'Continuar' para empezar la siguiente ronda ")
                    while not confirmacion == "Continuar":
                        confirmacion = gamelib.input("Ronda finalizada, escriba 'Continuar' para empezar la siguiente ronda ")
            # Se termino la ronda, pero no el juego. Se avanza la ronda y se genera un nuevo tablero
            juego.avanzar_ronda()
            juego.generar_tablero()
        # Se termino la partida, se obtiene el ganador y se muestra en pantalla
        ganador = juego.obtener_ganador()
        mostrar_ganador(juego, ganador)

gamelib.init(main)