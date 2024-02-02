import pygame
import heapq
from grid_graph_base import execute, draw

def heuristic(node, end):
    return abs(node.x - end.x) + abs(node.y - end.y)

def a_star(start, end, screen, grid):
    start.distance = 0
    open_set = []
    heapq.heappush(open_set, (0, start))

    while open_set:
        pygame.time.delay(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        current = heapq.heappop(open_set)[1]
        if current != start:
            current.color = (255, 255, 0) 

        if current == end:
            break

        for neighbor in current.neighbors:
            if neighbor.color != (0, 0, 255): 
                temp_distance = current.distance + 1

                if temp_distance < neighbor.distance:
                    neighbor.distance = temp_distance
                    neighbor.previous = current  
                    neighbor.color = (255, 0, 0) 
                    heapq.heappush(open_set, (neighbor.distance + heuristic(neighbor, end), neighbor))

        draw(screen, grid)
        pygame.display.update()

    node = end
    while node.previous is not None:
        pygame.time.delay(50)
        node = node.previous
        node.make_path()
        draw(screen, grid)
        pygame.display.update()

if __name__ == "__main__":
    execute(a_star)