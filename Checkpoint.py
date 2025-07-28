import pygame

class Checkpoint:
    def __init__(self, population, screen, x, y, number):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.population = population
        self.screen = screen
        self.number = number

        self.color = (0, 0, 255)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = (self.x, self.y)

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)
        self.surface.set_alpha(69)

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
        self.screen.blit(self.surface, (self.x, self.y))

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

        #If while selected the arrow keys are pressed change the width and height of the object
        if self.population.selected == self and (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]):
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.height += 0.5
                self.y -= 0.25
            else:
                self.height += 1
                self.y -= 0.5
            self.rect.height = self.height

        if self.population.selected == self and (pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]):
            if self.height <= 0:
                return
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.height -= 0.5
                self.y += 0.25
            else:
                self.height -= 1
                self.y += 0.5
            self.rect.height = self.height

        if self.population.selected == self and (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]):
            if self.width <= 0:
                return
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.width -= 0.5
                self.x -= 0.25
            else:
                self.width -= 1
                self.x -= 0.5
            self.rect.width = self.width
            
        if self.population.selected == self and (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]):
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.width += 0.5
                self.x += 0.25
            else:
                self.width += 1
                self.x += 0.5
            self.rect.width = self.width

        self.rect.topleft = (self.x, self.y)

    def kill(self):
        for i in self.population.Checkpoints:
            self.population.Checkpoints.remove(i)
        self.population.checkpointNumber = 0