import pygame
import random

class Node:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.neighbors = []
        self.width = width
        self.height = height
        self.color = (255, 255, 255)
        self.distance = float('inf')
        self.previous = None
        self.visited = False

    def add_neighbors(self, grid):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.x < len(grid) - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.y < len(grid[0]) - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x * self.width, self.y * self.height, self.width, self.height))

    def reset(self):
        self.color = (255, 255, 255)
        self.distance = float('inf')

    def make_obstacle(self):
        self.color = (0, 0, 255) 

    def make_path(self):
        self.color = (0, 255, 0) 

    def __lt__(self, other):
        return self.distance < other.distance
    
def draw(screen, grid):
    for row in grid:
        for node in row:
            node.draw(screen)

def execute(algorithm, percent_of_obstacles = 0.2):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    screen.fill((255, 255, 255))
    grid = [[Node(x, y, 20, 20) for y in range(30)] for x in range(40)]
    for row in grid:
        for node in row:
            node.add_neighbors(grid)
            if random.random() < percent_of_obstacles:
                node.make_obstacle()

    start = random.choice(random.choice(grid))
    end = random.choice(random.choice(grid))
    end.color = (0, 0, 0)
    start.color = (0, 0, 0)

    algorithm(start, end, screen, grid)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return