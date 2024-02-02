import pygame
import random
import time
from termcolor import colored

pygame.init()

WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Merge Sort Visualization")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 51, 51)


# Merge Sort
def merge_sort(array, l, r):
    if l < r:
        mid = (l + r) // 2
        merge_sort(array, l, mid)
        merge_sort(array, mid + 1, r)
        merge(array, l, mid, r)

def merge(array, l, mid, r):
    n1 = mid - l + 1
    n2 = r - mid

    left = [0] * n1
    right = [0] * n2

    for i in range(n1):
        left[i] = array[l + i]
    for j in range(n2):
        right[j] = array[mid + 1 + j]

    i = 0
    j = 0
    k = l

    while i < n1 and j < n2:
        if left[i] <= right[j]:
            array[k] = left[i]
            i += 1
            draw(array, k, j)
            k += 1
        else:
            array[k] = right[j]
            j += 1
            draw(array, i, k)
            k += 1

    while i < n1:
        array[k] = left[i]
        i += 1
        draw(array, k, j)
        k += 1

    while j < n2:
        array[k] = right[j]
        j += 1
        draw(array, i, k)
        k += 1


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

    merge_sort(array, 0, len(array) - 1)
    end = time.time()
    
    print(colored("Time taken:", "red"), colored(end - start, "green"))
    pygame.time.wait(1000)
    pygame.quit()

if __name__ == "__main__":
    main()

