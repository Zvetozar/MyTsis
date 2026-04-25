import pygame
from racer import run_game
from persistence import load_leaderboard, load_settings, save_settings

pygame.init()

screen = pygame.display.set_mode((400,600))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 30)

state = "menu"
username = ""
settings = load_settings()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # 🔥 ESC ВЕЗДЕ
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if state == "menu":
                pygame.quit()
                exit()
            else:
                state = "menu"

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
                if event.key == pygame.K_RETURN and username != "":
                    state = "game"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if event.unicode.isalnum():
                        username += event.unicode

        # ===== SETTINGS =====
        elif state == "settings":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]

                elif event.key == pygame.K_c:
                    settings["color"] = "red" if settings["color"] == "blue" else "blue"

                elif event.key == pygame.K_d:
                    if settings["difficulty"] == "easy":
                        settings["difficulty"] = "normal"
                    elif settings["difficulty"] == "normal":
                        settings["difficulty"] = "hard"
                    else:
                        settings["difficulty"] = "easy"

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
        screen.blit(font.render("1 - Play", True, (255,255,255)), (120,180))
        screen.blit(font.render("2 - Leaderboard", True, (255,255,255)), (120,230))
        screen.blit(font.render("3 - Settings", True, (255,255,255)), (120,280))
        screen.blit(font.render("ESC - Exit", True, (200,200,200)), (120,330))

    elif state == "input":
        screen.fill((0,0,0))
        screen.blit(font.render("Enter name:", True, (255,255,255)), (100,200))
        screen.blit(font.render(username, True, (255,255,0)), (100,250))
        screen.blit(font.render("Press ENTER to start", True, (200,200,200)), (70,300))

    elif state == "leaderboard":
        screen.fill((0,0,0))
        data = load_leaderboard()

        y = 100
        for i, p in enumerate(data):
            text = f"{i+1}. {p['name']} {p['score']}"
            screen.blit(font.render(text, True, (255,255,255)), (80, y))
            y += 40

        screen.blit(font.render("ESC - Back", True, (255,255,255)), (100,500))

    elif state == "settings":
        screen.fill((0,0,0))
        screen.blit(font.render(f"S - Sound: {settings['sound']}", True, (255,255,255)), (60,200))
        screen.blit(font.render(f"C - Color: {settings['color']}", True, (255,255,255)), (60,250))
        screen.blit(font.render(f"D - Difficulty: {settings['difficulty']}", True, (255,255,255)), (60,300))
        screen.blit(font.render("ESC - Save & Back", True, (200,200,200)), (60,380))

    elif state == "game":
        result = run_game(screen, username, settings)

        if result == "menu":
            state = "menu"
            username = ""

        if result == "quit":
            pygame.quit()
            exit()

    pygame.display.flip()
    clock.tick(60)