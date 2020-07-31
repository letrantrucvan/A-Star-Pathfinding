
# -*- coding: utf-8 -*-
import pygame 
import os, sys
from project import *
import time
import random
from threading import Thread
width = 1000
height = 800
size = 25
GREEN_LEAF = pygame.Color(128,255,0)
PINK = pygame.Color(255,128,255)
RED = pygame.Color(226,55,22)

BLUE = pygame.Color(0, 190, 218, 10)
BLACK_BLUE = pygame.Color(12,53,71)
ORANGE = pygame.Color(255,165,0)
PRUNE = pygame.Color(196,0,0)
LightGoldenrodYellow  = pygame.Color(250, 250, 210)
Moccasin = pygame.Color(255, 228, 181)
SlateBlue1 = pygame.Color(131, 111, 255)
IndianRed = pygame.Color(205, 92, 92)
Orchid1 = pygame.Color(255, 131, 250)
my_color = [GREEN_LEAF, ORANGE, LightGoldenrodYellow, Moccasin, SlateBlue1, IndianRed, BLUE, Orchid1]
FPS = 240
clock = pygame.time.Clock()
os.environ['SDL_VIDEO_CENTERED'] = '1' # Center the screen 
pygame.init()
display = pygame.display.set_mode((width,height))
display.fill((255,255,255))
    
def draw_grid():
    global width, height, display

    for i in range(int(height/size)):
        pygame.draw.aaline(display, BLUE, (0, i*size), (width, i*size))
    for i in range(int(width/size)):
        pygame.draw.aaline(display, BLUE, (i*size, 0), (i*size, height))
    pygame.display.update()

def update_obstacle(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                pygame.draw.rect(display, BLACK_BLUE, (j*size, i*size, size+1,size+1))
                
    
def update_path(path):
    global size
    for x, y in path:
        Cell(y*size, x*size, ORANGE, False)
        pygame.display.update()
        Thread(target = nghich_ngom, args = (y*size, x*size)).start()
        time.sleep(0.01)
def nghich_ngom(x, y):
    global size, display
    while True:
        pygame.draw.rect(display, random.choice(my_color), (x, y, size +1, size +1))    
        pygame.display.update()
        time.sleep(0.02)
def explored_path(path):
    global size
    for x, y in path:
        Cell(y*size, x*size, BLUE, True)
        pygame.display.update()
        

def update_grid(PATH):
    path, explored_set = PATH
    pygame.draw.circle(display, GREEN_LEAF, (int(path[0][1]*size + size/2), int(path[0][0]*size + size/2)), int(size/2), 0)
    pygame.draw.circle(display, RED, (int(path[-1][1]*size + size/2), int(path[-1][0]*size + size/2)), int(size/2), 0)
    

    pygame.display.update()
    explored_path(explored_set)
    update_path(path)

    
class Cell():
    def __init__(self, x, y, color, zoom):

        self.x = x
        self.y = y
        self.color = color
        self.zoom = zoom
        if zoom == True:
            pygame.draw.circle(display, self.color, (self.x + int(size/2), self.y + int(size/2)), int(size/8), 0)
            pygame.display.update()
            self.animation()
        
    def animation(self):
        for i in range(4):
            pygame.draw.circle(display, self.color,(self.x + int(size/2), self.y + int(size/2)), int(size/8 + size*i/8), 0)
            time.sleep(0.015)
            pygame.display.update()
        pygame.draw.rect(display, self.color, (self.x, self.y, size +1, size +1))    
        pygame.display.update()
pygame.display.flip()
draw_grid()
def update_display():
    global display, FPS

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(FPS)
        pygame.display.flip()
if __name__ == "__main__":
    problem = get_problem("E:\AI\input4.txt")

    Khoa_pr0 = a_star(problem)

    update_obstacle(problem.matrix)
    if Khoa_pr0[0] == -1:
        explored_path(Khoa_pr0[1])
    else:   
        thread = Thread(target=update_grid, args = (Khoa_pr0,))
        
        thread.start()
        update_display()

    