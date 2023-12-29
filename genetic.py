import random
import math
class Genetic:
    def __init__(self,len_population, cross_rate,target):
        self.len_gene = 7000
        self.target = target
        self.cross_rate = cross_rate
        self.len_population = len_population
        self.population = []
        self.offspring = []
        self.num_offspring = self.len_population*cross_rate
    
    def sel_survivers1(self):
        fit = [10000000/i['fitness'] for i in self.population]
        soma = sum(fit)
        while len(self.population) > self.len_population:
            choice = random.choices(self.population, weights = [f/soma for f in fit], k = 1)[0]
            fit.pop(self.population.index(choice))
            self.population.remove(choice)

    def sel_survivers(self):
        bests = sorted(self.population, key = lambda x: x['fitness'])
        while len(bests) > self.len_population:
            bests.pop(0)
        
        self.population = bests


    def worst_fit(self, group):
        return max(group, key=lambda x:x['fitness'])

    def best_fit(self, group):
        return min(group, key=lambda x:x['fitness'])
    
    def sel_parents(self):
        while len(self.offspring) < self.num_offspring:
           parent1 , parent2 = self.torneio()
           child1, child2 = self.cross_over(parent1,parent2)
           self.offspring.append({"gene":self.mutation(child1), "fitness": 0})
           self.offspring.append({"gene":self.mutation(child2), "fitness": 0})
        self.population = self.population + self.offspring

    def torneio(self):
        sample = random.sample(self.population,10)
        sample = sorted(sample, key = lambda x: x['fitness'] ,reverse = True)
        parents = [sample[0],sample[1]]
        return [p['gene'] for p in parents]
    
    def initialize_gene(self):
        n = 20
        gene = []
        for i in range(0,self.len_gene, n):
            choice = random.choices([0,1,2,3],weights=[0.25,0.25,0.25,0.25])[0]
            gene = gene + [choice for _ in range(n)]
        return {"gene": gene, "fitness": 0}
    
    def initialize_population(self):
        for i in range(self.len_population):
            self.population.append(self.initialize_gene())

    def mutation1(self,gene):
        cut1, cut2 = random.randint(0,len(gene)-1), random.randint(0,len(gene)-1)
        cut_start , cut_end = min(cut1,cut2), max(cut1,cut2)
        move = random.choices([0,1,2,3],weights=[.25,.25,.25,.25])[0]
        for i in range(cut_start,cut_end+1):
            gene[i] = move
        return gene
    
    def mutation(self,gene,p = 0.3):
        lim = random.randint(3,30)
        percent = p
        n = random.randint(1,math.ceil((self.len_gene//lim) * percent))
        for i in range(n):
            cut = random.randint(lim,len(gene)-1)
            move = random.choices([0,1,2,3],weights=self.probabilites(gene,cut,lim))[0]
            gene = gene[:(cut-lim)] + [move for i in range(lim)] + gene[cut:]
        return gene
    
    def probabilites(self,gene,cut,lim):
        op = lambda x: 1/x if x > 0 else 0
        amp = 4
        analise = gene[max(cut-amp*lim,0):cut-lim]
        length = len(analise)
        if length > 0:
            up,rigth,down,left = [analise.count(i)/length for i in range(4)]
            u, r, d , l = op(down),op(left),op(up),op(rigth)
            arr = [u,r,d,l]
            mx = max(arr)
            arr = [(mx*1.2 if x == 0 else x) for x in arr]
            s = sum(arr)
            up,rigth,down,left =[x/s for x in arr]
        else:
            up,rigth,down,left = [.25,.25,.25,.25]
        return [up,rigth,down,left]

    def cross_over(self,gene1,gene2):
        cut1, cut2 = random.randint(0,len(gene1)-1),random.randint(1,len(gene1)-1)
        cut1, cut2 = min(cut1,cut2), max(cut1,cut2)
        child1 = gene1[:cut1]+ gene2[cut1:cut2] + gene1[cut2:]
        child2 = gene2[:cut1]+ gene1[cut1:cut2] + gene2[cut2:]
        return child1, child2
    
    def fitness(self,reach):
        return 10000000/((self.target[0] - reach[0])**2 + (self.target[1] - reach[1])**2)




