"""Module implementing the Shape class."""
import pygame
from pygame.math import Vector2
from random import randint

from colours import *


WIDTH = 800
HEIGHT = 600
MAX_SPAWN_SPEED = 600
BARRIER_TOLERANCE = 1


class Shape:
    def __init__(self, vertices, color, id=-1):
        self.vertices = [Vector2(v) for v in vertices]
        self.color = color
        self.id = id
        self.velocity = Vector2(0, 0)
        self.intersecting = False
        self.x_overlapping = False
        self.centroid = Vector2(
            sum(v[0] for v in vertices) / len(vertices),
            sum(v[1] for v in vertices) / len(vertices),
        )
        self.calculate_bounds()
        self.wall_intersection_count = 0
        self.intersecting_neighbours = []
        self.cooldown = 0

    def displace(self, displacement):
        self.vertices = [v + displacement for v in self.vertices]
        self.centroid += displacement

    def support(self, d):
        """Return the vertex of the shape furthest in the given direction."""
        return max(self.vertices, key=lambda v: v.dot(d))

    def calculate_bounds(self):
        self.min_x = int(self.support(Vector2(-1, 0)).x)
        self.min_y = int(self.support(Vector2(0, -1)).y)
        self.max_x = int(self.support(Vector2(1, 0)).x)
        self.max_y = int(self.support(Vector2(0, 1)).y)
        self.bounding_box = [
            Vector2(self.min_x, self.max_y),
            Vector2(self.min_x, self.min_y),
            Vector2(self.max_x, self.min_y),
            Vector2(self.max_x, self.max_y),
        ]

    def wall_hit(self):
        return any([
            self.min_x <= BARRIER_TOLERANCE,
            self.max_x >= WIDTH - 1 - BARRIER_TOLERANCE,
        ])

    def floor_hit(self):
        return any([
            self.min_y <= BARRIER_TOLERANCE,
            self.max_y >= HEIGHT - 1 - BARRIER_TOLERANCE,
        ])

    def move(self, delta_time):
        """Update the shape's position and rotation based on velocity and time.
        Ensure it bounces off the screen edges.
        """
        # Check for intersection with screen edges
        barrier_hit = False
        bounce = 1
        if self.wall_hit():
            self.velocity.x = -self.velocity.x
            barrier_hit = True
        if self.floor_hit():
            self.velocity.y = -self.velocity.y
            barrier_hit = True
        if barrier_hit:
            self.wall_intersection_count += 1
            if self.wall_intersection_count > 1:
                self.spawn()
                return
            else:
                bounce = 1.1
        else:
            self.wall_intersection_count = 0
        displacement = Vector2(self.velocity.x, self.velocity.y) * delta_time
        self.displace(displacement * bounce)
        self.calculate_bounds()

    def spawn(self):
        self.calculate_bounds()
        spawn_clearance = 0
        self.displace(Vector2(
            randint(
                -self.min_x + BARRIER_TOLERANCE + spawn_clearance,
                WIDTH - 1 - self.max_x - BARRIER_TOLERANCE - spawn_clearance,
            ),
            randint(
                -self.min_y + BARRIER_TOLERANCE + spawn_clearance,
                HEIGHT - 1 - self.max_y - BARRIER_TOLERANCE - spawn_clearance,
            ),       
        ))
        self.calculate_bounds()
        print("{}: {}".format(self.color, self.bounding_box))
        assert(not (self.wall_hit() or self.floor_hit()))
        self.velocity = Vector2(
            randint(-MAX_SPAWN_SPEED, MAX_SPAWN_SPEED),
            randint(-MAX_SPAWN_SPEED, MAX_SPAWN_SPEED),
        )

    def draw(self, surface, draw_bbox, draw_x_bounds):
        """Draw the shape on the surface."""
        # Draw main shape
        if self.intersecting:
            color = WHITE
        elif self.x_overlapping and draw_x_bounds:
            color = PINK
        else:
            color = self.color
        pygame.draw.polygon(surface, color, self.vertices)
        if draw_bbox:
            pygame.draw.polygon(surface, GREEN, self.bounding_box, width=1)
        if draw_x_bounds:
            for bound in (self.min_x, self.max_x):
                pygame.draw.line(surface, GREEN, (bound, 0), (bound, HEIGHT))
        for id in self.intersecting_neighbours:
            neighbour_centroid = SHAPES[id].centroid
            pygame.draw.line(surface, GREEN, self.centroid, neighbour_centroid, 5)


PARALLELOGRAM = [(0, 0), (100, 0), (150, 100), (50, 100)]
OBLONG = [(0, 0), (200, 0), (200, 50), (0, 50)]
TRIANGLE = [(0, 0), (100, 0), (50, 100)]
PENTAGON = [(0, 50), (50, 0), (100, 50), (80, 100), (20, 100)]
SHAPES = [
    Shape(PARALLELOGRAM, RED, 0),
    Shape(OBLONG, PURPLE, 1),
    Shape(TRIANGLE, BLUE, 2),
    Shape(PENTAGON, YELLOW, 3),
]
