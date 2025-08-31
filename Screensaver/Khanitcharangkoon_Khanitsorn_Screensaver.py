# Example file showing a basic pygame "game loop"
import pygame
from pygame.draw import circle, polygon
from pygame.math import Vector2
import math
import random

# Window default setting
window_width = 1280
window_height = 720

# pygame setup
pygame.init()
#pygame.mixer.init() # To start music
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Meow! Winter Journey Screen Saver by Khanitsorn')
done = False
clock = pygame.time.Clock()
fps = 60
running = True
position = Vector2(window_width/2, window_height/2)
#pygame.mixer.music.load(r"BGM\winter_magic.wav")
#pygame.mixer.music.play(-1) # Infinity Looping Music
#meow_sound = pygame.mixer.Sound(r"Soundeffect\cat.ogg")

# 1. Snow rows falling
# Circle properties
circle_radius = 10
circle_speed_y = 3
circle_sway_amplitude = 30
circle_sway_speed = 0.02

rows = []
row_spacing = 150   # Distance between rows
row_timer = 0
spawn_delay = 60    # Frames between spawning new row

# Function use to created new role at top of screen
def create_row():
    return {
        "x": 160,
        "y": -circle_radius,  # Start the row offscreen, since if positive, the row may appear suddenly around screen area so it might not look natural.
        "sway_angle": 0
    }

# Function to add the first row of snow
rows.append(create_row())

#-----------#

