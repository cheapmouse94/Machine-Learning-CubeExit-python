import pygame
from tkinter import *
import sys
import random
import numpy as np
import AIproj_GUI
import AIproj_Plot
import AIproj_map

AIproj_GUI.GUI()

WIN_H = 720
WIN_W = 1280

SQM = 64
MIN_WIN_DX = 80
MIN_WIN_DY = 72

LEVEL = AIproj_map.LEVEL

WALLS = []
EXITS = []
PENALTY = []

STARTING_POSITION = 0
AI_ACTUAL_CORDS = []


MAP_MATRIX = []
REWARD_MATRIX = []
POSSIBLE_MOVES = []
Q_VALUE = []
MAP_CORDS = []
PENALTY_INDEX = []
EXITS_INDEX = []


GAMMA = AIproj_GUI.gamma_value
LIFE_PENALTY = AIproj_GUI.life_penalty_value
PUNISH = AIproj_GUI.penalty_value
REWARD = AIproj_GUI.reward_value
MAX_ITERATIONS = AIproj_GUI.iteration_value

iteration = 0
SCORE_POSITIVE = 0
SCORE_NEGATIVE = 0
MOVES_COUNT = 0
MOVES_COUNT_TOTAL = []

class AI:
    def __init__(self, enable):
        pass  

    def map_matrix(self):
        self.K = 0
        for x in range(len(LEVEL)):
            array_temp = []
            for y in LEVEL[x]:
                if y == 'W':
                    array_temp.append('W')
                elif y == 'P':
                    array_temp.append(self.K)
                    PENALTY_INDEX.append(self.K)
                    self.K += 1  
                elif y == 'E':
                    array_temp.append(self.K)
                    EXITS_INDEX.append(self.K)
                    self.K += 1                                       
                elif y == 'O':
                    array_temp.append(self.K)
                    self.K += 1
            MAP_MATRIX.append(array_temp)
 
    def avaible_moves(self):
        for x in range(len(MAP_MATRIX)):
            for y in range(len(MAP_MATRIX[x])):
                avaible_moves = []
                if type(MAP_MATRIX[x][y]) == int:
                    if type(MAP_MATRIX[x][y-1]) == int:
                        avaible_moves.append(MAP_MATRIX[x][y-1])

                    if type(MAP_MATRIX[x][y+1]) == int:
                        avaible_moves.append(MAP_MATRIX[x][y+1])

                    if type(MAP_MATRIX[x-1][y]) == int:
                        avaible_moves.append(MAP_MATRIX[x-1][y])

                    if type(MAP_MATRIX[x+1][y]) == int:
                        avaible_moves.append(MAP_MATRIX[x+1][y])
                    POSSIBLE_MOVES.append(avaible_moves)

    def map_reward(self):
        for x in range(len(POSSIBLE_MOVES)):
            self.reward_temp = np.full((len(POSSIBLE_MOVES)), (int(-1)))
            self.PM = POSSIBLE_MOVES[x]
            for f in self.PM:
                self.reward_temp[f] = -LIFE_PENALTY
            REWARD_MATRIX.append(self.reward_temp)

        for x in range(len(REWARD_MATRIX)):
            for y in PENALTY_INDEX:
                if REWARD_MATRIX[x][y] == -LIFE_PENALTY:
                    REWARD_MATRIX[x][y] = -PUNISH
                    
        for x in range(len(REWARD_MATRIX)):
            for y in EXITS_INDEX:
                if REWARD_MATRIX[x][y] == -LIFE_PENALTY:
                    REWARD_MATRIX[x][y] = REWARD

    def q_state(self):
        for x in range(len(REWARD_MATRIX)):
            self.q_temp = []
            for y in range(len(REWARD_MATRIX[0])):
                self.q_temp.append(0)
            Q_VALUE.append(self.q_temp)

    def find_cords(self):
        self.dy = MIN_WIN_DY
        for x in range(len(MAP_MATRIX)):
            self.dx = MIN_WIN_DX
            for y in range(len(MAP_MATRIX[x])):
                if type(MAP_MATRIX[x][y]) == int:
                    MAP_CORDS.append([self.dx, self.dy])
                    self.dx += SQM
                else:
                    self.dx += SQM
            self.dy += SQM

    def draw_cell_numbers(self, screen):
        for x in range(len(MAP_CORDS)):
            font_type = pygame.font.SysFont('Arial', 16)
            text_surface_detail = font_type.render(str(x), True, (255,255,255))
            screen.blit(text_surface_detail,(MAP_CORDS[x][0]+SQM/2.5,MAP_CORDS[x][1]+SQM/3))    

    def position_init_AI(self):
        self.dx = MAP_CORDS[STARTING_POSITION][0]
        self.dy = MAP_CORDS[STARTING_POSITION][1]
        return [self.dx, self.dy]
        
    def restart_AI(self):
        global STARTING_POSITION
        self.q_state()
        #STARTING_POSITION = 0

    def new_draw_AI(self, screen, AAC):
        self.RectAI = pygame.Rect(AAC[0], AAC[1], SQM, SQM)
        pygame.draw.rect(screen, (0, 0, 204), self.RectAI)

    def softmax(self, PM, Q, SP):   
        Q_VALUE_OF_POSSIBLE_MOVES = []
        Q_VALUE_RANDOM = []
        for x in PM:
            Q_VALUE_OF_POSSIBLE_MOVES.append(Q[SP][x])
        e_x = np.exp(Q_VALUE_OF_POSSIBLE_MOVES)
        d_x = e_x / e_x.sum()
        arr_temp_3 = []
        for x in range(len(d_x)):
            d = [str(PM[x])]
            arr_temp_3 += d*int(d_x[x]*100)
            
        Q_VALUE_RANDOM = int(np.random.choice(arr_temp_3,1))
        return Q_VALUE_RANDOM

    def action_AI(self, screen):
        global STARTING_POSITION, SCORE_POSITIVE, SCORE_NEGATIVE, iteration, MAX_ITERATIONS, MOVES_COUNT, MOVES_COUNT_TOTAL

        self.rand = self.softmax(POSSIBLE_MOVES[STARTING_POSITION], Q_VALUE ,STARTING_POSITION)
        Q_VALUE[STARTING_POSITION][self.rand] = float(REWARD_MATRIX[STARTING_POSITION][self.rand]) + GAMMA*max(Q_VALUE[self.rand])
        self.new_cords_AI = MAP_CORDS[self.rand]
        self.new_draw_AI(screen, self.new_cords_AI)

        if REWARD_MATRIX[STARTING_POSITION][self.rand] == REWARD:
            STARTING_POSITION = 0
            SCORE_POSITIVE += 1
            MOVES_COUNT_TOTAL.append(MOVES_COUNT)
            MOVES_COUNT = 0
        
        elif REWARD_MATRIX[STARTING_POSITION][self.rand] == -PUNISH:
            
            STARTING_POSITION = 0
            SCORE_NEGATIVE += 1
        else:
            STARTING_POSITION = self.rand
            MOVES_COUNT += 1

        if iteration % 125 == 0 or iteration == 0:
            AIproj_Plot.Plot(Q_VALUE, SCORE_POSITIVE, SCORE_NEGATIVE, iteration, MAX_ITERATIONS, MOVES_COUNT_TOTAL)
        
        if iteration == MAX_ITERATIONS:
            print('Closing program')
            sys.exit(0)
            AIproj_GUI.GUI()
            quit()
        iteration += 1 
        
