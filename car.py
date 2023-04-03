class Car:
    def __init__(self,id):
        self.id = id
        self.route = [0]
        self.place = 0
        self.time = 0
    
    def reset(self):
        self.route = [0]
        self.place = 0
        self.time = 0

