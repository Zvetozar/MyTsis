import pygame
from datetime import datetime
from tools import *

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

mode = 'blue'
tool = 'pencil'
brush = 5

drawing = False
start_pos = None
last_pos = None

text_mode = False
text_input = ""
text_pos = (0,0)
font = pygame.font.SysFont(None, 30)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, filename)

            if text_mode:
                if event.key == pygame.K_RETURN:
                    txt = font.render(text_input, True, get_color(mode))
                    canvas.blit(txt, text_pos)
                    text_mode = False
                    text_input = ""
                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_input = ""
                else:
                    text_input += event.unicode
                continue

            if event.key == pygame.K_r: mode='red'
            if event.key == pygame.K_g: mode='green'
            if event.key == pygame.K_b: mode='blue'

            if event.key == pygame.K_1: brush = 2
            if event.key == pygame.K_2: brush = 5
            if event.key == pygame.K_3: brush = 10

            if event.key == pygame.K_q: tool='pencil'
            if event.key == pygame.K_w: tool='line'
            if event.key == pygame.K_e: tool='rect'
            if event.key == pygame.K_c: tool='circle'
            if event.key == pygame.K_f: tool='fill'
            if event.key == pygame.K_t: tool='text'
            if event.key == pygame.K_6: tool='square'
            if event.key == pygame.K_7: tool='triangle'
            if event.key == pygame.K_8: tool='eq_triangle'
            if event.key == pygame.K_9: tool='rhombus'

        if event.type == pygame.MOUSEBUTTONDOWN:
            if tool == 'text':
                text_mode = True
                text_pos = event.pos
                text_input = ""
            elif tool == 'fill':
                flood_fill(canvas, event.pos, get_color(mode))
            else:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if tool == 'line':
                pygame.draw.line(canvas, get_color(mode), start_pos, end_pos, brush)

            elif tool == 'rect':
                pygame.draw.rect(canvas, get_color(mode),
                    pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1])), brush)

            elif tool == 'circle':
                dx = end_pos[0]-start_pos[0]
                dy = end_pos[1]-start_pos[1]
                r = int((dx*dx+dy*dy)**0.5)
                pygame.draw.circle(canvas, get_color(mode), start_pos, r, brush)

            elif tool == 'square':
                draw_square(canvas, get_color(mode), start_pos, end_pos, brush)

            elif tool == 'triangle':
                draw_triangle(canvas, get_color(mode), start_pos, end_pos, brush)

            elif tool == 'eq_triangle':
                draw_eq_triangle(canvas, get_color(mode), start_pos, end_pos, brush)

            elif tool == 'rhombus':
                draw_rhombus(canvas, get_color(mode), start_pos, end_pos, brush)

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == 'pencil':
                pygame.draw.line(canvas, get_color(mode), last_pos, event.pos, brush)
                last_pos = event.pos

    screen.blit(canvas, (0,0))

    if drawing and tool == 'line':
        pygame.draw.line(screen, get_color(mode), start_pos, pygame.mouse.get_pos(), brush)

    if text_mode:
        txt = font.render(text_input, True, get_color(mode))
        screen.blit(txt, text_pos)

    pygame.display.flip()
    clock.tick(60)