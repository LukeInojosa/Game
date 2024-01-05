import random
class Genetic:
    def __init__(self,len_population, cross_rate,target,labyrinth):
        self.culture = []
        self.population = []
        self.offspring = []
        self.labyrinth = labyrinth
        self.max_len = 0
        self.target = target
        self.cross_rate = cross_rate
        self.len_population = len_population
        self.num_offspring = self.len_population*cross_rate

    def sel_survivers(self):
        bests = sorted(self.population, key = lambda x: x['fitness'], reverse= True)
        while len(bests) > self.len_population:
            bests.pop(0)
        self.population = bests

    def best_fit(self):
        return min(self.population, key = lambda x: x["fitness"])
    def reproduce(self):
        for i in self.population:
            i["child"] = False
        while len(self.offspring) < self.num_offspring:
           parent1 , parent2 = self.torneio()
           child1, child2 = self.cross_over(parent1,parent2)
           self.offspring.append(self.mutation(child1))
           self.offspring.append(self.mutation(child2))
        self.population = self.population + self.offspring
        mx = max(self.population,key=lambda x: len(x["gene"]))
        self.max_len = len(mx["gene"])
        self.offspring.clear()


    def torneio(self):
        sample = random.sample(self.population,5)
        sample = sorted(sample, key = lambda x: x['fitness'])
        return (sample[0],sample[1])
    
    def initialize_gene(self,initial_position,gen):
        wrong_decision = (-1,-1)
        new_gene = gen["gene"]
        positions_decision , wrong_decisions = [], []
        if self.culture:
            positions_decision = [x[0] for x in self.culture]
            wrong_decisions = [x[1] for x in self.culture]
        
        current_position = initial_position
        new_move = 0
        dead_end = False
        while not dead_end:
            #remove wrong decisions
            free_directions = self.labyrinth.free_directions(current_position)
            #no reverse
            if len(new_gene) > 0:
                backtrack = self.labyrinth.reverse(new_gene[-1])
                free_directions.remove(backtrack)
            #remevo dead end decisions
            free_directions_before = [x for x in free_directions]
            for i in range(len(positions_decision)):
                if positions_decision[i] == current_position and wrong_decisions[i] in free_directions:
                    free_directions.remove(wrong_decisions[i])
            #switch decision
            if len(free_directions) > 0: new_move = random.choices(free_directions)[0]
            if len(free_directions_before) > 1 and len(free_directions) > 0: wrong_decision = (current_position,new_move)
            if len(free_directions) > 0:
                current_position = self.labyrinth.move_index(current_position,new_move)
                new_gene.append(new_move)
            else:
                dead_end = True
            
        new_gene.append(5)
        self.culture = self.culture + [wrong_decision] if wrong_decision not in self.culture else self.culture
        return self.individual(gene = new_gene)
    
    def initialize_population(self):
        for i in range(self.len_population):
            self.population.append(self.initialize_gene(self.labyrinth.start,{"gene":[], "fitness": float("inf"),"child": True}))
        self.max_len = len(max(self.population,key=lambda x: len(x["gene"]))["gene"])

    def mutation(self,gene,probability = 1):
        gen = gene["gene"]
        current_position = self.labyrinth.start
        possible = []
        if random.random() <= probability:
            for i in range(len(gen)):
                free_directions = self.labyrinth.free_directions(current_position)
                if self.labyrinth.reverse(gen[max(i-1,0)]) in free_directions:
                    free_directions.remove(self.labyrinth.reverse(gen[max(i-1,0)]))
                if gen[i] in free_directions:
                    free_directions.remove(gen[i])
                if len(free_directions) > 0:
                    possible.append({"i": i,"position": current_position})
                current_position = self.labyrinth.move_index(current_position,gen[i])
            choice = random.choices(possible)[0]
            gen = self.initialize_gene(choice["position"],self.individual(gene = gen[:choice["i"]]))
        else:
            gen = gene
        return gen

    def cross_over(self,gene1,gene2):
        gen1 = gene1["gene"]
        gen2 = gene2["gene"]
        cross = self.cross_points(gen1,gen2)
        if len(cross) > 0:
            cut = random.choices(cross)[0]
            child1 = self.individual(gene = gen1[:cut]+ gen2[cut:])
            child2 = self.individual(gene = gen2[:cut]+ gen1[cut:])
            childs = (child1,child2)
        else:
            childs = (gene1,gene2)
        return childs
    
    def cross_points(self,gene1,gene2):
        cross = []
        curr_pos_gen1 = self.labyrinth.start
        curr_pos_gen2 = self.labyrinth.start
        for i in range(min(len(gene1)-1,len(gene2)-1)):
            curr_pos_gen1 = self.labyrinth.move_index(curr_pos_gen1,gene1[i])
            curr_pos_gen2 = self.labyrinth.move_index(curr_pos_gen2,gene2[i])
            if curr_pos_gen1 == curr_pos_gen2:
                cross.append(i+1)
        return cross
    
    def calc_fitness(self,reach_generation):
        self.population = [{"gene" : self.population[i]["gene"], "fitness": self.fitness(reach_generation[i])} for i in range(len(self.population))]
    def individual(self,gene,fitness = float("inf"),child = True):
        return {"gene": gene,"fitness": fitness,"child":child}
    def fitness(self,reach):
        return (self.target[0] - reach[0])**2 + (self.target[1] - reach[1])**2




