import pygame

font = pygame.font.SysFont("Verdana", 30)


def draw_menu(screen):
    screen.fill((0,0,0))

    screen.blit(font.render("1 - Play", True, (255,255,255)), (120,200))
    screen.blit(font.render("2 - Leaderboard", True, (255,255,255)), (120,250))
    screen.blit(font.render("3 - Settings", True, (255,255,255)), (120,300))
    screen.blit(font.render("ESC - Quit", True, (255,255,255)), (120,350))


def draw_leaderboard(screen, data):
    screen.fill((0,0,0))

    y = 100
    for i, p in enumerate(data):
        text = f"{i+1}. {p['name']} {p['score']}"
        screen.blit(font.render(text, True, (255,255,255)), (80, y))
        y += 40

    screen.blit(font.render("ESC - Back", True, (255,255,255)), (100,500))


def draw_settings(screen, settings):
    screen.fill((0,0,0))

    screen.blit(font.render(f"Sound: {settings['sound']}", True, (255,255,255)), (80,200))
    screen.blit(font.render(f"Color: {settings['color']}", True, (255,255,255)), (80,250))
    screen.blit(font.render("ESC - Back", True, (255,255,255)), (100,500))