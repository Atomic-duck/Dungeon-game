from abc import ABC, abstractclassmethod
import pygame
import random


class State(ABC):
    STAND = 0
    WALK = 1
    ATTACK = 2
    SHIELD = 3
    DEATH = 4
    TAKEHIT = 5
    TURNBACK = 6

    def __init__(self) -> None:
        super().__init__()
        self._ctx = None
        self.state = None

    def initState():
        return [Standing(), Walking(), Attack(), Shield(), Death(), TakeHit(), TurnBack()]

    @property
    def ctx(self):
        return self._ctx

    @ctx.setter
    def ctx(self, ctx):
        self._ctx = ctx

    def getState(self):
        return self.state

    @abstractclassmethod
    def enter(self):
        pass

    @abstractclassmethod
    def handleInput(self, deltaTime):
        pass


class TurnBack(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.STAND

    def enter(self):
        self._ctx.direct.x = 0
        self._ctx.direct.y = 0
        self._ctx.changeAnim("walk")

    def handleInput(self, deltaTime):
        if self._ctx.xPos < self._ctx.rect.x and self._ctx.rect.x - self._ctx.xPos > 2:
            self._ctx.left = True
            self._ctx.direct.x = -2
        elif self._ctx.xPos > self._ctx.rect.x and self._ctx.xPos - self._ctx.rect.x > 2:
            self._ctx.left = False
            self._ctx.direct.x = 2
        else:
            self._ctx.transition_to(self.STAND)


class Standing(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.STAND

    def enter(self):
        self._ctx.direct.x = 0
        self._ctx.direct.y = 0
        self._ctx.changeAnim("idle")

    def handleInput(self, deltaTime):
        self._ctx.attack_timer -= deltaTime
        pos, detect = self._ctx.detectEnemy()
        attack = self._ctx.inRangeAttack()
        if detect:
            if not attack:
                self._ctx.transition_to(self.WALK)
            elif self._ctx.attack_timer <= 0:
                x = random.random()
                if x < 0.5:
                    self._ctx.transition_to(self.SHIELD)
                else:
                    self._ctx.transition_to(self.ATTACK)


class Walking(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.WALK

    def enter(self):
        self._ctx.changeAnim("walk")

    def handleInput(self, deltaTime):
        self._ctx.attack_timer -= deltaTime
        pos, detect = self._ctx.detectEnemy()
        if self._ctx.outBoundary():
            self._ctx.transition_to(self.TURNBACK)

        if detect:
            enemy_box = self._ctx.getCollideBox()
            attack = self._ctx.inRangeAttack()

            if pos.x < enemy_box.x:
                self._ctx.left = True
                if not attack:
                    self._ctx.direct.x = -2
            elif pos.x > enemy_box.x:
                self._ctx.left = False
                if not attack:
                    self._ctx.direct.x = 2

            if attack and self._ctx.attack_timer <= 0:
                if random.random() < 0.5:
                    self._ctx.transition_to(self.SHIELD)
                else:
                    self._ctx.transition_to(self.ATTACK)
        else:
            self._ctx.transition_to(self.TURNBACK)


class Attack(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.ATTACK

    def enter(self):
        self._ctx.direct.x = 0
        self._ctx.direct.y = 0
        self._ctx.changeAnim("attack")

    def handleInput(self, deltaTime):
        if not self._ctx.firstAnimated:
            self._ctx.attack_timer = random.random() + 0.6
            self._ctx.transition_to(self.STAND)


class Shield(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.SHIELD

    def enter(self):
        self._ctx.direct.x = 0
        self._ctx.direct.y = 0
        self._ctx.changeAnim("shield")
        self.timer = self._ctx.shield_timer * random.random()

    def handleInput(self, deltaTime):
        self.timer -= deltaTime

        if not self._ctx.firstAnimated and self.timer <= 0:
            self._ctx.attack_timer = random.random() + 0.6
            self._ctx.transition_to(self.STAND)


class TakeHit(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.TAKEHIT

    def enter(self):
        self._ctx.visible = True
        self.timer = self._ctx.takehit_timer
        self._ctx.direct.x = 0
        self._ctx.direct.y = 0
        self._ctx.changeAnim("takehit")

    def handleInput(self, deltaTime):
        self.timer -= deltaTime
        self._ctx.visible_timer = 5
        if self._ctx.health <= 0:
            self._ctx.transition_to(self.DEATH)
        if self.timer <= 0:
            self._ctx.transition_to(self.ATTACK)


class Death(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.DEATH

    def enter(self):
        self._ctx.direct.x = 0
        self._ctx.direct.y = 0
        self._ctx.changeAnim("death")

    def handleInput(self, deltaTime):
        if not self._ctx.firstAnimated:
            self._ctx.delete = True