class Frame:
    def __init__(self, enable):
        self.enable = enable
    def draw_prop(self, screen):
        if self.enable:
            pygame.draw.line(screen, (255,255,255), (MIN_WIN_DX, MIN_WIN_DY),(MIN_WIN_DX+SQM*10,MIN_WIN_DY))
            pygame.draw.line(screen, (255,255,255), (MIN_WIN_DX, MIN_WIN_DY),(MIN_WIN_DX,MIN_WIN_DY+SQM*7))
            pygame.draw.line(screen, (255,255,255), (MIN_WIN_DX+SQM*10,MIN_WIN_DY),(MIN_WIN_DX+SQM*10,MIN_WIN_DY+SQM*7))
            pygame.draw.line(screen, (255,255,255), (MIN_WIN_DX,MIN_WIN_DY+SQM*7),(MIN_WIN_DX+SQM*10,MIN_WIN_DY+SQM*7))

class Grid:
    def __init__(self, enable):
        self.enable = enable
    def draw_prop(self, screen):
        if self.enable:
            #Rysowanie siatki poziomej
            for r in range(len(LEVEL)):
                pygame.draw.line(screen,(255,255,255),(MIN_WIN_DX, MIN_WIN_DY+r*SQM),(MIN_WIN_DX+SQM*11, MIN_WIN_DY+r*SQM))
            #Rysowanie siatki pionowej
            for r in range(len(LEVEL[0])):
                pygame.draw.line(screen,(255,255,255),(MIN_WIN_DX+r*SQM, MIN_WIN_DY),(MIN_WIN_DX+r*SQM, MIN_WIN_DY+SQM*8))

