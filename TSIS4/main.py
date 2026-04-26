import pygame, json, os
from game import run_game
from db import create_tables, get_top_players

pygame.init()
create_tables()

WIDTH, HEIGHT = 600,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 40)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(BASE_DIR, "settings.json")

def load_settings():
    with open(settings_path,"r") as f:
        return json.load(f)

def save_settings(s):
    with open(settings_path,"w") as f:
        json.dump(s,f,indent=4)

settings = load_settings()

state = "menu"
username = ""
result = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # ===== MENU =====
        if state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    state = "input"
                elif event.key == pygame.K_2:
                    state = "leaderboard"
                elif event.key == pygame.K_3:
                    state = "settings"

        # ===== INPUT =====
        elif state == "input":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:
                    result = run_game(username)
                    state = "game_over"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        # ===== GAME OVER =====
        elif state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    state = "input"
                elif event.key == pygame.K_2:
                    state = "menu"

        # ===== SETTINGS =====
        elif state == "settings":
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_g:
                    settings["grid"] = not settings["grid"]

                elif event.key == pygame.K_c:
                    colors = [
                        [0,255,0],
                        [255,0,0],
                        [0,0,255],
                        [255,255,0]
                    ]
                    current = colors.index(settings["snake_color"])
                    settings["snake_color"] = colors[(current + 1) % len(colors)]

                elif event.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    state = "menu"

        # ===== LEADERBOARD =====
        elif state == "leaderboard":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "menu"

    # ===== DRAW =====

    if state == "menu":
        screen.fill((0,0,0))
        screen.blit(font.render("1 - Play", True,(255,255,255)),(220,180))
        screen.blit(font.render("2 - Leaderboard", True,(255,255,255)),(170,240))
        screen.blit(font.render("3 - Settings", True,(255,255,255)),(200,300))

    elif state == "input":
        screen.fill((0,0,0))
        screen.blit(font.render("Enter name:", True,(255,255,255)),(180,200))
        screen.blit(font.render(username, True,(255,255,0)),(200,260))

    elif state == "game_over":
        screen.fill((0,0,0))
        screen.blit(font.render("GAME OVER", True,(255,0,0)),(180,150))
        screen.blit(font.render(f"Score: {result['score']}", True,(255,255,255)),(200,220))
        screen.blit(font.render(f"Level: {result['level']}", True,(255,255,255)),(200,270))
        screen.blit(font.render("1 - Retry", True,(255,255,255)),(200,340))
        screen.blit(font.render("2 - Menu", True,(255,255,255)),(200,390))

    elif state == "settings":
        screen.fill((0,0,0))

        color = tuple(settings["snake_color"])

        screen.blit(font.render(f"G - Grid: {settings['grid']}", True,(255,255,255)),(150,200))
        screen.blit(font.render("C - Change Color", True,(255,255,255)),(150,260))

        pygame.draw.rect(screen, color, (250,320,100,40))

        screen.blit(font.render("ESC - Save & Back", True,(200,200,200)),(120,400))

    elif state == "leaderboard":
        screen.fill((0,0,0))

        data = get_top_players()
        y = 100

        for i,p in enumerate(data):
            text = f"{i+1}. {p[0]} {p[1]}"
            screen.blit(font.render(text, True,(255,255,255)),(150,y))
            y += 40

        screen.blit(font.render("ESC - Back", True,(200,200,200)),(200,500))

    pygame.display.flip()
    clock.tick(60)