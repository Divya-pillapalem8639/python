import pygame
import random
import sys

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# ---------------- Screen Setup ----------------
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Click the Circle Game ")

# ---------------- Load Assets ----------------
# Background image
bg_image = pygame.image.load("background.jpg")  # Replace with your file
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Circle image
circle_img = pygame.image.load("circle.png")  # Replace with your file
circle_radius = 40  # Size for collision detection
circle_img = pygame.transform.scale(circle_img,(circle_radius*2, circle_radius*2))

# Music and sound effects
pygame.mixer.music.load("background_music.mp3")  # Replace with your file
pygame.mixer.music.play(-1)  # Loop background music

click_sound = pygame.mixer.Sound("click_sound.wav")  # Replace with your file

# ---------------- Game Variables ----------------
score = 0
time_limit = 30
circle_x = random.randint(circle_radius, WIDTH - circle_radius)
circle_y = random.randint(circle_radius, HEIGHT - circle_radius)
font = pygame.font.SysFont("Arial", 32)
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()  # Track start time

# ---------------- Game Loop ----------------
running = True
while running:
    clock.tick(60)
    
    # Draw background
    win.blit(bg_image, (0, 0))
    
    # Calculate remaining time
    seconds = time_limit - (pygame.time.get_ticks() - start_ticks) // 1000
    if seconds <= 0:
        win.fill((0,0,0))
        over_text = font.render(" Time's Up!", True, (255,0,0))
        score_text = font.render(f"Your Score: {score}", True, (0,255,0))
        win.blit(over_text, (WIDTH//2 - 100, HEIGHT//2 - 40))
        win.blit(score_text, (WIDTH//2 - 100, HEIGHT//2 + 10))
        pygame.display.update()
        pygame.time.delay(5000)
        break

    # Draw the circle image
    win.blit(circle_img, (circle_x - circle_radius, circle_y - circle_radius))
    
    # Draw score and timer
    score_text = font.render(f"Score: {score}", True, (255,0,0))
    time_text = font.render(f"Time: {seconds}", True, (255,0,0))
    win.blit(score_text, (10, 10))
    win.blit(time_text, (WIDTH - 150, 10))
    
    pygame.display.update()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = event.pos
            dist = ((mouse_x - circle_x)**2 + (mouse_y - circle_y)**2)**0.5
            if dist <= circle_radius:
                score += 1
                click_sound.play()  # Play sound effect
                # Generate new random circle position
                circle_x = random.randint(circle_radius, WIDTH - circle_radius)
                circle_y = random.randint(circle_radius, HEIGHT - circle_radius)

pygame.quit()
