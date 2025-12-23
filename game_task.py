import pygame
import sys
import random
import math

pygame.init()

# ================= WINDOW =================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Player Paddle Game")

clock = pygame.time.Clock()

# ================= COLORS =================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
RED = (255, 80, 80)

# ================= FONTS =================
font = pygame.font.SysFont("Arial", 36)
big_font = pygame.font.SysFont("Arial", 60)
info_font = pygame.font.SysFont("Arial", 28)

# ================= PADDLES =================
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 6

left_paddle = pygame.Rect(30, HEIGHT//2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 45, HEIGHT//2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

# ================= BALL =================
BALL_RADIUS = 10
BALL_SPEED = 7

# ================= GAME STATE =================
game_started = False
left_score = 0
right_score = 0
WIN_SCORE = 10

# ================= FUNCTIONS =================
def reset_ball():
    global ball_x, ball_y, dx, dy

    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2

    # Random side (left or right)
    direction = random.choice([-1, 1])

    # Random angle (-45° to 45°)
    angle = random.uniform(-math.pi / 4, math.pi / 4)

    dx = direction * BALL_SPEED * math.cos(angle)
    dy = BALL_SPEED * math.sin(angle)

def start_game():
    global left_score, right_score, game_started
    left_score = 0
    right_score = 0
    reset_ball()
    game_started = True

def decide_winner():
    if left_score > right_score:
        return "Player 1 (Blue) Wins!"
    elif right_score > left_score:
        return "Player 2 (Red) Wins!"
    else:
        return "Match Draw!"

def show_result_screen():
    screen.fill(BLACK)

    title = big_font.render("GAME OVER", True, WHITE)
    winner = font.render(decide_winner(), True, WHITE)
    score = font.render(f"Final Score  {left_score} : {right_score}", True, WHITE)

    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 90))
    screen.blit(winner, (WIDTH//2 - winner.get_width()//2, HEIGHT//2 - 10))
    screen.blit(score, (WIDTH//2 - score.get_width()//2, HEIGHT//2 + 40))

    pygame.display.flip()
    pygame.time.delay(5000)
    pygame.quit()
    sys.exit()

# ================= MAIN LOOP =================
running = True
reset_ball()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            show_result_screen()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                start_game()
            if event.key == pygame.K_q:
                show_result_screen()

    keys = pygame.key.get_pressed()

    # Paddle movement
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED

    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

    # ================= GAME LOGIC =================
    if game_started:
        ball_x += dx
        ball_y += dy

        ball_rect = pygame.Rect(
            ball_x - BALL_RADIUS,
            ball_y - BALL_RADIUS,
            BALL_RADIUS * 2,
            BALL_RADIUS * 2
        )

        # LEFT paddle collision
        if ball_rect.colliderect(left_paddle) and dx < 0:
            dx = abs(dx)
            left_score += 1

        # RIGHT paddle collision
        if ball_rect.colliderect(right_paddle) and dx > 0:
            dx = -abs(dx)
            right_score += 1

        # Out of screen (no top/bottom bounce)
        if ball_x < 0 or ball_x > WIDTH or ball_y < 0 or ball_y > HEIGHT:
            reset_ball()

        # Win condition
        if left_score == WIN_SCORE or right_score == WIN_SCORE:
            show_result_screen()

    # ================= DRAW =================
    screen.fill(BLACK)

    score_text = font.render(f"{left_score} : {right_score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    pygame.draw.rect(screen, BLUE, left_paddle)
    pygame.draw.rect(screen, RED, right_paddle)

    if game_started:
        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), BALL_RADIUS)
    else:
        msg = info_font.render("Press R to Start | Press Q to Quit", True, WHITE)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))

    pygame.display.flip()
