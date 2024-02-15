import math
import time
import os

A = 0
B = 0
while True:
    rows, columns = os.popen('stty size', 'r').read().split()
    rows = int(rows)
    columns = int(columns)
    z = [0] * (columns * rows)
    b = [' '] * (columns * rows)
    for j in range(0, 628, 7):
        for i in range(0, 628, 2):
            c = math.sin(i)
            d = math.cos(j)
            e = math.sin(A)
            f = math.sin(j)
            g = math.cos(A)
            h = d + 2
            D = 1 / (c * h * e + f * g + 5)
            l = math.cos(i)
            m = math.cos(B)
            n = math.sin(B)
            t = c * h * g - f * e
            x = int(columns/2 + columns/2 * D * (l * h * m - t * n))
            y = int(rows/2 + rows/2 * D * (l * h * n + t * m))
            o = int(x + columns * y)
            N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))
            if 0 <= y < rows and 0 <= x < columns and D > z[o]:
                z[o] = D
                b[o] = '.,-~:;=!*#$@'[N if N > 0 else 0]

    print('\033[0;0H' + ''.join(b))
    time.sleep(0.01)
    A += 0.04
    B += 0.02