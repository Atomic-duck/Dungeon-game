import pygame
import sprite
from abc import ABC


class GameObj(sprite.AnimatedSprite, ABC):
    def __init__(self, xPos, yPos) -> None:
        super().__init__(xPos, yPos)
        self.setup()
        self.direct = pygame.Vector2(0, 0)
        self.left = False
        self.onGround = False

    def setup(self):
        pass

    def setLeftDir(self, v: bool):
        self.left = v

    def setPosition(self, xPos, yPos):
        self.rect.x = xPos
        self.rect.y = yPos

    def setOnGround(self, val):
        self.onGround = val

    def isOnGround(self):
        return self.onGround

    def getCollideBox(self):
        if self.left:
            return pygame.Rect(self.rect.x + self.rect.w - self.animData.rect_collide.right, self.rect.y + self.animData.rect_collide.y, self.animData.rect_collide.w, self.animData.rect_collide.h)

        return pygame.Rect(self.rect.x + self.animData.rect_collide.x, self.rect.y + self.animData.rect_collide.y, self.animData.rect_collide.w, self.animData.rect_collide.h)

    def setRectDisplay(self, x, y):
        if self.left:
            self.rect.x = x - (self.rect.w -
                               self.animData.rect_collide.right)
        else:
            self.rect.x = x - self.animData.rect_collide.x

        self.rect.y = y - self.animData.rect_collide.y

    def getDirect(self):
        return pygame.Vector2(self.direct.x, self.direct.y)

    def setDirect(self, x, y):
        self.direct.x = x
        self.direct.y = y

    def getWeight(self):
        return self.weight

    def updateCor(self, deltaTime):
        pass

    def update(self, deltaTime: float):
        self.updateAnim(deltaTime)
        self.updateCor(deltaTime)

    def drawCharacter(self, win: pygame.Surface, cx, cy):
        cropped = pygame.Surface((self.rect.w, self.rect.h))
        cropped.fill((11, 11, 11))
        cropped.set_colorkey((11, 11, 11))
        cropped.blit(self.image, (0, 0), self.area)

        if self.left:
            cropped = pygame.transform.flip(cropped, True, False)

        win.blit(cropped, (self.rect.x - cx, self.rect.y - cy))

    def draw(self, win: pygame.Surface, cx, cy):
        self.drawCharacter(win, cx, cy)


class Character(GameObj):
    def __init__(self, xPos, yPos, health, damage, takehit_timer) -> None:
        super().__init__(xPos, yPos)
        self.attack_rect = None
        self.max_health = health
        self.health = health
        self.damage = damage
        self.takehit_timer = takehit_timer

    def getDamaged(self, damage):
        pass

    def attack(self, obj):
        pass

    def getAttackRect(self):
        if self.left:
            return pygame.Rect(self.rect.x + self.rect.w - self.attack_rect.right, self.rect.y + self.attack_rect.y, self.attack_rect.w, self.attack_rect.h)

        return pygame.Rect(self.rect.x + self.attack_rect.x, self.rect.y + self.attack_rect.y, self.attack_rect.w, self.attack_rect.h)
