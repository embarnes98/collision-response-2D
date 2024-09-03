"""Module implementing the Shape class."""
import pygame
from pygame.math import Vector2
from random import randint

from colours import RED, GREEN, BLUE, YELLOW, WHITE


WIDTH = 800
HEIGHT = 600


class Shape:
    def __init__(self, vertices, color, velocity=Vector2(0, 0)):
        self.vertices = [Vector2(v) for v in vertices]
        self.velocity = Vector2(velocity)
        self.colliding = False
        self.centroid = Vector2(
            sum(v[0] for v in vertices) / len(vertices),
            sum(v[1] for v in vertices) / len(vertices),
        )
        self.calculate_extremities()
        self.color = color

    def displace(self, displacement):
        self.vertices = [v + displacement for v in self.vertices]
        self.centroid += displacement

    def support(self, d):
        """Return the vertex of the shape furthest in the given direction."""
        return max(self.vertices, key=lambda v: v.dot(d))
    
    def calculate_extremities(self):
        self.min_x = self.support(Vector2(-1, 0))
        self.min_y = self.support(Vector2(0, -1))
        self.max_x = self.support(Vector2(1, 0))
        self.max_y = self.support(Vector2(0, 1))

    def wall_hit(self):
        return self.min_x.x <= 0 or self.max_x.x >= WIDTH
    
    def floor_hit(self):
        return self.min_y.y <= 0 or self.max_y.y >= HEIGHT

    def move(self, delta_time):
        """Update the shape's position and rotation based on velocity and time.
        Ensure it bounces off the screen edges.
        """
        self.calculate_extremities()
        # Check for collision with screen edges
        if self.wall_hit():
            self.velocity.x = -self.velocity.x
        if self.floor_hit():
            self.velocity.y = -self.velocity.y
        self.displace(
            Vector2(int(self.velocity.x), int(self.velocity.y)) * delta_time
        )

    def spawn(self):
        self.displace(Vector2(
            randint(-self.min_x.x + 1, WIDTH - self.max_x.x - 1),
            randint(-self.min_y.y + 1, HEIGHT - self.max_y.y - 1),       
        ))
        self.velocity = Vector2(randint(-500, 500), randint(-500, 500))
        self.calculate_extremities()

    def draw(self, surface, color=None):
        """Draw the shape on the surface."""
        # Draw main shape
        color = WHITE if self.colliding else self.color
        pygame.draw.polygon(surface, color, self.vertices)
        # Draw dots at minima/maxima
        pygame.draw.circle(surface, WHITE, self.min_x, 2)
        pygame.draw.circle(surface, WHITE, self.min_y, 2)
        pygame.draw.circle(surface, WHITE, self.max_x, 2)
        pygame.draw.circle(surface, WHITE, self.max_y, 2)