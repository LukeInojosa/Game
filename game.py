import pygame as pg
import labirinty as lab
import genetic as gen
import numpy as np
import random
#define length of labyrinth
pg.init()

size_screen = width_screen, height_screen = (900,600)
screen = pg.display.set_mode(size_screen)
pg.display.set_caption("New game")
clock = pg.time.Clock()
level = [
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
 [0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
 [0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
 [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0],
 [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
 [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
 [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0],
 [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
 [0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
 [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
 [0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
 [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
 [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0],
 [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
 [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
 [0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0],
 [0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


end = 0
qtd_moves = 7000
individuals = []
janela_aberta = True
i , j = final = (18,19)
labirinty = lab.Labirynth(screen,level,(1,0),final)

qtd_individuals = 100
genetic = gen.Genetic(qtd_individuals,0.5,(labirinty.width_rect*j + labirinty.width_rect/2,labirinty.height_rect*i + labirinty.height_rect/2))
genetic.initialize_population()
k =0
labirinty.clear_players()
for x in range(len(genetic.population)):
    labirinty.start_player()
while janela_aberta:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            janela_aberta = False

    if not end:
        screen.fill('black')
        labirinty.draw_labyrinth()
        if k != qtd_moves:
            for x in range(len(genetic.population)):
                    end = labirinty.move_player_genetic(genetic.population[x]['gene'][k],x)
            k = k+1     
        else: 

            for x in range(len(genetic.population)):
                genetic.population[x]['fitness'] = genetic.fitness(labirinty.players[x])
            genetic.sel_survivers()
            print(np.mean([x['fitness'] for x in genetic.population]))
            genetic.sel_parents()
            labirinty.clear_players()
            for x in range(len(genetic.population)):
                labirinty.start_player()
            k = 0
            
    else:
        screen.fill('green')
    
    pg.display.flip()
    clock.tick(1000)
pg.quit()


