import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Player
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - player_size - 10
player_speed = 300  # Pixels per second

# Bullet
bullet_size = 5
bullet_speed = 500  # Pixels per second
bullet_state = "ready"  # "ready" - ready to fire, "fire" - bullet is moving
bullet_x = 0
bullet_y = 0

# Enemies
enemy_size = 50
enemy_x = random.randint(0, width - enemy_size)
enemy_y = random.randint(50, 150)
enemy_speed = 200
enemies = [(enemy_x, enemy_y, enemy_speed)]

# Score
score = 0
font = pygame.font.Font(None, 36)

# Clock for managing the frame rate
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Limit the frame rate to 60 FPS
    delta_time = clock.tick(60) / 1000.0

    window.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player shooting
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and bullet_state == "ready":
            bullet_x = player_x + player_size // 2 - bullet_size // 2
            bullet_y = player_y
            bullet_state = "fire"

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed * delta_time
    if keys[pygame.K_RIGHT]:
        player_x += player_speed * delta_time

    # Player movement boundaries
    if player_x < 0:
        player_x = 0
    elif player_x > width - player_size:
        player_x = width - player_size

    # Bullet movement
    if bullet_state == "fire":
        bullet_y -= bullet_speed * delta_time
        pygame.draw.circle(window, GREEN, (bullet_x, bullet_y), bullet_size)

    # Bullet boundaries
    if bullet_y <= 0:
        bullet_state = "ready"

    # Enemy movement
    for enemy in enemies:
        enemy_x, enemy_y, enemy_speed = enemy
        enemy_x += enemy_speed * delta_time

        if enemy_x <= 0 or enemy_x >= width - enemy_size:
            enemy_speed *= -1
            enemy_y += 20
        enemy = (enemy_x, enemy_y, enemy_speed)

        # Collision detection
        if (
                bullet_x >= enemy_x
                and bullet_x <= enemy_x + enemy_size
                and bullet_y >= enemy_y
                and bullet_y <= enemy_y + enemy_size
        ):
            bullet_state = "ready"
            score += 1

            # Add more enemies
            if score % 5 == 0:
                num_enemies = score // 5 + 1
                if num_enemies > 5:
                    num_enemies = 5
                for i in range(num_enemies):
                    enemy_size = 50
                    enemy_x = random.randint(0, width - enemy_size)
                    enemy_y = random.randint(50, 150)
                    enemy_speed = 200
                    enemies.append((enemy_x, enemy_y, enemy_speed))

            enemies.remove(enemy)
            enemy_x = random.randint(0, width - enemy_size)
            enemy_y = random.randint(50, 150)
            enemies.append((enemy_x, enemy_y, enemy_speed))

    # Draw player and enemies
    pygame.draw.polygon(
        window,
        WHITE,
        [
            (player_x, player_y),
            (player_x + player_size, player_y),
            (player_x + player_size // 2, player_y - player_size),
        ],
    )

    for enemy in enemies:
        enemy_x, enemy_y, enemy_speed = enemy
        pygame.draw.rect(window, WHITE, (enemy_x, enemy_y, enemy_size, enemy_size))

    # Display score
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))

    pygame.display.update() 