class Level:
    def __init__(self, enable):
        self.enable = enable
        self.prop_find_walls()
    
    def prop_find_walls(self):
        if self.enable:
            self.x = self.y = 0
            for row in LEVEL:
                for col in row:
                    if col == 'W':
                        global prop_walls
                        prop_walls = Walls((self.x + MIN_WIN_DX, self.y + MIN_WIN_DY))
                    elif col == 'P':
                        global prop_penalty
                        prop_penalty = Penalty((self.x + MIN_WIN_DX, self.y + MIN_WIN_DY))
                        pass
                    elif col == 'E':
                        global prop_exit
                        prop_exit = Exit((self.x + MIN_WIN_DX, self.y + MIN_WIN_DY))
                        pass
                    self.x+=SQM
                self.y+=SQM
                self.x=0

class Walls:
    def __init__(self, pos):
        WALLS.append(self)
        self.rectW = pygame.Rect((pos[0],pos[1],SQM,SQM))
        
    def draw_prop(self, screen):
        for x in WALLS:
            pygame.draw.rect(screen,(255,255,255),x.rectW)

class Penalty:
    def __init__(self, pos):
        PENALTY.append(self)
        self.rectP = pygame.Rect((pos[0],pos[1],SQM,SQM))

    def draw_prop(self, screen):
        for x in PENALTY:
            pygame.draw.rect(screen,(255,0,0),x.rectP)

class Exit:
    def __init__(self, pos):
        EXITS.append(self)
        self.rectE = pygame.Rect((pos[0],pos[1],SQM,SQM))

    def draw_prop(self, screen):
        for x in EXITS:
            pygame.draw.rect(screen,(0,255,0),x.rectE)   

