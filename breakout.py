import pygame
from array import array
import time

# Initialize Pygame
pygame.init()

# Set the screen size
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout")

# Set the background color
BACKGROUND_COLOR = (0, 0, 0)
screen.fill(BACKGROUND_COLOR)

# Set the paddle properties
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 20, PADDLE_WIDTH, PADDLE_HEIGHT)
PADDLE_COLOR = (255, 255, 255)

# Set the ball properties
BALL_SIZE = 10
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
BALL_COLOR = (255, 255, 255)
ball_dx = 5
ball_dy = -5

# Set the brick properties
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
NUM_BRICKS_X = 10
NUM_BRICKS_Y = 5
BRICKS_COLOR = (255, 255, 255)
bricks = []
for i in range(NUM_BRICKS_X):
    for j in range(NUM_BRICKS_Y):
        brick = pygame.Rect(i * (BRICK_WIDTH + 4) + 22, j * (BRICK_HEIGHT + 4) + 50, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# Sound setup
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Define a function to generate beep sounds with varying frequencies
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Load game over sound
game_over_sound = generate_beep_sound(220, 1)

# Main game loop
running = True
while running:
    start_time = time.time()  # Record the start time of each frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= 5
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.x += 5

    # Move the ball
    ball.x += ball_dx
    ball.y += ball_dy

    # Check for ball collision with walls
    if ball.left < 0 or ball.right > SCREEN_WIDTH:
        ball_dx *= -1
    if ball.top < 0:
        ball_dy *= -1

    # Check for ball collision with paddle
    if ball.colliderect(paddle) and ball_dy > 0:
        ball_dy *= -1

    # Check for ball collision with bricks
    for brick in bricks[:]:
        if ball.colliderect(brick):
            ball_dy *= -1
            bricks.remove(brick)
            # Play beep sound when the ball bounces from the brick
            generate_beep_sound().play()

    # Check for game over
    if ball.top > SCREEN_HEIGHT:
        game_over_sound.play()
        pygame.time.delay(2000)  # Delay to allow the game over sound to play
        running = False

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the paddle
    pygame.draw.rect(screen, PADDLE_COLOR, paddle)

    # Draw the ball
    pygame.draw.rect(screen, BALL_COLOR, ball)

    # Draw the bricks
    for brick in bricks:
        pygame.draw.rect(screen, BRICKS_COLOR, brick)

    # Update the display
    pygame.display.flip()

    # Calculate the time taken for the frame and introduce a delay to slow down the game
    frame_time = time.time() - start_time
    if frame_time < 0.05:  # Adjust this value to control the game speed
        time.sleep(0.05 - frame_time)

# Quit Pygame
pygame.quit()
# [PORTED TO M1 MAC ON 4.27.24$ 1.0 TEAM FLAMES]
