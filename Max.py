import pygame
import random
from math import sin
import socket
import json
import select
from maxnet import Network  # Import the Network class from maxnet.py

pygame.init()

size = width, height = 1920, 1080
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

clock = pygame.time.Clock()

background_image = pygame.image.load('images/maxbg.png')
max_face_image = pygame.image.load('images/maxhead.png').convert_alpha()
max_jaw_image = pygame.image.load('images/maxjaw.png').convert_alpha()
left_eye_image = pygame.image.load('images/maxeye1.png').convert_alpha()
right_eye_image = pygame.image.load('images/maxeye2.png').convert_alpha()

MAX_FACE_START_POS = (897, 704)
MAX_JAW_START_POS = (878, 528)
LEFT_EYE_START_POS = (824, 350)
RIGHT_EYE_START_POS = (951, 357)
DEFAULT_IMAGE_SIZE = (2500, 2500)
background = pygame.transform.scale(background_image, DEFAULT_IMAGE_SIZE)
rotated_background = background.copy()

class MaxSprite(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)

left_eye_sprite = MaxSprite(LEFT_EYE_START_POS, left_eye_image)
right_eye_sprite = MaxSprite(RIGHT_EYE_START_POS, right_eye_image)
max_face_sprite = MaxSprite(MAX_FACE_START_POS, max_face_image)
max_jaw_sprite = MaxSprite(MAX_JAW_START_POS, max_jaw_image)

all_sprites_group = pygame.sprite.Group()
all_sprites_group.add(left_eye_sprite)
all_sprites_group.add(right_eye_sprite)
all_sprites_group.add(max_face_sprite)
all_sprites_group.add(max_jaw_sprite)

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

bg_start_position = [-300, -500]
jaw_y_offset = 0
jaw_move_speed = 2  # Adjust this speed as needed
jaw_start_y = max_jaw_sprite.rect.y  # Store the initial position
right_eye_start_x = right_eye_sprite.rect.x
left_eye_start_x = left_eye_sprite.rect.x

running = True
angle = 0
current_bg_speed = 0.1
jaw_speed = 0
eye_angle_x = 0
eye_angle_y = 0
eye_triangulation_distance = 100 
eye_distance_apart = 1
ideal_bg_speed = 1
# Initialize the network
net = Network()
current_bg_offset_x = 0
current_bg_offset_y = 0
ideal_bg_offset_x = -200
ideal_bg_offset_y = -200
bg_position = [bg_start_position[0], bg_start_position[1]]

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            running = False
        if event.type == pygame.QUIT:
            running = False

    # Use the Network class to send and receive data
    received_numbers = net.receive_numbers()
    if received_numbers:
        # Process received numbers here
        jaw_speed = received_numbers[1]
        eye_angle_x = received_numbers[2]
        eye_angle_y = received_numbers[3]
        eye_triangulation_distance = received_numbers[4]
        pass

    if random.randint(1, 100) == 1:
        ideal_bg_speed = .1 * random.randint(-10, 10)
        jaw_speed = random.randint(0,1) * 2
        eye_angle_x = random.randint(-45,45)
        eye_angle_y = random.randint(-20,20)
    if random.randint(1, 100) == 1:
        ideal_bg_offset_x = random.randint(-400,400)
        ideal_bg_offset_y = random.randint(-400,400)

    if jaw_speed > 0:
        jaw_y_offset += jaw_move_speed
        if jaw_y_offset > 10:
            jaw_move_speed = -jaw_move_speed
        elif jaw_y_offset < 0:
            jaw_move_speed = -jaw_move_speed
    else:
        if jaw_y_offset != -2:
            jaw_y_offset = -2
            jaw_move_speed = abs(jaw_move_speed)
    current_bg_offset_x = (current_bg_offset_x * 99 + ideal_bg_offset_x) * .01
    current_bg_offset_y = (current_bg_offset_y * 99 + ideal_bg_offset_y) * .01
    current_bg_speed = (current_bg_speed * 19 + ideal_bg_speed) * .05
    angle += current_bg_speed
    if angle > 360:
        angle -= 360

    rotated_background = rot_center(background, angle)
    max_jaw_sprite.rect.y = jaw_start_y + jaw_y_offset  # Apply offset to the initial position
    right_eye_sprite.rect.x = right_eye_start_x + (10 * sin(eye_angle_x))
    left_eye_sprite.rect.x = left_eye_start_x + (10 * sin(eye_angle_x))
    all_sprites_group.update()

    bg_position[0] = bg_start_position[0] + current_bg_offset_y
    bg_position[1] = bg_start_position[1] + current_bg_offset_x
    #screen.fill((0, 0, 0))
    screen.blit(rotated_background, bg_position)
    all_sprites_group.draw(screen)

    pygame.display.flip()
    clock.tick(30)

# Properly close the client socket before exiting
if client_socket:
    client_socket.close()

server_socket.close()
pygame.quit()
