# Example file showing a circle moving on screen
import pygame
import time
import random
import color

# Settings for snake
snake_speed = 10
snake_size = 5

# Färger (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (56, 219, 31)
BLUE = (50, 153, 213)

test = color.Color.BLACK

# Screen display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


def draw_snake():
    pass


def stop_game():
    pass


def message():
    pass


def game_over():
    pass


def show_score():
    pass


def start():
    # pygame setup
    pygame.init()
    pygame.display.set_caption("Snake Game for Hackathon")
    screen = pygame.display.set_mode((1280, 720))
    fps = pygame.time.Clock()  # FPS (frames per second) controller
    running = True
    dt = 0  # dt is delta time in seconds since last frame, used for framerate-

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("blue")

        pygame.draw.circle(screen, "green", player_pos, 40)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 500 * dt
        if keys[pygame.K_s]:
            player_pos.y += 500 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 500 * dt
        if keys[pygame.K_d]:
            player_pos.x += 500 * dt
        if keys[pygame.K_q]:
            running = False
            pygame.display.set_caption("Show Text")

            # create a font object.
            # 1st parameter is the font file
            # which is present in pygame.
            # 2nd parameter is size of the font
            font = pygame.font.Font("freesansbold.ttf", 32)

            # create a text surface object,
            # on which text is drawn on it.
            text = font.render("GeeksForGeeks", True)

            # create a rectangular object for the
            # text surface object
            textRect = text.get_rect()

            # set the center of the rectangular object.
            textRect.center = (X // 2, Y // 2)
            time.sleep(5)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # independent physics.
        dt = fps.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    start()
