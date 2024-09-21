import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sky Jumper")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
YELLOW = (255, 223, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Player settings
player_width = 40
player_height = 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 50
player_velocity_y = 0
jump_power = -15
gravity = 1
player_speed = 5

# Cloud settings
cloud_width = 100
cloud_height = 20
clouds = []
cloud_speed = 2
cloud_speed_increase = 0.01  # Speed increment

# Star settings
star_width = 20
stars = []
score = 0

# Game state
game_over = False

# Load images
player_image = pygame.Surface((player_width, player_height))
player_image.fill(YELLOW)

cloud_image = pygame.Surface((cloud_width, cloud_height))
cloud_image.fill(GRAY)

star_image = pygame.Surface((star_width, star_width))
star_image.fill(YELLOW)

# Fonts
font = pygame.font.SysFont("Arial", 30)
game_over_font = pygame.font.SysFont("Arial", 50)

# Functions
def create_clouds():
    for i in range(5):
        x = random.randint(0, WIDTH - cloud_width)
        y = random.randint(0, HEIGHT - cloud_height)
        clouds.append([x, y])

def create_star():
    x = random.randint(0, WIDTH - star_width)
    y = random.randint(-HEIGHT, 0)
    stars.append([x, y])

def draw_clouds():
    for cloud in clouds:
        screen.blit(cloud_image, (cloud[0], cloud[1]))

def draw_stars():
    for star in stars:
        screen.blit(star_image, (star[0], star[1]))

def move_clouds():
    global cloud_speed
    for cloud in clouds:
        cloud[1] += cloud_speed
        if cloud[1] > HEIGHT:
            cloud[0] = random.randint(0, WIDTH - cloud_width)
            cloud[1] = random.randint(-HEIGHT, 0)
    cloud_speed += cloud_speed_increase  # Increase cloud speed over time

def move_stars():
    for star in stars:
        star[1] += cloud_speed
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH - star_width)
            star[1] = random.randint(-HEIGHT, 0)

def check_collision(player_rect, clouds):
    for cloud in clouds:
        cloud_rect = pygame.Rect(cloud[0], cloud[1], cloud_width, cloud_height)
        if player_rect.colliderect(cloud_rect):
            return True  # Collision detected
    return False

def check_star_collision(player_rect, stars):
    global score
    for star in stars:
        star_rect = pygame.Rect(star[0], star[1], star_width, star_width)
        if player_rect.colliderect(star_rect):
            score += 1
            stars.remove(star)

def display_game_over():
    game_over_text = game_over_font.render("Game Over", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

# Create initial clouds
create_clouds()

# Game loop
running = True
while running:
    screen.fill(BLUE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # If the game is over, display the game over screen and skip game logic
    if game_over:
        display_game_over()
        pygame.display.flip()
        continue
    
    # Player controls for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and player_y == HEIGHT - player_height - 50:
        player_velocity_y = jump_power
    
    # Player movement and gravity
    player_velocity_y += gravity
    player_y += player_velocity_y
    
    # Prevent player from going out of bounds (left/right)
    if player_x < 0:
        player_x = 0
    if player_x + player_width > WIDTH:
        player_x = WIDTH - player_width
    
    # Prevent falling off screen
    if player_y > HEIGHT - player_height:
        player_y = HEIGHT - player_height
        player_velocity_y = 0

    # Draw player
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    screen.blit(player_image, (player_x, player_y))
    
    # Move and draw clouds
    move_clouds()
    draw_clouds()

    # Collision with clouds (Game Over condition)
    if check_collision(player_rect, clouds):
        game_over = True
    
    # Create, move, and draw stars
    if random.randint(1, 100) < 2:
        create_star()
    move_stars()
    draw_stars()
    
    # Collision with stars
    check_star_collision(player_rect, stars)
    
    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Update screen
    pygame.display.flip()
    
    # Set FPS
    clock.tick(FPS)

pygame.quit()
