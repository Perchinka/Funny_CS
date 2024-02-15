import os
import time
import math

def cube_point(i, j, k, scale):
    return [(-scale if i else scale), (-scale if j else scale), (-scale if k else scale)]

def generate_cube_points(scale):
    return [cube_point(i//4, i//2%2, i%2, scale) for i in range(8)]

def cube_edge(i, j):
    return (i, i ^ (1 << j))

def generate_cube_edges():
    return [cube_edge(i, j) for i in range(8) for j in range(3)]

def rotate_point(x, y, z, ax, ay, az):
    y, z = y*math.cos(ax) - z*math.sin(ax), z*math.cos(ax) + y*math.sin(ax)
    z, x = z*math.cos(ay) - x*math.sin(ay), x*math.cos(ay) + z*math.sin(ay)
    x, y = x*math.cos(az) - y*math.sin(az), y*math.cos(az) + x*math.sin(az)
    return x, y, z

def draw_line(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x2:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    points.append((x, y))
    return points

shades = '01'

def draw_cube(ax, ay, az, scale):
    os.system('clear')
    term_size = os.get_terminal_size()
    scale = min(term_size.lines, term_size.columns) // 8
    cube_points = generate_cube_points(scale)
    cube_edges = generate_cube_edges()
    buffer = []
    for edge in cube_edges:
        x1, y1, z1 = cube_points[edge[0]]
        x2, y2, z2 = cube_points[edge[1]]
        x1, y1, z1 = rotate_point(x1, y1, z1, ax, ay, az)
        x2, y2, z2 = rotate_point(x2, y2, z2, ax, ay, az)
        points = draw_line(int(term_size.lines//2+x1), int(term_size.columns//2+y1), int(term_size.lines//2+x2), int(term_size.columns//2+y2))
        depth = (z1 + z2) / 2 / scale
        shade = shades[min(int((depth + 1) * len(shades) / 2), len(shades) - 1)]
        for point in points:
            buffer.append(f"\033[{term_size.lines - point[1]};{point[0]}H{shade}")
    print(''.join(buffer))

scale = 6
ax, ay, az = 0, 0, 0
while True:
    draw_cube(ax, ay, az, scale)
    time.sleep(0.1)
    ax += 0.1
    ay += 0.08
    az += 0.13