"""Utils module."""
from broad_phase import intersecting_shapes


def spawn_shapes(shapes, allow_intersections=False):
    # Initially assume random shape placement has caused intersections
    if allow_intersections:
        for shape in shapes:
            shape.spawn()
        return
    intersections = True 
    while (intersections):
        intersections = False
        for i, shape in enumerate(shapes):
            # Update shape's starting position/velocity
            shape.spawn()
            for other_shape in shapes[i+1:]:
                while (intersecting_shapes(shape, other_shape)):
                    intersections = True
                    # Reset the shape's starting data until it no longer
                    # intersects its neighbour
                    shape.spawn()

