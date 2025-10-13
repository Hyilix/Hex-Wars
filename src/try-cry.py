import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def hexagon_points(center, radius):
    x, y = center
    return [(x + radius * math.cos(math.pi/3 * i),
             y + radius * math.sin(math.pi/3 * i))
            for i in range(6)]

def point_in_hexagon(point, hex_points):
    x, y = point
    n = len(hex_points)
    inside = False
    px, py = hex_points[0]
    for i in range(n+1):
        qx, qy = hex_points[i % n]
        if ((qy > y) != (py > y)) and (x < (px - qx) * (y - qy) / (py - qy) + qx):
            inside = not inside
        px, py = qx, qy
    return inside

def generate_hex_centers(rows, cols, start_x=100, start_y=100, radius=30):
    centers = []
    hex_height = math.sqrt(3) * radius
    hex_width = 2 * radius
    horiz_spacing = 3/4 * hex_width
    vert_spacing = hex_height
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * horiz_spacing
            y = start_y + row * vert_spacing + (col % 2) * (hex_height / 2)
            centers.append((x, y))
    return centers

# === BOARD SETUP ===
radius = 30
centers = generate_hex_centers(5, 6, 100, 100, radius)
hex_colors = [(80, 80, 120) for _ in centers]

# === MAIN LOOP ===
running = True
while running:
    screen.fill((25, 25, 35))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, c in enumerate(centers):
                if point_in_hexagon(event.pos, hexagon_points(c, radius)):
                    print(f"Clicked hex {i}")
                    hex_colors[i] = (200, 80, 80)

    # Draw the grid
    for i, c in enumerate(centers):
        pygame.draw.polygon(screen, hex_colors[i], hexagon_points(c, radius))
        pygame.draw.polygon(screen, (0, 0, 0), hexagon_points(c, radius), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
