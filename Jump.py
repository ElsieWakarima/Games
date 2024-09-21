import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 20
WALL_WIDTH = 100
INITIAL_HOLE_SIZE = 150
WALL_SPEED = 5
COLLECTIBLE_SIZE = 30
COLLECTIBLE_MIN_DISTANCE_FROM_WALL = 150
GRAVITY = 0.5
JUMP_STRENGTH = -7

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Through the Walls with Collectibles")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Ball class
class Ball:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.radius = BALL_RADIUS
        self.color = GREEN
        self.speed = 5
        self.velocity = 0  # Ball starts with no velocity (stationary)

    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity

        # Prevent ball from going off the screen
        if self.y - self.radius < 0:
            self.y = self.radius
            self.velocity = 0
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

# Wall class
class Wall:
    def __init__(self, hole_size):
        self.x = WIDTH
        self.width = WALL_WIDTH
        self.hole_y = random.randint(hole_size, HEIGHT - hole_size)
        self.hole_size = hole_size
        self.color = RED
        self.passed = False
        self.speed = WALL_SPEED

    def move(self):
        self.x -= self.speed

    def draw(self):
        # Draw top part of the wall
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.hole_y - self.hole_size // 2))
        # Draw bottom part of the wall
        pygame.draw.rect(screen, self.color, (self.x, self.hole_y + self.hole_size // 2, self.width, HEIGHT))

    def off_screen(self):
        return self.x + self.width < 0

    def get_rects(self):
        return [
            pygame.Rect(self.x, 0, self.width, self.hole_y - self.hole_size // 2),
            pygame.Rect(self.x, self.hole_y + self.hole_size // 2, self.width, HEIGHT - (self.hole_y + self.hole_size // 2)),
        ]

# Collectible class
class Collectible:
    def __init__(self, walls):
        self.x = WIDTH
        self.y = random.randint(COLLECTIBLE_SIZE, HEIGHT - COLLECTIBLE_SIZE)
        self.size = COLLECTIBLE_SIZE
        self.color = YELLOW
        self.speed = WALL_SPEED
        self.walls = walls

        # Make sure the collectible is not near any wall
        while self.is_near_wall():
            self.y = random.randint(COLLECTIBLE_SIZE, HEIGHT - COLLECTIBLE_SIZE)

    def is_near_wall(self):
        for wall in self.walls:
            if abs(self.x - wall.x) < COLLECTIBLE_MIN_DISTANCE_FROM_WALL:
                return True
        return False

    def move(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size // 2)

    def off_screen(self):
        return self.x + self.size < 0

    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

# Main game function
def main():
    ball = Ball()
    walls = []
    collectibles = []
    score = 0
    wall_frequency = 2000  # milliseconds between walls
    collectible_frequency = 5000  # milliseconds between collectibles
    last_wall_time = pygame.time.get_ticks()
    last_collectible_time = pygame.time.get_ticks()

    speed_increase_time = 0  # Time when the last speed/hole change occurred
    speed_increase_interval = 10000  # Every 10 seconds
    hole_size = INITIAL_HOLE_SIZE
    speed = WALL_SPEED

    running = True
    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball.jump()

        # Create new walls
        current_time = pygame.time.get_ticks()
        if current_time - last_wall_time > wall_frequency:
            walls.append(Wall(hole_size))
            last_wall_time = current_time

        # Create new collectibles not near walls
        if current_time - last_collectible_time > collectible_frequency:
            collectibles.append(Collectible(walls))
            last_collectible_time = current_time

        # Gradually increase speed and decrease hole size
        if current_time - speed_increase_time > speed_increase_interval:
            speed += 1
            if hole_size > 100:
                hole_size -= 10
            for wall in walls:
                wall.speed = speed
            for collectible in collectibles:
                collectible.speed = speed
            speed_increase_time = current_time

        # Move and draw walls
        for wall in walls[:]:
            wall.move()
            wall.draw()

            # Check if the ball passes through the hole in the wall
            if not wall.passed and wall.x + wall.width < ball.x - ball.radius:
                score += 1
                wall.passed = True

            # Remove walls that have gone off screen
            if wall.off_screen():
                walls.remove(wall)

        # Move and draw collectibles
        for collectible in collectibles[:]:
            collectible.move()
            collectible.draw()

            # Check if ball collides with collectible
            if ball.get_rect().colliderect(collectible.get_rect()):
                score += 5  # Earn extra points for collecting
                collectibles.remove(collectible)

            # Remove collectibles that have gone off screen
            if collectible.off_screen():
                collectibles.remove(collectible)

        # Update ball position with gravity
        ball.update()

        # Check for collisions with walls
        ball_rect = ball.get_rect()
        for wall in walls:
            for rect in wall.get_rects():
                if ball_rect.colliderect(rect):
                    running = False  # Game over if the ball hits a wall

        # Draw the ball
        ball.draw()

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
