from abc import ABC, abstractclassmethod
import pygame


class State(ABC):
    STAND = 0
    JUMP = 1
    RUN = 2
    ATTACK = 3
    HURT = 4
    CLIMB = 5
    ROLL = 6
    D_JUMP = 7
    AIR_ATTACK = 8
    CROUCH_ATTACK = 9
    CROUCH = 10
    FALL = 11
    PRAY = 12
    DEATH = 13

    def __init__(self) -> None:
        super().__init__()
        self._knight = None
        self.state = None

    def initState():
        return [Standing(), Jumping(), Running(), Attack(), Hurt(), Climbing(), Rolling(), DoubleJump(), AirAttack(), CrouchAttack(), Crouch(), Fall(), Pray(), Death()]

    @property
    def knight(self):
        return self._knight

    @knight.setter
    def knight(self, knight):
        self._knight = knight

    def getState(self):
        return self.state

    @abstractclassmethod
    def enter(self):
        pass

    @abstractclassmethod
    def handleInput(self, deltaTime):
        pass


class Death(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.DEATH

    def enter(self):
        self._knight.direct.x = 0
        self._knight.direct.y = 0
        self._knight.changeAnim("death")

    def handleInput(self, deltaTime):
        self._knight.deadth = True
        if self._knight.frame == 3:
            self._knight.updateframe = False


class Pray(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.PRAY

    def enter(self):
        self._knight.direct.x = 0
        self._knight.direct.y = 0
        self._knight.changeAnim("pray")

    def handleInput(self, deltaTime):
        if not self._knight.firstAnimated:
            self._knight.transition_to(self.STAND)


class Fall(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.FALL

    def enter(self):
        self._knight.changeAnim("jump")

    def handleInput(self, deltaTime):
        self._knight.frame = 4
        if self._knight.isOnGround():
            self._knight.transition_to(self.STAND)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self._knight.left = True
            self._knight.direct.x = -5
        if keys[pygame.K_d]:
            self._knight.left = False
            self._knight.direct.x = 5
        if keys[pygame.K_w] and self._knight.atLadder():
            self._knight.transition_to(self.CLIMB)
        if keys[pygame.K_s] and keys[pygame.K_j]:
            self._knight.transition_to(self.AIR_ATTACK)


class Crouch(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.CROUCH

    def enter(self):
        self._knight.direct.x = 0
        self._knight.direct.y = 0
        self._knight.changeAnim("crouch")

    def handleInput(self, deltaTime):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] is False:
            self._knight.transition_to(self.STAND)
        if keys[pygame.K_a]:
            self._knight.left = True
        if keys[pygame.K_d]:
            self._knight.left = False
        if keys[pygame.K_j]:
            self._knight.transition_to(self.CROUCH_ATTACK)


class CrouchAttack(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.CROUCH_ATTACK

    def enter(self):
        self._knight.sword_sd.play()
        self._knight.changeAnim("crouchattack")
        self._knight.attack_rect = pygame.Rect(115, 30, 150-115, 96-30)

    def handleInput(self, deltaTime):
        if not self._knight.firstAnimated:
            self._knight.transition_to(self.CROUCH)


class AirAttack(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.AIR_ATTACK

    def enter(self):
        self.play = True
        self._knight.direct.x = 0
        self._knight.changeAnim("airattack")
        self._knight.attack_rect = pygame.Rect(75, 52, 115, 96-52)

    def handleInput(self, deltaTime):
        if self._knight.isOnGround():
            if self.play:
                self._knight.sword_sd.play()
                self.play = False
            if not self._knight.firstAnimated:
                self._knight.transition_to(self.STAND)
        elif self._knight.frame >= 2:
            self._knight.frame = 1


class DoubleJump(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.D_JUMP

    def enter(self):
        self.frame = 4
        self._knight.direct.y = -16
        self._knight.changeAnim("jump")

    def handleInput(self, deltaTime):
        keys = pygame.key.get_pressed()
        if self._knight.frame > self.frame:
            self._knight.frame = self.frame
        if self._knight.direct.y >= 0:
            self._knight.transition_to(self.FALL)

        if keys[pygame.K_a]:
            self._knight.left = True
            self._knight.direct.x = -5
        if keys[pygame.K_d]:
            self._knight.left = False
            self._knight.direct.x = 5
        if keys[pygame.K_w] and self._knight.atLadder():
            self._knight.transition_to(self.CLIMB)
        if keys[pygame.K_s] and keys[pygame.K_j]:
            self._knight.transition_to(self.AIR_ATTACK)


class Rolling(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.ROLL

    def enter(self):
        self._knight.direct.x = -6 if self._knight.left else 6
        self.timer = 0.3
        self._knight.direct.y = 0
        self._knight.changeAnim("roll")

    def handleInput(self, deltaTime):
        self._knight.roll_timer = self._knight.ROllTIMER
        self.timer -= deltaTime
        if self.timer <= 0:
            self._knight.transition_to(self.STAND)


class Climbing(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.CLIMB

    def enter(self):
        self._knight.direct.x = 0
        self._knight.direct.y = 0
        self._knight.changeAnim("climb")

    def handleInput(self, deltaTime):
        self._knight.updateframe = False
        self._knight.direct.y = -self._knight.weight
        self._knight.direct.x = 0

        if not self._knight.atLadder():
            self._knight.transition_to(self.STAND)
            self._knight.updateframe = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and keys[pygame.K_s]:
            self._knight.transition_to(self.FALL)
            self._knight.updateframe = True
        elif keys[pygame.K_SPACE] and self._knight.jump_timer <= 0:
            self._knight.transition_to(self.JUMP)
            self._knight.updateframe = True
        if keys[pygame.K_w]:
            self._knight.direct.y = -6
            self._knight.updateframe = True
        if keys[pygame.K_s] and self._knight.isOnGround():
            self._knight.transition_to(self.STAND)
            self._knight.updateframe = True
        elif keys[pygame.K_s]:
            self._knight.direct.y = 3
            self._knight.updateframe = True
        if keys[pygame.K_a]:
            self._knight.direct.x = -2
            self._knight.updateframe = True
        if keys[pygame.K_d]:
            self._knight.direct.x = 2
            self._knight.updateframe = True
        if keys[pygame.K_s] and keys[pygame.K_j]:
            self._knight.transition_to(self.AIR_ATTACK)


class Standing(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.STAND

    def enter(self):
        self._knight.direct.x = 0
        self._knight.direct.y = 0
        self._knight.changeAnim("idle")

    def handleInput(self, deltaTime):
        keys = pygame.key.get_pressed()
        if self._knight.isOnGround() is False:
            self._knight.transition_to(self.FALL)
        if self._knight.left is False and keys[pygame.K_a]:
            self._knight.left = True
        if self._knight.left and keys[pygame.K_a]:
            self._knight.transition_to(self.RUN)
        if self._knight.left is False and keys[pygame.K_d]:
            self._knight.transition_to(self.RUN)
        if self._knight.left and keys[pygame.K_d]:
            self._knight.left = False
        if keys[pygame.K_e] and self._knight.allow_pray:
            self._knight.transition_to(self.PRAY)
        if keys[pygame.K_SPACE] and self._knight.isOnGround() and self._knight.jump_timer <= 0:
            self._knight.transition_to(self.JUMP)
        if keys[pygame.K_j] and keys[pygame.K_s]:
            self._knight.transition_to(self.CROUCH_ATTACK)
        if keys[pygame.K_j]:
            self._knight.transition_to(self.ATTACK)
        if keys[pygame.K_s]:
            self._knight.transition_to(self.CROUCH)
        if keys[pygame.K_w] and self._knight.atLadder():
            self._knight.transition_to(self.CLIMB)
        if keys[pygame.K_l] and self._knight.roll_timer <= 0:
            self._knight.transition_to(self.ROLL)


class Running(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.RUN

    def enter(self):
        self._knight.changeAnim("run")

    def handleInput(self, deltaTime):
        keys = pygame.key.get_pressed()
        if self._knight.isOnGround() is False:
            self._knight.transition_to(self.FALL)
        if keys[pygame.K_a] is False and keys[pygame.K_d] is False:
            self._knight.transition_to(self.STAND)
        if keys[pygame.K_a]:
            self._knight.left = True
            self._knight.direct.x = -5
        if keys[pygame.K_d]:
            self._knight.left = False
            self._knight.direct.x = 5
        if keys[pygame.K_j] and keys[pygame.K_s]:
            self._knight.transition_to(self.CROUCH_ATTACK)
        if keys[pygame.K_j]:
            self._knight.transition_to(self.ATTACK)
        if keys[pygame.K_s]:
            self._knight.transition_to(self.CROUCH)
        if keys[pygame.K_SPACE] and self._knight.isOnGround() and self._knight.jump_timer <= 0:
            self._knight.transition_to(self.JUMP)
        if keys[pygame.K_w] and self._knight.atLadder():
            self._knight.transition_to(self.CLIMB)
        if keys[pygame.K_l] and self._knight.roll_timer <= 0:
            self._knight.transition_to(self.ROLL)


class Jumping(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.JUMP

    def enter(self):
        self.frame = 4
        self._knight.direct.y = -22
        self._knight.changeAnim("jump")
        self.djump = False

    def handleInput(self, deltaTime):
        keys = pygame.key.get_pressed()
        if self._knight.frame > self.frame:
            self._knight.frame = self.frame
        self._knight.jump_timer = self._knight.JUMPTIMER

        if keys[pygame.K_SPACE] == False:
            self.djump = True

        if keys[pygame.K_a]:
            self._knight.left = True
            self._knight.direct.x = -5
        if keys[pygame.K_d]:
            self._knight.left = False
            self._knight.direct.x = 5
        if keys[pygame.K_SPACE] and self.djump:
            self._knight.transition_to(self.D_JUMP)
        if keys[pygame.K_s] and keys[pygame.K_j]:
            self._knight.transition_to(self.AIR_ATTACK)
        if keys[pygame.K_w] and self._knight.atLadder():
            self._knight.transition_to(self.CLIMB)

        if self._knight.direct.y >= 10:
            self._knight.transition_to(self.FALL)


class Attack(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.ATTACK

    def enter(self):
        self._knight.direct.x = 0
        self._knight.direct.y = 0
        self._knight.changeAnim("attack")
        self._knight.attack_rect = pygame.Rect(115, 30, 150-115, 96-30)
        self.cur = 0
        self.count = 0
        self.press = True
        self.atcks = [(0, 5), (6, 9), (10, 13), (14, 19)]
        self._knight.sword_sd.play()

    def handleInput(self, deltaTime):
        keys = pygame.key.get_pressed()
        if self.count < 3 and keys[pygame.K_j] and self.press:
            self.count += 1
            self.press = False
        if keys[pygame.K_j] is False:
            self.press = True

        if keys[pygame.K_l] and self._knight.roll_timer <= 0:
            self._knight.transition_to(self.ROLL)
        if keys[pygame.K_SPACE] and self._knight.isOnGround() and self._knight.jump_timer <= 0:
            self._knight.transition_to(self.JUMP)

        if self.cur == self.count and self._knight.frame >= self.atcks[self.cur][1]:
            self._knight.transition_to(self.STAND)
        if self.cur < self.count and self._knight.frame > self.atcks[self.cur][1]:
            self.cur += 1


class Hurt(State):
    def __init__(self) -> None:
        super().__init__()
        self.state = self.HURT

    def enter(self):
        self._knight.direct.y = 0
        self._knight.direct.x = 0
        self._knight.changeAnim("hurt")
        self.timer = self._knight.takehit_timer

    def handleInput(self, deltaTime):
        self.timer -= deltaTime
        if self._knight.health <= 0:
            self._knight.transition_to(self.DEATH)
        if self.timer <= 0:
            self._knight.transition_to(self.STAND)
