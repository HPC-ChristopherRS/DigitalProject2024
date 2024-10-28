import pygame
from level import *
from player import *
from enemy import *
from bullet import *
from settings import *
from textures import *  
from objects import *
from inventory import *  

#checks for collision and sets those that collide to a list that they are then removed from
def update_bullets(bullets, grid, tile_size):
    to_remove = []
    for bullet in bullets:
        bullet.update()
        if bullet.check_collision(grid, tile_size):
            to_remove.append(bullet)
    
    for bullet in to_remove:
        bullets.remove(bullet)

#handles dash input for the player, setting direction based on keys pressed which is then used to handle the dash direction in the player 
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
    
    #timer for dash cooldown
    return last_pressed_time

#draws fade out effect for bombs, levels, and pretty much everything I love this thing
def draw_fade_out(screen, alpha):
    fade_surface = pygame.Surface((640, 640)) #rect
    fade_surface.fill((255, 255, 255)) #color
    fade_surface.set_alpha(alpha) #alpha value
    screen.blit(fade_surface, (0, 0)) #draw

#the main loop :D
def main():
    pygame.init()
    pygame.display.set_caption("Jerry the Epic Spaceman") #games fantastic title

    #sound imports
    pygame.mixer.init()
    gun = pygame.mixer.Sound('sound/test.wav')
    level_music = pygame.mixer.Sound('sound/Music.wav')
    gun.set_volume(0.2)
    level_music.set_volume(1)

    #Font imports/setup
    my_font = pygame.font.Font("Daydream.ttf", 20)
    my_font2 = pygame.font.Font("Daydream.ttf", 8)
    my_font4 = pygame.font.Font("Daydream.ttf", 15)

    #General variables level, player, objects, game setup, etc
    level = Level(1) #level one
    health = 5 #health
    pos_x = 100 #starting x position
    pos_y = 100 #starting y position
    player = Player(level, health) #inizalise player
    bullet_dmg = 1 #set bullet damage
    bomb = 3 #starting bomb amount
    score = 0 #score
    enemies = [] #list for enemies to spawn
    power_list = [] #list for powers to spawn
    object_list = [] #list for objects to spawn
    bullets = [] #list for bullets to spawn
    game_state = "start_menu" #initial game state
    done = False #game loop setup variable
    secret_ending = False #...
    last_pressed_time = 0 #timer setup variable for dash cooldown
    clock = pygame.time.Clock() #clock setup
    level_music.play(-1)

    #fading variables
    fade_alpha = 0 #fully transparent
    fading = False

    def update_text():
        #Set up for text function as they constantly change
        texts = [
            (my_font4.render("Level: " + str(round(level.level_number)), True, WHITE), (750, 30)),
            (my_font.render("Score: " + str(round(score, 1)), True, WHITE), (715, 90)),
            (my_font.render("Health: " + str(round(player.health, 1)), True, WHITE), (715, 125)),
            (my_font.render("Power: " + str(round(bullet_dmg, 1)) + "/4", True, WHITE), (715, 160)),
            (my_font.render("Bomb: " + str(round(bomb)), True, WHITE), (715, 195)),
            (my_font2.render("Jerry the Epic Spaceman", True, WHITE), (650, 620)),
            (my_font2.render(str(round(clock.get_fps(), 1)) + " FPS", True, WHITE), (890, 620)),
            (my_font2.render("-------------------------------", True, WHITE), (660, 65)),
            (my_font2.render("-------------------------------", True, WHITE), (660, 240)),
            (my_font4.render("Inventory:", True, WHITE), (720, 270))
        ]

        #update text
        for text, pos in texts:
            screen.blit(text, pos)

        #UI images for visual flair    
        screen.blit(coin_png, (680, 87))
        screen.blit(jerry, (680, 122))
        screen.blit(power_png, (680, 157))
        screen.blit(bomb_png, (680, 192))

    #Start menu
    def draw_start_menu(screen):
        titleimage = pygame.image.load("tiles/jerrytitle.png")
        imagerect = titleimage.get_rect()
        screen.blit(titleimage, imagerect)
        pygame.display.update()

    #Game over menu
    def draw_game_over(screen):
        screen.fill((0, 0, 0))
        text = my_font.render("Game Over! Press Q", True, WHITE)
        screen.blit(text, (300, 300))
        pygame.display.update()

    #Spawning function, sets the amount depending on a level, then appends the enemies to the enemies list which is then drawn in the main loop
    def spawn_enemies(level_number):
        num_enemies = 0
        if level_number == 2:
            num_enemies = 1
        elif level_number == 3:
            num_enemies = 3

        for _ in range(num_enemies): #append to enemy list
            enemies.append(Enemies(level, health))
            
    #Spawning function, sets the amount depending on a level, then appends the objects to the objects list which is then drawn in the main loop
    def spawn_objects(level_number):
        obj_number = 0
        if level_number == 5:
            obj_number = 1

        for _ in range(obj_number): #append to object list
            object_list.append(Objects(level))

    #Initial spawn calls
    spawn_enemies(level.level_number)
    spawn_objects(level.level_number)

    while not done:
        #setup
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            #if game state = start menu, pressning q changes it to game. While in game state it calls the draw_start_menu function drawing the start menu
            if game_state == 'start_menu':
                draw_start_menu(screen)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    game_state = 'game'
                    fading = True
                    fade_alpha = 255 #fully visible

            #if the game state is game_over it calls the draw_game_over function drawing the game over menu, allowing q to change it back to the game state
            elif game_state == 'game_over':
                draw_game_over(screen)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    items.clear()
                    #initial gamesetup, clears all variables and spawns in the enemies and objects
                    game_state = 'game'
                    level = Level(1) #level set
                    player = Player(level, health) #player initialization
                    bullet_dmg = 1 #bullet damage
                    event = pygame.event.Event(CUSTOM_EVENT)
                    pygame.event.post(event) #runs the event to update the level code in the mainloop

            elif game_state == 'game':
                #event that clears pior level and then sets up the next one
                if event.type == CUSTOM_EVENT:
                    Enemies.occupied_positions.clear() #if not done they spawn at 0,0 because the positions are taken up
                    Objects.occupied_positions.clear()

                    if level.level_number in range(1,5): #player positions, for next level, depends on level as different spawns
                        player.rect.topleft = (35, 304)
                    elif level.level_number == 5:
                        player.rect.topleft = (304, 35)

                    enemies.clear() #enemies list, clears screen of enemies
                    power_list.clear() #likewise with power
                    object_list.clear() #and keys
                    spawn_enemies(level.level_number) #setup for next level
                    spawn_objects(level.level_number) #setup for next level

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]: #left click only
                        gun.play()
                        pos = player.rect.x + 15, player.rect.y + 15 #spawns incentre
                        bullets.append(Bullet(*pos)) #appends bullets to the list
                        player.state = 2 #hanges player state to 2 when clicked
                        player.animate() #plays animation
 
                if bullet_dmg >= 4: #if damage is greater than 4 it sets it to 4 as a cap
                    bullet_dmg = 4

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:#fade and bomb 
                    if bomb > 0:
                        fading = True
                        fade_alpha = 255 #fully visible
                        bomb -= 1
                        score += 100 * len(enemies)
                        enemies.clear()

        #game state
        if game_state == 'game':
            update_bullets(bullets, level.get_grid(), WIDTH)

            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.health -= bullet_dmg
                        bullets.remove(bullet)
                        if enemy.health <= 0:
                            #Spawn item at the enemy's last pos
                            power_spawn = Power(level, enemy.rect.x, enemy.rect.y)
                            power_list.append(power_spawn)
                            enemies.remove(enemy) #nemy death
                            score += 100
                        break

            for power in power_list[:]:
                if player.rect.colliderect(power.rect):
                    power_list.remove(power)
                    if power.duck:
                        fading = True #easter egg in my game, 0.05% chance to get a duck item setting power to max
                        fade_alpha = 255 #fully visible
                        bullet_dmg = 4
                        if duck_item not in items: #checks if item already in inventory incase you get super lucky ducky (unlocks secret ending)
                            items.append('items/duck.png')
                            secret_ending = True
                    elif power.bomb:
                        bomb += 1
                    else: 
                        if bullet_dmg < 4:
                            bullet_dmg += 0.1
                            score += 10
                        else:
                            bullet_dmg = 4
                            score += 10
                        break

            #object list append code
            for obj in object_list[:]:
                if player.rect.colliderect(obj.rect):
                    object_list.remove(obj)
                    if level.level_number == 1:
                        items.append('items/key.png')
                    if level.level_number == 2:
                        items.append('items/key1.png')
                    if level.level_number == 3:
                        items.append('items/key2.png')

            dx = (keys[pygame.K_d] - keys[pygame.K_a]) * 2
            dy = (keys[pygame.K_s] - keys[pygame.K_w]) * 2
            player.move(dx, dy)

            screen.fill(BLACK)
            draw_grid(screen, level)
            inventory_grid()

            for bullet in bullets:
                bullet.draw(screen)
            for enemy in enemies:
                enemy.move_towards_player(player, speed)
                enemy.check_collision()
                enemy.collide_player(player)
                enemy.draw(screen)

            for power in power_list:
                power.draw(screen)

            for obj in object_list:
                obj.draw(screen)

            player.draw(screen)
            player.update_self()

            update_text()

            #fading
            if fading:
                draw_fade_out(screen, fade_alpha)
                fade_alpha -= 255 / 60 #Decrease alpha
                if fade_alpha <= 0:
                    fade_alpha = 0
                    fading = False

            pygame.display.flip()

            clock.tick(60)

            last_pressed_time = handle_dash_input(player, keys, current_time, last_pressed_time)

            # Check for game over
            if player.health <= 0:
                game_state = 'game_over'

    pygame.quit()

if __name__ == "__main__":
    main()

