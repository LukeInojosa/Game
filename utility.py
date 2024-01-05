 
import pygame as pg
def start_all_players(lab,n,color):
    lab.clear_players()
    for i in range(n):
        lab.start_new_player(color[i])
def move_all_players(lab,positions,k):
    for i in range(len(positions)):
        gene = positions[i]["gene"]
        p = min(k,len(gene) - 1)
        lab.move_player(i,gene[p])
def draw_all_players(lab,n):
    for i in range(n):
        lab.draw_player(i)