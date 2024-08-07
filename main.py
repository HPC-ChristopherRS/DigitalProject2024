import pygame
from level import *
from player import *
from enemy import *
from settings import *

def draw_grid(screen, level):
    for row in range(20):
        for column in range(20):
            color = GREEN if level.grid[row][column] == 1 else WHITE
            pygame.draw.rect(screen, color, 
                            [(MARGIN + WIDTH) * column + MARGIN,
                            (MARGIN + HEIGHT) * row + MARGIN,
                            WIDTH, HEIGHT])

def handle_dash_input(player, keys, current_time, last_pressed_time, grid):
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
                player.dash(direction, grid)

    return last_pressed_time

def main():
    pygame.init()
    screen = pygame.display.set_mode((660, 660))
    pygame.display.set_caption("Jerry The Epic SpaceMan")

    level = Level(1)
    player = Player(level)
    enemies = Enemies(level)
    clock = pygame.time.Clock()
    done = False
    last_pressed_time = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                level = Level(level.level_number + 1)
                player.rect.topleft = (80, 80) 

        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 2
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 2
        player.move(dx, dy, level.grid)
        enemies.move_towards_player(player) 
        enemies.collide_player(player)
        enemies.check_collision()

        current_time = pygame.time.get_ticks()

        screen.fill(BLACK)
        draw_grid(screen, level)
        pygame.draw.rect(screen, (0, 0, 0), enemies.rect)
        pygame.draw.rect(screen, (255, 200, 0), player.rect)
        pygame.display.flip()
        clock.tick(60)

        last_pressed_time = handle_dash_input(player, keys, current_time, last_pressed_time, level.grid)

    pygame.quit()

if __name__ == "__main__":
    main()


