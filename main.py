import pygame
from level import *
from player import Player
from enemy import *
from bullet import *
from settings import *
from textures import *   

def draw_start_menu():
    font = pygame.font.SysFont('arial', 40)
    pygame.display.update()
    
def draw_game_over():
    font = pygame.font.SysFont('arial', 40)
    pygame.display.update()
    
def update_bullets(bullets, grid, tile_size):
    to_remove = []
    for bullet in bullets:
        bullet.update()
        if bullet.check_collision(grid, tile_size):
            to_remove.append(bullet)
    
    for bullet in to_remove:
        bullets.remove(bullet)

def handle_dash_input(player, keys, current_time, last_pressed_time):
    if keys[pygame.K_SPACE]:
        if current_time - last_pressed_time > COOLDOWN_TIME:
            last_pressed_time = current_time
            direction = None
            if keys[pygame.K_d]:
                direction = 'right'
                if keys[pygame.K_s]:
                    direction = 'down-right'
                elif keys[pygame.K_w]:
                    direction = 'up-right'
            elif keys[pygame.K_a]:
                direction = 'left'
                if keys[pygame.K_s]:
                    direction = 'down-left'
                elif keys[pygame.K_w]:
                    direction = 'up-left'
            elif keys[pygame.K_s]:
                direction = 'down'
            elif keys[pygame.K_w]:
                direction = 'up'
            if direction:
                player.dash(direction)

    return last_pressed_time

def main():
    pygame.init()
    pygame.display.set_caption("Jerry The Epic Spaceman")

    level = Level(1)
    player = Player(level, health)
    enemies = []
    clock = pygame.time.Clock()
    bullets = []
    game_state = "game"
    done = False
    last_pressed_time = 0

    def spawn_enemies(level_number):
        num_enemies = 5
        if level_number == 2:
            num_enemies = 1
        elif level_number == 3:
            num_enemies = 10

        for _ in range(num_enemies):
            enemies.append(Enemies(level, health))

    spawn_enemies(level.level_number)

    while not done:
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if game_state == 'start_menu':
                draw_start_menu()
            elif game_state == 'game_over':
                draw_game_over()
            elif game_state == 'game':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    level.load_level(level.level_number + 1)
                    player.rect.topleft = (80, 80)
                    player.level = level
                    enemies.clear()
                    spawn_enemies(level.level_number)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]: # Left click
                        pos = player.rect.x + 15, player.rect.y + 15
                        bullets.append(Bullet(*pos))

        update_bullets(bullets, level.get_grid(), WIDTH)

        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.health -= 1
                    print(enemy.health)
                    bullets.remove(bullet)
                    if enemy.health == 0:
                        enemies.remove(enemy)
                    break

        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * 2
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * 2
        player.move(dx, dy)
        screen.fill(BLACK)
        draw_grid(screen, level)
        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.move_towards_player(player, speed)
            enemy.check_collision()
            enemy.collide_player(player)
            enemy.draw(screen)
        player.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        last_pressed_time = handle_dash_input(player, keys, current_time, last_pressed_time)

    pygame.quit()

if __name__ == "__main__":
    main()