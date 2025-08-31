import pygame
import random
from pygame.draw import circle, rect
from pygame.math import Vector2

# pygame setup
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

redColor = [255, 0, 0]
greenColor = [0, 255, 0]
blackColor = [0, 0, 0]
condition = 1

# Circle varibles
circles = []
circle_color = [128,0,128]
circle_redius = 50
circle_position = Vector2(circle_redius, circle_redius)
circle_scale = 0.125
circle_vec = Vector2(0, 0)

circle_acc = Vector2(0, 0)
circle_acc.x = 3
circle_acc.y = 3

# Rectengle varibles
rect_color = [0,0,0]
rect_width = 50
rect_height = 50
rect_tran = [0, 0, rect_width, rect_height]


# Functions
def negetive(number):
    number = number * (-1)
    return number

def positive(number):
    number = (number ** 2) ** 0.5
    return number

def random_color(color):
    color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    return color

def random_position(redius):
    position = (random.randint(int(redius), int(screen_width - redius)), random.randint(int(redius), int(screen_height - redius)))
    return position

def add_circles(color, position, redius):
    circles.append([color, position, redius])

def display_circles():
    for cir in circles:
        circle(screen, cir[0], cir[1], cir[2])

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    """ Begin Circle """

    # make circle move
    circle_vec = circle_vec + circle_acc
    circle_position += circle_vec
    circle_redius = circle_redius + circle_scale

    # make circle
    display_circles() # draw all circle in pools

    circle(screen, circle_color, circle_position, circle_redius)

    # check if circle hit screen X position
    if circle_position.x >= screen_width - circle_redius or circle_position.x <= circle_redius:
        circle_vec.x = negetive(circle_vec.x)
        circle_color = random_color(circle_color)
        circle_scale = circle_scale * -1
        add_circles(circle_color, random_position(circle_redius), circle_redius) # add circle to pools

    # check if circle hit screen Y position
    if circle_position.y >= screen_height - circle_redius or circle_position.y <= circle_redius:
        circle_vec.y = negetive(circle_vec.y)
        circle_color = random_color(circle_color)
        circle_scale = circle_scale * -1
        add_circles(circle_color, random_position(circle_redius), circle_redius) # add circle to pools

    # one time acceleration
    circle_acc.x, circle_acc.y = 0, 0

    """ Begin Rectangle """

    rect_color = greenColor

    # get mouse position and set rectangle position
    mouse_pos = pygame.mouse.get_pos()
    rect_posX = mouse_pos[0] - (rect_width // 2)
    rect_posY = mouse_pos[1] - (rect_height // 2)

    # check if rectangle hit screen X position
    if rect_posX >= screen_width - rect_width:
        rect_posX = screen_width - rect_width
        rect_color = redColor
    elif rect_posX <= 0:
        rect_posX = 0
        rect_color = redColor

    # check if rectangle hit screen Y position
    if rect_posY >= screen_height - rect_height:
        rect_posY = screen_height - rect_height
        rect_color = redColor
    elif rect_posY <= 0:
        rect_posY = 0
        rect_color = redColor
    
    # create rectangle
    rect_tran = [rect_posX, rect_posY, rect_width, rect_height]

    rect(screen, rect_color, rect_tran)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()