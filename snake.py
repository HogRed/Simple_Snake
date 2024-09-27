# Package imports
import pygame # Functions for creating Snake
import random # Random number gen
import sys # Interacting with sys vars

# Initialize Pygame
pygame.init()

# Set up the display / game board
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20

# Defining grids for game board
# Floor division for int
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Setting up screen space
# Passing tuple of window width & height
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Getting caption for game
pygame.display.set_caption('Simple Snake Game')

# Set up clock to help framerate
clock = pygame.time.Clock()

# Define tuple colors (R,G,B)
WHITE = (255, 255, 255)
GRAY = (230, 230, 230)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

### GAME FUNCTIONS ###

# Function to draw game grid
# Draws vertical and horizontal lines to create a grid
def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y))

# Defining food spawn location
def random_position(snake):
    while True:
        # Create random x/y coordinate pair for food to be spawned
        x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE

        # Check to make sure food doesn't spawn on snake
        if (x, y) not in snake:
            return (x, y)

# Show score at the top of the screen
def show_score(score):
    font = pygame.font.SysFont('arial', 35)
    score_surface = font.render(f'Current Score: {score}', True, YELLOW)
    screen.blit(score_surface, (10, 10))

# Main program function
def main():
    # Set up snake in the middle of the screen, pointed to the right
    snake = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
    direction = 'RIGHT'
    change_to = direction

    # Spawn food
    food_pos = random_position(snake)

    # Initialize score
    score = 0


    # Main game loop; gets events from game
    while True:
        for event in pygame.event.get():
            # Exit if user quits
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key presses and update the direction if valid
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != 'DOWN':
            change_to = 'UP'
        elif keys[pygame.K_DOWN] and direction != 'UP':
            change_to = 'DOWN'
        elif keys[pygame.K_LEFT] and direction != 'RIGHT':
            change_to = 'LEFT'
        elif keys[pygame.K_RIGHT] and direction != 'LEFT':
            change_to = 'RIGHT'

        # Change snake heading / direction
        direction = change_to

        # Move the snake
        x, y = snake[0]  # Current position (snake's head)

        # Update position based on direction
        if direction == 'UP':
            y -= CELL_SIZE
        elif direction == 'DOWN':
            y += CELL_SIZE
        elif direction == 'LEFT':
            x -= CELL_SIZE
        elif direction == 'RIGHT':
            x += CELL_SIZE

        # Insert new head position
        snake.insert(0, (x, y))

        # Check if snake has eaten the food
        if snake[0] == food_pos:  # Checking head of snake
            score += 1  # If so, add one point
            food_pos = random_position(snake)  # Add new food
        else:
            # Remove the tail segment
            snake.pop()  # Removes last index / tail

        # Boundary collision check
        if (x < 0) or (x >= WINDOW_WIDTH) or (y < 0) or (y >= WINDOW_HEIGHT):
            game_over(score)

        # Check if snake ran into itself
        if snake[0] in snake[1:]:
            game_over(score)

        # Refresh game screen (fill with black color)
        screen.fill(BLACK)

        # Draw food as a red rectangle (20x20 pixels)
        pygame.draw.rect(
            screen,
            RED,
            pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE)
        )

        # Draw snake as green rectangles (20x20 pixels)
        for pos in snake:
            pygame.draw.rect(
                screen,
                GREEN,
                pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            )

        # Draw grid lines (if you want them in your game)
        #draw_grid()

        # Initialize score counter
        show_score(score)
        
        # Update display / render
        pygame.display.update()

        # Control the game's frame rate
        clock.tick(10)


# Game over function
def game_over(score):
    # Create and render font
    font = pygame.font.SysFont('arial', 35)  # Use 'arial' font
    message = font.render(f'Sorry, Game Over! Your Score Is: {score}', True, WHITE)
    # Place the message in the middle of the screen
    rect = message.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
    screen.blit(message, rect)  # Display message
    pygame.display.update()  # Update display
    pygame.time.wait(3000)  # Pause for 3 seconds
    # Exit game
    pygame.quit()
    sys.exit()

# Start the game
if __name__ == '__main__':
    main()
