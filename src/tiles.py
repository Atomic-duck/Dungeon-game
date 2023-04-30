import pygame
import math
from support import import_folder
import random


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size) -> None:
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, deltaTime):
        pass

    def draw(self, win, cx, cy):
        win.blit(self.image, (self.rect.x - cx, self.rect.y - cy))


class StaticTile(Tile):
    def __init__(self, pos, size, surface) -> None:
        super().__init__(pos, size)
        self.image = surface


class AnimatedTile(Tile):
    def __init__(self, pos, size, frames):
        super().__init__(pos, size)
        self.frames = frames
        self.frame_index = 0
        self.old_frame = 0
        self.image = self.frames[self.frame_index]
        self.firstAnimated = True
        self.animFPS = 10
        self.frameTime = 0

    def updateAnim(self, deltaTime: float):
        self.frameTime += deltaTime
        self.old_frame = self.frame_index
        if self.frameTime > (1/self.animFPS):
            self.frame_index += math.floor(self.frameTime * self.animFPS)
            if self.frame_index >= len(self.frames):
                self.frame_index = self.frame_index % len(self.frames)
                if self.firstAnimated:
                    self.firstAnimated = not self.firstAnimated

            self.image = self.frames[self.frame_index]

            self.frameTime = math.fmod(self.frameTime, 1/self.animFPS)

    def reverseImage(self):
        if int(self.frame_index) != int(self.old_frame):
            self.image = pygame.transform.flip(self.image, True, False)
            self.old_frame = self.frame_index

    def updateCor(self):
        pass

    def update(self, deltaTime):
        self.updateAnim(deltaTime)
        self.updateCor()
