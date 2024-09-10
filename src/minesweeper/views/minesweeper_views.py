import pygame, random
from pygame.locals import *

# Dimensions and colors
SIZE = 250, 250
LIGHTGRAY = (198, 198, 198)
GRAY = (192, 192, 192)
BLACK = (132, 132, 132)
RED = (255, 0, 0)
BLUE = (0,0,255)

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Minesweeper')

# Rectangle dimensions
rect_width = 20
rect_height = 20
rect_dist = 2

# Store block positions and their initial color (LIGHTGRAY)
block_positions = []
for i in range(9):
    for j in range(9):
        x = 20 + i * (rect_dist + rect_width)
        y = 20 + j * (rect_dist + rect_height)
        block_positions.append({"rect": pygame.Rect(x, y, rect_width, rect_height), "color": LIGHTGRAY})
        
hidden_blocks = random.sample(block_positions, 10)

# Main loop
running = True
while running:
    # Fill the screen with gray
    screen.fill(GRAY)
    # Draw all rectangles
    for block in block_positions:
        pygame.draw.rect(screen, block["color"], block["rect"], 0)
        pygame.draw.rect(screen, BLACK, block["rect"], 1)
        
    for block in hidden_blocks:
        block["hidden"] = True
        
    # Update the display
    pygame.display.update()
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Mouse click detection
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check if any rectangle was clicked
            for block in block_positions:
                if block["rect"].collidepoint(mouse_pos):
                    # Toggle color between RED and LIGHTGRAY for that rectangle
                    if block["color"] == LIGHTGRAY:
                        block["color"] = RED
                    # Hide some rectangle behind LIGHTGRAY rectangle 
                    if block.get("hidden"):
                        block["color"] = BLUE  

pygame.quit()