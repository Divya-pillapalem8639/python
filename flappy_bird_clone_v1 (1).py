import pygame
import sys
import random

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Box Clone")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# -----------------------------
# Load Box Image and Resize
# -----------------------------
box_img = pygame.image.load("bird.png")  # can replace with any image
box_size = 30
box_img = pygame.transform.scale(box_img, (box_size, box_size))

box_x = 100
flap_strength = -8
gravity = 0.35

# -----------------------------
# Pipes
# -----------------------------
pipe_width = 70
pipe_gap = 220
pipe_velocity = 4
pipe_spawn_delay = 90
max_pipe_change = 100

# -----------------------------
# Score
# -----------------------------
font = pygame.font.SysFont("Arial", 32)

# -----------------------------
# Function to reset game
# -----------------------------
def reset_game():
    box_y = HEIGHT // 2
    box_velocity = 0
    pipe_list = []
    pipe_timer = 0
    prev_gap_y = HEIGHT // 2 - pipe_gap // 2
    score = 0
    game_started = False
    return box_y, box_velocity, pipe_list, pipe_timer, prev_gap_y, score, game_started

# Initialize game variables
box_y, box_velocity, pipe_list, pipe_timer, prev_gap_y, score, game_started = reset_game()

# -----------------------------
# Game Loop
# -----------------------------
running = True
while running:
    screen.fill(BLUE)

    # -----------------------------
    # Event Handling
    # -----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                box_velocity = flap_strength
                game_started = True

    if game_started:
        # -----------------------------
        # Box Movement
        # -----------------------------
        box_velocity += gravity
        box_y += box_velocity

        # -----------------------------
        # Pipe Spawn
        # -----------------------------
        pipe_timer += 1
        if pipe_timer >= pipe_spawn_delay:
            pipe_timer = 0
            # Smooth vertical position: limit change from previous pipe
            new_gap_y = prev_gap_y + random.randint(-max_pipe_change, max_pipe_change)
            new_gap_y = max(50, min(HEIGHT - pipe_gap - 50, new_gap_y))
            pipe_list.append({"x": WIDTH, "top": new_gap_y, "bottom": new_gap_y + pipe_gap})
            prev_gap_y = new_gap_y

        # -----------------------------
        # Move & Draw Pipes
        # -----------------------------
        for pipe in pipe_list:
            pipe["x"] -= pipe_velocity
            pygame.draw.rect(screen, GREEN, (pipe["x"], 0, pipe_width, pipe["top"]))
            pygame.draw.rect(screen, GREEN, (pipe["x"], pipe["bottom"], pipe_width, HEIGHT - pipe["bottom"]))

        # -----------------------------
        # Remove off-screen pipes and increase score
        # -----------------------------
        for pipe in pipe_list[:]:
            if pipe["x"] + pipe_width < 0:
                pipe_list.remove(pipe)
                score += 1

        # -----------------------------
        # Collision Detection
        # -----------------------------
        collision = False
        for pipe in pipe_list:
            if (box_x + box_size > pipe["x"] and box_x < pipe["x"] + pipe_width) and \
               (box_y < pipe["top"] or box_y + box_size > pipe["bottom"]):
                collision = True
        if box_y <= 0 or box_y + box_size >= HEIGHT:
            collision = True

        # -----------------------------
        # Handle Collision: Restart Game
        # -----------------------------
        if collision:
            game_over_text = font.render(f"GAME OVER! Score: {score}", True, RED)
            screen.blit(game_over_text, (30, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(2000)  # pause before restart
            box_y, box_velocity, pipe_list, pipe_timer, prev_gap_y, score, game_started = reset_game()

    # -----------------------------
    # Draw Box
    # -----------------------------
    screen.blit(box_img, (box_x, box_y))

    # -----------------------------
    # Display Score
    # -----------------------------
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # -----------------------------
    # Show Instructions Before Start
    # -----------------------------
    if not game_started:
        start_text = font.render("Press SPACE to start", True, WHITE)
        screen.blit(start_text, (50, HEIGHT // 2 - 20))

    # Update Screen
    pygame.display.update()
    clock.tick(FPS)
