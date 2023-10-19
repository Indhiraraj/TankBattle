import pygame
import random
import sys

# Game window dimensions
WIDTH = 1100
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255,0)

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Battle Game")
clock = pygame.time.Clock()

# Load images
background_image = pygame.image.load("images/background.jpg").convert()
tank_image = pygame.image.load("images/tank.png").convert_alpha()
tank_image2=pygame.image.load("images/tank2.png").convert_alpha()
bullet_image = pygame.image.load("images/bullet.png").convert_alpha()
enemy_image = pygame.image.load("images/enemy.png").convert_alpha()

# Scale images to fit the game window
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
tank_image = pygame.transform.scale(tank_image, (70, 70))
tank_image2=pygame.transform.scale(tank_image2, (60,60))
bullet_image = pygame.transform.scale(bullet_image, (50, 50))
enemy_image = pygame.transform.scale(enemy_image, (60, 60))

# Load sounds
bullet_sound = pygame.mixer.Sound("music/bullet.mp3")

# Tank class
class Tank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = tank_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if health1==0:
            self.kill()
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))  # Keep tank within screen boundaries

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.y)
        all_sprites.add(bullet)
        bullets.add(bullet)
        bullet_sound.play()

# tank2 class
class Tank2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = tank_image2
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if health2==0:
            self.kill()
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))  # Keep tank within screen boundaries

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.y)
        all_sprites.add(bullet)
        bullets.add(bullet)
        bullet_sound.play()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.uniform(1.0, 2.0)  # Randomized enemy speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.uniform(1.0, 2.0)  # Randomized enemy speed
            decrease_health()

def decrease_health():
    global health1
    global health2
    health1 -= 3
    health2 -= 3
    is_game_over()

def decrease_health1():
    global health1
    health1 -= 10
    if health1 <= 0:
        is_game_over()

def decrease_health2():
    global health2
    health2 -= 10
    if health2 <= 0:
        is_game_over()

def is_game_over():
    global health1
    global health2
    if health1 <= 0 and health2 <=0:
        game_over()
      
def game_over():
    global game_over_screen
    pygame.time.delay(1000)  # Delay for 1 second
    game_over_screen = True

def game_complete():
    global game_complete_screen
    pygame.time.delay(1000)  # Delay for 1 second
    game_complete_screen = True

def show_start_screen():
    window.fill(BLACK)
    title_font = pygame.font.SysFont(None, 80)
    text_font = pygame.font.SysFont(None, 40)

    title_text = title_font.render("Tank Battle Game", True, WHITE)
    start_text = text_font.render("Press ENTER to Start", True, GREEN)
    controls_text0 = text_font.render("Controls", True, WHITE)
    controls_text = text_font.render("1st Player : Left/Right Arrow Keys to Move, Right Ctrl key to Shoot", True, WHITE)
    controls_text1 = text_font.render("2nd Player : A/D Keys to Move, Space to Shoot", True, WHITE)
    quit_text = text_font.render("Press Q to Quit", True, RED)

    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 130))
    control = start_text.get_rect(center=(WIDTH // 2 + 80, HEIGHT // 2 - 70))
    controls_rect = controls_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 ))
    controls_rect1 = controls_text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 125))

    window.blit(title_text, title_rect)
    window.blit(start_text, start_rect)
    window.blit(controls_text0, control)
    window.blit(controls_text, controls_rect)
    window.blit(controls_text1, controls_rect1)
    window.blit(quit_text, quit_rect)

    pygame.display.flip()

def draw_health_bar():
    pygame.draw.rect(window, RED, (20, 20, health1, 20))
    pygame.draw.rect(window, WHITE, (20, 20, 100, 20), 2)
    pygame.draw.rect(window, RED, (20, 50, health2, 20))
    pygame.draw.rect(window, WHITE, (20, 50, 100, 20), 2)



def show_game_over_screen():
    window.fill(BLACK)
    title_font = pygame.font.SysFont(None, 80)
    text_font = pygame.font.SysFont(None, 40)

    title_text = title_font.render("Game Over", True, WHITE)
    restart_text = text_font.render("Press ENTER to Restart", True, WHITE)
    quit_text = text_font.render("Press Q to Quit", True, WHITE)

    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    window.blit(title_text, title_rect)
    window.blit(restart_text, restart_rect)
    window.blit(quit_text, quit_rect)

    pygame.display.flip()

