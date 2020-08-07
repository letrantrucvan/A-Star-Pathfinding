# -*- coding: utf-8 -*-

import pygame 
import os, sys
#from project import *
from color import *
import time
import random
from threading import Thread


my_color = [GREEN_LEAF, ORANGE, LightGoldenrodYellow, Moccasin, SlateBlue1, IndianRed, Orchid1, LemonChiffon1, NavajoWhite3, Sienna2]
clock = pygame.time.Clock()
os.environ['SDL_VIDEO_CENTERED'] = '1' # Center the screen 
size = 25

class Cell():
    
    def __init__(self, x, y, color, zoom):
        self.x = x  
        self.y = y
        self.color = color
 
        if zoom == True:
            pygame.draw.circle(display, self.color, (self.x + int(size/2), self.y + int(size/2)), int(size/8), 0)
            pygame.display.update()
            Thread(target = self.animation(), args=(self,)).start()
        else:
            pygame.draw.rect(display, random.choice(my_color), (x, y, size +1, size +1))    
            
    def animation(self):
        
        for i in range(6):
            pygame.draw.circle(display, self.color,(self.x + int(size/2), self.y + int(size/2)), int(size/12 + size*i/12), 0)
            time.sleep(0.015)
            pygame.display.flip()
            
        pygame.draw.rect(display, self.color, (self.x, self.y, size , size))    
        pygame.display.update()

        
def draw_grid():

    global width, height, display

    for i in range(int(height/size)):
        pygame.draw.aaline(display, BLUE, (0, i*size), (width, i*size))
    for i in range(int(width/size)):
        pygame.draw.aaline(display, BLUE, (i*size, 0), (i*size, height))
    pygame.display.update()

def update_obstacle(matrix):
    """
    Draw all obstacles with black blue color
    """
    global width, height, display, size
    print(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 'o':
                pygame.draw.rect(display, BLACK_BLUE, (j*size, i*size, size+1,size+1))
               
    pygame.display.update()
    
def update_path(path):
    """
    Draw the solution - the path from A* algorithm
    """
    
    global width, height, display, size
    
    for x, y in path:
        Cell(y*size, x*size, random.choice(my_color), False)
        pygame.display.update()      
        time.sleep(0.01)    
        
    while True:
        for x, y in path:
            Cell(y*size, x*size, random.choice(my_color), False)
            pygame.display.flip()
            #Thread(target = change_color, args = (y*size, x*size)).start()
            

def change_color(x, y):
    global width, height, display, size
    while True:
        pygame.draw.rect(display, random.choice(my_color), (x, y, size+1, size+1))    
        pygame.display.update()
        time.sleep(0.04)

def explored_path(path):
    """
    Show all the explored cells 
    """
    global width, height, display, size
    for x, y in path:
        Cell(y*size, x*size, BLUE, True)
        pygame.display.update()
        

def update_grid(PATH):
    global width, height, display, size
    path, explored_set = PATH

    # initial state - green circle
    pygame.draw.circle(display, GREEN_LEAF, (int(path[0][1]*size + size/2) + 1, int(path[0][0]*size + size/2) + 1), int(size/2), 0)

    # goal state - red circle
    pygame.draw.circle(display, RED, (int(path[-1][1]*size + size/2) + 1, int(path[-1][0]*size + size/2) + 1), int(size/2), 0)
    
    pygame.display.update()

    time.sleep(1)

    explored_path(explored_set)

    update_path(path)

    



def update_display():
    global display, width, height, size
    FPS = 240
    while True:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    pygame.quit()
                    sys.exit()
        except:
            pass
        clock.tick(FPS)
        pygame.display.flip()

    print("OUT")
def main(p, s):
    global width, height, size, display

    problem = p
    width = problem.column * size
    height = problem.row * size
    solution = s


    pygame.init()
    pygame.display.set_caption("A-Star Visualization")
    display = pygame.display.set_mode((width,height))
    display.fill((255,255,255))

        
    draw_grid()

    pygame.display.flip()
   
    update_obstacle(problem.matrix)
    if solution[0] == -1:
        explored_path(solution[1])        
    else:   

        thread = Thread(target=update_grid, args = (solution,))
        thread.start()

        update_display()
   