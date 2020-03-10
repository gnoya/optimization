import numpy as np
import math
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
    def __init__(self, objective_function, dimension, number_particles, c1, c2, w_min, w_max, lower_bound, upper_bound, max_velocity, iterations):
        # Initialize the starting global best point
        self.global_best = Point(np.random.rand(dimension, 1), -math.inf)

        # Initialize the objective function
        self.objective_function = objective_function
        
        # Initialize the Swarm's parameters
        self.iterations = iterations
        self.number_particles = number_particles
        self.c1 = c1
        self.c2 = c2
        self.w_min = w_min
        self.w_max = w_max
        self.w = w_max
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.max_velocity = max_velocity

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


# Declare parameters
dimension = 4
number_particles = 500
c1 = 1
c2 = 1
w_min = 0.2
w_max = 0.9
lower_bound = 0
upper_bound = 7500
iterations = 5000
max_velocity = 10

# Problem parameters
x = 1000
y = 1000
z = 1000
m = 1000

p = 1000
alpha = 10
beta = 1

# Initialize classes
objective_function = Objective(x, y, z, m, p, alpha, beta)
swarm = Swarm(objective_function, dimension, number_particles, c1, c2, w_min, w_max, lower_bound, upper_bound, max_velocity, iterations)

# Main loop
for k in range(iterations):
    swarm.calculate_objective()
    swarm.update_inertia(k)
    swarm.update_position()
    # print(swarm.global_best.x)
    # print(swarm.global_best.value)
    objective_function.print_values(swarm.global_best.x)
    print()