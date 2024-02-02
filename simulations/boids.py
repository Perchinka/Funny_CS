import pygame
import random
from collections import defaultdict
import numpy as np
import math

BIRD_COUNT = 1000
PERSONAL_SPACE = 1
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
CELL_SIZE = 30
BIRD_SIZE = 2
MOUSE_SPEED_DUMPING = 0.001
MAX_SPEED = 5

class Grid:
    def __init__(self):
        self.cell_size = CELL_SIZE
        self.grid = defaultdict(list)

    def add_bird(self, bird):
        cell = self.get_cell(bird.x, bird.y)
        self.grid[cell].append(bird)

    def get_neighbors(self, bird):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                cell = self.get_cell(bird.x + dx * self.cell_size, bird.y + dy * self.cell_size)
                neighbors.extend(self.grid[cell])
        return neighbors

    def get_cell(self, x, y):
        return int(x // self.cell_size), int(y // self.cell_size)

class Bird:
    def __init__(self, x, y, velocity: pygame.Vector2):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = CELL_SIZE
        self.mouse_mode = 'None'
        self.mouse_radius = 200 
        self.color_mode = 1
        self.random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def follow_mouse(self):
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        difference = mouse_position - pygame.Vector2(self.x, self.y)
        distance = difference.length()
        if distance < self.mouse_radius:
            if self.mouse_mode == 'follow':
                steer = difference * MOUSE_SPEED_DUMPING
            elif self.mouse_mode == 'avoid':
                steer = -difference * MOUSE_SPEED_DUMPING
            else:
                steer = pygame.Vector2()
            self.velocity += steer


    def move(self, neighbors):
        self.alignment(neighbors)
        self.cohesion(neighbors)
        self.separation(neighbors)

        self.x = (self.x + self.velocity.x) % SCREEN_WIDTH
        self.y = (self.y + self.velocity.y) % SCREEN_HEIGHT
        self.velocity += pygame.Vector2(random.uniform(-1, 1)*0.5, random.uniform(-1, 1)*0.5)

        self.follow_mouse()

        speed = self.velocity.length()
        if speed > MAX_SPEED:
            self.velocity = (self.velocity / speed) * MAX_SPEED

    def separation(self, neighbors):
        force = pygame.Vector2()
        for bird in neighbors:
            if bird != self:
                difference = pygame.Vector2(self.x, self.y) - pygame.Vector2(bird.x, bird.y)
                force += difference / (difference.length_squared() + 1e-6)
        self.velocity += force * PERSONAL_SPACE

    def alignment(self, neighbors):
        average_velocity = pygame.Vector2()
        for bird in neighbors:
            if bird != self:
                average_velocity += bird.velocity
        if len(neighbors) > 1:
            average_velocity /= len(neighbors) - 1
            steer = (average_velocity - self.velocity) * 0.05
            self.velocity += steer

    def cohesion(self, neighbors):
        average_position = pygame.Vector2()
        for bird in neighbors:
            if bird != self:
                average_position += pygame.Vector2(bird.x, bird.y)
        if len(neighbors) > 1:
            average_position /= len(neighbors) - 1
            steer = (average_position - pygame.Vector2(self.x, self.y)) * 0.01
            self.velocity += steer
    
    def draw(self, screen, grid: Grid):
        if self.color_mode == 1:
            color = (255, 255, 255)
        elif self.color_mode == 2:
            speed = self.velocity.length()
            normalized_speed = min(1, speed / MAX_SPEED)
            red = int((1 - normalized_speed) * 255)
            green = int(normalized_speed * 255)
            color = (red, green, 0)
        elif self.color_mode == 3:
            neighbors = grid.get_neighbors(self)
            color = (0, min(255, int(len(neighbors) * 10)), 0)
        elif self.color_mode == 4:
            color = self.random_color
        elif self.color_mode == 5:
            angle = math.atan2(self.velocity.y, self.velocity.x) / (2 * math.pi) + 0.5
            color = pygame.Color(0)
            color.hsva = (angle * 360, 100, 100)
        elif self.color_mode == 6:
            normalized_x = self.x / SCREEN_WIDTH
            normalized_y = self.y / SCREEN_HEIGHT
            color = (int(normalized_x * 255), int(normalized_y * 255), 0)
            
        pygame.draw.circle(screen, color, (self.x, self.y), BIRD_SIZE)



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    birds = [Bird(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))) for _ in range(BIRD_COUNT)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for bird in birds:
                        bird.mouse_mode = 'follow'
                elif event.button == 3:
                    for bird in birds:
                        bird.mouse_mode = 'avoid'
            elif event.type == pygame.MOUSEBUTTONUP:
                for bird in birds:
                    bird.mouse_mode = 'None'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    for bird in birds:
                        bird.color_mode = 1
                elif event.key == pygame.K_2:
                    for bird in birds:
                        bird.color_mode = 2
                elif event.key == pygame.K_3:
                    for bird in birds:
                        bird.color_mode = 3
                elif event.key == pygame.K_4:
                    for bird in birds:
                        bird.color_mode = 4
                elif event.key == pygame.K_5:
                    for bird in birds:
                        bird.color_mode = 5
                elif event.key == pygame.K_6:
                    for bird in birds:
                        bird.color_mode = 6

        grid = Grid()
        screen.fill((0, 0, 0))
        for bird in birds:
            grid.add_bird(bird)

        for bird in birds:
            neighbors = grid.get_neighbors(bird)
            bird.move(neighbors)
            bird.draw(screen, grid)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()