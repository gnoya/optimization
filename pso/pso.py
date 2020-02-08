import numpy as np
import math
from random import random

class Objective():    
    def calculate(self, x):
        return np.sum(np.square(x))

class Point():
    def __init__(self, x, value):
        self.x = x
        self.value = value

class Particle():
    def __init__(self, dimension):
        self.x = np.random.rand(dimension, 1)
        self.v = np.random.rand(dimension, 1)
        self.personal_best = Point(self.x.copy(), math.inf)

    def cap_velocity(self, max_velocity):
        self.v[self.v > max_velocity] = max_velocity
        self.v[self.v < -max_velocity] = -max_velocity

    def cap_x(self, lower_bound, upper_bound):
        self.x[self.x > upper_bound] = upper_bound
        self.x[self.x < lower_bound] = lower_bound

class Swarm():
    def __init__(self, objective_function, dimension, number_particles, c1, c2, w_min, w_max, lower_bound, upper_bound, max_velocity, iterations):
        self.global_best = Point(np.random.rand(dimension, 1), math.inf)
        self.objective_function = objective_function
        self.particles = np.array([])
        self.c1 = c1
        self.c2 = c2
        self.w_min = w_min
        self.w_max = w_max
        self.w = w_max
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.max_velocity = max_velocity
        self.iterations = iterations
        self.number_particles = number_particles

        for i in range(self.number_particles):
            self.particles = np.append(self.particles, Particle(dimension))

    def calculate_objective(self):
        for i in range(self.number_particles):
            objective = self.objective_function.calculate(self.particles[i].x)

            if objective < self.particles[i].personal_best.value:
                self.particles[i].personal_best = Point(self.particles[i].x.copy(), objective)
            
            if objective < self.global_best.value:
                self.global_best = Point(self.particles[i].x.copy(), objective)

    def update_inertia(self, i):
        self.w = self.w_max - i * ((self.w_max - self.w_min) / self.iterations)

    def update_position(self):
        for i in range(self.number_particles):
            # Velocity
            self.particles[i].v = self.w * self.particles[i].v.copy() + self.c1 * random() * (self.particles[i].personal_best.x.copy() - self.particles[i].x.copy()) + self.c2 * random() * (self.global_best.x.copy() - self.particles[i].x.copy())
            self.particles[i].cap_velocity(self.max_velocity)

            # Position
            self.particles[i].x += self.particles[i].v.copy()
            self.particles[i].cap_x(self.lower_bound, self.upper_bound)

dimension = 10
number_particles = 50
c1 = 1
c2 = 2
w_min = 0.2
w_max = 0.9
lower_bound = -10
upper_bound = 10
iterations = 5000
max_velocity = 0.1

objective_function = Objective()
swarm = Swarm(objective_function, dimension, number_particles, c1, c2, w_min, w_max, lower_bound, upper_bound, max_velocity, iterations)

for k in range(iterations):
    swarm.calculate_objective()
    swarm.update_inertia(k)
    swarm.update_position()
    print(k, swarm.global_best.value)