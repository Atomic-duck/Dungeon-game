import os
import pygame
import sprite
from setting import *
from gameObj import Character, GameObj
import skeletonstate
import goblinstate
import wizardstate


class Enemy(Character):
    def __init__(self, xPos, yPos, health, damage) -> None:
        super().__init__(xPos, yPos, health, damage, 0.3)
        self.delete = False
        self.visible = False
        self.visible_timer = 0
        self.hitted = 0.4

    def setBoundary(self, boundaries):
        self.boundaries = boundaries

    def updateCor(self, deltaTime):
        self.hitted -= deltaTime
        self.visible_timer -= deltaTime
        self.state.handleInput(deltaTime)
        if self.visible_timer <= 0:
            self.visible = False
        # self.direct.y += self.weight

        self.rect.x += self.direct.x
        self.rect.y += self.direct.y

    def transition_to(self, idx):
        self.state = self.stateList[idx]
        self.state.ctx = self
        self.state.enter()

    def inState(self, state):
        return state == self.state.getState()

    def inRangeAttack(self):
        player_box = self.getPlayerBox()
        attackRect = self.getAttackRect()
        return attackRect.colliderect(player_box)

    def outBoundary(self):
        rect = self.getCollideBox()
        for boundry in self.boundaries:
            if rect.colliderect(boundry.rect):
                return True

        return False

    def detectEnemy(self):
        player_box = self.getPlayerBox()
        self_box = self.getCollideBox()

        return player_box, self_box.bottom - player_box.bottom < 16*10 and abs(player_box.centerx - self_box.centerx) < self.range_detect*TILE_SIZE


class Skeleton(Enemy):
    def __init__(self, center_xPos, bottom_yPos, getPlayerBox) -> None:
        self.xPos = center_xPos - 150/2
        self.yPos = bottom_yPos - 200+66
        super().__init__(self.xPos, self.yPos, 50, 5)
        self.range_detect = 20
        self.attack_rect = pygame.Rect(120, 66, 155-120, 200-66)
        self.getPlayerBox = getPlayerBox
        self.attack_timer = 0
        self.shield_timer = 2
        # state
        self.stateList = skeletonstate.State.initState()

    def setup_sub(self, img_list):
        width = 200
        height = 200
        self.addImg('idle', img_list[0], 800,
                    sprite.AnimData(8, pygame.Rect(85, 66, 120-85, 70), width, height, 4, []))
        self.addImg('walk', img_list[1], 800,
                    sprite.AnimData(8, pygame.Rect(85, 66, 120-85, 70), width, height, 4, []))
        self.addImg('attack', img_list[2], 1600,
                    sprite.AnimData(12, pygame.Rect(85, 66, 120-85, 70), width, height, 8, []))
        self.addImg('shield', img_list[3], 800,
                    sprite.AnimData(8, pygame.Rect(85, 66, 120-85, 70), width, height, 4, []))
        self.addImg('death', img_list[4], 800,
                    sprite.AnimData(8, pygame.Rect(85, 66, 120-85, 70), width, height, 4, []))
        self.addImg('takehit', img_list[5], 800,
                    sprite.AnimData(8, pygame.Rect(85, 66, 120-85, 70), width, height, 4, []))

        self.transition_to(skeletonstate.State.STAND)

    def getDamaged(self, damage):
        if not self.inState(skeletonstate.State.TAKEHIT) and not self.inState(skeletonstate.State.SHIELD) and not self.inState(skeletonstate.State.DEATH) and self.hitted <= 0:
            self.health -= damage
            self.hitted = 0.1
            if self.inState(skeletonstate.State.ATTACK):
                pass
            else:
                self.transition_to(skeletonstate.State.TAKEHIT)

    def attack(self, obj):
        if self.inState(skeletonstate.State.ATTACK) and (self.frame == 6 or self.frame == 7):
            if self.getAttackRect().colliderect(obj.getCollideBox()):
                obj.getDamaged(self.damage)


class Goblin(Enemy):
    def __init__(self, center_xPos, bottom_yPos, getPlayerBox) -> None:
        self.xPos = center_xPos - 150/2
        self.yPos = bottom_yPos - 200+66
        super().__init__(self.xPos, self.yPos, 50, 5)
        self.range_detect = 20
        self.attack_rect = pygame.Rect(120, 66, 155-120, 200-66)
        self.getPlayerBox = getPlayerBox
        self.attack_timer = 0
        # state
        self.stateList = goblinstate.State.initState()

    def setup_sub(self, img_list):
        width = 200
        height = 200
        self.addImg('idle', img_list[0], 800,
                    sprite.AnimData(8, pygame.Rect(85, 90, 120-85, 40), width, height, 4, []))
        self.addImg('walk', img_list[1], 1600,
                    sprite.AnimData(8, pygame.Rect(85, 90, 120-85, 40), width, height, 8, []))
        self.addImg('attack', img_list[2], 1600,
                    sprite.AnimData(14, pygame.Rect(85, 90, 120-85, 40), width, height, 8, []))
        self.addImg('death', img_list[3], 800,
                    sprite.AnimData(8, pygame.Rect(85, 90, 120-85, 40), width, height, 4, []))
        self.addImg('takehit', img_list[4], 800,
                    sprite.AnimData(8, pygame.Rect(85, 90, 120-85, 40), width, height, 4, []))

        self.transition_to(skeletonstate.State.STAND)

    def getDamaged(self, damage):
        if not self.inState(goblinstate.State.TAKEHIT) and not self.inState(goblinstate.State.DEATH) and self.hitted <= 0:
            self.health -= damage
            self.hitted = 0.1
            if self.inState(goblinstate.State.ATTACK):
                pass
            else:
                self.transition_to(goblinstate.State.TAKEHIT)

    def attack(self, obj):
        if self.inState(goblinstate.State.ATTACK) and (self.frame == 6 or self.frame == 7):
            if self.getAttackRect().colliderect(obj.getCollideBox()):
                obj.getDamaged(self.damage)


