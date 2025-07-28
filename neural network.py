#crate a blank pygame window
import pygame
import random
import numpy as np

# initialize the pygame module
pygame.init()

pygame.display.set_caption("Neural Network")

# create a surface on screen that has the size of 640 x 480
screen = pygame.display.set_mode((640, 480))

#set background white
screen.fill((255, 255, 255))

#Create a dot class without a random size and color or thickness
class Dot:
    def __init__(self, id, gene = None):
        self.x = 320
        self.y = 460

        if gene:
            self.gene = gene
            self.velX = float(gene[0][0] + random.randint(-100, 100)/1000)
            self.velY = float(gene[0][1] + random.randint(-100, 100)/1000)

        else:
            self.gene = None
            self.velX = float(random.randint(-1000, 1000)/1000)
            self.velY = float(random.randint(-1000, 1000)/1000)

        self.steps = 10
        self.stepCount = 0
        self.stepList = [[self.velX, self.velY]]
        self.id = id
        self.dead = False
        
    def draw(self):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 4)
        #draw it's id
        #font = pygame.font.SysFont("Arial", 14)
        #text = font.render(str(self.id), True, (0, 0, 0))
        #screen.blit(text, (self.x + 4, self.y + 4))


    #Move function
    def move(self):
        if not self.dead:
            self.steps -= 1
            if self.steps <= 0:
                self.stepCount += 1
                if self.gene:
                    self.velX = float(self.gene[self.stepCount][0] + random.randint(-100, 100)/1000)
                    self.velY = float(self.gene[self.stepCount][1] + random.randint(-100, 100)/1000)
                    self.stepList.append([self.velX, self.velY])
                    self.steps = 10
                
                else:
                    self.velX = float(random.randint(-1000, 1000)/1000)
                    self.velY = float(random.randint(-1000, 1000)/1000)
                    self.stepList.append([self.velX, self.velY])
                    self.steps = 10
            self.x = float(self.x+self.velX)
            self.y = float(self.y+self.velY)
            if self.x < 0:
                self.dead = True
            if self.x > 639:
                self.dead = True
            if self.y < 0:
                self.dead = True
            if self.y > 479:
                self.dead = True

    def calculateFitness(self, goal):
        #calculate distance from dot to goal
        if self.dead:
            return 100000.0
        
        else:
            xd = self.x - goal.x
            yd = self.y - goal.y
            distance = np.sqrt(xd * xd + yd * yd)
            return distance
        

        


#Create a goal class
class Goal:
    def __init__(self):
        self.x = 320
        self.y = 20
        
    def draw(self):
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 12)

#add some dots to the screen
dots = []
for i in range(0, 100):
    dot = Dot(i)
    dots.append(dot)

#ADd the goal to the screen
goal = Goal()

#restart function
def restart():
    for i in range(0, 100):
        dot = Dot(i, bestGene)
        dots.append(dot)

running = True
generation = 0
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 14)
generation_text = font.render("Generation: " + str(generation), True, (0, 0, 0))

timer = 0
#render the dots
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    for dot in dots:
        dot.draw()
        goal.draw()
        dot.move()
        #display the current generation number in the top left
        screen.blit(generation_text, (0, 0))
    timer += 1
    if timer >= 1000:
        list = []
        for dot in dots:
            list.append([dot, f"dot {dot.id}", dot.calculateFitness(goal)])
        #Order the dots by fitness
        list.sort(key=lambda x: x[2])
        bestGene = list[0][0].stepList
        print(list)
        print(bestGene)
        dots = []
        generation += 1
        generation_text = font.render("Generation: " + str(generation), True, (0, 0, 0))
        timer = 0
        restart()
    clock.tick(60)
    pygame.display.flip()
