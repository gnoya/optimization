import numpy as np
import math
import json
from random import random
from problem import Objective

class Point():
    def __init__(self, x, value):
        # Parameters of this points
        self.x = x
        
        # Value of the objective function for these parameters
        self.value = value

class Particle():
    def __init__(self, dimension):
        # Parameters of this particle
        self.x = np.random.rand(dimension, 1)

        # Velocity of this particle
        self.v = np.random.rand(dimension, 1)

        # Initialize the starting personal best point
        self.personal_best = Point(self.x.copy(), -math.inf)

    # Cap the velocity
    def cap_velocity(self, max_velocity):
        self.v[self.v > max_velocity] = max_velocity
        self.v[self.v < -max_velocity] = -max_velocity

    # Cap the parameters
    def cap_x(self, lower_bound, upper_bound):
        self.x[self.x > upper_bound] = upper_bound
        self.x[self.x < lower_bound] = lower_bound

class Swarm():
    def __init__(self, objective_function, dimension, lower_bound, upper_bound, number_particles, c1, c2, w_min, w_max, max_velocity, iterations):
        # Initialize the starting global best point
        self.global_best = Point(np.random.rand(dimension, 1), -math.inf)

        # Initialize the objective function
        self.objective_function = objective_function
        
        # Initialize the Swarm's parameters
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.number_particles = number_particles
        self.c1 = c1
        self.c2 = c2
        self.w_min = w_min
        self.w_max = w_max
        self.max_velocity = max_velocity
        self.iterations = iterations
        self.w = w_max

        # Initialize particles
        self.particles = np.array([])
        for i in range(self.number_particles):
            self.particles = np.append(self.particles, Particle(dimension))

    def calculate_objective(self):
        # Calculate objective for each particle
        for i in range(self.number_particles):
            # Calculate the objective for given parameters
            objective, _, _, _, _, _ = self.objective_function.calculate(self.particles[i].x)
            
            # Check for personal best value update
            if objective > self.particles[i].personal_best.value:
                self.particles[i].personal_best = Point(self.particles[i].x.copy(), objective)
            
            # Check for global best value update
            if objective > self.global_best.value:
                self.global_best = Point(self.particles[i].x.copy(), objective)

    def update_inertia(self, i):
        # Inertia update
        self.w = self.w_max - i * ((self.w_max - self.w_min) / self.iterations)

    def update_position(self):
        for i in range(self.number_particles):
            # Velocity update
            self.particles[i].v = self.w * self.particles[i].v.copy() + self.c1 * random() * (self.particles[i].personal_best.x.copy() - self.particles[i].x.copy()) + self.c2 * random() * (self.global_best.x.copy() - self.particles[i].x.copy())
            self.particles[i].cap_velocity(self.max_velocity)

            # Position update
            self.particles[i].x += self.particles[i].v.copy()
            self.particles[i].cap_x(self.lower_bound, self.upper_bound)


if __name__ == '__main__':
    with open('problem_config.json') as config_file:
        problem_config = json.load(config_file)
    
    with open('pso_config.json') as config_file:
        pso_config = json.load(config_file)

    # Initialize classes
    objective_function = Objective(problem_config['x'], problem_config['y'], problem_config['z'], problem_config['m'], 
                                    problem_config['p'], problem_config['alpha'], problem_config['beta'])

    swarm = Swarm(objective_function, problem_config['dimension'], problem_config['lower_bound'], problem_config['upper_bound'], 
                    pso_config['number_particles'], pso_config['c1'], pso_config['c2'], pso_config['w_min'], pso_config['w_max'], 
                    pso_config['max_velocity'], pso_config['iterations'])

    # Main loop
    for k in range(pso_config['iterations']):
        swarm.calculate_objective()
        swarm.update_inertia(k)
        swarm.update_position()
        objective_function.print_values(swarm.global_best.x)
        print()