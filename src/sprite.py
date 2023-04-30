from dataclasses import dataclass
import pygame
import math


@dataclass
class Point:
    x: int
    y: int


@dataclass
class AnimData:
    fps: int
    rect_collide: pygame.Rect
    width: int
    height: int
    frameNum: int
    frameLoc: list[Point]


@dataclass
class ImageData:
    width: int
    image: pygame.Surface
    anim: AnimData


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, xPos: int, yPos: int) -> None:
        super().__init__()
        self.imgList: dict[str, ImageData] = {}
        self.animFPS = 24
        self.firstAnimated = True
        self.rect = pygame.Rect(xPos, yPos, 0, 0)
        self.updateframe = True

    def updateAnim(self, deltaTime: float):
        if self.updateframe:
            self.frameTime += deltaTime
            if self.frameTime > (1/self.animFPS):
                self.frame += math.floor(self.frameTime * self.animFPS)
                if self.frame >= self.animData.frameNum:
                    self.frame = self.frame % self.animData.frameNum
                    if self.firstAnimated:
                        self.firstAnimated = False

                self.area = pygame.Rect(
                    self.animData.frameLoc[self.frame].x, self.animData.frameLoc[self.frame].y, self.animData.width, self.animData.height)

                self.frameTime = math.fmod(self.frameTime, 1/self.animFPS)

    def changeAnim(self, imgName: str):
        self.imgName = imgName
        self.frame = 0
        self.frameTime = 0
        #self.animTime = 0

        self.image = self.imgList[self.imgName].image
        self.animData = self.imgList[self.imgName].anim
        self.rect.w = self.animData.width
        self.rect.h = self.animData.height
        self.animFPS = self.animData.fps
        self.firstAnimated = True

        self.area = pygame.Rect(
            self.animData.frameLoc[self.frame].x, self.animData.frameLoc[self.frame].y, self.animData.width, self.animData.height)

    def addImg(self, name: str, imgSur: pygame.Surface, img_w, anim: AnimData):
        for i in range(anim.frameNum):
            x = anim.width * i
            y = int(x/img_w) * anim.height
            if x >= img_w:
                x %= img_w
            anim.frameLoc.append(Point(x, y))

        # ImageData
        imgData = ImageData(img_w, imgSur, anim)
        self.imgList[name] = imgData
