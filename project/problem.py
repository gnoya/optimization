class Objective():
    def __init__(self, x, y, z, m, p, alpha, beta):
        self.x = x
        self.y = y
        self.z = z
        self.m = m
        self.p = p
        self.alpha = alpha
        self.beta = beta

    def calculate(self, parameters):
        x = self.x
        y = self.y
        z = self.z
        m = self.m

        # Chair
        x = x - 2 * parameters[0]
        y = y - parameters[0]
        z = z - parameters[0]

        # Table
        m = m - 4 * parameters[1]
        y = y - parameters[1]
        x = x - 2 * parameters[1]

        # Pot
        x = x - 3 * parameters[2]
        z = z - 2 * parameters[2]

        # Pan
        x = x - 2 * parameters[3]
        z = z - parameters[3]
        m = m - parameters[3]

        sales = 0

        if not (x < 0 or y < 0 or z < 0 or m < 0):
            objective = parameters[0] * self.p + \
                    parameters[1] * 2 * self.p + \
                    parameters[2] * 0.5 * self.p + \
                    parameters[3] * 0.75 * self.p

            sales = objective
            objective -= self.alpha * (x + y + z + m)
        else:
            objective = 0

        return objective, sales, x, y, z, m

    def print_values(self, parameters):
        objective, sales, x, y, z, m = self.calculate(parameters)
        print('\nValue: {}'.format(objective))
        print('Sales: {}'.format(sales))
        print('x: {}'.format(x))
        print('y: {}'.format(y))
        print('z: {}'.format(z))
        print('m: {}'.format(m))
        print('Chairs: {}'.format(parameters[0]))
        print('Tables: {}'.format(parameters[1]))
        print('Pots: {}'.format(parameters[2]))
        print('Pans: {}'.format(parameters[3]))