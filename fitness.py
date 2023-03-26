class Fitness:
    def __init__(self, route, id, time):
        self.id = id
        self.route = route
        self.time = time
        self.fitness= 0.0
    
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness