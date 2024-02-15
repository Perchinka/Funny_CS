import pygame
import math

pygame.init()

size = (800, 800)
screen = pygame.display.set_mode(size)

r = math.pi * 40
R = 100
d = math.pi 

for theta in range(0, 360 * 100):
    theta_rad = math.radians(theta)

    x = R * math.cos(theta_rad)
    y = R * math.sin(theta_rad)

    x_epicycle = x + r * math.cos(theta_rad * d)
    y_epicycle = y + r * math.sin(theta_rad * d)

    pygame.draw.line(screen, (0, 255, 0), (400, 400), (int(x) + 400, int(y) + 400), 1)

    pygame.draw.line(screen, (255, 0, 0), (int(x) + 400, int(y) + 400), (int(x_epicycle) + 400, int(y_epicycle) + 400), 1)

    pygame.draw.circle(screen, (0, 0, 255), (int(x_epicycle) + 400, int(y_epicycle) + 400), 5)

    pygame.display.flip()
    pygame.time.wait(100)
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True