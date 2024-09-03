"""Module implementing the GJK algortithm."""
from pygame.math import Vector2


def triple_product_2d(a, b, c):
    """Calculates the triple product of three vectors (which are 2D, meaning
        z-components are set to zero and their products exluded here).
    
    Args:
        a (pygame.Math.Vector2): vector a.
        b (pygame.Math.Vector2): vector b.
        c (pygame.Math.Vector2): vector c.

    Returns:
        pygame.Math.Vector2: the vector triple product of the incoming 2D
            vectors.
    """
    return Vector2(a.y * (b.x * c.y - b.y * c.x), a.x * (b.y * c.x - b.x * c.y))


def line_case(simplex):
    """Calculates the next search direction for a simplex of two points.

    Args:
        simplex (list [pygame.Math.Vector2]): simplex two points across the two
            shapes being checked for intersection.

    Returns:
        tuple (bool, pygame.Math.Vector2): False (a simplex of fewer than three
            points cannot possibly contain the origin), and the next search
            direction.
    """
    B, A = simplex
    AB = B - A
    AO = -A
    ABperp = triple_product_2d(AB, AO, AB)
    return False, ABperp


def triangle_case(simplex):
    """Calculates whether the current 3-point simplex represents a collision,
    and if not, the next search direction.

    Args:
        simplex (list [pygame.Math.Vector2]): list of three points on two shapes
            being checked for intersection.

    Returns:
        tuple (bool, pygame.Math.Vector2): Whether a collision has been
            detected. Return also the next search direction if a collision was
            not detected, otherwise None.
    """
    C, B, A = simplex
    AB = B - A
    AC = C - A
    AO = -A
    ABperp = triple_product_2d(AC, AB, AB)
    if ABperp.dot(AO) > 0:
        del simplex[0]
        return False, ABperp
    else:
        ACperp = triple_product_2d(AB, AC, AC)
        if ACperp.dot(AO) > 0:
            del simplex[1]
            return False, ACperp
        else:
            return True, None  # Collision detected


def handle_simplex(simplex):
    """Returns whether the current simplex represents a collision, and if not,
        the next search direction.

    Args:
        simplex (list [pygame.Math.Vector2]): list of points on two shapes
            being checked for intersection.

    Returns:
        tuple (bool, pygame.Math.Vector2): The line simplex result if the
            simplex consists of two points, else the triangle simplex result.
    """
    if len(simplex) == 2:
        return line_case(simplex)
    return triangle_case(simplex)


def gjk_collision(body1, body2):
    """Implementation of the GJK algorithm to detect collision between two
    convex bodies.

    Args:
        body1 (Body): first body tested for intersection.
        body2 (Body): second body tested for intersection.
    Returns:
        bool: whether the two bodies are intersecting.
    """
    dir = Vector2.normalize(
        body2.centroid - body1.centroid
    ) # Initial arbitrary direction
    simplex = [body1.support(dir) - body2.support(-dir)]
    dir = -simplex[0]  # New direction is towards the origin
    while True:
        A = body1.support(dir) - body2.support(-dir)
        if A.dot(dir) < 0:
            return False  # No collision
        simplex.append(A)
        # Handle the simplex
        handled_simplex, dir = handle_simplex(simplex)
        if handled_simplex:
            return True
