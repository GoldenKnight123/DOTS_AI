import random
import pygame
import math
import json
from Dot import Dot
from Obstacle import Obstacle
from Checkpoint import Checkpoint

class Goal:
    def __init__(self, population, screen):
        self.x = 360
        self.y = 20
        self.population = population
        self.screen = screen

        self.rect = pygame.Rect(self.x-10, self.y-10, 20, 20)
        
    def draw(self):
        pygame.draw.circle(self.screen, (0, 255, 0), (self.x, self.y), 12)
        #pygame.draw.rect(self.screen, (0, 0, 0), self.rect)
        #Draw an outline around the circle
        if self.population.selected == self:
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x, self.y), 12, 1)

    def update(self):
        #If the user clicks on this object
        if pygame.mouse.get_pressed()[0] and self.population.selected == None:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.population.selected = self

        if pygame.mouse.get_pressed()[0] and self.population.selected == self:
            if not self.rect.collidepoint(pygame.mouse.get_pos()) and not self.followMouse:
                self.population.selected = None

        #If the object is selected let the user drag it around
        if self.population.selected == self and pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()) and not self.followMouse:
                self.followMouse = True
                self.xDiff = pygame.mouse.get_pos()[0] - self.x
                self.yDiff = pygame.mouse.get_pos()[1] - self.y

        if not pygame.mouse.get_pressed()[0]:
            self.followMouse = False

        if self.followMouse:
            self.x = pygame.mouse.get_pos()[0] - self.xDiff
            self.y = pygame.mouse.get_pos()[1] - self.yDiff
            print('following')

        #If while selected the arrow keys are pressed change the width and height of the object
        if self.population.selected == self and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]):
            self.height += 1
            self.y -= 0.5
            self.rect.height = self.height
        if self.population.selected == self and (pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]):
            if self.height <= 0:
                return
            self.height -= 1
            self.y += 0.5
            self.rect.height = self.height
        if self.population.selected == self and (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]):
            self.width -= 1
            self.x -= 0.5
            self.rect.width = self.width
        if self.population.selected == self and (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]):
            self.width += 1
            self.x += 0.5
            self.rect.width = self.width

        self.rect.center = (self.x, self.y)

