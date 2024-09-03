import pygame
import time

from colours import RED, GREEN, BLUE, YELLOW
from shape import Shape, WIDTH, HEIGHT
from gjk import gjk_collision
from vertices import PARALLELOGRAM, OBLONG, TRIANGLE, PENTAGON


SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

def main():
    # Create shapes with initial positions and velocities
    shapes = [
        Shape(PARALLELOGRAM, RED),
        Shape(OBLONG, GREEN),
        Shape(TRIANGLE, BLUE),
        Shape(PENTAGON, YELLOW),
    ]
    #return
    collisions = True
    while (collisions):
        collisions = False
        for i, shape in enumerate(shapes):
            shape.spawn()
            for other_shape in shapes[i+1:]:
                while (gjk_collision(shape, other_shape)):
                    collisions = True
                    shape.spawn()

    # Initialize Pygame
    pygame.init()

    # Main loop
    running = True
    while running:
        start_time = time.time()

        # Measure the time elapsed since the last frame (in seconds)
        # 60 frames per second, converted to seconds
        delta_time = CLOCK.tick(60) / 1000.0 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        SCREEN.fill((0, 0, 0))
        
        for shape in shapes:
            shape.colliding = False
        # Update each shape
        for i, shape in enumerate(shapes):
            shape.move(delta_time)
            # Check for collisions with other shapes
            for other_shape in shapes[i+1:]:
                if not shape.colliding:
                    shapes_colliding = gjk_collision(shape, other_shape)
                    shape.colliding |= shapes_colliding
                    other_shape.colliding |= shapes_colliding
            shape.draw(SCREEN)
        # Update the display
        pygame.display.flip()

        # Timeout check: if the cycle took longer than 0.1 seconds, break the loop
        if time.time() - start_time > 0.1:
            print("Cycle taking too long, exiting...")
            running = False

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
