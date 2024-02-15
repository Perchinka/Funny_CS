import pygame
import random

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
CIRCLE_RADIUS = 300
CREATURE_SIZE = 1
CREATURES_AMOUNT = 100
CIRCLE_SPEED_CHANGE = 0.5
CHANCE_TO_REPRODUCE = 0.01
MUTATION_RATE = 0.15
CREATURES_LIMIT = 2000

class Creature:
    def __init__(self, x, y, speedX, speedY):
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY
        self.children = 0
        self.alpha = 255
        self.is_dead = False

    def fade(self):
        self.alpha = max(0, self.alpha - 20)
        pygame.draw.circle(screen, (255, 0, 0, self.alpha), (int(self.x), int(self.y)), CREATURE_SIZE)

    def move(self, circle_speed_x, circle_speed_y):
        self.x += self.speedX - circle_speed_x
        self.y += self.speedY - circle_speed_y

    def reproduce(self):
        if self.children < 2 and random.random() < CHANCE_TO_REPRODUCE:
            self.children += 1
            return Creature(self.x, self.y, self.speedX + random.uniform(-1, 1)*MUTATION_RATE, self.speedY + random.uniform(-1, 1)*MUTATION_RATE)
        return None

    def inside_circle(self, circle_x, circle_y, circle_radius):
        return (self.x - circle_x)**2 + (self.y - circle_y)**2 <= circle_radius**2

class World:
    def __init__(self, circle_x, circle_y, circle_speed_x, circle_speed_y, circle_radius):
        self.creatures = [Creature(random.uniform(0, WINDOW_WIDTH), random.uniform(0, WINDOW_HEIGHT), random.uniform(-2, 2), random.uniform(-2, 2)) for _ in range(CREATURES_AMOUNT)]
        self.circle_x = circle_x
        self.circle_y = circle_y
        self.circle_speed_x = circle_speed_x
        self.circle_speed_y = circle_speed_y
        self.circle_radius = circle_radius
        self.background_x = 0
        self.background_y = 0


    def simulate(self):
        for creature in self.creatures:
            creature.move(self.circle_speed_x, self.circle_speed_y)
            if creature.is_dead:
                if creature.alpha > 0:
                    creature.fade()
                else:
                    self.creatures.remove(creature)
                continue
            if len(self.creatures) < CREATURES_LIMIT:
                child = creature.reproduce()
                if child is not None:
                    self.creatures.append(child)
            if not creature.inside_circle(self.circle_x, self.circle_y, self.circle_radius):
                creature.is_dead = True

    def draw(self, screen, background):
        self.background_x += self.circle_speed_x
        self.background_y += self.circle_speed_y

        background.fill((0, 0, 0))
        
        screen.blit(background, (0, 0))
        pygame.draw.circle(screen, (255, 255, 255), (int(self.circle_x), int(self.circle_y)), int(self.circle_radius), 1)
        
        for creature in self.creatures:
            pygame.draw.circle(screen, (255, 0, 0, creature.alpha), (int(creature.x), int(creature.y)), CREATURE_SIZE)

pygame.init()
pygame.display.set_caption("Natural Selection")
pygame.font.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background = pygame.Surface((WINDOW_WIDTH * 2, WINDOW_HEIGHT))  

world = World(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 1, 1, CIRCLE_RADIUS)
running = True
while running:
    background.fill((0, 0, 0)) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                world.circle_speed_x -= CIRCLE_SPEED_CHANGE
            elif event.key == pygame.K_RIGHT:
                world.circle_speed_x += CIRCLE_SPEED_CHANGE
            elif event.key == pygame.K_UP:
                world.circle_speed_y -= CIRCLE_SPEED_CHANGE
            elif event.key == pygame.K_DOWN:
                world.circle_speed_y += CIRCLE_SPEED_CHANGE
    
    world.simulate()
    world.draw(screen, background)
    pygame.display.flip()

pygame.quit()