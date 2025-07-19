import pygame
import random
import sys

# To handle PyInstaller's temp folder
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # When using PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Initialize
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grover’s Quest for Cookies")
clock = pygame.time.Clock()

# Fonts
score_font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)
start_font = pygame.font.Font(None, 48)

# Load Images
bg_start = pygame.image.load (resource_path("images/bg1.png"))
bg_start = pygame.transform.scale(bg_start, (WIDTH, HEIGHT))

bg_game = pygame.image.load (resource_path("images/background.png"))
bg_game = pygame.transform.scale(bg_game, (WIDTH, HEIGHT))

frames = [pygame.transform.scale(
    pygame.image.load (resource_path(f"images/grover_frame_{i}.png")), (70, 70)) for i in range(16)]

medusa_frames = [pygame.transform.scale(
    pygame.image.load (resource_path(f"images/medusa_{i}.png")), (110, 110)) for i in range(8)]

cookie_image = pygame.image.load (resource_path("images/cookie.png"))
cookie_image = pygame.transform.scale(cookie_image, (int(cookie_image.get_width() * 0.05), int(cookie_image.get_height() * 0.05)))

# Game Variables
grover_rect = frames[0].get_rect(topleft=(100, 100))
medusa_rect = medusa_frames[0].get_rect(topleft=(600, 300))
cookie_rect = cookie_image.get_rect(topleft=(400, 300))

frame_index = 0
medusa_index = 0
frame_delay = 8
frame_counter = 0

score = 0
medusa_speed = 1.32
game_over = False

# Blinking control
cookie_blink_counter = 0
cookie_blink_speed = 30  # Lower = faster blink

# Fade transition function
def fade(screen):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(15)

# Show start screen
def show_start_screen():
    while True:
        screen.blit(bg_start, (0, 0))
        title_text = start_font.render("You’ve reached Medusa’s temple", True, (255, 255, 255))
        prompt_text = score_font.render("Press SPACE to begin", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                fade(screen)
                return

# Show start screen first
show_start_screen()

# --- Main Game Loop ---
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT] and grover_rect.x > 0:
            grover_rect.x -= 5
        if keys[pygame.K_RIGHT] and grover_rect.x < WIDTH - grover_rect.width:
            grover_rect.x += 5
        if keys[pygame.K_UP] and grover_rect.y > 0:
            grover_rect.y -= 5
        if keys[pygame.K_DOWN] and grover_rect.y < HEIGHT - grover_rect.height:
            grover_rect.y += 5

        # Speed increase
        medusa_speed += (score * 0.001)

        # Medusa follows Grover
        dx = grover_rect.x - medusa_rect.x
        dy = grover_rect.y - medusa_rect.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        medusa_rect.x += int(medusa_speed * dx / distance)
        medusa_rect.y += int(medusa_speed * dy / distance)

        # Cookie collection
        if grover_rect.colliderect(cookie_rect):
            score += 1
            cookie_rect.topleft = (random.randint(50, 750), random.randint(50, 550))

        # Game Over Detection
        medusa_hitbox = medusa_rect.inflate(-200, -200)
        if grover_rect.colliderect(medusa_hitbox):
            game_over = True

        # Animation updates
        frame_counter += 1
        if frame_counter >= frame_delay:
            frame_index = (frame_index + 1) % len(frames)
            medusa_index = (medusa_index + 1) % len(medusa_frames)
            frame_counter = 0

        # Drawing
        screen.blit(bg_game, (0, 0))
        screen.blit(frames[frame_index], grover_rect)
        screen.blit(medusa_frames[medusa_index], medusa_rect)

        # Blinking cookie
        cookie_blink_counter += 1
        if (cookie_blink_counter // cookie_blink_speed) % 2 == 0:
            screen.blit(cookie_image, cookie_rect)

        # Score
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    else:
        screen.blit(bg_game, (0, 0))
        game_over_text = game_over_font.render("YOU TURNED INTO A STONE", True, (255, 0, 0))
        final_score_text = score_font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 20))

    # Debug: medusa hitbox (remove in final)
    # pygame.draw.rect(screen, (255, 0, 0), medusa_hitbox, 2)

    pygame.display.flip()

pygame.quit()
