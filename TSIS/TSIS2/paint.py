import pygame
import sys
from tools import *

pygame.init()

WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont("Arial", 20)
text_font = pygame.font.SysFont("Arial", 28)

colors = [(0,0,0),(255,0,0),(0,180,0),(0,0,255),(255,220,0),(255,255,255)]

current_color = (0,0,0)
brush_size = 5
tool = "pencil"

drawing = False
start_pos = None
last_pos = None

typing = False
text_position = None
current_text = ""


# ---------------------------------------------------------
# Draw toolbar UI
# ---------------------------------------------------------
def draw_toolbar():
    pygame.draw.rect(screen, (220,220,220), (0,0,WIDTH,TOOLBAR_HEIGHT))

    tools_list = ["pencil","line","rect","circle","square",
                  "right_tri","eq_tri","rhombus","eraser","fill","text"]

    x = 10

    for t in tools_list:
        rect = pygame.Rect(x,10,80,30)

        if tool == t:
            pygame.draw.rect(screen, (180,180,180), rect)
        else:
            pygame.draw.rect(screen, (255,255,255), rect)

        pygame.draw.rect(screen, (0,0,0), rect, 1)

        label = font.render(t, True, (0,0,0))
        screen.blit(label,(x+5,15))

        x += 85

    # colors
    x = 10
    for c in colors:
        rect = pygame.Rect(x,50,30,30)
        pygame.draw.rect(screen,c,rect)
        pygame.draw.rect(screen,(0,0,0),rect,2)
        x += 40
def handle_toolbar_click(pos):
    global tool, current_color

    tools_list = [
        "pencil","line","rect","circle","square",
        "right_tri","eq_tri","rhombus","eraser","fill","text"
    ]

    x = 10

    # Check tool buttons
    for t in tools_list:
        rect = pygame.Rect(x, 10, 80, 30)

        if rect.collidepoint(pos):
            tool = t
            print(f"Tool changed to: {tool}")
            return

        x += 85

    # Check color buttons
    x = 10
    y = 50

    for c in colors:
        rect = pygame.Rect(x, y, 30, 30)

        if rect.collidepoint(pos):
            current_color = c
            print(f"Color changed")
            return

        x += 40

# ---------------------------------------------------------
# Main loop
# ---------------------------------------------------------
clock = pygame.time.Clock()

while True:
    screen.fill((255,255,255))
    screen.blit(canvas,(0,TOOLBAR_HEIGHT))
    draw_toolbar()

    #save png
    
    # Preview shapes
    if drawing and start_pos and last_pos:
        preview = canvas.copy()
        draw_shape(preview, tool, start_pos, last_pos, current_color, brush_size)
        screen.blit(preview,(0,TOOLBAR_HEIGHT))

    # Text preview
    if typing:
        txt = text_font.render(current_text, True, current_color)
        screen.blit(txt,(text_position[0], text_position[1]+TOOLBAR_HEIGHT))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                brush_size += 1   # scroll up → bigger
            elif event.y < 0:
                brush_size -= 1   # scroll down → smaller

            # limit size (important)
            brush_size = max(1, min(brush_size, 50))

            print("Brush size:", brush_size)

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            ctrl_pressed = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
            cmd_pressed = keys[pygame.K_LMETA] or keys[pygame.K_RMETA]

            if (ctrl_pressed or cmd_pressed) and event.key == pygame.K_s:
                save_canvas(canvas)

            # Brush size
            if event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            # Text input
            if typing:
                if event.key == pygame.K_RETURN:
                    canvas.blit(text_font.render(current_text, True, current_color), text_position)
                    typing = False
                    current_text = ""

                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    current_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    current_text = current_text[:-1]

                else:
                    current_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:

            # If click is on toolbar → change tool
            if event.pos[1] < TOOLBAR_HEIGHT:
                handle_toolbar_click(event.pos)
                continue
            if inside_canvas(event.pos, TOOLBAR_HEIGHT):

                pos = to_canvas_pos(event.pos, TOOLBAR_HEIGHT)

                if tool == "fill":
                    flood_fill(canvas, pos, current_color)

                elif tool == "text":
                    typing = True
                    text_position = pos
                    current_text = ""

                else:
                    drawing = True
                    start_pos = pos
                    last_pos = pos

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                pos = to_canvas_pos(event.pos, TOOLBAR_HEIGHT)

                if tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, (255,255,255), last_pos, pos, brush_size)
                    last_pos = pos

                else:
                    last_pos = pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end = to_canvas_pos(event.pos, TOOLBAR_HEIGHT)

                draw_shape(canvas, tool, start_pos, end, current_color, brush_size)

                drawing = False

    pygame.display.flip()
    clock.tick(60)