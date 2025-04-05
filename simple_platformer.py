import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino-Style Platformer")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player settings
player_width, player_height = 30, 30
player_x, player_y = 50, HEIGHT - player_height - 50
player_speed = 5
player_jump = -15
player_velocity_y = 0
gravity = 1
is_jumping = False

# Ground settings
ground_height = 50
ground = pygame.Rect(0, HEIGHT - ground_height, WIDTH, ground_height)

# Obstacle settings
obstacle_width, obstacle_height = 20, 40
obstacle_speed = 5
obstacles = []

# Function to generate obstacles
def generate_obstacle():
    obstacle_x = WIDTH
    obstacle_y = HEIGHT - ground_height - obstacle_height
    return pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

# Add the first obstacle
obstacles.append(generate_obstacle())

# Function to display text on the screen
def draw_text(text, font, color, x, y):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

# Game loop
running = True
game_started = False  # Game starts in a waiting state
score = 0

while running:
    screen.fill(WHITE)  # Clear the screen

    # Draw the ground
    pygame.draw.rect(screen, GREEN, ground)

    # Draw the player
    player = pygame.Rect(player_x, player_y, player_width, player_height)
    pygame.draw.rect(screen, BLUE, player)

    # Draw the obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    # Waiting for the player to start the game
    if not game_started:
        font = pygame.font.SysFont(None, 36)
        draw_text("Press any key to start", font, BLACK, WIDTH // 2 - 150, HEIGHT // 2 - 20)
        pygame.display.flip()

        # Wait for key press to start the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                game_started = True
        continue

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:  # Jump only if not already jumping
        player_velocity_y = player_jump
        is_jumping = True

    # Apply gravity
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Prevent the player from falling below the ground
    if player_y + player_height >= HEIGHT - ground_height:
        player_y = HEIGHT - ground_height - player_height
        player_velocity_y = 0
        is_jumping = False

    # Move obstacles
    for obstacle in obstacles:
        obstacle.x -= obstacle_speed

    # Remove obstacles that go off-screen
    passed_obstacles = [obstacle for obstacle in obstacles if obstacle.x + obstacle_width <= 0]
    obstacles = [obstacle for obstacle in obstacles if obstacle.x + obstacle_width > 0]

    # Generate new obstacles
    if len(obstacles) == 0 or obstacles[-1].x < WIDTH - 200:
        obstacles.append(generate_obstacle())

    # Check for collisions
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            print("Game Over! Final Score:", score)
            running = False

    # Check for successful jumps
    for passed_obstacle in passed_obstacles:
        if player_x > passed_obstacle.x + obstacle_width:
            obstacle_speed *= 1.003  # Increase speed by 0.3%
            print(f"Speed increased! New speed: {obstacle_speed:.2f}")

    # Update the score
    score += 1
    font = pygame.font.SysFont(None, 24)
    draw_text(f"Score: {score}", font, BLACK, 10, 10)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
