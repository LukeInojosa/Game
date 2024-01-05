import pygame as pg
import labirinty as lab
import genetic as gen
import numpy as np
import utility
import maze
def get_move():
    if event.key == pg.K_w:
        return 0
    if event.key == pg.K_s:
        return 2
    if event.key == pg.K_d:
        return 1
    if event.key == pg.K_a:
        return 3
    if event.key == pg.K_ESCAPE:
        return 4
#Initial configurations
pg.init()
size_screen = width_screen, height_screen = (1300,700)

#initialize display
screen = pg.display.set_mode(size_screen)
pg.display.set_caption("New game")

#initialize clock controller
clock = pg.time.Clock()

start = (1,0)
level = maze.create_maze(50,start)
# level = [[1,1,1,1,1],
#          [0,0,0,1,0],
#          [1,0,1,1,1],
#          [1,1,1,0,0],
#          [1,0,0,0,0]
#          ]
end = False
final = (len(level[0]) - 2,len(level[0]) - 1)


#define labirinty
labirinty = lab.Labirynth(screen,level,start,final)
NO_MOVE = -1
move = NO_MOVE

#genetic algorithm
genetic = gen.Genetic(50,0.5,(final[1]*labirinty.width_rect,final[0]*labirinty.height_rect),labirinty)
genetic.initialize_population()
utility.start_all_players(labirinty,len(genetic.population),[x["child"] for x in genetic.population])
k = 0
janela_aberta = True
fps = 100000
gen =0
while janela_aberta:
    #move = NO_MOVE
    for event in pg.event.get():
        if event.type == pg.QUIT:
            janela_aberta = False
        if event.type == pg.KEYDOWN:
            move = get_move()
    # if move == 4:
    #     labirinty.draw_labyrinth()
    #     for i in genetic.population:
    #         print(i)
    if not end and move != 4:
        # labirinty.draw_labyrinth()
        # pos = labirinty.move_player(0,move)
        # print(genetic.fitness(pos["current_position"]))
        # labirinty.draw_player(0)
        if k < genetic.max_len:
            labirinty.draw_labyrinth()
            utility.move_all_players(labirinty,genetic.population,k)
            utility.draw_all_players(labirinty,len(genetic.population))
            k += 1
        else:
            gen +=1
            print("geração:  ", gen)
            genetic.calc_fitness([labirinty.players[i].info[-1]["current_position"] for i in range(len(labirinty.players))])
            best = genetic.best_fit()
            if best["fitness"] == 0:
                fps = 10
                end = True
            genetic.sel_survivers()
            print(np.mean([x["fitness"] for x in genetic.population]))
            genetic.reproduce()
            utility.start_all_players(labirinty,len(genetic.population),[x["child"] for x in genetic.population])
            k = 0
    elif move != 4:
        if k < genetic.max_len:
            labirinty.draw_labyrinth()
            labirinty.move_player(0,best["gene"][k])
            labirinty.draw_player(0)
            k+=1
        else :
            k =0
            labirinty.clear_players()
            labirinty.start_new_player()
        
    pg.display.flip()
    clock.tick(fps)
pg.quit()



