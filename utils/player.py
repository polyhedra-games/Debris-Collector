import pygame as pg
from pygame.math import Vector2
from utils.entity import Entity


def get_input():
    keys = pg.key.get_pressed()
    out = []

    if keys[pg.K_SPACE]:
        out.append('space')
    if keys[pg.K_d]:
        out.append('right')
    if keys[pg.K_a]:
        out.append('left')
    if keys[pg.K_w]:
        out.append('up')
    if keys[pg.K_s]:
        out.append('down')

    return out

class Player:

    SPEED = 400
    def __init__(self, pos):
        self.pos = Vector2(pos)

        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

        self.image_open = pg.image.load('Assets/Raw/open.png')
        self.image_open = pg.transform.rotozoom(self.image_open, 0, 0.25)
        self.image_open.set_colorkey('white')

        self.image_shut = pg.image.load('Assets/Raw/shut.png')
        self.image_shut = pg.transform.rotozoom(self.image_shut, 0, 0.25)
        self.image_shut.set_colorkey('white')

        self.rect = self.image_open.get_rect(center=self.pos)
        self.facing = Vector2(1, 0)
        self.target_facing = self.facing.copy()

        self.counter = 0

        self.traila = [] 
        self.trailb = [] 
        self.trailc = [] 

        self.inventory = Entity(Vector2(0, 0))

        self.image = self.image_open

        self.forcefield = pg.Surface((256, 256), pg.SRCALPHA)
        self.forcefield.set_alpha(32)
        self.forcefield.set_colorkey('black')

    def check_collisions(self, obstacle):
        if ((self.pos + self.facing * 61) - obstacle.pos).length() < 64:
            return True
        if (self.pos - obstacle.pos).length() < 80:
             return True
        if ((self.pos - self.facing * 61) - obstacle.pos).length() < 64:
            return True
                
        return False
    
    def update(self, deltatime):
        if self.inventory:
            self.image = self.image_shut
        else:
            self.image = self.image_open

        flag = False
        inp = get_input()

        self.acc = Vector2(0, 0)

        if 'right' in inp:
            self.target_facing = self.target_facing.rotate(90 * deltatime)
        if 'left' in inp:
            self.target_facing = self.target_facing.rotate(-90 * deltatime)
        if 'up' in inp:
            self.acc = self.facing
        if 'down' in inp:
            self.vel = self.vel * 0.99

        self.acc = self.acc.normalize() if self.acc.length() > 0 else self.acc

        self.vel = self.vel.normalize() * Player.SPEED if self.vel.length() > Player.SPEED else self.vel
        self.vel += self.acc * 2000 * deltatime
        self.facing = self.facing.lerp(self.target_facing, 0.05)




        for obstacle in Entity.entities:
            if self.check_collisions(obstacle):
                flag = True
                break

        self.forcefield.fill('black')
        pg.draw.circle(self.forcefield, 'cyan', Vector2(128, 128), 55)
        pg.draw.circle(self.forcefield, 'cyan', Vector2(128, 128) + self.facing * 64, 45)
        pg.draw.circle(self.forcefield, 'cyan', Vector2(128, 128) - self.facing * 64, 45)


        if not flag:
            self.pos += self.vel * deltatime
        else:

            obstacle.vel = (obstacle.pos - self.pos).normalize() * self.vel.length() if self.vel.length() > 100 else (obstacle.pos - self.pos).normalize() * 50



        if self.acc.length() == 0:
            if self.counter > 0.01:
                self.vel = self.vel * 0.99


        self.rect.center = self.pos


        self.counter += deltatime
        if self.counter > 0.02:
            self.traila.append(self.pos.copy() - Vector2(0, 1).rotate(-self.facing.angle_to(Vector2(-1, 0))) * 16 - self.facing * 90)
            self.trailb.append(self.pos.copy() - self.facing * 90)
            self.trailc.append(self.pos.copy() + Vector2(0, 1).rotate(-self.facing.angle_to(Vector2(-1, 0))) * 16 - self.facing * 90)

            self.counter = 0

            
            self.traila = self.traila[-200:]
            self.trailb = self.trailb[-200:]
            self.trailc = self.trailc[-200:]

    def capture_release_entity(self):
        if self.inventory:
            self.inventory.pos = self.pos.copy() + self.facing * 128
            self.inventory.vel = self.facing * 200

            Entity.entities.append(self.inventory)

            self.inventory = None
        else:
            ray = self.pos.copy()
            for i in range(64):
                ray += self.facing * 2
                for entity in Entity.entities.copy():
                    if (ray - entity.pos).length() < 32:
                        Entity.entities.remove(entity)
                        self.inventory = entity
                        break

    def draw_extras(self, screen, offset):
        drawA = [offset(pos) for pos in self.traila]
        
        if len(drawA) >=2:
            pg.draw.lines(screen, "#333333",False, drawA, 3)

        drawB = [offset(pos) for pos in self.trailb]
        
        if len(drawB) >=2:
            pg.draw.lines(screen, "#333333",False, drawB, 3)

        drawC = [offset(pos) for pos in self.trailc]
        
        if len(drawC) >=2:
            pg.draw.lines(screen, "#333333",False, drawC, 3)


        if self.inventory:
            self.inventory.draw_in_inventory(screen, offset(self.pos), self.facing)

        screen.blit(self.forcefield, self.forcefield.get_rect(center=offset(self.pos)))

            



        