def show_game_complete_screen():
    window.fill(BLACK)
    title_font = pygame.font.SysFont(None, 80)
    text_font = pygame.font.SysFont(None, 40)

    title_text = title_font.render("Awesome!", True, WHITE)
    congrat_text=text_font.render("You have completed the game",True,WHITE)
    restart_text = text_font.render("Press ENTER to Restart", True, WHITE)
    quit_text = text_font.render("Press Q to Quit", True, WHITE)

    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    congrat_rect = congrat_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2+50))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    window.blit(title_text, title_rect)
    window.blit(congrat_text,congrat_rect)
    window.blit(restart_text, restart_rect)
    window.blit(quit_text, quit_rect)

    pygame.display.flip()

# Sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player tank
player_tank = Tank()
all_sprites.add(player_tank)

# Create player tank2
player_tank2 = Tank2()
all_sprites.add(player_tank2)

# Game variables
health2= 100
health1=100
score = 0
level = 1
enemy_spawn_rate = 0
enemy_speed = 1.0

running = True
start_screen = True
game_over_screen = False
game_complete_screen=False

text_font = pygame.font.SysFont(None, 40)  # Define font for score and level text

while running:
    if start_screen:
        show_start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_screen = False
                if event.key == pygame.K_q:
                    running = False

    elif game_over_screen:
        show_game_over_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_over_screen = False
                    health2 = 100
                    health1=100
                    score = 0
                    level = 1
                    enemy_spawn_rate = 0
                    enemy_speed = 1.0
                    all_sprites.empty()
                    bullets.empty()
                    enemies.empty()
                    player_tank = Tank()
                    all_sprites.add(player_tank)
                    player_tank2 = Tank2()
                    all_sprites.add(player_tank2)
                if event.key == pygame.K_q:
                    running = False

    elif game_complete_screen:
        show_game_complete_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_complete_screen = False
                    health2 = 100
                    health1=100
                    score = 0
                    level = 1
                    enemy_spawn_rate = 0
                    enemy_speed = 1.0
                    all_sprites.empty()
                    bullets.empty()
                    enemies.empty()
                    player_tank = Tank()
                    all_sprites.add(player_tank)
                    player_tank2 = Tank2()
                    all_sprites.add(player_tank2)
                if event.key == pygame.K_q:
                    running = False

    else:
        if len(enemies) < level + enemy_spawn_rate:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == event.key == pygame.K_RCTRL:
                    player_tank.shoot()
                if event.key == pygame.K_SPACE:
                    player_tank2.shoot()
                if event.key == pygame.K_q:
                    running = False

        all_sprites.update()

        # Check for bullet collisions with enemies
        bullet_hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for bullet in bullet_hits.keys():
            score += 10
            if score >= 100*level and level<15:
                level += 1
                
                enemy_spawn_rate += 1
                enemy_speed += 0.3
            if score >= 100*level and level >= 15 and level < 25:
                level += 1
                # enemy_spawn_rate +=1
                enemy_speed += 0.5 
            if level==25:
                game_complete()

        # Check for enemy collisions with player tank
        enemy_hits = pygame.sprite.spritecollide(player_tank, enemies, True)
        if enemy_hits:
            decrease_health1()

        # Check for enemy collisions with player tank
        enemy_hits1 = pygame.sprite.spritecollide(player_tank2, enemies, True)
        if enemy_hits1:
            decrease_health2()


        window.blit(background_image, (0, 0))
        all_sprites.draw(window)
        draw_health_bar()

        # Display score and level
        score_text = text_font.render("Score: " + str(score), True, WHITE)
        level_text = text_font.render("Level: " + str(level), True, WHITE)
        window.blit(score_text, (20, HEIGHT - 50))
        window.blit(level_text, (WIDTH - 120, HEIGHT - 50))

        pygame.display.flip()

        if len(enemies) == 0:
            level += 1
            enemy_spawn_rate += 1
            enemy_speed += 0.2

    clock.tick(60)

pygame.quit()
sys.exit()
