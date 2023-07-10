import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Math Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Set up fonts
font_small = pygame.font.Font(None, 36)
font_medium = pygame.font.Font(None, 48)
font_large = pygame.font.Font(None, 64)

# Set up game variables
clock = pygame.time.Clock()
level = 1
score = 0
player_x = 50
player_y = window_height // 2
player_speed = 5
question = ""
answer = 0
user_answer = ""
correct_answers = 0
times_table = 2

# Set up leaderboard
leaderboard = {}

# Define game states
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_GAME_OVER = "game_over"
state = STATE_MENU

# Define obstacles
obstacles = []
obstacle_width = 50
obstacle_height = 200
obstacle_gap = 200
obstacle_speed = 5
obstacle_spawn_delay = 3000
last_obstacle_spawn = pygame.time.get_ticks()

# Define coins
coins = []
coin_radius = 20
coin_speed = 5
coin_spawn_delay = 2000
last_coin_spawn = pygame.time.get_ticks()

# Define functions
def generate_question():
    global question, answer
    num1 = random.randint(1, 10)
    question = f"What is {times_table} x {num1}?"
    answer = times_table * num1

def spawn_obstacle():
    global obstacles
    obstacle_x = window_width + obstacle_width
    obstacle_y = random.randint(obstacle_height, window_height - obstacle_height)
    obstacles.append(pygame.Rect(obstacle_x, obstacle_y - obstacle_height, obstacle_width, obstacle_height))
    obstacles.append(pygame.Rect(obstacle_x, obstacle_y + obstacle_gap, obstacle_width, window_height - obstacle_y - obstacle_gap))

def spawn_coin():
    global coins
    coin_x = window_width + coin_radius
    coin_y = random.randint(coin_radius, window_height - coin_radius)
    coins.append(pygame.Rect(coin_x, coin_y, coin_radius, coin_radius))

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)

def show_menu():
    window.fill(WHITE)
    draw_text("Math Game", font_large, BLACK, window_width // 2, 100)
    draw_text("Enter Username:", font_medium, BLACK, window_width // 2, 200)
    pygame.display.update()

def show_game():
    window.fill(WHITE)
    draw_text(f"Level: {level}", font_small, BLACK, 60, 10)
    draw_text(f"Score: {score}", font_small, BLACK, window_width - 60, 10)
    draw_text(question, font_medium, BLACK, window_width // 2, 100)
    draw_text(user_answer, font_medium, BLUE, window_width // 2, 200)
    pygame.draw.circle(window, BLACK, (player_x, player_y), 20)
    for obstacle in obstacles:
        pygame.draw.rect(window, BLACK, obstacle)
    for coin in coins:
        pygame.draw.circle(window, BLACK, coin.center, coin_radius)
    pygame.display.update()

def show_game_over():
    window.fill(WHITE)
    draw_text("Game Over", font_large, BLACK, window_width // 2, 100)
    draw_text(f"Score: {score}", font_medium, BLACK, window_width // 2, 200)
    draw_text("Press Enter to Play Again", font_small, BLACK, window_width // 2, 300)
    pygame.display.update()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if state == STATE_MENU:
                if event.key == pygame.K_RETURN:
                    state = STATE_GAME
                    generate_question()
                elif event.key == pygame.K_UP:
                    if times_table < 10:
                        times_table += 1
                elif event.key == pygame.K_DOWN:
                    if times_table > 1:
                        times_table -= 1
            elif state == STATE_GAME:
                if event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                elif event.key == pygame.K_RETURN:
                    try:
                        if int(user_answer) == answer:
                            score += 1
                            correct_answers += 1
                            if correct_answers >= 3:
                                level += 1
                                correct_answers = 0
                            generate_question()
                        else:
                            state = STATE_GAME_OVER
                    except ValueError:
                        pass
                else:
                    user_answer += event.unicode
            elif state == STATE_GAME_OVER:
                if event.key == pygame.K_RETURN:
                    state = STATE_MENU
                    score = 0
                    level = 1
                    obstacles.clear()
                    coins.clear()
                    user_answer = ""

    # Update game logic
    if state == STATE_GAME:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        for obstacle in obstacles:
            obstacle.x -= obstacle_speed
            if obstacle.right < 0:
                obstacles.remove(obstacle)

            if obstacle.colliderect(pygame.Rect(player_x-20, player_y-20, 40, 40)):
                state = STATE_GAME_OVER

        for coin in coins:
            coin.x -= coin_speed
            if coin.right < 0:
                coins.remove(coin)

            if coin.colliderect(pygame.Rect(player_x-20, player_y-20, 40, 40)):
                coins.remove(coin)
                score += 1

        if pygame.time.get_ticks() - last_obstacle_spawn > obstacle_spawn_delay:
            spawn_obstacle()
            last_obstacle_spawn = pygame.time.get_ticks()

        if pygame.time.get_ticks() - last_coin_spawn > coin_spawn_delay:
            spawn_coin()
            last_coin_spawn = pygame.time.get_ticks()

    # Render the game
    if state == STATE_MENU:
        show_menu()
    elif state == STATE_GAME:
        show_game()
    elif state == STATE_GAME_OVER:
        show_game_over()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
