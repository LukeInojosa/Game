 
import pygame as pg
def start_all_players(lab,n):
    lab.clear_players()
    for i in range(n):
        lab.start_new_player()
def move_all_players(lab,positions,k):
    for i in range(len(positions)):
        lab.move_player(i,positions[i]["gene"][k])
def draw_all_players(lab,n):
    for i in range(n):
        lab.draw_player(i)