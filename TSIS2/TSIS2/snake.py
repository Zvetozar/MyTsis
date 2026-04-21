import pygame, sys, random

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

snake = [(100,100), (80,100), (60,100)]
direction = (20, 0)

food = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))

score = 0
level = 1
speed = 10

font = pygame.font.SysFont(None, 30)

def generate_food():
    while True:
        pos = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
        if pos not in snake:
            return pos

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = (0, -CELL)
            elif event.key == pygame.K_DOWN:
                direction = (0, CELL)
            elif event.key == pygame.K_LEFT:
                direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT:
                direction = (CELL, 0)

    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)

    # проверка границ
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        pygame.quit()
        sys.exit()

    # проверка на саму себя
    if head in snake[1:]:
        pygame.quit()
        sys.exit()

    # если съели еду
    if head == food:
        score += 1
        food = generate_food()

        # уровни
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    screen.fill((0,0,0))

    # рисуем змейку
    for segment in snake:
        pygame.draw.rect(screen, (0,255,0), (*segment, CELL, CELL))

    # рисуем еду
    pygame.draw.rect(screen, (255,0,0), (*food, CELL, CELL))

    # текст
    text = font.render(f"Score: {score}  Level: {level}", True, (255,255,255))
    screen.blit(text, (10,10))

    pygame.display.flip()
    clock.tick(speed)