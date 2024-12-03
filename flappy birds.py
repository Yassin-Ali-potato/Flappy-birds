import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -6
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_VELOCITY = 4
BIRD_WIDTH = 40
BIRD_HEIGHT = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 191, 255)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load bird image
bird_image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
bird_image.fill(RED)

# Clock to control game speed
clock = pygame.time.Clock()

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def move(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)

    def move(self):
        self.x -= PIPE_VELOCITY
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

# Main game loop
def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Move bird and pipes
        bird.move()
        for pipe in pipes:
            pipe.move()

        # Check for pipe collisions
        for pipe in pipes:
            if bird.y < 0 or bird.y + BIRD_HEIGHT > SCREEN_HEIGHT:
                running = False  # Bird hit the ground or the ceiling
            if pipe.top_rect.colliderect(pygame.Rect(bird.x, bird.y, BIRD_WIDTH, BIRD_HEIGHT)) or \
               pipe.bottom_rect.colliderect(pygame.Rect(bird.x, bird.y, BIRD_WIDTH, BIRD_HEIGHT)):
                running = False  # Bird hit a pipe

        # Add new pipes
        if pipes[-1].x < SCREEN_WIDTH - 300:
            pipes.append(Pipe())

        # Remove pipes that are off the screen
        if pipes[0].x < -PIPE_WIDTH:
            pipes.pop(0)
            score += 1  # Increment score when a pipe is passed

        # Draw everything
        screen.fill(BLUE)
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        # Draw the score
        font = pygame.font.SysFont("Arial", 32)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Control the game frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
