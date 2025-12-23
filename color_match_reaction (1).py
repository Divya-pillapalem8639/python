import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🔥 Color Match Reaction Hard")

# Colors
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

colors = [RED, GREEN, BLUE, YELLOW]
color_names = ["R", "G", "B", "Y"]
key_mapping = {pygame.K_r: 0, pygame.K_g: 1, pygame.K_b: 2, pygame.K_y: 3}

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
FPS = 60

# Game variables
blocks = []
spawn_timer = 0
spawn_interval = 60  # initial frames
block_speed = 3
score = 0

running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in key_mapping:
                pressed_index = key_mapping[event.key]
                hit = False
                for block in blocks[:]:
                    if block['color_index'] == pressed_index:
                        blocks.remove(block)
                        score += 1
                        hit = True
                        break
                if not hit:
                    score = max(0, score - 1)  # penalty for wrong key

    # Spawn blocks
    spawn_timer += 1
    if spawn_timer >= spawn_interval:
        spawn_timer = 0
        new_block = {
            'x': random.randint(50, WIDTH-50),
            'y': -50,
            'color_index': random.randint(0, 3),
            'size': 50
        }
        blocks.append(new_block)

    # Move blocks
    for block in blocks[:]:
        block['y'] += block_speed
        if block['y'] > HEIGHT:
            blocks.remove(block)
            score = max(0, score - 1)  # penalty for missed block
        pygame.draw.rect(screen, colors[block['color_index']],
                         (block['x'], block['y'], block['size'], block['size']))
        # draw key hint
        key_text = font.render(color_names[block['color_index']], True, BLACK)
        screen.blit(key_text, (block['x'] + 15, block['y'] + 10))

    # Increase difficulty over time
    if score % 10 == 0 and score != 0:
        block_speed = min(10, 3 + score // 10)
        spawn_interval = max(20, 60 - score // 2)

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(FPS)
