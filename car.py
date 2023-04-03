class Car:
    def __init__(self,id):
        self.id = id
        self.route = []
        self.place = 0
        self.time = 0
    
    def reset(self):
        self.route = []
        self.place = 0
        self.time = 0

