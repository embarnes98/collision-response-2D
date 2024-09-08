import pygame
from pygame.math import Vector2

from broad_phase import (
    naive_intersection_check, sort_and_sweep
)
from colours import *
from mechanics import resolve_intersections
from shape import SHAPES, WIDTH, HEIGHT
from ui import display_data
from utils import spawn_shapes


SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
CORNERS = [
    Vector2(0, 0),
    Vector2(0, HEIGHT - 1),
    Vector2(WIDTH - 1, HEIGHT - 1),
    Vector2(WIDTH - 1, 0),
]

def main():
    # Create shapes with initial positions and velocities
    
    shapes_to_check = SHAPES
    for shape in shapes_to_check:
        print(shape.id)
    spawn_shapes(SHAPES)

    # Initialize Pygame
    pygame.init()

    # Main loop
    intersection_check = sort_and_sweep
    simulating = True
    draw_bbox = False
    draw_x_bounds = False
    while True:
        # Measure the time elapsed since the last frame (in seconds)
        # 60 frames per second, converted to seconds
        delta_time = CLOCK.tick(60) / 1000.0 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    intersection_check = naive_intersection_check
                    shapes_to_check = SHAPES
                elif event.key == pygame.K_2:
                    intersection_check = sort_and_sweep
                elif event.key == pygame.K_x:
                    draw_x_bounds = not draw_x_bounds
                elif event.key == pygame.K_b:
                    draw_bbox = not draw_bbox
                else:
                    simulating = not simulating
            elif event.type == pygame.QUIT:
                pygame.quit()
        if not simulating:
            continue
        # Clear the screen
        SCREEN.fill((0, 0, 0))
        # Render the text with a yellow color (R, G, B)
        display_data(
            [str(int(CLOCK.get_fps())), intersection_check.__name__], SCREEN
        )
        for shape in SHAPES:
            shape.draw(SCREEN, draw_bbox, draw_x_bounds)
            shape.move(delta_time)
            shape.intersecting = False
            shape.intersecting_neighbours = []
            shape.x_overlapping = False
        shapes_to_check = intersection_check(shapes_to_check)

        # Draw border
        pygame.draw.polygon(SCREEN, GREEN, CORNERS, width=1)
        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    main()