# 2. Star bouncing
# Star properties
stars = []
num_stars = 20
for i in range(num_stars):
    stars.append({
        "x": random.randint(0, window_width),
        "y": random.randint(0, window_height // 2),
        "vel_x": random.uniform(0.5, 1.5),   # horizontal speed
        "vel_y": random.uniform(0.3, 1.0),   # vertical speed
        "twinkle_phase": random.random() * math.pi * 2
    })

# Function use to draw the star from polygon
def draw_star(surface, x, y, radius, color):
    points = []
    num_points = 5
    for i in range(num_points * 2):
        angle = i * math.pi / num_points
        r = radius if i % 2 == 0 else radius / 2
        px = x + math.cos(angle - math.pi/2) * r
        py = y + math.sin(angle - math.pi/2) * r
        points.append((px, py))
    pygame.draw.polygon(surface, color, points)

#-----------#

# 3. Scrolling background
# Bg properties
bg_image = pygame.image.load(r"Image\bg1.png").convert_alpha() #Replace the path in the blanket with the directory that contain image
bg_width, bg_height = bg_image.get_size()
# For horizontal scroll image use x, if vertical change x to y
bg_x1 = 0
bg_x2 = -bg_width # Negative x cause the scrolling to become left side
bg_speed = 1.5

#-----------#

# 4. Walking cat sprite
cat_sprite = pygame.image.load(r"Image\cat_walking_sprite.png").convert_alpha()
cat_frame_width = cat_sprite.get_width() // 4 # cat walking sprite sheet has 4 frame
cat_frame_height = cat_sprite.get_height()
cat_frames = [cat_sprite.subsurface(pygame.Rect(i * cat_frame_width, 0, cat_frame_width, cat_frame_height)) for i in range(4)]

# Function to tint a sprite
def tint_image(image, color):
    tinted = image.copy()
    tinted.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
    return tinted

# Original cat color frames
cat_frames_original = cat_frames

# Blue cat tinted frames
cat_frames_blue = [tint_image(f, (0, 0, 255, 255)) for f in cat_frames_original]

# Purple cat tinted frames
cat_frames_purple = [tint_image(f, (128, 0, 128, 255)) for f in cat_frames_original]

# Function to switching cat tinted
cat_frame_sets = [cat_frames_original, cat_frames_blue, cat_frames_purple]
current_cat_set_index = 0
last_switch_time = pygame.time.get_ticks()
switch_interval = 3000  # 3 seconds

cat_x = window_width // 2  # cat will start in the middle of screen
cat_y = window_height - cat_frame_height - -40  # cat will walk near the bottom of screen, low number = increase y, higher number = decrease y.
cat_speed = 2
cat_direction = 1   # 1 = right, -1 = left
cat_frame_index = 0
cat_frame_delay = 8
cat_frame_counter = 0
cat_frames = cat_frame_sets[current_cat_set_index]

#Render start here#

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # When press exit button on screen, cause game to quit.
            running = False
        elif event.type == pygame.KEYDOWN: # When press escape button, cause game to quit.
            if event.key == pygame.K_ESCAPE:
                running = False
        #elif event.type == pygame.MOUSEBUTTONDOWN:
            #if event.button == 1:  # When pressing left mouse button, cause cat to meow! (event button number 3 is right mouse button)
                #meow_sound.play()

    screen.fill("midnight blue")

    # 1. Update stars bouncing (Star appear from the back of bg since I put in the first order)
    for star in stars:
        # Star moving controller
        star["x"] += star["vel_x"]
        star["y"] += star["vel_y"]

        # Horizontal bouncing controller
        if star["x"] <= 0:
            star["x"] = 0
            star["vel_x"] *= -1
        elif star["x"] >= window_width:
            star["x"] = window_width
            star["vel_x"] *= -1

        # Vertical bouncing controller
        if star["y"] <= 0:
            star["y"] = 0
            star["vel_y"] *= -1
        elif star["y"] >= window_height / 2: #limit to half since I want the star to only bouncing half of screen.
            star["y"] = window_height / 2
            star["vel_y"] *= -1

        # Twinkle effect controller
        twinkle = (math.sin(star["twinkle_phase"]) + 1) * 0.5
        radius = 2 + twinkle * 2
        star["twinkle_phase"] += 0.05

        # Draw yellow polygon star
        draw_star(screen, int(star["x"]), int(star["y"]), int(radius), "yellow")

    #-----------#
   
    # 2. Update background scrolling (bg appear in middle, since I place in the middle order)
    bg_x1 += bg_speed
    bg_x2 += bg_speed

    # To handle bg image reset when it scrolling off the screen
    if bg_x1 >= window_width:
        bg_x1 = -bg_width
    if bg_x2 >= window_width:
        bg_x2 = -bg_width

    # To draw both bg at the same time
    screen.blit(bg_image, (bg_x1, 0))
    screen.blit(bg_image, (bg_x2, 0))

    #-----------#

    # 3. Update cat color from switch_interval
    current_time = pygame.time.get_ticks()
    if current_time - last_switch_time >= switch_interval:
        last_switch_time = current_time
        current_cat_set_index = (current_cat_set_index + 1) % len(cat_frame_sets)
        cat_frames = cat_frame_sets[current_cat_set_index]

    # 4. Update walking cat (cat will walk and flip with the position of cursor)
    mouse_x, _ = pygame.mouse.get_pos() # To obtain mouse at x axis position

    # Cat move toward mouse controller
    if abs(mouse_x - (cat_x + cat_frame_width / 2)) > cat_speed:
        if mouse_x > cat_x + cat_frame_width / 2:
            cat_x += cat_speed
            cat_direction = 1  # Cat facing right
        else:
            cat_x -= cat_speed
            cat_direction = -1  # Cat facing left

    # Walking Animation controller
    cat_frame_counter += 1
    if cat_frame_counter >= cat_frame_delay:
        cat_frame_counter = 0
        cat_frame_index = (cat_frame_index + 1) % len(cat_frames)

    # Flip controller when cat moving to the left
    current_frame = cat_frames[cat_frame_index]
    if cat_direction == -1:
        current_frame = pygame.transform.flip(current_frame, True, False)

    screen.blit(current_frame, (cat_x, cat_y))

    #-----------#

    # 5. Update snow rows falling (Snow will appear in the upmost front since I put in the last order)
    for row in rows:
        row["y"] += circle_speed_y
        row["sway_angle"] += circle_sway_speed
        sway_offset = math.sin(row["sway_angle"]) * circle_sway_amplitude

        # To draw 7 circles (snow) in the rows
        for i in range(7):
            size = circle_radius + (5 if i % 2 == 1 else 0)  # To control the odd number of circle to increase it size to the number of pixel "normal 5 pixel".
            circle(screen, "snow2", ((row["x"] + 160*i) + sway_offset, row["y"]), size)

    # To remove snow rows that are completely off screen
    rows = [row for row in rows if row["y"] < window_height + circle_radius]

    # To handle spawning new row
    row_timer += 1
    if row_timer >= spawn_delay:
        rows.append(create_row())
        row_timer = 0

    #-----------#


    pygame.display.flip()
    clock.tick(fps)

#pygame.mixer.music.stop() # Use to stop music from playing before quit
pygame.quit()


#Credit for resources
# 1. Suno - BGM
# 2. Kadokawa - Soundeffect