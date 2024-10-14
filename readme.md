1. Initialize the game environment:
    - Initialize game window with width and height (SCREEN_WIDTH, SCREEN_HEIGHT)
    - Set colors for background, snake, and food (BLACK, GREEN, RED)
    - Set frames per second (FPS)
    - Set snake size (SNAKE_SIZE) and speed (SNAKE_SPEED)
    - Initialize font for displaying text

2. Create helper functions:
    Function draw_text(text, color, position):
        - Render text using the provided font and draw it on the screen at the given position

    Function draw_snake(snake_body):
        - For each segment in the snake_body, draw a rectangle representing the segment on the screen

    Function generate_food():
        - Generate random x, y coordinates for food within screen boundaries, making sure they align with the grid

3. Initialize game state:
    - Set the initial position of the snake head at the center of the screen
    - Set snake_body as a list containing the head's position
    - Set initial direction as 'RIGHT'
    - Generate initial food position using generate_food()

4. Main game loop:
    While the game is not over:
        4.1 Event handling:
            - Check for user input (keyboard events)
            - If UP arrow key is pressed and current direction is not DOWN:
                - Change direction to 'UP'
            - If DOWN arrow key is pressed and current direction is not UP:
                - Change direction to 'DOWN'
            - If LEFT arrow key is pressed and current direction is not RIGHT:
                - Change direction to 'LEFT'
            - If RIGHT arrow key is pressed and current direction is not LEFT:
                - Change direction to 'RIGHT'
        
        4.2 Update snake position:
            - Move snake head in the current direction:
                - If direction is 'UP': decrease y-coordinate of snake head
                - If direction is 'DOWN': increase y-coordinate of snake head
                - If direction is 'LEFT': decrease x-coordinate of snake head
                - If direction is 'RIGHT': increase x-coordinate of snake head
            - Insert the new head position at the beginning of the snake_body list
        
        4.3 Food collision detection:
            - If the snake's head position matches the food position:
                - Increase score
                - Set food_spawn to False (so that new food is generated)
            - Else:
                - Remove the last segment of the snake (to simulate movement)

        4.4 Check if food needs to be spawned:
            - If food_spawn is False:
                - Generate new food position and set food_spawn to True

        4.5 Collision detection:
            - Check if the snake's head touches the screen boundaries:
                - If yes, set game_over to True
            - Check if the snake's head collides with any part of its body:
                - If yes, set game_over to True
        
        4.6 Drawing:
            - Clear the screen
            - Draw food at its current position
            - Draw the snake using the snake_body list
            - Display the current score on the screen

        4.7 Update the screen display
        4.8 Control the frame rate to ensure consistent game speed using FPS

5. Game over handling:
    - Clear the screen
    - Display "Game Over" and the final score
    - Wait for a short duration (e.g., 3 seconds)
    - End the game

6. Start the game loop:
    - When the program is run, start the main game loop
