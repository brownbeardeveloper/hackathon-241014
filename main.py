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


def draw_snake(snake_size, snake_list) -> None:
    """
    Draw the snake on the game screen.

    This function takes the size of the snake segments and a list of
    coordinates representing the positions of each segment. It then
    draws rectangles on the screen for each segment of the snake.

    Args:
        snake_size (int): The width and height of each segment of the snake.
        snake_list (list): A list of tuples, where each tuple contains
                           the (x, y) coordinates of a segment of the snake.
    """
    for x in snake_list:
        pygame.draw.rect(SCREEN, GREEN, [x[0], x[1], snake_size, snake_size])


def pause_game() -> None:
    """
    Pause the game and display a pause message on the screen.

    This function overlays a pause message indicating that the game is paused
    and waits for the player to press the 'P' key to resume the game. It also
    handles quitting the game if the player closes the window.
    """
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


def message(text, color, position) -> None:
    """
    Display a message on the screen at a specified position.

    This function renders a message using the specified font style and color,
    and then blits it onto the game screen at the provided position.

    Args:
        text (str): The message text to display.
        color (tuple): A tuple representing the RGB color of the text (e.g., (255, 255, 255) for white).
        position (tuple): A tuple representing the (x, y) coordinates to center the message on the screen.
    """
    font_style = pygame.font.SysFont("bahnschrift", 50)
    message_surface = font_style.render(text, True, color)
    message_rect = message_surface.get_rect(center=position)
    SCREEN.blit(message_surface, message_rect)
    pygame.display.update()


def get_player_name() -> str:
    """
    Prompt the player to enter their name via a graphical input box.

    This function creates an input box where the player can type their name.
    It listens for mouse and keyboard events to handle user interaction,
    allowing the player to activate the input box, type their name,
    and submit it by pressing the Enter key.

    Returns:
        str: The player's name, formatted with the first letter of each word capitalized.
    """
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

    return player_name.title()


def game_over(score: int, player_name: str) -> bool:
    """
    Handle the game over screen, save the player's score, and display high scores.

    This function performs the following tasks:
    1. Adds the player's score and name to the Firebase database.
    2. Retrieves and displays the top 5 high scores from the database.
    3. Shows a game over message with the player's score.
    4. Displays instructions to restart or quit the game.
    5. Waits for user input to either restart or quit the game.

    Args:
        score (int): The player's final score.
        player_name (str): The name of the player to be added to the high score list.

    Returns:
        bool: Returns True if the player chooses to restart the game, otherwise the game quits.
    """
    # Add this player to the database
    firebase = Firebase()
    firebase.add_player_to_db(name=player_name, score=score)

    # Get high score list from the database
    highscore_list = firebase.get_sorted_highscore_list_from_db(5)

    # Create a font object
    my_font = pygame.font.SysFont("times new roman", 50)

    # Clear the screen
    SCREEN.fill(BLACK)

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

    # Create the game over text surface
    game_over_surface = my_font.render(
        f"{player_name}, your score is: {score}", True, RED
    )
    restart_surface = my_font.render("Press R to Restart or Q to Quit", True, WHITE)

    # Create rectangular objects for the text surfaces
    game_over_rect = game_over_surface.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    )
    restart_rect = restart_surface.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    )

    # Blit the game over text and restart instructions on the screen
    SCREEN.blit(game_over_surface, game_over_rect)
    SCREEN.blit(restart_surface, restart_rect)

    # Update the display
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


def show_score(score: int):
    """
    Display the current score on the screen.

    This function renders the player's score using the specified font
    and displays it in the top-left corner of the game window.

    Args:
        score (int): The player's current score to display.
    """
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
    fps = pygame.time.Clock()  # FPS controller

    # Fruit position
    fruit_position = [
        random.randrange(1, (SCREEN_WIDTH // 10)) * 10,
        random.randrange(1, (SCREEN_HEIGHT // 10)) * 10,
    ]
    fruit_spawn = True

    # Setting default snake direction
    direction = "RIGHT"
    change_direction = direction

    running = True

    while running:
        # Handling key events
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
                    game_over(player_name=player_name, score=score)
                    running = False

        # Ensure the snake doesn't move in two opposite directions simultaneously
        # (i.e., prevent 180-degree turns).
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

            # Increase the snake's speed for every 5 fruits eaten.
            if score > 50:
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

        # Control the frame rate of the game to match the snake's speed
        fps.tick(snake_speed)

    pygame.quit()


if __name__ == "__main__":
    start()
