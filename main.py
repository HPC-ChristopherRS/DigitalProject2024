import pygame
from level import Level
from player import Player
from enemy import Enemies
from settings import *

def draw_start_menu():
    font = pygame.font.SysFont('arial', 40)
    pygame.display.update()
    
def draw_game_over():
    font = pygame.font.SysFont('arial', 40)
    pygame.display.update()

def draw_grid(screen, level):
    for row in range(20):
        for column in range(20):
            color = GREEN if level.get_grid()[row][column] == 1 else WHITE
            pygame.draw.rect(screen, color, 
                            [(MARGIN + WIDTH) * column + MARGIN,
                            (MARGIN + HEIGHT) * row + MARGIN,
                            WIDTH, HEIGHT])

def handle_dash_input(player, keys, current_time, last_pressed_time):
    if keys[pygame.K_q]:
        if current_time - last_pressed_time > COOLDOWN_TIME:
            last_pressed_time = current_time
            direction = None
            if keys[pygame.K_RIGHT]:
                direction = 'right'
                if keys[pygame.K_DOWN]:
                    direction = 'down-right'
                elif keys[pygame.K_UP]:
                    direction = 'up-right'
            elif keys[pygame.K_LEFT]:
                direction = 'left'
                if keys[pygame.K_DOWN]:
                    direction = 'down-left'
                elif keys[pygame.K_UP]:
                    direction = 'up-left'
            elif keys[pygame.K_DOWN]:
                direction = 'down'
            elif keys[pygame.K_UP]:
                direction = 'up'
            if direction:
                player.dash(direction)

    return last_pressed_time

def main():
    pygame.init()
    screen = pygame.display.set_mode((660, 660))
    pygame.display.set_caption("Jerry The Epic SpaceMan")

    level = Level(1)
    player = Player(level)
    enemies = Enemies(level)
    clock = pygame.time.Clock()
    game_state = "game"
    done = False
    last_pressed_time = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            if game_state == 'start_menu':
                draw_start_menu()
                
            if game_state == 'game_over':
                draw_game_over()

            if game_state == 'game':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    level.load_level(level.level_number + 1)  
                    player.rect.topleft = (80, 80) 
                    player.level = level
                    enemies.level = level

        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 2
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 2
        player.move(dx, dy)
        enemies.move_towards_player(player, speed) 
        enemies.collide_player(player)
        enemies.check_collision()

        current_time = pygame.time.get_ticks()

        screen.fill(BLACK)
        draw_grid(screen, level)
        pygame.draw.rect(screen, (0, 0, 0), enemies.rect)
        pygame.draw.rect(screen, (255, 200, 0), player.rect)
        pygame.display.flip()
        clock.tick(60)

        last_pressed_time = handle_dash_input(player, keys, current_time, last_pressed_time)

    pygame.quit()

if __name__ == "__main__":
    main()
