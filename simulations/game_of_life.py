import pygame
import numpy as np

WINDOW_SIZE = [600, 600]
CELL_SIZE = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 0, 0) 

def initialize_game(size, randomize: bool = True):
    if randomize: 
        return np.random.choice([0, 1], size*size, p=[0.5, 0.5]).reshape(size, size)
    else:
        return np.zeros((size, size))

def next_board_state(board):
    new_board = np.copy(board)
    rows, cols = board.shape
    for i in range(rows):
        for j in range(cols):
            new_board[i, j] = apply_rules(board, i, j)
    return new_board

def apply_rules(board, i, j):
    num_neighbours = np.sum(board[max(i-1, 0):min(i+2, board.shape[0]), max(j-1, 0):min(j+2, board.shape[1])]) - board[i, j]
    if board[i, j] == 1 and num_neighbours < 2 or num_neighbours > 3:
        return 0
    elif board[i, j] == 0 and num_neighbours == 3:
        return 1
    return board[i, j]

def game_of_life(size = 100):
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    board = initialize_game(size)
    paused = False
    pygame.mouse.set_visible(False)

    brush_size = 3
    brush_pos = [size // 2, size // 2]
    move_delay = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                brush_pos = [x // CELL_SIZE, y // CELL_SIZE]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(max(0, brush_pos[1] - brush_size // 2), min(size, brush_pos[1] + brush_size // 2 + 1)):
                        for j in range(max(0, brush_pos[0] - brush_size // 2), min(size, brush_pos[0] + brush_size // 2 + 1)):
                            board[i, j] = 1
                elif event.button == 3:
                    for i in range(max(0, brush_pos[1] - brush_size // 2), min(size, brush_pos[1] + brush_size // 2 + 1)):
                        for j in range(max(0, brush_pos[0] - brush_size // 2), min(size, brush_pos[0] + brush_size // 2 + 1)):
                            board[i, j] = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                brush_size = min(5, brush_size + 1)
            if keys[pygame.K_s]:
                brush_size = max(1, brush_size - 1)
            if keys[pygame.K_r]:
                board = initialize_game(size)
            if keys[pygame.K_c]:
                board = initialize_game(size, False)
            if keys[pygame.K_UP]:
                brush_pos[1] = max(0, brush_pos[1] - 1)
            if keys[pygame.K_DOWN]:
                brush_pos[1] = min(size - 1, brush_pos[1] + 1)
            if keys[pygame.K_LEFT]:
                brush_pos[0] = max(0, brush_pos[0] - 1)
            if keys[pygame.K_RIGHT]:
                brush_pos[0] = min(size - 1, brush_pos[0] + 1)
            if keys[pygame.K_RETURN]:
                for i in range(max(0, brush_pos[1] - brush_size // 2), min(size, brush_pos[1] + brush_size // 2 + 1)):
                    for j in range(max(0, brush_pos[0] - brush_size // 2), min(size, brush_pos[0] + brush_size // 2 + 1)):
                        board[i, j] = 1
            if keys[pygame.K_BACKSPACE]:
                for i in range(max(0, brush_pos[1] - brush_size // 2), min(size, brush_pos[1] + brush_size // 2 + 1)):
                    for j in range(max(0, brush_pos[0] - brush_size // 2), min(size, brush_pos[0] + brush_size // 2 + 1)):
                        board[i, j] = 0
            if keys[pygame.K_d]:
                board = next_board_state(board)
            pygame.time.delay(move_delay)

        screen.fill(BLACK)

        for i in range(size):
            for j in range(size):
                if board[i, j] == 1:
                    pygame.draw.rect(screen, WHITE, pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        x, y = brush_pos[0]*CELL_SIZE, brush_pos[1]*CELL_SIZE
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, pygame.Rect((x // CELL_SIZE - brush_size // 2) * CELL_SIZE, (y // CELL_SIZE - brush_size // 2) * CELL_SIZE, CELL_SIZE*brush_size, CELL_SIZE*brush_size), 1)

        pygame.display.flip()

        if not paused:
            board = next_board_state(board)
        
        clock.tick(10)

game_of_life()