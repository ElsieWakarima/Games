import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horizontal Circle Loop Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Game variables
player_radius = 10
player_x, player_y = WIDTH // 2, HEIGHT - 30
player_speed = 5

circle_radius = 30
circle_speed = 3
circle_list = []

score = 0
font = pygame.font.Font(None, 36)

# Function to create new circle loop
def create_circle():
    x = random.randint(circle_radius, WIDTH - circle_radius)
    y = -circle_radius
    return [x, y]

# Function to move and draw circles
def move_circles(circles):
    for circle in circles:
        circle[1] += circle_speed  # Move downwards
        circle[0] += random.choice([-1, 1]) * circle_speed  # Move horizontally
        # Ensure circles stay within bounds
        if circle[0] - circle_radius < 0 or circle[0] + circle_radius > WIDTH:
            circle[0] = max(circle_radius, min(WIDTH - circle_radius, circle[0]))
        pygame.draw.circle(screen, BLUE, (circle[0], circle[1]), circle_radius, 2)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x - player_radius > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x + player_radius < WIDTH:
        player_x += player_speed

    # Add new circles
    if random.randint(1, 60) == 1:
        circle_list.append(create_circle())

    # Move circles and check for collisions
    move_circles(circle_list)
    circle_list = [circle for circle in circle_list if circle[1] - circle_radius < HEIGHT]

    # Check for collision
    for circle in circle_list:
        dist_x = player_x - circle[0]
        dist_y = player_y - circle[1]
        distance = (dist_x ** 2 + dist_y ** 2) ** 0.5
        if distance < player_radius + circle_radius:
            running = False

    # Draw player
    pygame.draw.circle(screen, RED, (player_x, player_y), player_radius)

    # Update score
    score_text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(score_text, (10, 10))
    score += 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
