import pygame
import random

import time
from termcolor import colored

pygame.init()

WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Bubble Sort Visualization")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 51, 51)


def bubble_sort(array):
    for i in range(len(array)):
        for j in range(len(array) - 1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                draw(array, j, j+1)
    return array


def draw(array, i, j):
    screen.fill(BLACK)
    for k in range(len(array)):
        if k == i or k == j:
            pygame.draw.rect(screen, RED, (k * 10, HEIGHT - array[k]*10, 10, array[k]*10))
        else:
            pygame.draw.rect(screen, WHITE, (k * 10, HEIGHT - array[k]*10, 10, array[k]*10))
    pygame.display.update()


def main():
    array = [random.randint(1, 50) for i in range(WIDTH // 10)]

    start = time.time()
    bubble_sort(array)
    end = time.time()

    print(colored("Time taken:", "red"), colored(round(end - start, 3), "green"))
    pygame.quit()


if __name__ == "__main__":
    main()

