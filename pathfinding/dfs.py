from grid_graph_base import execute, draw
import pygame

def dfs(start, end, screen, grid):
    stack = [start]
    start.visited = True

    while stack:
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        current = stack.pop()
        if current != start:
            current.color = (255, 255, 0) 

        if current == end:
            break

        for neighbor in current.neighbors:
            if neighbor.color != (0, 0, 255) and not neighbor.visited:
                neighbor.previous = current  
                neighbor.color = (255, 0, 0) 
                neighbor.visited = True
                stack.append(neighbor)

        draw(screen, grid)
        pygame.display.update()

    node = end
    while node.previous is not None:
        pygame.time.delay(50)
        node = node.previous
        node.make_path()
        draw(screen, grid)
        pygame.display.update()

if __name__ == '__main__':
    execute(dfs)