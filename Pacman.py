import pygame
import random
import sys
import copy
import tkinter as tk
from tkinter import messagebox

pygame.init()

# Configuración del mapa y pantalla
mapa_ancho = 20
mapa_alto = 9
ancho, alto = 1200, 800
tamano_celda = min(ancho // mapa_ancho, alto // mapa_alto)

pantalla = pygame.display.set_mode((mapa_ancho * tamano_celda, mapa_alto * tamano_celda))
pygame.display.set_caption("PAXMAN")

# Definir colores
negro = (0, 0, 0)
azul = (0, 0, 255)
amarillo = (255, 255, 0)
blanco = (255, 255, 255)
rojo = (255, 0, 0)

# Variables del juego
pac_x, pac_y = 1, 1
fan_x, fan_y = 10, 5
puntos = 0
total_puntos = 0 # Contador total de puntos blancos en el mapa

mapa = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1],
    [1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

mapa_original = copy.deepcopy(mapa) ## Variable para Reiniciar el mapa

# Contar el total de puntos blancos en el mapa con una nueva variable
total_puntos = sum(fila.count(2) for fila in mapa)

## se crea una nueva funcion par mostrar los puntos en la parte superior de la pantalla 
def mostrar_puntaje():
    font = pygame.font.Font(None, 36) # Fuente del texto en tamaño en pixeles
    texto = font.render(f"Puntos: {puntos}", True, blanco) # Texto blanco y mostramos el texto en la interfas
    pantalla.blit(texto, (20, 20)) # dimencion del texto

def mover_pacman(dx, dy):
    global pac_x, pac_y, puntos
    if mapa[pac_y + dy][pac_x + dx] != 1: # Sirve para no poder pasar a travez de las paredes
        pac_x += dx
        pac_y += dy
        if mapa[pac_y][pac_x] == 2: #Recoje los puntos del mapa
            puntos += 6
            mapa[pac_y][pac_x] = 3 # Elimina el punto comestible después de comerlo

def mover_fantasma(): 
    global fan_x, fan_y # La funcion ayuda a definir fan x y fan y se tomaran en varias partes del codigo
    direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]# Utilizamos variable para definir el movimiento del fantasma
    random.shuffle(direcciones) # EL movimiento del fantasma es aleatorio
    for dx, dy in direcciones: 
        if mapa[fan_y + dy][fan_x + dx] != 1: # El fantasma no pasara a travez de los muros
            fan_x += dx
            fan_y += dy
            break

def reiniciar_juego():
    global pac_x, pac_y, puntos, fan_x, fan_y, mapa
    fan_x, fan_y = 10 , 5 # Volvemos a definir la posicion del fantasma
    pac_x , pac_y = 1 , 1 # Volvemos a definir la posicion del pacman
    puntos = 0 # Establecemos los puntos en 0
    mapa = [fila[:] for fila in mapa_original] # Restaurar el mapa original a demas itera fila por fila en la variable de reinicio del mapa original

def dibujar_mapa():
    pantalla.fill(negro) ## carga una pantalla en negro con las siguientes componentes en X y Y
    for y in range(mapa_alto):
        for x in range(mapa_ancho):
            if mapa[y][x] == 1:
                pygame.draw.rect(pantalla, azul, (x * tamano_celda, y * tamano_celda, tamano_celda, tamano_celda))
            elif mapa[y][x] == 2:
                pygame.draw.circle(pantalla, blanco, (x * tamano_celda + tamano_celda // 2, y * tamano_celda + tamano_celda // 2),tamano_celda // 6)
    mostrar_puntaje() ## se le agrega la funcion para presentar el puntaje

#"""Muestra la pantalla de Game Over 
def mostrar_game_over():
    pantalla.fill(negro) ## al perder sale una pantalla negra
    font = pygame.font.Font(None, 64) # Fuente del texto en tamaño en pixeles
    texto = font.render("GAME OVER", True, rojo) ## la palabra " Game over " sale en rojito 
    pantalla.blit(texto, texto.get_rect(center=(ancho // 2, alto // 2))) # dimenciones del mensaje
    pygame.display.flip() # muestra la pantalla game over
    pygame.time.delay(2000) # tiempo que tarda en mostrarte la pantalla de game over
    preguntar_volver_a_jugar("Game Over. ¿Quieres jugar de nuevo?") # Muestra el mensaje cocn tkinter de game over

# Y agreagamos la funcion volver a jugar

## Ventana de mensaje al ganar o perder si quiere seguir jugando
def preguntar_volver_a_jugar(mensaje):
    root = tk.Tk()
    root.withdraw()
    respuesta = messagebox.askyesno("Fin del juego", mensaje)
    if respuesta:
        reiniciar_juego()
    else:
        pygame.quit()
        sys.exit()

## creamos un funcion para una pantalla de win 
def mostrar_you_win():
    pantalla.fill(negro) ## al ganar sale una pantalla negra
    font = pygame.font.Font(None, 64) # Fuente del texto en tamaño en pixeles
    texto = font.render("YOU WIN", True, amarillo) ## la palabra " YOU WIN " sale en amarillo 
    pantalla.blit(texto, texto.get_rect(center=(ancho // 2, alto // 2))) # centra el mesase y define las dimenciones del mensaje
    pygame.display.flip() # muestra la pantalla game over
    pygame.time.delay(2000) # tiempo que tarda en mostrarte la pantalla de You win
    preguntar_volver_a_jugar("You win. ¿Quieres jugar de nuevo?")# Muestra el mensaje cocn tkinter de You win

# Bucle del juego
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: # Si cerramos la pestaña la variable corriendo se vuelve falso
            corriendo = False    
    
    teclas = pygame.key.get_pressed() # Cuando presionamos las flechas la posicion del pacman cambia
    if teclas[pygame.K_LEFT]:
        mover_pacman(-1, 0)
    if teclas[pygame.K_RIGHT]:
        mover_pacman(1, 0)
    if teclas[pygame.K_UP]:
        mover_pacman(0, -1)
    if teclas[pygame.K_DOWN]:
        mover_pacman(0, 1)
    
    mover_fantasma()
    mostrar_puntaje()
    dibujar_mapa()
    
    #verificar si ya no quedan puntos
    if not any(2 in fila for fila in mapa): #si no hay puntos en el mapa, llama a la funcion you win
        mostrar_you_win()
    elif pac_x == fan_x and pac_y == fan_y: # Si la posicion del pacman es igual a la del fantasma mujestra la funcion gamje over
        mostrar_game_over()
    
    pygame.draw.circle(pantalla, amarillo, (pac_x * tamano_celda + tamano_celda // 2, pac_y * tamano_celda + tamano_celda // 2), tamano_celda // 2 - 5) # Dibujamos el pacman
    pygame.draw.circle(pantalla, rojo, (fan_x * tamano_celda + tamano_celda // 2, fan_y * tamano_celda + tamano_celda // 2), tamano_celda // 2 - 5) # dibujamos el fantasma
    pygame.display.flip()
    pygame.time.delay(100)
pygame.quit()