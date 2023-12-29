sample = [{'a': 1, 'fitness': 0},{'a': 4, 'fitness': 2}] 
s = sorted(sample, key = lambda x: x['fitness'] ,reverse = True)
print(s)
