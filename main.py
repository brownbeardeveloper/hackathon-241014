# Example file showing a circle moving on screen
import pygame
import random
import time

# RGB (Red, Green, Blue)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (56, 219, 31)
BLUE = (50, 153, 213)

# The font what type of writing
# font_style = pygame.font.SysFont("bahnschrift", 25)
# score_font = pygame.font.SysFont("comicsansms", 35)

# Screen display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

fruit_position = [
    random.randrange(1, (SCREEN_WIDTH // 10)) * 10,
    random.randrange(1, (SCREEN_HEIGHT // 10)) * 10,
]

fruit_spawn = True


def draw_snake(snake_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(SCREEN, GREEN, [x[0], x[1], snake_size, snake_size])


def pause_game():
    paused = True
    font_style = pygame.font.SysFont("bahnschrift", 50)
    message = font_style.render("Paused. Press P to Resume", True, WHITE)
    # Overlays a pause screen on top of the gameplay surface.
    SCREEN.blit(message, [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2])
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press P to unpause
                    paused = False


def message(text, color, position):
    font_style = pygame.font.SysFont("bahnschrift", 50)
    message_surface = font_style.render(text, True, color)
    message_rect = message_surface.get_rect(center=position)
    SCREEN.blit(message_surface, message_rect)
    pygame.display.update()


def game_over(score: int):
    # creating font object my_font
    my_font = pygame.font.SysFont("times new roman", 50)

    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render("Your Score is : " + str(score), True, RED)

    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    )

    # blit will draw the text on screen
    SCREEN.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # after 2 seconds we will quit the program
    time.sleep(5)

    # deactivating pygame library
    pygame.quit()

    # quit the program
    quit()


def show_score(score):
    font = pygame.font.SysFont("bahnschrift", 35)
    score_surface = font.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_surface, (10, 10))  # Display score at top left corner


def start():
    # Settings for snake
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    snake_speed = 20  # This is the base speed

    # Initalise pygame
    pygame.init()

    # Initialise game window
    pygame.display.set_caption("Snake Game for Hackathon")

    # Set pygame setup
    score = 0
    fps = pygame.time.Clock()  # FPS (frames per second) controller
    running = True

    # fruit position
    fruit_position = [
        random.randrange(1, (SCREEN_WIDTH // 10)) * 10,
        random.randrange(1, (SCREEN_HEIGHT // 10)) * 10,
    ]
    fruit_spawn = True

    # setting default snake direction
    direction = "RIGHT"
    change_direction = direction

    while running:
        # handling key events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_direction = "UP"
                if event.key == pygame.K_DOWN:
                    change_direction = "DOWN"
                if event.key == pygame.K_LEFT:
                    change_direction = "LEFT"
                if event.key == pygame.K_RIGHT:
                    change_direction = "RIGHT"
                if event.key == pygame.K_p:
                    pause_game()
                if event.key == pygame.K_q:
                    # game_over(score)
                    running = False

        # If two keys pressed simultaneously
        # we don't want snake to move into two directions
        # simultaneously.
        if change_direction == "UP" and direction != "DOWN":
            direction = "UP"
        if change_direction == "DOWN" and direction != "UP":
            direction = "DOWN"
        if change_direction == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        if change_direction == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"

        # Moving the snake
        if direction == "UP":
            snake_position[1] -= 10
        if direction == "DOWN":
            snake_position[1] += 10
        if direction == "LEFT":
            snake_position[0] -= 10
        if direction == "RIGHT":
            snake_position[0] += 10

        # Snake body growing mechanism
        # if fruits and snakes collide then scores will be incremented by 10
        snake_body.insert(0, list(snake_position))
        if (
            snake_position[0] == fruit_position[0]
            and snake_position[1] == fruit_position[1]
        ):
            score += 10
            fruit_spawn = False

            # Increase the snake's speed for every 10 fruits eaten.
            if score % 100 == 0:
                snake_speed += 2  # Increase the speed by 2
        else:
            snake_body.pop()

        if not fruit_spawn:
            # Generate a new fruit position
            fruit_position = [
                random.randrange(1, (SCREEN_WIDTH // 10)) * 10,
                random.randrange(1, (SCREEN_HEIGHT // 10)) * 10,
            ]
            fruit_spawn = True

        SCREEN.fill(BLACK)

        # Display the current score and instructions
        show_score(score)

        for pos in snake_body:
            pygame.draw.rect(SCREEN, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(
            SCREEN,
            WHITE,
            pygame.Rect(fruit_position[0], fruit_position[1], 10, 10),
        )

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > SCREEN_WIDTH - 10:
            game_over(score)
        if snake_position[1] < 0 or snake_position[1] > SCREEN_HEIGHT - 10:
            game_over(score)

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over(score)

        # Refresh game screen
        pygame.display.update()

        # Frame Per Second /Refresh Rate
        fps.tick(snake_speed)

    pygame.quit()


if __name__ == "__main__":
    start()
