import numpy as np
import time
from problem import Objective

generations = 50000
population_size = 2000
crossover_rate = 0.98
mutation_rate = 0.01
DNA_size = 4
mutation_dist = 0.25

# Problem parameters
x = 1000
y = 1000
z = 1000
m = 1000

p = 1000
alpha = 10
beta = 1

best_fitness = 0
best_DNA = 0

class GA(object):
    def __init__(self, DNA_size, cross_rate, mutation_rate, population_size, objective_function):
        self.DNA_size = DNA_size
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.population_size = population_size
        self.objective_function = objective_function
        
        population = np.random.randint(low=0, high=4000, size=(population_size, DNA_size))
        self.population = population.astype(float)


    def calculate_fitness(self):
        fitness = []
        for member in self.population:
            objective, sales, x, y, z, m = self.objective_function.calculate(member)
            if objective < 0:
                objective = 0
            fitness.append(objective)
        assert len(fitness) == self.population_size
        return np.array(fitness)

    def select(self, fitness):
        fitness += 1e-6    # add a small amount to avoid all zero fitness
        indexA = np.random.choice(np.arange(self.population_size), size=self.population_size, replace=True, p=fitness/fitness.sum())
        return self.population[indexA]

    def crossover(self, parentsA, pop, indexB):
        if np.random.rand() < self.cross_rate:
            cross_points = np.random.randint(0, 2, self.DNA_size).astype(np.bool)   # choose crossover points
            parentsA[cross_points] = pop[indexB, cross_points]
        return parentsA

    def mutate(self, child):
        for point in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:
                child[point] *= np.random.randint(low=(1-mutation_dist), high=(1+mutation_dist), size=1)
        return child

    def new_generation(self, fitness):
        pop = self.select(fitness)
        pop_copy = pop.copy()
        for parent in pop:  # for every parent
            indexB = np.random.choice(np.arange(self.population_size), size=1, replace=True, p=fitness/fitness.sum()) # Get the second parent.
            child = self.crossover(parent, pop_copy, indexB)
            child = self.mutate(child)
            parent[:] = child
        self.population = pop

def print_data(generation, fitness):
    global best_fitness, best_DNA
    local_max_fitness = np.amax(fitness)
    print('Current fitness: ' + str(local_max_fitness))

    if(local_max_fitness > best_fitness):
        best_fitness = local_max_fitness
        best_DNA = ga.population[np.argmax(best_fitness)]

    print('Gen: ' + str(generation) + ' | fitness: ' + str(best_fitness))
    print(best_DNA)



if __name__ == '__main__':
    objective_function = Objective(x, y, z, m, p, alpha, beta)

    ga = GA(DNA_size = DNA_size, cross_rate = crossover_rate,
            mutation_rate = mutation_rate, population_size = population_size,
            objective_function = objective_function)

    for generation in range(generations):
        start_time = time.time()
        fitness = ga.calculate_fitness()
        print("\n--- %s seconds ---" % (time.time() - start_time))
        print_data(generation, fitness)
        ga.new_generation(fitness)