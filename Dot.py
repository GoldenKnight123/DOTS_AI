import pygame
import random
import numpy as np
import math
from Brain import Brain

class Dot:
    def __init__(self, population, screen, steps, brain = None):
        self.x = 360
        self.y = 900
        self.velX = 0
        self.velY = 0
        self.population = population
        self.screen = screen
        self.steps = steps
        self.step = 0
        if brain == None:
            self.brain = Brain(self.steps)
        else:
            self.brain = brain
        self.dead = False
        self.goalReached = False
        self.directions = self.brain.directions

        self.maxCheckpoint = 0
        for i in self.population.Checkpoints:
            if i.number > self.maxCheckpoint:
                self.maxCheckpoint = i.number
        self.currentCheckpoint = 0

        self.rect = pygame.Rect(self.x, self.y, 3, 3)
        self.color = (0, 0, 0)
        
    def move(self):
        try:
            self.accX = self.directions[self.step][0]*2
            self.accY = self.directions[self.step][1]*2
        except IndexError:
            angle = random.randint(0, 360)
            self.directions.append([math.cos(angle * (math.pi /180)), math.sin(angle * (math.pi /180))])
            self.accX = self.directions[self.step][0]*2
            self.accY = self.directions[self.step][1]*2

        if self.accX >= 1: self.accX = 1
        if self.accX <= -1: self.accX = -1
        if self.accY >= 1: self.accY = 1
        if self.accY <= -1: self.accY = -1

        self.velX += self.accX
        self.velY += self.accY

        if self.velX >= 5: self.velX = 5
        if self.velX <= -5: self.velX = -5
        if self.velY >= 5: self.velY = 5
        if self.velY <= -5: self.velY = -5

        """if abs(self.velX) + abs(self.velY) > 5:
            self.velX = self.velY/math.sin((self.velX/2.5)*(math.pi/2))
            self.velY = self.velX/math.sin((self.velY/2.5)*(math.pi/2))"""

        self.x += self.velX
        self.y += self.velY

        self.rect.center = (self.x, self.y)
    
    def update(self):
        if not self.dead and not self.goalReached:
            self.move()
            self.step += 1

        #If the dot touches the edge of the screen, set dead to True
        if self.x > 720 or self.x < 0 or self.y > 960 or self.y < 0:
            self.dead = True

        #Once it has run out of directions, set dead to True
        if self.step >= self.steps-1:
            self.dead = True

        #If the dot collides with the goal, set goalReached to True
        if self.rect.colliderect(self.population.goal.rect):
            self.goalReached = True

        for i in self.population.Obstacles:
            if self.rect.colliderect(i.rect):
                self.dead = True
                break
        
        for i in self.population.Checkpoints:
            if self.rect.colliderect(i.rect):
                if self.currentCheckpoint < i.number:
                    self.currentCheckpoint = i.number

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 3)
        #pygame.draw.rect(self.screen, (0, 255, 0), self.rect)

    def calculateFitness(self):
        if self.goalReached:
            self.fitness = ((1*10**50)/((self.step*(400/self.population.steps))**20))
            if self.population.minSteps == None:
                self.population.minSteps = self.step
            if self.step < self.population.minSteps:
                self.population.minSteps = self.step
        else:
            maxCheckpointReached = 0
            for i in self.population.Dots:
                if i.currentCheckpoint > maxCheckpointReached:
                    maxCheckpointReached = i.currentCheckpoint
            if not self.currentCheckpoint == self.maxCheckpoint:
                for i in self.population.Checkpoints:
                    if i.number == self.currentCheckpoint+1:
                        xd = self.x - i.x
                        yd = self.y - i.y
                        distance = np.sqrt(xd * xd + yd * yd)
                        print(self.maxCheckpoint)
                        self.fitness = (1*10**-8 / distance**2) + (self.currentCheckpoint/self.maxCheckpoint)*10**-7

            else:
                xd = self.x - self.population.goal.x
                yd = self.y - self.population.goal.y
                distance = np.sqrt(xd * xd + yd * yd)
                self.fitness = (1*10**-8 / distance**2) + 2*10**-7

    def mutate(self):
        for i in range(0, len(self.directions)):
            randomiser = random.randint(0, 1000)
            if randomiser < 10:
                angle = random.randint(0, 360)
                self.directions[i][0] = math.cos(angle * (math.pi /180))
                self.directions[i][1] = math.sin(angle * (math.pi /180))
