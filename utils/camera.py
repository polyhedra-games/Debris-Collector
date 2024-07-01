import pygame as pg
from pygame.math import Vector2

class Camera:
    offset = Vector2(900, 450)

    def __init__(self, screen, target):
        self.screen = screen
        self.target = target
        self.pos = target.pos.copy()


    def update(self, deltatime):
        self.pos += (self.target.pos - self.pos) * 96 * deltatime
        
    def convert_to_screen(self, pos):
        return (pos - self.pos) + Camera.offset
    
    def draw_bg(self):
        offset = Vector2(-self.pos.x % 32, -self.pos.y % 32)
        for i in range(0, 1800, 32):
            for j in range(0, 900, 32):
                pg.draw.circle(self.screen, "#555555", Vector2(i, j) + offset, 1)
    
    def draw(self, entity):
        offset = self.convert_to_screen(entity.pos)
        if -50 < offset.x < 1850 and -50 < offset.y < 950:
            self.screen.blit(entity.image, entity.image.get_rect(center=offset))
            

    def draw_player(self):
        offset = self.convert_to_screen(self.target.pos)
        self.target.draw_extras(self.screen, self.convert_to_screen) 

        img = pg.transform.rotozoom(self.target.image, self.target.facing.angle_to(Vector2(1, 0)) + -90, 1)
        self.screen.blit(img, img.get_rect(center=offset))

    def draw_image(self, image, pos):
        offset = self.convert_to_screen(pos)
        self.screen.blit(image, image.get_rect(center=offset))