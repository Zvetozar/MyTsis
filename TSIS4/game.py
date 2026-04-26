def run_game(username):
    import pygame, random, os, json
    from db import save_game, get_best_score

    pygame.init()

    WIDTH, HEIGHT = 600, 600
    CELL = 20

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(BASE_DIR, "settings.json"), "r") as f:
        settings = json.load(f)

    snake_color = tuple(settings["snake_color"])
    show_grid = settings["grid"]

    snake = [(100,100), (80,100), (60,100)]
    direction = (CELL, 0)

    foods = []
    obstacles = []

    power = None
    power_spawn_time = 0

    active_power = None
    power_timer = 0

    score = 0
    speed = 10
    level = 1

    font = pygame.font.SysFont(None, 30)

    best = get_best_score(username)

    def generate_food():
        while True:
            pos = (random.randrange(0, WIDTH, CELL),
                   random.randrange(0, HEIGHT, CELL))
            if pos not in snake and pos not in obstacles:
                return {
                    "pos": pos,
                    "value": random.choice([1,2,3]),
                    "type": random.choice(["normal", "poison"]),
                    "time": pygame.time.get_ticks()
                }

    def generate_power():
        while True:
            pos = (random.randrange(0, WIDTH, CELL),
                   random.randrange(0, HEIGHT, CELL))
            if pos not in snake and pos not in obstacles:
                return {
                    "pos": pos,
                    "type": random.choice(["speed","slow","shield"]),
                    "time": pygame.time.get_ticks()
                }

    def generate_obstacles():
        obs = []
        for _ in range(5):
            pos = (random.randrange(0, WIDTH, CELL),
                   random.randrange(0, HEIGHT, CELL))
            if pos not in snake:
                obs.append(pos)
        return obs

    for _ in range(2):
        foods.append(generate_food())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(username, score, level)
                return score

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL):
                    direction = (0, -CELL)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                    direction = (0, CELL)
                elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                    direction = (-CELL, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                    direction = (CELL, 0)

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, head)

        current_time = pygame.time.get_ticks()

        # power spawn
        if power is None and random.randint(1,200) == 1:
            power = generate_power()
            power_spawn_time = current_time

        if power and current_time - power_spawn_time > 8000:
            power = None

        # power logic
        speed = 10
        if active_power:
            if active_power == "speed":
                speed = 20
            elif active_power == "slow":
                speed = 5

            if current_time - power_timer > 5000:
                active_power = None

        # collisions
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            if active_power == "shield":
                active_power = None
            else:
                save_game(username, score, level)
                return {"score": score, "level": level}

        if head in snake[1:]:
            if active_power == "shield":
                active_power = None
            else:
                save_game(username, score, level)
                return score

        if head in obstacles:
            save_game(username, score, level)
            return score

        # foods
        foods = [f for f in foods if current_time - f["time"] < 5000]

        while len(foods) < 2:
            foods.append(generate_food())

        ate = False
        for f in foods:
            if head == f["pos"]:
                if f["type"] == "poison":
                    if len(snake) > 2:
                        snake.pop()
                        snake.pop()
                    else:
                        save_game(username, score, level)
                        return score
                else:
                    score += f["value"]
                    level = score // 5 + 1

                    if level >= 3:
                        obstacles = generate_obstacles()

                foods.remove(f)
                ate = True
                break

        if power and head == power["pos"]:
            active_power = power["type"]
            power_timer = current_time
            power = None

        if not ate:
            snake.pop()

        # draw
        screen.fill((0,0,0))

        if show_grid:
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(screen, (40,40,40), (x,0), (x,HEIGHT))
            for y in range(0, HEIGHT, CELL):
                pygame.draw.line(screen, (40,40,40), (0,y), (WIDTH,y))

        for o in obstacles:
            pygame.draw.rect(screen, (120,120,120), (*o, CELL, CELL))

        for s in snake:
            pygame.draw.rect(screen, snake_color, (*s, CELL, CELL))

        for f in foods:
            if f["type"] == "poison":
                color = (139,0,0)
            else:
                color = (255,0,0) if f["value"] == 1 else (0,255,0) if f["value"] == 2 else (0,0,255)
            pygame.draw.rect(screen, color, (*f["pos"], CELL, CELL))

        if power:
            color = (255,255,0) if power["type"]=="speed" else (0,255,255) if power["type"]=="slow" else (255,0,255)
            pygame.draw.rect(screen, color, (*power["pos"], CELL, CELL))

        screen.blit(font.render(f"Score: {score}", True,(255,255,255)),(10,10))
        screen.blit(font.render(f"Level: {level}", True,(255,255,255)),(10,40))
        screen.blit(font.render(f"Best: {best}", True,(255,255,0)),(10,70))

        if active_power:
            screen.blit(font.render(f"Power: {active_power}", True,(255,255,0)),(10,100))

        pygame.display.flip()
        clock.tick(speed)