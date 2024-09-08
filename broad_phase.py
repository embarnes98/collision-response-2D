from narrow_phase import gjk_intersection
from shape import SHAPES


def overlapping_bboxes(shape1, shape2):
    return all((
        shape1.min_x <= shape2.max_x,
        shape2.min_x <= shape1.max_x,
        shape1.min_y <= shape2.max_y,
        shape2.min_y <= shape1.max_y,
    ))


def intersecting_shapes(shape1, shape2):
    if overlapping_bboxes(shape1, shape2):
        return gjk_intersection(shape1, shape2)
    return False


def handle_intersections(shapes):
    for i, shape in enumerate(shapes):
        shape.intersecting = True
        shapes[i].intersecting_neighbours.append(shapes[1-i].id)


def naive_intersection_check(shapes):
    for i, shape in enumerate(shapes):
        # Check for intersections with other shapes
        for other_shape in SHAPES[i+1:]:
            if intersecting_shapes(shape, other_shape):
                handle_intersections((shape, other_shape))
    return shapes


def sort_and_sweep(shapes):
    ordered_shape_pairs = []
    unpaired_shape_ids = set()
    for shape in shapes:
        if shape.id in unpaired_shape_ids: # Handles already paired shapes
            ordered_shape_pairs.append((shape, shape.max_x))
            unpaired_shape_ids.remove(shape.id)
        else:
            ordered_shape_pairs.append((shape, shape.min_x))
            unpaired_shape_ids.add(shape.id)
    for id in unpaired_shape_ids: # Handles not yet paired/ordered shape list
        ordered_shape_pairs.append((SHAPES[id], SHAPES[id].max_x))
    ordered_shape_pairs.sort(key=lambda x: x[1])
    ordered_shape_pairs = [shape for shape, _ in ordered_shape_pairs]
    active_shape_ids = set()
    tested_shape_pairs = set()
    for shape in ordered_shape_pairs:
        if shape.id in active_shape_ids:
            active_shape_ids.remove(shape.id)
            continue
        active_shape_ids.add(shape.id)
        if len(active_shape_ids) >= 2:
            active_shape_id_list = list(active_shape_ids)
            for i, id in enumerate(active_shape_id_list):
                SHAPES[id].x_overlapping = True
                for other_id in active_shape_id_list[i+1:]:
                    shape_pair = (id, other_id)
                    if shape_pair not in tested_shape_pairs:
                        if intersecting_shapes(SHAPES[id], SHAPES[other_id]):
                            handle_intersections((SHAPES[id], SHAPES[other_id]))
                        tested_shape_pairs.add(shape_pair)
    return ordered_shape_pairs
