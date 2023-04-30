import pygame
import os
from gameObj import GameObj
import sprite
import random
from tiles import AnimatedTile


class Crate(GameObj):
    def __init__(self, center_xPos, bottom_yPos) -> None:
        xPos = center_xPos - 64/2
        yPos = bottom_yPos - 64 + 2
        self.bottom_yPos = bottom_yPos
        super().__init__(xPos, yPos)
        self.takehit = False
        self.health = 15
        self.state = 'idle'
        self.delete = False
        self.coin_num = int(random.random() * 6)
        self.potion_num = 0
        self.potion = True if random.random() < 0.5 else False
        if self.potion:
            self.potion_num = int(random.random() * 3)

    def getCenterPos(self):
        return (self.rect.x + 64/2 + random.random()*4 - 2, self.rect.y + 64/2 + random.random()*2 - 1)

    def setup(self):
        IDLE_IMAGE = pygame.image.load(
            os.path.join('../images/assets/', 'crate_spritesheet.png')).convert_alpha()

        width = 64
        height = 64
        self.addImg('idle', IDLE_IMAGE, 192,
                    sprite.AnimData(16, pygame.Rect(20, 32, 42-20, 64-32), width, height, 1, []))
        self.addImg('destroy', IDLE_IMAGE, 192,
                    sprite.AnimData(16, pygame.Rect(20, 32, 42-20, 64-32), width, height, 6, []))

        self.changeAnim('idle')

    def getDamaged(self, damage):
        if self.state == 'idle':
            self.health -= damage
            self.takehit = True

    def updateState(self):
        if self.health <= 0 and self.state == 'idle':
            self.state = 'destroy'
            self.changeAnim('destroy')

        if self.state != 'idle' and self.firstAnimated is False:
            self.delete = True

    def update(self, deltaTime: float):
        super().update(deltaTime)
        self.updateState()


class Asset(AnimatedTile):
    def __init__(self, pos, y, size, frames):
        super().__init__(pos, size, frames)
        self.y = y
        self.weight = 1
        self.direct = pygame.Vector2(0, 0)
        self.onGround = False
        self.eaten = False
        self.delete = False

    def getCollideBox(self):
        return pygame.Rect(self.rect.x + self.rect_collide.x, self.rect.y + self.rect_collide.y, self.rect_collide.w, self.rect_collide.h)

    def update(self, deltaTime):
        if self.timer is not None:
            self.timer -= deltaTime
            if self.timer <= 0 or self.eaten:
                self.delete = True
        super().update(deltaTime)

    def updateCor(self):
        self.direct.y += self.weight
        self.rect.x += self.direct.x
        self.rect.y += self.direct.y

    def setOnGround(self, val):
        self.onGround = val

    def isOnGround(self):
        return self.onGround

    def setRectDisplay(self, x, y):
        self.rect.x = x - self.rect_collide.x
        self.rect.y = y - self.rect_collide.y

    def getDirect(self):
        return pygame.Vector2(self.direct.x, self.direct.y)

    def setDirect(self, x, y):
        self.direct.x = x
        self.direct.y = y


class Coin(Asset):
    def __init__(self, pos, y, size, frames):
        super().__init__(pos, y, size, frames)
        self.direct.x = random.random()*4 - 2
        self.direct.y = -5
        self.rect_collide = pygame.Rect(3, 3, 10, 10)
        self.timer = 3
        self.type = 'coin'


class Potion(Asset):
    def __init__(self, pos, y, size, frames):
        super().__init__(pos, y, size, frames)
        self.direct.x = random.random()*4 - 2
        self.direct.y = -5
        self.rect_collide = pygame.Rect(2, 2, 22, 22)
        self.timer = 5
        self.type = 'potion'
        self.heal = 10


class Statue(Asset):
    def __init__(self, center_xPos, bottom_yPos, size, frames) -> None:
        xPos = center_xPos - 112/2
        yPos = bottom_yPos - 224
        super().__init__((xPos, yPos), 0, size, frames)
        self.rect_collide = pygame.Rect(-50, 224-30, 212, 30)
        self.timer = None
        self.weight = 0
        self.type = 'statue'
        self.blessed = False
        self.attack = 2
