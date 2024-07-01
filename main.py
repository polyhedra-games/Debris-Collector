import pygame as pg
import sys
from pygame.math import Vector2
import random
from time import time

import utils

pg.init()
screen = pg.display.set_mode((1800, 900), pg.DOUBLEBUF)
clock = pg.time.Clock()
player = utils.Player(Vector2(4000, 3000))
camera = utils.Camera(screen, player)

for i in range(60):
    utils.Entity(Vector2(random.randint(-1000, 1000), random.randint(-1000, 1000)))




deltatime = 1/60

font = pg.font.Font('Assets/Fonts/Mono.ttf', 24)

def display_fps():
    fps = font.render(str(1/deltatime), True, 'white')
    screen.blit(fps, (50, 50))

while True:
    prevtime = time()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.capture_release_entity()

    screen.fill("#2B2B2B")
    camera.draw_bg()


    camera.draw_player()
    player.update(deltatime)
    camera.update(deltatime)


    for entity in utils.Entity.entities:
        camera.draw(entity)
        entity.update(deltatime)

    display_fps()

    pg.display.flip()

    deltatime = time() - prevtime 
    

   