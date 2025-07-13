import pygame
import random
import os

# Initialize pygame
pygame.init()
pygame.joystick.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20
BASE_FPS = 8
MAX_FPS = 25

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

# Background music (optional)
try:
    pygame.mixer.music.load(os.path.join("assets", "bg_music.mp3"))
    pygame.mixer.music.set_volume(0.2)
    # pygame.mixer.music.play(-1)
except:
    print("Music not found, continuing without sound.")

clock = pygame.time.Clock()

# Particle system
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 10
        self.color = random.choice([NEON_GREEN, NEON_BLUE, WHITE])

    def update(self):
        self.life -= 1
        self.x += random.randint(-2, 2)
        self.y += random.randint(-2, 2)

    def draw(self):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (self.x, self.y), 2)

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (20, 20, 20), (0, y), (SCREEN_WIDTH, y))

def draw_text(text, color, x, y, center=True):
    surface = FONT.render(text, True, color)
    rect = surface.get_rect()
    rect.center = (x, y) if center else (x, y)
    screen.blit(surface, rect)

def draw_food(food_x, food_y):
    pygame.draw.rect(screen, NEON_BLUE, [food_x, food_y, CELL_SIZE, CELL_SIZE], border_radius=5)

def save_high_score(score):
    with open("highscore.txt", "a+") as file:
        file.seek(0)
        scores = [int(line.strip()) for line in file.readlines()]
        scores.append(score)
        file.seek(0)
        file.truncate()
        for s in sorted(scores, reverse=True)[:5]:
            file.write(f"{s}\n")

def game_over_screen(score):
    save_high_score(score)
    screen.fill(BLACK)
    draw_text("GAME OVER", RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
    draw_text(f"Your Score: {score}", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Press R to Restart or Q to Quit", NEON_BLUE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False

def main(auto_play=False):
    x = SCREEN_WIDTH // 2
    y = SCREEN_HEIGHT // 2
    dx = 0
    dy = 0
    snake = []
    snake_length = 1
    hue = 0
    particles = []

    food_x = round(random.randrange(0, SCREEN_WIDTH - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
    food_y = round(random.randrange(0, SCREEN_HEIGHT - CELL_SIZE) / CELL_SIZE) * CELL_SIZE

    powerup = None
    powerup_x = powerup_y = -100
    powerup_timer = 0
    score_multiplier = 1
    speed_boost = False

    score = 0
    frame_count = 0

    joystick = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None
    if joystick: joystick.init()

    running = True
    while running:
        screen.fill(BLACK)
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Input: Keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and dx == 0: dx, dy = -CELL_SIZE, 0
        if keys[pygame.K_RIGHT] and dx == 0: dx, dy = CELL_SIZE, 0
        if keys[pygame.K_UP] and dy == 0: dx, dy = 0, -CELL_SIZE
        if keys[pygame.K_DOWN] and dy == 0: dx, dy = 0, CELL_SIZE
        if keys[pygame.K_d]: auto_play = True

        # 🎮 Input: Joystick
        if joystick:
            axis0 = round(joystick.get_axis(0))
            axis1 = round(joystick.get_axis(1))
            if axis0 == -1 and dx == 0: dx, dy = -CELL_SIZE, 0
            elif axis0 == 1 and dx == 0: dx, dy = CELL_SIZE, 0
            elif axis1 == -1 and dy == 0: dx, dy = 0, -CELL_SIZE
            elif axis1 == 1 and dy == 0: dx, dy = 0, CELL_SIZE

        # 🧠 Auto-play AI (simple greedy logic)
        if auto_play:
            if abs(food_x - x) > abs(food_y - y):
                dx = CELL_SIZE if food_x > x else -CELL_SIZE
                dy = 0
            else:
                dy = CELL_SIZE if food_y > y else -CELL_SIZE
                dx = 0

        # Movement
        x += dx
        y += dy

        # Border collision
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            if not game_over_screen(score):
                return
            else:
                main()

        # Snake collision
        head = [x, y]
        snake.append(head)
        if len(snake) > snake_length:
            del snake[0]
        if head in snake[:-1]:
            if not game_over_screen(score):
                return
            else:
                main()

        # 🍕 Eat food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, SCREEN_WIDTH - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
            food_y = round(random.randrange(0, SCREEN_HEIGHT - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
            snake_length += 1
            score += 10 * score_multiplier
            particles += [Particle(x, y) for _ in range(15)]
            if random.random() < 0.3:
                powerup = random.choice(["boost", "multiplier"])
                powerup_x = round(random.randrange(0, SCREEN_WIDTH - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
                powerup_y = round(random.randrange(0, SCREEN_HEIGHT - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
                powerup_timer = 100

        # 👾 Powerup logic
        if x == powerup_x and y == powerup_y:
            if powerup == "boost":
                speed_boost = True
            elif powerup == "multiplier":
                score_multiplier = 2
            powerup_x = powerup_y = -100
            powerup_timer = 200

        # ⏳ Powerup timer
        if powerup_timer > 0:
            powerup_timer -= 1
        else:
            powerup = None
            speed_boost = False
            score_multiplier = 1

        # Draw food and powerup
        draw_food(food_x, food_y)
        if powerup:
            pygame.draw.rect(screen, RED if powerup == "boost" else WHITE,
                             [powerup_x, powerup_y, CELL_SIZE, CELL_SIZE], border_radius=3)

        # 🌈 Snake with shifting color tail
        hue = (hue + 2) % 360
        color = pygame.Color(0)
        color.hsva = (hue, 100, 100, 100)
        for i, (sx, sy) in enumerate(snake):
            pygame.draw.rect(screen, color, [sx, sy, CELL_SIZE, CELL_SIZE], border_radius=4)

        # 🌠 Particles
        for p in particles[:]:
            p.update()
            if p.life <= 0:
                particles.remove(p)
            else:
                p.draw()

        # 🧠 Auto Mode Prompt
        draw_text(f"Score: {score}", NEON_BLUE, 10, 10, center=False)
        draw_text("D = AI Mode", WHITE, SCREEN_WIDTH - 150, 10, center=False)

        # ⏩ Dynamic Speed Scaling
        current_fps = BASE_FPS + min(score // 20, MAX_FPS - BASE_FPS)
        if speed_boost:
            current_fps = MAX_FPS

        pygame.display.update()
        clock.tick(current_fps)

    pygame.quit()

if __name__ == "__main__":
    main()