class Population:
    def __init__(self, steps):
        self.screen = pygame.display.set_mode((720, 960))
        pygame.init()
        pygame.display.set_caption("Literally Just DOTS")
        self.clock = pygame.time.Clock()
        self.running = True
        self.steps = steps
        self.generation = 1
        self.goal = Goal(self, self.screen)
        self.CheckpointCount = 0
        self.Dots = []
        self.Obstacles = []
        self.Checkpoints = []
        self.isRunning = False
        self.selected = None
        self.onlyBest = False
        self.paused = False
        self.speed = 120
        self.mutationRate = 0.01
        self.minSteps = None
        #Basic right and left
        """self.Obstacles.append(Obstacle(self, self.screen, 100, 300, 640, 20))
        self.Obstacles.append(Obstacle(self, self.screen, -100, 600, 640, 20))"""
        
        #Complex right and left then small gap
        """self.Obstacles.append(Obstacle(self, self.screen, 380, 200, 640, 20))
        self.Obstacles.append(Obstacle(self, self.screen, -280, 200, 640, 20))
        self.Obstacles.append(Obstacle(self, self.screen, 100, 400, 640, 20))
        self.Obstacles.append(Obstacle(self, self.screen, -600, 400, 640, 20))
        self.Obstacles.append(Obstacle(self, self.screen, 700, 600, 640, 20))
        self.Obstacles.append(Obstacle(self, self.screen, 0, 600, 640, 20))

        self.Checkpoints.append(Checkpoint(self, self.screen, 675, 600, 1))
        self.Checkpoints.append(Checkpoint(self, self.screen, 75, 400, 2))"""

        #hell
        """for i in range(200):
            self.Obstacles.append(Obstacle(self, self.screen, random.randint(0, 720), random.randint(0, 960), 32, 32))"""

        #fun
        """self.Obstacles.append(Obstacle(self, self.screen, 390, 200, 640, 20))
        self.Obstacles.append(Obstacle(self, self.screen, -270, 200, 640, 20))
        self.Obstacles.append(Obstacle(self, self.screen, 410, 300, 640, 20))
        self.Obstacles.append(Obstacle(self, self.screen, -250, 300, 640, 20))
        self.Obstacles.append(Obstacle(self, self.screen, 440, 400, 640, 20))
        self.Obstacles.append(Obstacle(self, self.screen, -220, 400, 640, 20))
        self.Obstacles.append(Obstacle(self, self.screen, 370, 500, 640, 20))
        self.Obstacles.append(Obstacle(self, self.screen, -290, 500, 640, 20))

        self.Checkpoints.append(Checkpoint(self, self.screen, 350, 500, 1))
        self.Checkpoints.append(Checkpoint(self, self.screen, 430, 400, 2))
        self.Checkpoints.append(Checkpoint(self, self.screen, 400, 300, 3))
        self.Checkpoints.append(Checkpoint(self, self.screen, 380, 200, 4))"""

    def run(self):
        while self.running:
            self.clock.tick(self.speed)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and self.selected != None:
                    self.selected.kill()
                    self.selected = None
                if event.key == pygame.K_0 and self.generation > 1:
                    if self.onlyBest:
                        self.onlyBest = False
                    else:
                        self.onlyBest = True
                if event.key == pygame.K_5:
                    self.load()
                if event.key == pygame.K_6:
                    with open('directions.json', 'w') as f:
                        json.dump(self.bestDot.directions, f)
                if event.key == pygame.K_7 and not self.isRunning:
                    self.start()
                    self.isRunning = True
                if event.key == pygame.K_8 and self.isRunning:
                    self.stop()
                    self.isRunning = False
                if event.key == pygame.K_9:
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                if event.key == pygame.K_1:
                    #find mouse x and y
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.Obstacles.append(Obstacle(self, self.screen, mouse_x, mouse_y, 32, 32))
                if event.key == pygame.K_2:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.Checkpoints.append(Checkpoint(self, self.screen, mouse_x-16, mouse_y-16, self.CheckpointCount+1))
                    self.CheckpointCount += 1
    
    def start(self):
        for i in range(1000):
            self.Dots.append(Dot(self, self.screen, self.steps))

    def stop(self):
        self.Dots = []
        self.generation = 1
        self.minSteps = None

    def load(self):
        print('Loading lastest saved directions from file...')
        with open('directions.json', 'r') as f:
            directions = json.load(f)
        newDot = Dot(self, self.screen, self.steps)
        newDot.directions = directions
        newDot.color = (0, 0, 255)
        for i in range(len(directions)):
            newDot.update()
            newDot.draw()
            pygame.display.flip()
            self.clock.tick(self.speed)
        self.clock.tick(1)
    
    def update(self):
        #If the - or + key is held
        if pygame.key.get_pressed()[pygame.K_MINUS] or pygame.key.get_pressed()[pygame.K_KP_MINUS]:
            if self.speed > 1:
                self.speed -= 1
        if pygame.key.get_pressed()[pygame.K_EQUALS] or pygame.key.get_pressed()[pygame.K_KP_PLUS]:
            if self.speed < 600:
                self.speed += 1

        #if the [ or ] key is held
        if pygame.key.get_pressed()[pygame.K_LEFTBRACKET]:
            if self.mutationRate > 0.001:
                self.mutationRate -= 0.001
                self.mutationRate = round(self.mutationRate, 3)
        if pygame.key.get_pressed()[pygame.K_RIGHTBRACKET]:
            if self.mutationRate < 0.999:
                self.mutationRate += 0.001
                self.mutationRate = round(self.mutationRate, 3)

        #if the ; or ' key is held, change steps
        if pygame.key.get_pressed()[pygame.K_SEMICOLON]:
            if self.steps > 100:
                self.steps -= 1
        if pygame.key.get_pressed()[pygame.K_QUOTE]:
            if self.steps < 1000:
                self.steps += 1

        self.goal.update()
        for i in self.Obstacles:
            i.update()

        for i in self.Checkpoints:
            i.update()

        if not self.isRunning or self.paused:
            return

        for i in self.Dots:
            i.update()
        
        if self.allDead():
            self.calculateFitness()
            self.totalFitness = 0
            for i in self.Dots:
                self.totalFitness += i.fitness

            max = 0
            for i in self.Dots:
                i.color = (0, 0, 0)
                if i.fitness > max:
                    max = i.fitness
                    self.bestDot = i
            self.Dots.remove(self.bestDot)
            self.Dots.append(self.bestDot)
            self.bestDot.color = (0, 0, 255)
            self.bestDot.x = 360
            self.bestDot.y = 900
            self.bestDot.velX = 0
            self.bestDot.velY = 0
            self.bestDot.population = self
            self.bestDot.screen = self.screen
            self.bestDot.steps = self.steps
            self.bestDot.step = 0
            self.bestDot.dead = False
            self.bestDot.goalReached = False

            self.bestDot.maxCheckpoint = 0
            for i in self.Checkpoints:
                if i.number > self.bestDot.maxCheckpoint:
                    self.maxCheckpoint = i.number
            self.bestDot.currentCheckpoint = 0
            
            for a in self.Dots:
                if not a == self.bestDot:
                    parent = self.selectParent()
                    newDirections = parent.directions.copy()
                    for b in range(0, len(newDirections)):
                        randomiser = random.uniform(0, 1)
                        if randomiser < self.mutationRate:
                            angle = random.randint(0, 360)
                            newDirections[b] = [math.cos(angle * (math.pi /180)), math.sin(angle * (math.pi /180))]
                
                    a.x = 360
                    a.y = 900
                    a.velX = 0
                    a.velY = 0
                    a.population = self
                    a.screen = self.screen
                    a.steps = self.steps
                    a.step = 0
                    a.dead = False
                    a.goalReached = False
                    a.directions = newDirections

                    a.maxCheckpoint = 0
                    for i in self.Checkpoints:
                        if i.number > a.maxCheckpoint:
                            a.maxCheckpoint = i.number
                    a.currentCheckpoint = 0

            #self.Dots.append(self.bestDot)
            self.generation += 1
            print(f'Generation: {self.generation}')

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.goal.draw()
        for i in self.Obstacles:
            i.draw()

        for i in self.Checkpoints:
            i.draw()

        if self.onlyBest:
            self.bestDot.draw()
        else:
            for i in self.Dots:
                i.draw()

        font = pygame.font.SysFont('Arial', 20)
        text_1 = font.render(f'Generation: {self.generation}', True, (0, 0, 0))
        self.screen.blit(text_1, (10, 10))
        text_2 = font.render(f'Speed: {self.speed}', True, (0, 0, 0))
        self.screen.blit(text_2, (10, 30))
        text_3 = font.render(f'Mutation Rate: {self.mutationRate}', True, (0, 0, 0))
        self.screen.blit(text_3, (10, 50))
        text_4 = font.render(f'Steps: {self.steps}', True, (0, 0, 0))
        self.screen.blit(text_4, (10, 70))
        text_5 = font.render(f'Min Steps: {self.minSteps}', True, (0, 0, 0))
        self.screen.blit(text_5, (10, 90))

        pygame.display.flip()

    def calculateFitness(self):
        for i in self.Dots:
            i.calculateFitness()

    def allDead(self):
        for i in self.Dots:
            if not i.dead and not i.goalReached:
                return False
        return True

    def selectParent(self):
        runningSum = 0
        randomiser = random.uniform(0, self.totalFitness)

        for i in self.Dots:
            runningSum += i.fitness
            if runningSum > randomiser:
                return i