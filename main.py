import pygame
import random
from services.firebase import Firebase

# RGB (Red, Green, Blue)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (56, 219, 31)
BLUE = (50, 153, 213)

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


def get_player_name():
    font = pygame.font.SysFont("bahnschrift", 50)
    input_box = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, 600, 50)
    color_inactive = pygame.Color("lightskyblue3")
    color_active = pygame.Color("dodgerblue2")
    color = color_inactive
    active = False
    player_name = ""
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        SCREEN.fill(BLACK)
        # Render the player's input text.
        txt_surface = font.render(player_name, True, WHITE)
        # Blit the text.
        SCREEN.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input box rect.
        pygame.draw.rect(SCREEN, color, input_box, 2)

        # Display instructions to the player
        instruction_text = font.render("Enter your name and press Enter", True, WHITE)
        SCREEN.blit(instruction_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))

        pygame.display.flip()

    return player_name


def game_over(score: int, player_name: str):
    # Add the player to database
    firebase = Firebase()
    firebase.add_player_to_db(name=player_name, score=score)

    # Get highscore list from database
    highscore_list = firebase.get_sorted_highscore_list_from_db(5)

    # creating font object my_font
    my_font = pygame.font.SysFont("times new roman", 50)

    # Display the high scores
    highscore_surface = my_font.render("High Scores:", True, WHITE)
    highscore_rect = highscore_surface.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
    )
    SCREEN.blit(highscore_surface, highscore_rect)

    # Render the top 5 high scores
    for index, player in enumerate(highscore_list):
        score_surface = my_font.render(
            f"{index + 1}. {player[0]}: {player[1]}", True, WHITE
        )
        score_rect = score_surface.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100 + index * 40)
        )
        SCREEN.blit(score_surface, score_rect)

    # creating a text surface on whhich will be drawn
    game_over_surface = my_font.render(
        f"{player_name}, your score is: {score}", True, RED
    )
    restart_surface = my_font.render("Press R to Restart or Q to Quit", True, WHITE)

    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    )
    restart_rect = restart_surface.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    )

    # Blit the game over text and restart instructions on the screen
    SCREEN.fill(BLACK)  # Clear the screen
    SCREEN.blit(game_over_surface, game_over_rect)
    SCREEN.blit(restart_surface, restart_rect)
    pygame.display.flip()

    # Wait for player input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game with "r"
                    return True
                if event.key == pygame.K_q:  # Quit the game with "q"
                    pygame.quit()
                    quit()


def show_score(score):
    font = pygame.font.SysFont("bahnschrift", 35)
    score_surface = font.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_surface, (10, 10))  # Display score at top left corner


def start():
    pygame.init()  # Initialize Snake game here
    player_name = get_player_name()  # Capture player's name before starting the game

    # Settings for snake
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    snake_speed = 20  # This is the base speed

    # Initalise pygame
    pygame.init()
    pygame.display.set_caption(f"Snake Game - Player: {player_name}")

    # Initialise game window
    pygame.display.set_caption("Snake Game for Hackathon")

    # Set pygame setup
    score = 0
    fps = pygame.time.Clock()  # FPS (frames per second) controller

    # fruit position
    fruit_position = [
        random.randrange(1, (SCREEN_WIDTH // 10)) * 10,
        random.randrange(1, (SCREEN_HEIGHT // 10)) * 10,
    ]
    fruit_spawn = True

    # setting default snake direction
    direction = "RIGHT"
    change_direction = direction

    running = True
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

        # Game Over conditions
        if (
            snake_position[0] < 0
            or snake_position[0] > SCREEN_WIDTH - 10
            or snake_position[1] < 0
            or snake_position[1] > SCREEN_HEIGHT - 10
        ):
            if game_over(score, player_name):
                start()  #  Restart the game
                return
            else:
                running = False

        # Colliding with self
        for block in snake_body[1:]:
            if snake_position == block:
                if game_over(score, player_name):
                    start()
                    return
                else:
                    running = False

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

        pygame.display.update()

        # Frame Per Second /Refresh Rate
        fps.tick(snake_speed)

    pygame.quit()


if __name__ == "__main__":
    start()
