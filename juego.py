import pygame
import random

pygame.init()

# Cargar sonidos
sonido_nivel = pygame.mixer.Sound("nivel.wav.mp3")
sonido_punto = pygame.mixer.Sound("punto.wav.mp3")
sonido_ganador = pygame.mixer.Sound("ganador.wav.mp3")

ANCHO, ALTO = 600, 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("The battle of tomorrow")

# Cargar imágenes de inicio, game over, fondo del jefe y victoria
imagen_inicio = pygame.image.load("inicio.png.jpg")
imagen_inicio = pygame.transform.scale(imagen_inicio, (ANCHO, ALTO))
imagen_gameover = pygame.image.load("gameover.png.jpg")
imagen_gameover = pygame.transform.scale(imagen_gameover, (ANCHO, ALTO))
fondo_jefe = pygame.image.load("fondo.png.webp")
fondo_jefe = pygame.transform.scale(fondo_jefe, (ANCHO, ALTO))
imagen_ganar = pygame.image.load("ganar.wav.jpg")
imagen_ganar = pygame.transform.scale(imagen_ganar, (ANCHO, ALTO))

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)

# Fuentes
fuente = pygame.font.SysFont(None, 48)
fuente_peque = pygame.font.SysFont(None, 32)

# Variables de juego
vidas = 3
puntaje = 0
nivel = 1
jugando = False
game_over = False
victoria = False
vida_extra_otorgada = False
musica_inicio_sonando = False

# Jugador
jugador = pygame.Rect(300, 350, 50, 30)
velocidad = 7

# Objeto a recolectar
objeto = pygame.Rect(random.randint(0, ANCHO-30), 0, 30, 30)
velocidad_objeto = 3

# Jefe
jefe = pygame.Rect(250, 50, 100, 40)
vida_jefe = 10
vida_jefe_max = 10
velocidad_jefe = 2
direccion_jefe = 1  # 1: derecha, -1: izquierda

# Imagen del jefe
jefe_imagen = pygame.image.load("jefe.png")
jefe_imagen = pygame.transform.scale(jefe_imagen, (100, 40))

def mostrar_texto(texto, fuente, color, x, y):
    superficie = fuente.render(texto, True, color)
    ventana.blit(superficie, (x, y))

def pantalla_inicio():
    global musica_inicio_sonando
    ventana.blit(imagen_inicio, (0, 0))
    mostrar_texto("The battle of tomorrow", fuente, ROJO, 100, 80)
    mostrar_texto("Presiona ESPACIO para empezar", fuente_peque, BLANCO, 100, 320)
    pygame.display.flip()
    if not musica_inicio_sonando:
        pygame.mixer.music.load("musicafondo.wav.mp3")
        pygame.mixer.music.play(-1)
        musica_inicio_sonando = True

def pantalla_game_over():
    ventana.blit(imagen_gameover, (0, 0))
    mostrar_texto(f"Puntaje final: {puntaje}", fuente_peque, NEGRO, 200, 250)
    mostrar_texto("Presiona R para reiniciar", fuente_peque, NEGRO, 170, 300)
    pygame.display.flip()

def pantalla_victoria():
    ventana.blit(imagen_ganar, (0, 0))  # Fondo solo al ganar
    mostrar_texto("¡FELICITACIONES, GANASTEIS!", fuente, BLANCO, 50, 150)
    mostrar_texto(f"Puntaje final: {puntaje}", fuente_peque, BLANCO, 200, 220)
    mostrar_texto("Presiona R para reiniciar", fuente_peque, BLANCO, 170, 300)
    pygame.display.flip()

def reiniciar_juego():
    global vidas, puntaje, nivel, jugador, objeto, velocidad_objeto, jugando, game_over, victoria
    global jefe, vida_jefe, vida_jefe_max, velocidad_jefe, direccion_jefe, vida_extra_otorgada, musica_inicio_sonando
    vidas = 3
    puntaje = 0
    nivel = 1
    jugador.x = 300
    objeto.x = random.randint(0, ANCHO-30)
    objeto.y = 0
    velocidad_objeto = 3
    jefe.x = 250
    vida_jefe_max = 10
    vida_jefe = vida_jefe_max
    velocidad_jefe = 2
    direccion_jefe = 1
    jugando = True
    game_over = False
    victoria = False
    vida_extra_otorgada = False
    musica_inicio_sonando = False
    pygame.mixer.music.stop()
    pygame.mixer.music.load("musicafondo.wav.mp3")
    pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if not jugando and not game_over and not victoria and evento.key == pygame.K_SPACE:
                reiniciar_juego()
            if (game_over or victoria) and evento.key == pygame.K_r:
                reiniciar_juego()

    if not jugando and not game_over and not victoria:
        pantalla_inicio()
    elif game_over:
        pantalla_game_over()
    elif victoria:
        pantalla_victoria()
    else:
        # Fondo del jefe
        ventana.blit(fondo_jefe, (0, 0))

        # Vida extra al llegar a 450 puntos
        if puntaje >= 450 and not vida_extra_otorgada:
            vidas += 1
            vida_extra_otorgada = True

        # Subir nivel cada 200 puntos
        if puntaje >= nivel * 200:
            nivel += 1
            velocidad_objeto += 1
            velocidad_jefe += 1
            sonido_nivel.play()

        # Victoria a los 1000 puntos
        if puntaje >= 1000:
            jugando = False
            victoria = True
            pygame.mixer.music.stop()
            sonido_ganador.play()

        # Dibujar jefe con imagen
        ventana.blit(jefe_imagen, jefe)
        mostrar_texto(f"Jefe: {vida_jefe}/{vida_jefe_max}", fuente_peque, BLANCO, jefe.x+5, jefe.y-25)
        # Dibujar jugador y objeto
        pygame.draw.rect(ventana, VERDE, jugador)
        pygame.draw.rect(ventana, AMARILLO, objeto)
        # HUD
        mostrar_texto(f"Vidas: {vidas}", fuente_peque, BLANCO, 10, 10)
        mostrar_texto(f"Puntaje: {puntaje}", fuente_peque, BLANCO, 250, 10)
        mostrar_texto(f"Nivel: {nivel}", fuente_peque, BLANCO, 500, 10)
        pygame.display.flip()

        # Movimiento del objeto
        objeto.y += velocidad_objeto
        if objeto.y > ALTO:
            vidas -= 1
            objeto.x = random.randint(0, ANCHO-30)
            objeto.y = 0
            if vidas == 0:
                jugando = False
                game_over = True
                pygame.mixer.music.stop()
                sonido_punto.play()

        # Movimiento del jefe
        jefe.x += velocidad_jefe * direccion_jefe
        if jefe.right >= ANCHO or jefe.left <= 0:
            direccion_jefe *= -1

        # Colisión jugador-objeto
        if jugador.colliderect(objeto):
            puntaje += 10
            vida_jefe -= 1
            objeto.x = random.randint(0, ANCHO-30)
            objeto.y = 0
            if vida_jefe <= 0:
                vida_jefe_max += 5
                vida_jefe = vida_jefe_max

        # Movimiento jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador.x > 0:
            jugador.x -= velocidad
        if teclas[pygame.K_RIGHT] and jugador.x < ANCHO - jugador.width:
            jugador.x += velocidad

    clock.tick(60)

pygame.quit()