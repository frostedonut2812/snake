import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
BORDER_WIDTH = 6

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 30, 30)
BLACK = (0, 0, 0)
BORDER_COLOR = (80, 80, 80)
BG_TOP = (30, 30, 60)
BG_BOTTOM = (60, 60, 120)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial Black', 32)
score_font = pygame.font.SysFont('Arial', 28, bold=True)

def draw_gradient_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_border():
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH, HEIGHT), BORDER_WIDTH)

def draw_snake(snake, direction):
    for i, segment in enumerate(snake):
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE), border_radius=8)
        if i == 0:
            # Draw eyes on the head
            cx, cy = segment[0], segment[1]
            eye_radius = 3
            # Eye positions based on direction
            if direction == UP:
                eye1 = (cx + 6, cy + 4)
                eye2 = (cx + CELL_SIZE - 6, cy + 4)
                pupil1 = (cx + 6, cy + 6)
                pupil2 = (cx + CELL_SIZE - 6, cy + 6)
            elif direction == DOWN:
                eye1 = (cx + 6, cy + CELL_SIZE - 4)
                eye2 = (cx + CELL_SIZE - 6, cy + CELL_SIZE - 4)
                pupil1 = (cx + 6, cy + CELL_SIZE - 6)
                pupil2 = (cx + CELL_SIZE - 6, cy + CELL_SIZE - 6)
            elif direction == LEFT:
                eye1 = (cx + 4, cy + 6)
                eye2 = (cx + 4, cy + CELL_SIZE - 6)
                pupil1 = (cx + 6, cy + 6)
                pupil2 = (cx + 6, cy + CELL_SIZE - 6)
            else:  # RIGHT
                eye1 = (cx + CELL_SIZE - 4, cy + 6)
                eye2 = (cx + CELL_SIZE - 4, cy + CELL_SIZE - 6)
                pupil1 = (cx + CELL_SIZE - 6, cy + 6)
                pupil2 = (cx + CELL_SIZE - 6, cy + CELL_SIZE - 6)
            pygame.draw.circle(screen, WHITE, eye1, eye_radius)
            pygame.draw.circle(screen, WHITE, eye2, eye_radius)
            pygame.draw.circle(screen, BLACK, pupil1, 1)
            pygame.draw.circle(screen, BLACK, pupil2, 1)

def draw_food(food):
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE), border_radius=10)

def random_food(snake):
    while True:
        x = random.randint(BORDER_WIDTH // CELL_SIZE, (WIDTH - BORDER_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(BORDER_WIDTH // CELL_SIZE, (HEIGHT - BORDER_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

def show_score(score):
    score_surface = score_font.render(f'Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect(center=(WIDTH // 2, 24))
    screen.blit(score_surface, score_rect)

def main():
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = RIGHT
    food = random_food(snake)
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT
        # Move snake
        new_head = (snake[0][0] + direction[0] * CELL_SIZE, snake[0][1] + direction[1] * CELL_SIZE)
        # Check collisions
        if (
            new_head[0] < BORDER_WIDTH or new_head[0] >= WIDTH - BORDER_WIDTH or
            new_head[1] < BORDER_WIDTH or new_head[1] >= HEIGHT - BORDER_WIDTH or
            new_head in snake
        ):
            running = False
            continue
        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = random_food(snake)
        else:
            snake.pop()
        # Draw everything
        draw_gradient_background()
        draw_border()
        draw_snake(snake, direction)
        draw_food(food)
        show_score(score)
        pygame.display.flip()
        clock.tick(12)
    # Game over
    draw_gradient_background()
    draw_border()
    draw_snake(snake, direction)
    draw_food(food)
    show_score(score)
    game_over_surface = font.render('Game Over!', True, RED)
    final_score_surface = score_font.render(f'Final Score: {score}', True, WHITE)
    screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(final_score_surface, (WIDTH // 2 - final_score_surface.get_width() // 2, HEIGHT // 2 - 10))
    prompt_surface = score_font.render('Press any key to exit.', True, WHITE)
    screen.blit(prompt_surface, (WIDTH // 2 - prompt_surface.get_width() // 2, HEIGHT // 2 + 30))
    pygame.display.flip()
    wait_for_key()
    pygame.quit()
    sys.exit()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                waiting = False

if __name__ == '__main__':
    main() 