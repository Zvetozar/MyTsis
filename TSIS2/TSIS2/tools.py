import pygame
import math
from collections import deque

def get_color(mode):
    if mode == 'blue':
        return (0, 0, 255)
    elif mode == 'red':
        return (255, 0, 0)
    elif mode == 'green':
        return (0, 255, 0)

def flood_fill(surface, pos, new_color):
    width, height = surface.get_size()
    target = surface.get_at(pos)

    if target == new_color:
        return

    q = deque([pos])

    while q:
        x, y = q.popleft()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != target:
            continue

        surface.set_at((x, y), new_color)

        q.append((x+1, y))
        q.append((x-1, y))
        q.append((x, y+1))
        q.append((x, y-1))

def draw_square(surface, color, start, end, width):
    size = abs(end[0] - start[0])
    pygame.draw.rect(surface, color, (start[0], start[1], size, size), width)

def draw_triangle(surface, color, start, end, width):
    pygame.draw.polygon(surface, color, [
        start,
        (start[0], end[1]),
        end
    ], width)

def draw_eq_triangle(surface, color, start, end, width):
    size = abs(end[0] - start[0])
    h = size * math.sqrt(3) / 2

    pygame.draw.polygon(surface, color, [
        (start[0], start[1]),
        (start[0] + size, start[1]),
        (start[0] + size//2, start[1] - h)
    ], width)

def draw_rhombus(surface, color, start, end, width):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2

    pygame.draw.polygon(surface, color, [
        (cx, start[1]),
        (end[0], cy),
        (cx, end[1]),
        (start[0], cy)
    ], width)