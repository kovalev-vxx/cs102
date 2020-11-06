# Подключение библиотеки PyGame
import pygame
# Инициализация PyGame
pygame.init()
# Окно игры: размер, позиция
gameScreen = pygame.display.set_mode((400, 300))
# Модуль os - позиция окна
import os
x = 100
y = 100
os.environ['Sp_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
# Параметры окна
size = [500, 500]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Test drawings")
gameScreen.fill((0,0,255))
pygame.display.flip()
