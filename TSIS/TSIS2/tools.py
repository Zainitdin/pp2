import pygame
from collections import deque
from datetime import datetime


# ---------------------------------------------------------
# Convert screen position → canvas position
# ---------------------------------------------------------
def to_canvas_pos(pos, toolbar_height):
    x, y = pos
    return x, y - toolbar_height


# ---------------------------------------------------------
# Check if mouse inside canvas
# ---------------------------------------------------------
def inside_canvas(pos, toolbar_height):
    return pos[1] >= toolbar_height


# ---------------------------------------------------------
# Flood Fill Tool
# BFS algorithm (queue-based)
# ---------------------------------------------------------
def flood_fill(surface, start, fill_color):
    width, height = surface.get_size()
    x, y = start

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))

    if target_color == fill_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))


# ---------------------------------------------------------
# Save canvas with timestamp
# ---------------------------------------------------------
def save_canvas(canvas):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paint_{timestamp}.png"
    pygame.image.save(canvas, filename)
    print(f"Saved: {filename}")

#
# Save canvas as png
#
def handle_save_shortcut(event, canvas):
    """
    Handles saving the canvas when user presses:
    - Ctrl + S (Windows/Linux)
    - Command + S (Mac)

    Parameters:
    event  -> pygame event
    canvas -> surface to save
    """

    # Only react to key press events
    if event.type != pygame.KEYDOWN:
        return

    # Get current keyboard state
    keys = pygame.key.get_pressed()

    # Check if Control is pressed (Windows/Linux)
    ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]

    # Check if Command (Meta) is pressed (Mac)
    cmd_pressed = keys[pygame.K_LMETA] or keys[pygame.K_RMETA]

    # If Ctrl+S OR Command+S → save
    if (ctrl_pressed or cmd_pressed) and event.key == pygame.K_s:
        save_canvas(canvas)

# ---------------------------------------------------------
# Draw all shapes (used for preview + final draw)
# ---------------------------------------------------------
def draw_shape(surface, shape, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    rect = pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )

    if shape == "line":
        pygame.draw.line(surface, color, start, end, width)

    elif shape == "rect":
        pygame.draw.rect(surface, color, rect, width)

    elif shape == "circle":
        radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
        pygame.draw.circle(surface, color, start, radius, width)

    elif shape == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(surface, color, (x1, y1, side, side), width)

    elif shape == "right_tri":
        pygame.draw.polygon(surface, color, [(x1, y1), (x1, y2), (x2, y2)], width)

    elif shape == "eq_tri":
        pygame.draw.polygon(surface, color, [
            ((x1 + x2) // 2, y1),
            (x1, y2),
            (x2, y2)
        ], width)

    elif shape == "rhombus":
        pygame.draw.polygon(surface, color, [
            ((x1 + x2) // 2, y1),
            (x2, (y1 + y2) // 2),
            ((x1 + x2) // 2, y2),
            (x1, (y1 + y2) // 2)
        ], width)