class Charge(GameObj):
    def __init__(self, center_xPos, center_yPos, xDes, yDes) -> None:
        xPos = 0
        if xDes < center_xPos:
            xPos = center_xPos - 64
        else:
            xPos = center_xPos - 64
        yPos = center_yPos - 64
        super().__init__(xPos, yPos)
        if xDes < center_xPos:
            self.left = True
        self.direct = pygame.Vector2(
            xDes - center_xPos, yDes - center_yPos).normalize() * 5
        self.delete = False
        self.timer = 3

    def setup(self):
        CHARGE2_IMAGE = pygame.image.load(
            os.path.join('../images/Wanderer Magican/', 'Charge_2.png')).convert_alpha()

        self.addImg('charge2', CHARGE2_IMAGE, 384,
                    sprite.AnimData(8, pygame.Rect(31, 61, 15, 4), 64, 128, 6, []))
        self.changeAnim('charge2')

    def updateCor(self, deltaTime):
        self.timer -= deltaTime
        if self.timer <= 0:
            self.delete = True
        self.rect.x += self.direct.x
        self.rect.y += self.direct.y

    def draw(self, win: pygame.Surface, cx, cy):
        return super().draw(win, cx, cy)


class Wizard(Enemy):
    def __init__(self, center_xPos, bottom_yPos, getPlayerBox) -> None:
        self.xPos = center_xPos - 115/2
        self.yPos = bottom_yPos - 115
        super().__init__(self.xPos, self.yPos, 50, 5)
        self.range_detect = 50
        self.attack_rect = pygame.Rect(120, 66, 155-120, 200-66)
        self.getPlayerBox = getPlayerBox
        self.attack_timer = 0
        # state
        self.stateList = wizardstate.State.initState()
        self.transition_to(wizardstate.State.STAND)
        self.charges = []

    def setup(self):
        IDLE_IMAGE = pygame.image.load(
            os.path.join('../images/Wanderer Magican/', 'Idle.png')).convert_alpha()
        WALK_IMAGE = pygame.image.load(
            os.path.join('../images/Wanderer Magican/', 'Walk.png')).convert_alpha()
        ATTACK2_IMAGE = pygame.image.load(
            os.path.join('../images/Wanderer Magican/', 'Attack_2.png')).convert_alpha()
        DEATH_IMAGE = pygame.image.load(
            os.path.join('../images/Wanderer Magican/', 'Dead.png')).convert_alpha()
        TAKEHIT_IMAGE = pygame.image.load(
            os.path.join('../images/Wanderer Magican/', 'Hurt.png')).convert_alpha()

        width = 115
        height = 115
        self.addImg('idle', IDLE_IMAGE, 920,
                    sprite.AnimData(8, pygame.Rect(85, 90, 120-85, 40), width, height, 8, []))
        self.addImg('walk', WALK_IMAGE, 805,
                    sprite.AnimData(8, pygame.Rect(85, 90, 120-85, 40), width, height, 7, []))
        self.addImg('attack2', ATTACK2_IMAGE, 1035,
                    sprite.AnimData(8, pygame.Rect(85, 90, 120-85, 40), width, height, 9, []))
        self.addImg('death', DEATH_IMAGE, 460,
                    sprite.AnimData(8, pygame.Rect(85, 90, 120-85, 40), width, height, 4, []))
        self.addImg('takehit', TAKEHIT_IMAGE, 460,
                    sprite.AnimData(8, pygame.Rect(85, 90, 120-85, 40), width, height, 4, []))

        self.changeAnim('idle')

    def getDamaged(self, damage):
        if not self.inState(goblinstate.State.TAKEHIT) and not self.inState(goblinstate.State.DEATH):
            self.health -= damage
            self.transition_to(goblinstate.State.TAKEHIT)

    def attack(self, obj):
        for charge in self.charges:
            if charge.delete is False and charge.getCollideBox().colliderect(obj.getCollideBox()):
                obj.getDamaged(self.damage)
                charge.delete = True

        self.charges = [charge for charge in self.charges if not charge.delete]

    def createCharge2(self, despos):
        self.charges.append(
            Charge(self.rect.x + 80, self.rect.y + 75, despos[0], self.rect.y + 75))

    def updateCharges(self, deltatime):
        for charge in self.charges:
            charge.update(deltatime)

    def update(self, deltaTime: float):
        self.updateCharges(deltaTime)
        return super().update(deltaTime)

    def draw(self, win: pygame.Surface, cx, cy):
        for charge in self.charges:
            charge.draw(win, cx, cy)
        return super().draw(win, cx, cy)
