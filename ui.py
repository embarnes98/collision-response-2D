"""UI module."""
from pygame.font import Font


def get_fps_text(clock):
    # Get the FPS from the clock
    fps = str(int(clock.get_fps()))
    # Render the text with a yellow color (R, G, B)
    return Font(None, 36).render(fps, True, (255, 255, 0))


def display_data(data, screen):
    for i, datum in enumerate(data):
        font = Font(None, 36).render(datum, True, (255, 255, 0))
        screen.blit(font, (10, 10 + 25 * i))
