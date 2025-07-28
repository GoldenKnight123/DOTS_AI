import random
import math

class Brain:
    def __init__(self, size):
        self.directions = []
        self.size = size
        self.randomize()

    def randomize(self):
        for i in range(0, self.size):
            self.angle = random.randint(0, 360)
            self.directions.append([math.cos(self.angle * (math.pi /180)), math.sin(self.angle * (math.pi /180))])

    def clone(self, steps):
        clone = Brain(steps)
        clone.directions = self.directions
        return clone
        
    def mutate(self):
        for i in range(0, len(self.directions)):
            randomiser = random.randint(0, 1000)
            if randomiser < 10:
                self.angle = random.randint(0, 360)
                self.directions[i][0] = math.cos(self.angle * (math.pi /180))
                self.directions[i][1] = math.sin(self.angle * (math.pi /180))