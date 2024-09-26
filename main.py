import pygame
from level import *
from player import *
from enemy import *
from bullet import *
from settings import *
from textures import *  
from objects import *

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
    pygame.display.set_caption("Jerry the Epic Spaceman")
    
    my_font = pygame.font.Font("Daydream.ttf", 20)
    my_font2 = pygame.font.Font("Daydream.ttf", 8)
    my_font4 = pygame.font.Font("Daydream.ttf", 15)

    level = Level(1)
    player = Player(level, health)
    bullet_dmg = 1
    bomb = 1
    score = 0
    enemies = []
    object_list = []
    bullets = []
    game_state = "start_menu"
    done = False
    last_pressed_time = 0
    clock = pygame.time.Clock()
    
    def update_text():
        texts = [
            (my_font4.render("Level: " + str(round(level.level_number)), 40, WHITE), (750, 30)),
            (my_font.render("Score: " + str(round(score, 1)), 40, WHITE), (715, 90)),
            (my_font.render("Health: " + str(round(player.health, 1)), 40, WHITE), (715, 125)),
            (my_font.render("Power: " + str(round(bullet_dmg, 1)) + "/4", 40, WHITE), (715, 160)),
            (my_font.render("Bomb: " + str(round(bomb)), 40, WHITE), (715, 195)),
            (my_font2.render("Jerry the Epic Spaceman", 40, WHITE), (650, 620)),
            (my_font2.render(str(round(clock.get_fps(), 1)) + " FPS", 40, WHITE), (890, 620)),
            (my_font2.render("-------------------------------", 40, WHITE), (660, 65)),
            (my_font2.render("-------------------------------", 40, WHITE), (660, 240)),
            (my_font4.render("Inventory:", 40, WHITE), (720, 270))
        ]

        for text, pos in texts:
            screen.blit(text, pos)
            
        screen.blit(coin_png, (680, 87))
        screen.blit(jerry, (680, 122))
        screen.blit(power_png, (680, 157))
        screen.blit(bomb_png, (680, 192))
        screen.blit(duck_png, (705, 335))

    def draw_start_menu(screen):
        screen.fill((0,0,0))
        text = my_font.render("Press Q", True, WHITE)
        screen.blit(text, (400, 300))
        pygame.display.update()

    def draw_game_over(screen):
        screen.fill((0,0,0))
        text = my_font.render("Game Over!  Press Q", True, WHITE)
        screen.blit(text, (300, 300))
        pygame.display.update()


    def spawn_enemies(level_number):
        num_enemies = 1
        if level_number == 2:
            num_enemies = 1
        elif level_number == 3:
            num_enemies = 10

        for _ in range(num_enemies):
            enemies.append(Enemies(level, health))
            
    def spawn_objects(level_number):
        obj_number = 0
        if level_number == 2:
            obj_number = 1
        elif level_number == 3:
            obj_number = 10

        for _ in range(obj_number):
            object_list.append(Object(level))

    spawn_enemies(level.level_number)
    spawn_objects(level.level_number)

    while not done:
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if game_state == 'start_menu':
                draw_start_menu(screen)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    game_state = 'game'  

            elif game_state == 'game_over':
                draw_game_over(screen)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    game_state = 'game'
                    level = Level(1)
                    player = Player(level, health)
                    bullet_dmg = 1
                    enemies.clear()
                    object_list.clear()
                    spawn_enemies(level.level_number)
                    spawn_objects(level.level_number)


            elif game_state == 'game':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        level.load_level(level.level_number + 1)
                        player.rect.topleft = (80, 80)
                        player.level = level
                        enemies.clear()
                        object_list.clear()
                        spawn_enemies(level.level_number)
                        spawn_objects(level.level_number)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:  # Left click
                        pos = player.rect.x + 15, player.rect.y + 15
                        bullets.append(Bullet(*pos))

                if bullet_dmg >= 4:
                    bullet_dmg = 4

        if game_state == 'game':
            update_bullets(bullets, level.get_grid(), WIDTH)

            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.health -= bullet_dmg
                        bullets.remove(bullet)
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                            score += 100
                        break

            for objects in object_list[:]:
                if player.rect.colliderect(objects.rect):
                    object_list.remove(objects)
                    if bullet_dmg != 4:
                        bullet_dmg += 0.1
                        score += 10
                    else:
                        bullet_dmg = 4
                        score += 10
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

            for objects in object_list:
                objects.draw(screen)

            player.draw(screen)

            x_positions = [690, 770, 850]
            y_positions = [320, 400, 480]

            for y in y_positions:
                for x in x_positions:
                    screen.blit(inventory, (x, y))

            update_text()
            pygame.display.flip()

            clock.tick(60)

            last_pressed_time = handle_dash_input(player, keys, current_time, last_pressed_time)

            # Check for game over
            if player.health <= 0:
                game_state = 'game_over'

    pygame.quit()

if __name__ == "__main__":
    main()
