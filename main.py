import pygame
import random
import os

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20
FPS = 15

# Colors
BLACK = (10, 10, 10)
NEON_GREEN = (0, 255, 128)
NEON_BLUE = (0, 204, 255)
RED = (255, 50, 50)
WHITE = (255, 255, 255)

# Fonts
FONT = pygame.font.Font(pygame.font.match_font('consolas', bold=True), 28)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("⚡ Futuristic Snake Game ⚡")

# Load background music
pygame.mixer.music.load(os.path.join("assets", "bg_music.mp3"))
pygame.mixer.music.set_volume(0.2)
# Uncomment the line below to play background music if available
# pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (20, 20, 20), (0, y), (SCREEN_WIDTH, y))

def draw_text(text, color, x, y, center=True):
    surface = FONT.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

def draw_snake(snake_list):
    for x, y in snake_list:
        pygame.draw.rect(screen, NEON_GREEN, [x, y, CELL_SIZE, CELL_SIZE], border_radius=5)
        pygame.draw.rect(screen, WHITE, [x + 4, y + 4, 4, 4])

def draw_food(food_x, food_y):
    pygame.draw.rect(screen, NEON_BLUE, [food_x, food_y, CELL_SIZE, CELL_SIZE], border_radius=5)

def save_high_score(score):
    with open("highscore.txt", "a+") as file:
        file.seek(0)
        scores = [int(line.strip()) for line in file.readlines()]
        scores.append(score)
        file.seek(0)
        file.truncate()
        for s in sorted(scores, reverse=True)[:5]:  # Save top 5
            file.write(f"{s}\n")

def get_high_scores():
    if not os.path.exists("highscore.txt"):
        return []
    with open("highscore.txt", "r") as file:
        return [int(line.strip()) for line in file.readlines()]

def game_over_screen(score):
    save_high_score(score)
    screen.fill(BLACK)
    draw_text("Game Over", RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
    draw_text(f"Your Score: {score}", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Press R to Restart or Q to Quit", NEON_BLUE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False

def main():
    x = SCREEN_WIDTH // 2
    y = SCREEN_HEIGHT // 2
    dx = 0
    dy = 0
    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, SCREEN_WIDTH - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
    food_y = round(random.randrange(0, SCREEN_HEIGHT - CELL_SIZE) / CELL_SIZE) * CELL_SIZE

    score = 0
    running = True

    while running:
        screen.fill(BLACK)
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -CELL_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = CELL_SIZE
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -CELL_SIZE
                    dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = CELL_SIZE
                    dx = 0

        x += dx
        y += dy

        # Check boundaries
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            if not game_over_screen(score):
                running = False
            else:
                main()
                return

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check self-collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                if not game_over_screen(score):
                    running = False
                else:
                    main()
                    return

        # Check food collision
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, SCREEN_WIDTH - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
            food_y = round(random.randrange(0, SCREEN_HEIGHT - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
            snake_length += 1
            score += 10

        draw_snake(snake_list)
        draw_food(food_x, food_y)
        draw_text(f"Score: {score}", NEON_BLUE, 10, 10, center=False)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

