class Fitness:
    def __init__(self, route, id):
        self.id = id
        self.route = route
        self.time = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        if self.time ==0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i + 1 < len(self.route):
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.time(toCity)
            self.time = pathDistance
        return self.time
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness