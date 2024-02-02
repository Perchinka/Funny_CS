import pygame
import random
import time
from termcolor import colored

pygame.init()

WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Quick Sort Visualization")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 51, 51)


def partition(array, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        draw(array, i, j)
        if array[j] < pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1

def quick_sort(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        quick_sort(array, low, pi - 1)
        quick_sort(array, pi + 1, high)


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

    quick_sort(array, 0, len(array) - 1)
    end = time.time()
    
    print(colored("Time taken:", "red"), colored(end - start, "green"))
    pygame.quit()


if __name__ == "__main__":
    main()

