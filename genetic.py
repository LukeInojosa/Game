import random
import math
class Genetic:
    def __init__(self,len_population, cross_rate,target,len_gene,labyrinth):
        self.labyrinth = labyrinth
        self.len_gene = len_gene
        self.target = target
        self.cross_rate = cross_rate
        self.len_population = len_population
        self.population = []
        self.offspring = []
        self.num_offspring = self.len_population*cross_rate

    def sel_survivers(self):
        bests = sorted(self.population, key = lambda x: x['fitness'], reverse= True)
        while len(bests) > self.len_population:
            bests.pop(0)
        self.population = bests

    def best_fit(self):
        return min(self.population, key = lambda x: x["fitness"])
    def reproduce(self):
        while len(self.offspring) < self.num_offspring:
           parent1 , parent2 = self.torneio()
           child1, child2 = self.cross_over(parent1,parent2)
           self.offspring.append({"gene":self.mutation(child1), "fitness": float("inf")})
           self.offspring.append({"gene":self.mutation(child2), "fitness": float("inf")})
        self.population = self.population + self.offspring
        self.offspring.clear()

    def torneio(self):
        sample = random.sample(self.population,5)
        sample = sorted(sample, key = lambda x: x['fitness'])
        parents = [sample[0],sample[1]]
        return [p['gene'] for p in parents]
    
    def initialize_gene(self,length,initial_position,gen):
        new_gene = gen
        current_position = initial_position
        new_move = 0
        dead_end = False
        for i in range(length):
            if not dead_end:
                free_directions = self.labyrinth.free_directions(current_position)
                if len(new_gene)!= 0:
                    backtrack = self.labyrinth.reverse(new_gene[-1])
                    if backtrack in free_directions:
                        free_directions.remove(backtrack)
                if len(free_directions) > 0:
                    new_move = random.choices(free_directions)[0]
                    current_position = self.labyrinth.move_index(current_position,new_move)
                else:
                    dead_end = True
                new_gene.append(new_move)
            else:
                new_gene.append(new_move)

        return {"gene": new_gene , "fitness": float("inf")}
    
    def initialize_population(self):
        for i in range(self.len_population):
            self.population.append(self.initialize_gene(self.len_gene,self.labyrinth.start,[]))

    def mutation(self,gene,probability = 0.4):
        current_position = self.labyrinth.start
        possible = []
        if random.random() <= probability:
            for i in range(len(gene)):
                free_directions = self.labyrinth.free_directions(current_position)
                if self.labyrinth.reverse(gene[max(i-1,0)]) in free_directions:
                    free_directions.remove(self.labyrinth.reverse(gene[max(i-1,0)]))
                if gene[i] in free_directions:
                    free_directions.remove(gene[i])
                if len(free_directions) > 0:
                    possible.append({"i": i,"position": current_position})
                current_position = self.labyrinth.move_index(current_position,gene[i])
            choice = random.choices(possible)[0]
            gene = self.initialize_gene(self.len_gene - choice["i"],choice["position"],gene[:choice["i"]])["gene"]
        return gene

    def cross_over(self,gene1,gene2):
        cross = self.cross_paths(gene1,gene2)
        if len(cross) != 0:
            cut = random.choices(cross)[0]
            child1 = gene1[:cut]+ gene2[cut:]
            child2 = gene2[:cut]+ gene1[cut:]
            child = (child1,child2)
        else:
            child = (gene1,gene2)
        return child
    
    def cross_paths(self,gene1,gene2):
        cross = []
        curr_pos_gen1 = self.labyrinth.start
        curr_pos_gen2 = self.labyrinth.start
        for i in range(self.len_gene):
            curr_pos_gen1 = self.labyrinth.move_index(curr_pos_gen1,gene1[i])
            curr_pos_gen2 = self.labyrinth.move_index(curr_pos_gen2,gene2[i])
            if curr_pos_gen1 == curr_pos_gen2:
                cross.append(i+1)
        return cross
    
    def calc_fitness(self,reach_generation):
        self.population = [{"gene" : self.population[i]["gene"], "fitness": self.fitness(reach_generation[i])} for i in range(len(self.population))]

    def fitness(self,reach):
        return (self.target[0] - reach[0])**2 + (self.target[1] - reach[1])**2




