"""Utils module."""

def resolve_collision(body1, body2):
    """ Resolve the collision by separating the shapes. """
    separation_vector = (body1.velocity - body2.velocity).normalize() * 5
    body1.vertices = [v + separation_vector for v in body1.vertices]
    body2.vertices = [v - separation_vector for v in body2.vertices]
    body1.velocity = -body1.velocity
    body2.velocity = -body2.velocity