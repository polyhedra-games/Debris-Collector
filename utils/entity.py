import pygame as pg
from pygame.math import Vector2

class Entity:
    entities = []

    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector2(0, 0)

        from random import randint
        self.image = pg.image.load('Assets/Raw/debris-0' + str(randint(1, 2)) + '.png')
        self.image = pg.transform.rotozoom(self.image, randint(-45,45), 0.5)
        del randint

        self.rect = self.image.get_rect(center=self.pos)

        Entity.entities.append(self)

    def update(self, deltatime):
        self.rect.center = self.pos

        self.vel = self.vel * 0.99

        for entity in Entity.entities:
            if entity != self:
                if (self.pos - entity.pos).length() < 32: 
                    entity.vel += (entity.pos - self.pos).normalize() * self.vel.length()
                    self.vel = (self.pos - entity.pos).normalize() * self.vel.length()
                    

        self.pos += self.vel * deltatime


    def draw_in_inventory(self, screen, offset, player_facing):
        image = pg.transform.rotozoom(self.image, 0, 0.5)
        screen.blit(image, image.get_rect(center=(offset + player_facing * 96)))
        

    def draw_extras(self, screen, offset):
        pass

    