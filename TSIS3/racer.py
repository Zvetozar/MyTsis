import pygame
import random
import time
import os
from persistence import save_score

pygame.init()
pygame.mixer.init()

WIDTH = 400
HEIGHT = 600

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image(name, size):
    return pygame.transform.scale(
        pygame.image.load(os.path.join(BASE_DIR, "assets", name)),
        size
    )

def load_sound(name):
    try:
        return pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", name))
    except:
        return None

IMAGE_PLAYER = load_image("Player.png", (40, 60))
IMAGE_ANOTHERPLAYER = load_image("Player2.png", (40, 60))
IMAGE_ENEMY = load_image("Enemy.png", (40, 60))
IMAGE_BG = load_image("AnimatedStreet.png", (400, 600))

sound_crash = load_sound("crash.wav")
sound_coin = load_sound("coin.wav")
sound_power = load_sound("power.wav")

font_big = pygame.font.SysFont("Verdana", 50)
font_small = pygame.font.SysFont("Verdana", 20)


def run_game(screen, username, settings):

    clock = pygame.time.Clock()

    player = pygame.Rect(180, 500, 40, 60)

    coins = 0
    distance = 0
    speed = 5

    enemy_speed = 5 if settings["difficulty"] == "easy" else 12 if settings["difficulty"] == "hard" else 8

    traffic = [pygame.Rect(random.randint(0,360), -60, 40,60)]
    obstacle = pygame.Rect(random.randint(0,360), -30, 30,30)
    coin = pygame.Rect(random.randint(0,380), -20, 20,20)
    power = pygame.Rect(random.randint(0,380), -20, 20,20)

    power_type = random.choice(["nitro","shield","repair"])
    player_power = None
    power_timer = 0

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]: player.x -= speed
        if keys[pygame.K_RIGHT]: player.x += speed

        player.clamp_ip(pygame.Rect(0,0,WIDTH,HEIGHT))
        distance += 1

        # TRAFFIC
        for t in traffic:
            t.y += enemy_speed
            if t.top > HEIGHT:
                t.x = random.randint(0,360)
                t.y = -60

            if player.colliderect(t):
                if player_power == "shield":
                    player_power = None
                    t.x = random.randint(0,360)
                    t.y = -60
                else:
                    if settings["sound"] and sound_crash: sound_crash.play()
                    save_score(username, coins*10+distance, distance)

                    screen.fill((255,0,0))
                    screen.blit(font_big.render("GAME OVER", True, (0,0,0)), (60,250))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    return "menu"

        # OBSTACLE
        obstacle.y += 5
        if obstacle.top > HEIGHT:
            obstacle.x = random.randint(0,360)
            obstacle.y = -30

        speed = 2 if player.colliderect(obstacle) else 5

        # COIN
        coin.y += 5
        if coin.top > HEIGHT:
            coin.x = random.randint(0,380)
            coin.y = -20

        if player.colliderect(coin):
            coins += 1
            if settings["sound"] and sound_coin: sound_coin.play()
            coin.x = random.randint(0,380)
            coin.y = -20

        # POWER
        power.y += 5
        if power.top > HEIGHT:
            power.x = random.randint(0,380)
            power.y = -20
            power_type = random.choice(["nitro","shield","repair"])

        if player.colliderect(power):
            player_power = power_type
            power_timer = time.time()
            if settings["sound"] and sound_power: sound_power.play()
            power.x = random.randint(0,380)
            power.y = -20

        # POWER LOGIC
        if player_power:
            if player_power == "nitro":
                speed = 10
            elif player_power == "repair":
                coins += 5

            if time.time() - power_timer > 5:
                player_power = None
                speed = 5

        # DRAW
        screen.blit(IMAGE_BG, (0,0))
        screen.blit(IMAGE_ANOTHERPLAYER if settings["color"]=="red" else IMAGE_PLAYER, player)

        for t in traffic:
            screen.blit(IMAGE_ENEMY, t)

        pygame.draw.rect(screen,(255,215,0),coin)
        pygame.draw.rect(screen,(120,120,120),obstacle)

        color = (0,255,0) if power_type=="shield" else (255,0,0) if power_type=="nitro" else (0,0,255)
        pygame.draw.rect(screen,color,power)

        if player_power:
            screen.blit(font_small.render(f"Power: {player_power}", True,(255,255,0)),(10,40))

        screen.blit(font_small.render(f"Coins:{coins} Dist:{distance}",True,(255,255,255)),(10,10))

        pygame.display.flip()
        clock.tick(60)