class Inputs:
    def __init__(self):
        pass

    def draw_prop(self, screen):
        self.draw_prop_gamma(screen)
        self.draw_prop_reward(screen)
        self.draw_prop_penalty(screen)
        self.draw_prop_life_penalty(screen)
        self.draw_prop_max_iteration(screen)
        self.draw_prop_iteration(screen)
        self.draw_prop_score_positive(screen)
        self.draw_prop_score_negative(screen)

    def draw_prop_gamma(self, screen):
        self.font = pygame.font.Font(None, 32)
        self.input_box = pygame.Rect(900, 200, 100, 32)
        self.color = pygame.Color('white')
        self.text_full_z = 'Gamma = {}'
        self.text_full = self.text_full_z.format(GAMMA)
        self.txt_surface = self.font.render(self.text_full, True, self.color)
        self.width = max(200, self.txt_surface.get_width()+10)
        self.input_box.w = self.width
        screen.blit(self.txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(screen, self.color, self.input_box, 2)
    
    def draw_prop_reward(self, screen):
        self.font = pygame.font.Font(None, 32)
        self.input_box = pygame.Rect(900, 232, 100, 32)
        self.color = pygame.Color('white')
        self.text_full_z = 'Reward = {}'
        self.text_full = self.text_full_z.format(REWARD)
        self.txt_surface = self.font.render(self.text_full, True, self.color)
        self.width = max(200, self.txt_surface.get_width()+10)
        self.input_box.w = self.width
        screen.blit(self.txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(screen, self.color, self.input_box, 2)

    def draw_prop_penalty(self, screen):
        self.font = pygame.font.Font(None, 32)
        self.input_box = pygame.Rect(900, 264, 100, 32)
        self.color = pygame.Color('white')
        self.text_full_z = 'Penalty = {}'
        self.text_full = self.text_full_z.format(PUNISH)
        self.txt_surface = self.font.render(self.text_full, True, self.color)
        self.width = max(200, self.txt_surface.get_width()+10)
        self.input_box.w = self.width
        screen.blit(self.txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(screen, self.color, self.input_box, 2)

    def draw_prop_life_penalty(self, screen):
        self.font = pygame.font.Font(None, 32)
        self.input_box = pygame.Rect(900, 296, 100, 32)
        self.color = pygame.Color('white')
        self.text_full_z = 'Life Penalty = {}'
        self.text_full = self.text_full_z.format(LIFE_PENALTY)
        self.txt_surface = self.font.render(self.text_full, True, self.color)
        self.width = max(200, self.txt_surface.get_width()+10)
        self.input_box.w = self.width
        screen.blit(self.txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(screen, self.color, self.input_box, 2)
    
    def draw_prop_iteration(self, screen):
        self.font = pygame.font.Font(None, 32)
        self.input_box = pygame.Rect(900, 396, 100, 32)
        self.color = pygame.Color('white')
        self.text_full_z = 'Iteration = {}'
        self.text_full = self.text_full_z.format(iteration)
        self.txt_surface = self.font.render(self.text_full, True, self.color)
        self.width = max(200, self.txt_surface.get_width()+10)
        self.input_box.w = self.width
        screen.blit(self.txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(screen, self.color, self.input_box, 2)

    def draw_prop_max_iteration(self, screen):
        self.font = pygame.font.Font(None, 32)
        self.input_box = pygame.Rect(900, 428, 100, 32)
        self.color = pygame.Color('white')
        self.text_full_z = 'Maximum Iterations = {}'
        self.text_full = self.text_full_z.format(MAX_ITERATIONS)
        self.txt_surface = self.font.render(self.text_full, True, self.color)
        self.width = max(200, self.txt_surface.get_width()+10)
        self.input_box.w = self.width
        screen.blit(self.txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(screen, self.color, self.input_box, 2)

    def draw_prop_score_positive(self, screen):
        self.font = pygame.font.Font(None, 32)
        self.input_box = pygame.Rect(900, 492, 100, 32)
        self.color = pygame.Color('white')
        self.text_full_z = 'Score Positive = {}'
        self.text_full = self.text_full_z.format(SCORE_POSITIVE)
        self.txt_surface = self.font.render(self.text_full, True, self.color)
        self.width = max(200, self.txt_surface.get_width()+10)
        self.input_box.w = self.width
        screen.blit(self.txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(screen, self.color, self.input_box, 2)

    def draw_prop_score_negative(self, screen):
        self.font = pygame.font.Font(None, 32)
        self.input_box = pygame.Rect(900, 524, 100, 32)
        self.color = pygame.Color('white')
        self.text_full_z = 'Score Negative = {}'
        self.text_full = self.text_full_z.format(SCORE_NEGATIVE)
        self.txt_surface = self.font.render(self.text_full, True, self.color)
        self.width = max(200, self.txt_surface.get_width()+10)
        self.input_box.w = self.width
        screen.blit(self.txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(screen, self.color, self.input_box, 2)


def refresh_props(screen, ai, ai_piAI, prop_frame, prop_grid, prop_walls, prop_penalty, prop_exit, prop_inputs):
    
    prop_frame.draw_prop(screen)
    prop_grid.draw_prop(screen)
    prop_walls.draw_prop(screen)
    prop_penalty.draw_prop(screen)
    prop_exit.draw_prop(screen)
    prop_inputs.draw_prop(screen)
    ai.draw_cell_numbers(screen)
    if AIproj_GUI.VFR:
        for x in range(MAX_ITERATIONS):
            ai.action_AI(screen)
    else:
        ai.action_AI(screen)
    
def events(prop_inputs):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
            quit()

def main():
    clock = pygame.time.Clock()
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Reinforcement Learining with Python - by Grzegorz Jakimiuk')
    screen = pygame.display.set_mode((WIN_W,WIN_H))

    prop_frame = Frame(True)
    prop_grid = Grid(True)
    prop_level = Level(True)
    prop_inputs = Inputs()
    ai = AI(True)
    ai.map_matrix()
    ai.avaible_moves()
    ai.map_reward()
    ai.q_state()
    ai.find_cords()
    ai_piAI = ai.position_init_AI()
    
    flag = True
    while flag:
        clock.tick(200)
        events(prop_inputs)
        screen.fill((0,0,0))
        refresh_props(screen, ai, ai_piAI, prop_frame, prop_grid, prop_walls, prop_penalty, prop_exit, prop_inputs)
        pygame.display.flip()

if AIproj_GUI.destiny:
    main()