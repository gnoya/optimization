import numpy as np
import time
import json
from problem import Objective

best_fitness = 0
best_DNA = 0

class GA(object):
    def __init__(self, objective_function, DNA_size, lower_bound, upper_bound, population_size, crossover_rate, mutation_rate, mutation_dist):
        self.objective_function = objective_function
        self.DNA_size = DNA_size
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.population_size = population_size
        self.cross_rate = crossover_rate
        self.mutate_rate = mutation_rate
        self.mutation_dist = mutation_dist

        population = np.random.randint(low=0, high=1000, size=(population_size, DNA_size))
        self.population = population.astype(float)

    def calculate_fitness(self):
        fitness = []
        for member in self.population:
            objective, sales, x, y, z, m = self.objective_function.calculate(member.reshape(-1, 1))
            if objective < 0:
                objective = 0
            fitness.append(objective)
        assert len(fitness) == self.population_size
        return np.array(fitness).astype(float)

    def select(self, fitness):
        fitness += 1e-6
        indexA = np.random.choice(np.arange(self.population_size), size=self.population_size, replace=True, p=fitness/fitness.sum())
        return self.population[indexA]

    def crossover(self, parentsA, pop, indexB):
        if np.random.rand() < self.cross_rate:
            cross_points = np.random.randint(0, 2, self.DNA_size).astype(np.bool)
            parentsA[cross_points] = pop[indexB, cross_points]
        return parentsA

    def mutate(self, child):
        for point in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:
                child[point] *= np.random.randint(low=(1-self.mutation_dist), high=(1+self.mutation_dist), size=1)
        return child

    def new_generation(self, fitness):
        pop = self.select(fitness)
        pop_copy = pop.copy()
        for parent in pop:
            indexB = np.random.choice(np.arange(self.population_size), size=1, replace=True, p=fitness/fitness.sum())
            child = self.crossover(parent, pop_copy, indexB)
            child = self.mutate(child)
            parent[:] = child
        self.population = pop

def print_data(generation, fitness):
    global best_fitness, best_DNA
    local_max_fitness = np.amax(fitness)

    if(local_max_fitness > best_fitness):
        print(local_max_fitness, best_fitness)
        best_fitness = local_max_fitness
        best_DNA = ga.population[np.argmax(fitness)]

    objective_function.print_values(best_DNA.reshape(-1, 1))

if __name__ == '__main__':
    with open('problem_config.json') as config_file:
        problem_config = json.load(config_file)
    
    with open('genetic_config.json') as config_file:
        genetic_config = json.load(config_file)

    # Initialize classes
    objective_function = Objective(problem_config['x'], problem_config['y'], problem_config['z'], problem_config['m'], 
                                    problem_config['p'], problem_config['alpha'], problem_config['beta'])

    ga = GA(objective_function, problem_config['dimension'], problem_config['lower_bound'], problem_config['upper_bound'], 
            genetic_config['population_size'], genetic_config['crossover_rate'], genetic_config['mutation_rate'],
            genetic_config['mutation_dist'])

    for generation in range(genetic_config['generations']):
        fitness = ga.calculate_fitness()
        print_data(generation, fitness)
        ga.new_generation(fitness)