import pygame as pg
import math
import random
class Labirynth:
    def __init__(self,screen,lab,start,end):
        self.players = []
        self.width_screen, self.height_screen = screen.get_size()
        self.start = start
        self.end = end
        self.screen = screen
        self.len_lab = len(lab)
        self.lab = lab
        self.width_rect, self.height_rect = self.width_screen//self.len_lab , self.height_screen//self.len_lab

    def draw_labyrinth(self):
        for i in range(self.len_lab):
            for j in range(self.len_lab):
                pg.draw.rect(self.screen,"white",pg.Rect(self.width_rect*j,self.height_rect*i,self.width_rect*self.lab[i][j],self.height_rect*self.lab[i][j]),0)
        i,j = self.end
        pg.draw.rect(self.screen,"green",pg.Rect(self.width_rect*j,self.height_rect*i,self.width_rect*self.lab[i][j],self.height_rect*self.lab[i][j]),0)

    def start_player(self):
        i, j = self.start
        self.size_player = 10 
        self.players.append((self.width_rect*j + self.width_rect/2,self.height_rect*i + self.height_rect/2))
        pg.draw.circle(self.screen,
                       (0,255,0),
                       self.players[len(self.players)-1],
                       self.size_player
                       )
    
    def move_player(self,n):

        x , y  = self.players[n]
        i_center, j_center = math.floor(y/self.height_rect),math.floor(x/self.width_rect)
        i_front, j_front = math.floor(((y+self.size_player)/self.height_rect)), math.floor(((x+self.size_player)/self.width_rect))
        i_back, j_back = math.floor((y-self.size_player)/self.height_rect), math.floor((x-self.size_player)/self.width_rect)
        
        if (i_center,j_front) == self.end:
            return 1
        
        up_free = self.lab[i_back][j_center]
        down_free = self.lab[i_front][j_center]
        back_free = self.lab[i_center][j_back]
        front_free = self.lab[i_center][j_front]

        desloc = 2
        
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            y -= desloc
        if keys[pg.K_s]:
            y += desloc
        if keys[pg.K_a]:
            x -= desloc
        if keys[pg.K_d]:
            x += desloc

        if not up_free:
            y += desloc
        if not front_free:
            x -= desloc
        if not back_free:
            x += desloc
        if not down_free:
            y -= desloc

        self.players[n] = (x,y)
        pg.draw.circle(self.screen,
                       (0,255,0),
                       (x,y),
                       self.size_player
                       )
        return 0
    
    def move_player_genetic(self,pos,n):

        x , y  = self.players[n]
        i_center, j_center = math.floor(y/self.height_rect),math.floor(x/self.width_rect)
        i_front, j_front = math.floor(((y+self.size_player)/self.height_rect)), math.floor(((x+self.size_player)/self.width_rect))
        i_back, j_back = math.floor((y-self.size_player)/self.height_rect), math.floor((x-self.size_player)/self.width_rect)
        
        if (i_center,j_front) == self.end:
            return 1
        
        up_free = self.lab[i_back][j_center]
        down_free = self.lab[i_front][j_center]
        back_free = self.lab[i_center][j_back]
        front_free = self.lab[i_center][j_front]
        desloc = 2
        if pos == 0:
            y -= desloc
        if pos == 2:
            y += desloc
        if pos == 3:
            x -= desloc
        if pos == 1:
            x += desloc

        if not up_free:
            y += desloc
        if not front_free:
            x -= desloc
        if not back_free:
            x += desloc
        if not down_free:
            y -= desloc

        self.players[n] = (x,y)
        pg.draw.circle(self.screen,
                       (0,255,0),
                       (x,y),
                       self.size_player
                       )
        return 0
    def clear_players(self):
        self.players.clear()


def create_labyrinth(N,start,end):
    NotImplemented

