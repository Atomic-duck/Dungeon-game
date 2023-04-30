import os
import pygame
import sprite
from setting import *
from playerstate import State
from gameObj import Character


class Player(Character):
    JUMPTIMER = 0.3
    ROllTIMER = 0.3

    def __init__(self, xPos, yPos, checkAtladder, sword_sd) -> None:
        health = 100
        damage = 10
        super().__init__(xPos, yPos, health, damage, 0.5)
        self.weight = 2
        self.attack_rect = pygame.Rect(115, 30, 150-115, 96-30)
        # state
        self.stateList = State.initState()
        self.transition_to(State.STAND)
        self.jump_timer = 0
        self.roll_timer = 0
        self.allow_pray = False
        self.deadth = False
        self.hitted = 1
        # func
        self.checkAtladder = checkAtladder
        self.sword_sd = sword_sd

    def setStartPos(self, pos):
        self.rect.x = pos[0] - 192/2
        self.rect.y = pos[1] - 96

    def setup(self):
        IDLE_IMAGE = pygame.image.load(
            os.path.join('../images/Knight/', 'Idle.png')).convert_alpha()
        RUN_IMAGE = pygame.image.load(
            os.path.join('../images/Knight/', 'Run.png')).convert_alpha()
        ATTACK_IMAGE = pygame.image.load(
            os.path.join('../images/Knight/', 'Attacks.png')).convert_alpha()
        JUMP_IMAGE = pygame.image.load(
            os.path.join('../images/Knight/', 'Jump.png')).convert_alpha()
        CLIMB_IMAGE = pygame.image.load(
            os.path.join('../images/Knight/', 'Climb.png')).convert_alpha()
        ROLL_IMAGE = pygame.image.load(
            os.path.join('../images/Knight/', 'Roll.png')).convert_alpha()
        HURT_IMAGE = pygame.image.load(
            os.path.join('../images/Knight/', 'Hurt.png')).convert_alpha()
        AIR_ATTACK_IMAGE = pygame.image.load(
            os.path.join('../images/Knight/', 'attack_from_air.png')).convert_alpha()
        CROUCH_ATTACK_IMAGE = pygame.image.load(
            os.path.join('../images/Knight/', 'crouch_attacks.png')).convert_alpha()
        CROUCH_IMAGE = pygame.image.load(
            os.path.join('../images/Knight/', 'crouch_idle.png')).convert_alpha()
        PRAY_IMAGE = pygame.image.load(
            os.path.join('../images/Knight/', 'pray.png')).convert_alpha()
        DEAD_IMAGE = pygame.image.load(
            os.path.join('../images/Knight/', 'death.png')).convert_alpha()

        width = 192
        height = 96
        self.addImg('idle', IDLE_IMAGE, 384,
                    sprite.AnimData(16, pygame.Rect(85, 26, 110-85, height-26), width, height, 8, []))
        self.addImg('run', RUN_IMAGE, 384,
                    sprite.AnimData(16, pygame.Rect(88, 26, 112-88, height-26), width, height, 8, []))
        self.addImg('attack', ATTACK_IMAGE, 1536,
                    sprite.AnimData(24, pygame.Rect(85, 26, 110-85, height-26), width, height, 20, []))
        self.addImg('jump', JUMP_IMAGE, 384,
                    sprite.AnimData(16, pygame.Rect(84, 26, 111-84, height-26), width, height, 8, []))
        self.addImg('climb', CLIMB_IMAGE, 384,
                    sprite.AnimData(12, pygame.Rect(84, 26, 105-84, height-26), width, height, 6, []))
        self.addImg('roll', ROLL_IMAGE, 384,
                    sprite.AnimData(12, pygame.Rect(84, 26, 110-84, height-26), width, height, 4, []))
        self.addImg('hurt', HURT_IMAGE, 384,
                    sprite.AnimData(12, pygame.Rect(84, 26, 110-84, height-26), width, height, 3, []))
        self.addImg('airattack', AIR_ATTACK_IMAGE, 384,
                    sprite.AnimData(16, pygame.Rect(84, 26, 110-84, height-26), width, height, 7, []))
        self.addImg('crouchattack', CROUCH_ATTACK_IMAGE, 384,
                    sprite.AnimData(16, pygame.Rect(84, 26, 110-84, height-26), width, height, 7, []))
        self.addImg('crouch', CROUCH_IMAGE, 384,
                    sprite.AnimData(16, pygame.Rect(84, 30, 110-84, height-30), width, height, 8, []))
        self.addImg('pray', PRAY_IMAGE, 768,
                    sprite.AnimData(10, pygame.Rect(84, 30, 110-84, height-30), width, height, 12, []))
        self.addImg('death', DEAD_IMAGE, 384,
                    sprite.AnimData(10, pygame.Rect(84, 30, 110-84, height-30), width, height, 4, []))

        self.changeAnim('idle')

    def atLadder(self):
        return self.checkAtladder(self)

    def reset(self):
        pass

    def getWeight(self):
        return self.weight

    def updateHealth(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def updateAttack(self, amount):
        self.damage += amount

    def updateCor(self, deltaTime):
        self.hitted -= deltaTime
        self.jump_timer -= deltaTime
        self.roll_timer -= deltaTime
        self.state.handleInput(deltaTime)
        self.direct.y += self.weight

        self.rect.x += self.direct.x
        self.rect.y += self.direct.y

    def transition_to(self, idx):
        self.state = self.stateList[idx]
        self.state.knight = self
        self.state.enter()

    def inState(self, state):
        return state == self.state.getState()

    def getDamaged(self, damage):
        if not self.inState(State.HURT) and not self.inState(State.DEATH) and self.hitted <= 0:
            self.health -= damage
            self.transition_to(State.HURT)

    def attack(self, obj):
        if self.inState(State.ATTACK) and self.frame in [3, 7, 10, 16, 17] or self.inState(State.AIR_ATTACK) and self.frame in [0, 1, 2, 3, 4] or self.inState(State.CROUCH_ATTACK) and self.frame in [0, 4]:
            if self.getAttackRect().colliderect(obj.getCollideBox()):
                obj.getDamaged(self.damage)
