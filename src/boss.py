import pygame
from support import import_folder
from dataclasses import dataclass
import bossstate
from setting import TILE_SIZE


@dataclass
class AnimData:
    animation_speed: int
    img_list: list


class Boss(pygame.sprite.Sprite):
    def __init__(self, center_xPos, bottom_yPos, getPlayerBox):
        xPos = center_xPos - 185
        yPos = bottom_yPos - 163 + 2
        super().__init__()
        self.import_character_assets()
        self.frame = 0
        self.animation_speed = 0.15
        self.firstAnimated = True
        self.image = self.animations['idle'].img_list[0]
        self.rect = self.image.get_rect(topleft=(xPos, yPos))
        self.centerx = 106
        self.rect_collide = pygame.Rect(170, 72, 203-170, 163-72)
        self.attack_rect = pygame.Rect(23, 75, 80-23, 163 - 75)
        self.spell_attack_rect = None

        self.direct = pygame.Vector2(0, 0)
        self.left = True
        self.pos_flip = True
        self.onGround = False

        self.max_health = 200
        self.health = 200
        self.damage = 10
        self.delete = False
        self.visible = False
        self.visible_timer = 0
        self.attack_timer = 0
        self.takehit_timer = 0.3
        self.hitted = 0.5
        self.range_detect = 45
        self.offset = 45

        self.getPlayerBox = getPlayerBox
        self.spell_animation = self.animations['spell']
        self.spell_frame = 0
        self.spell_pos = (0, 0)
        self.spell = False

        # state
        self.stateList = bossstate.State.initState()
        self.transition_to(bossstate.State.STAND)

    def import_character_assets(self):
        character_path = '../images/Bringer-Of-Death/'
        self.animations = {'attack': AnimData(0.2, []), 'cast': AnimData(0.2, []), 'death': AnimData(0.2, []), 'hurt': AnimData(
            0.2, []), 'idle': AnimData(0.2, []), 'spell': AnimData(0.2, []), 'walk': AnimData(0.2, [])}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation].img_list = import_folder(full_path)

    def updateAnim(self):
        # loop over frame index
        self.frame += self.animation_speed
        if self.frame >= len(self.animation):
            self.frame = 0
            self.firstAnimated = False

        image = self.animation[int(self.frame)]
        if self.left:
            self.image = image
            if self.pos_flip is False:
                self.rect.x -= 85
                self.pos_flip = True
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            if self.pos_flip:
                self.rect.x += 85
                self.pos_flip = False

    def changeAnim(self, anim: str):
        self.frame = 0
        self.firstAnimated = True
        self.animation = self.animations[anim].img_list
        self.animation_speed = self.animations[anim].animation_speed

    def updateCor(self, deltaTime):
        self.hitted -= deltaTime
        self.visible_timer -= deltaTime
        self.state.handleInput(deltaTime)
        if self.visible_timer <= 0:
            self.visible = False
        # self.direct.y += self.weight

        self.rect.x += self.direct.x
        self.rect.y += self.direct.y

    def update(self, deltatime):
        self.updateAnim()
        self.updateCor(deltatime)

    def drawSpell(self, win, cx, cy):
        if self.spell:
            self.spell_frame += self.spell_animation.animation_speed
            if self.spell_frame >= len(self.spell_animation.img_list):
                self.spell = False
            else:
                image = self.spell_animation.img_list[int(self.spell_frame)]
                win.blit(
                    image, (self.spell_pos[0] - 134 - cx, self.spell_pos[1] - 186 - cy))

    def draw(self, win, cx, cy):
        win.blit(self.image, (self.rect.x - cx, self.rect.y - cy))
        self.drawSpell(win, cx, cy)

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

    def detectEnemy(self):
        player_box = self.getPlayerBox()
        self_box = self.getCollideBox()

        return player_box, abs(player_box.bottom - self_box.bottom) < 16 and abs(player_box.centerx - self_box.centerx) < self.range_detect*TILE_SIZE

    def getDamaged(self, damage):
        if not self.inState(bossstate.State.TAKEHIT) and not self.inState(bossstate.State.DEATH) and self.hitted <= 0:
            self.hitted = 0.2
            self.health -= damage
            if self.inState(bossstate.State.ATTACK) or self.spell:
                pass
            else:
                self.transition_to(bossstate.State.TAKEHIT)

    def attack(self, obj):
        if (self.inState(bossstate.State.ATTACK) and (int(self.frame) == 4)) or (self.spell and (int(self.spell_frame) in [6, 7, 8, 9])):
            if self.spell and self.spell_attack_rect.colliderect(obj.getCollideBox()):
                obj.getDamaged(self.damage)
            elif self.getAttackRect().colliderect(obj.getCollideBox()):
                obj.getDamaged(self.damage)

    def getAttackRect(self):
        if self.left:
            return pygame.Rect(self.rect.x + self.rect.w - self.attack_rect.right - self.offset, self.rect.y + self.attack_rect.y, self.attack_rect.w, self.attack_rect.h)

        return pygame.Rect(self.rect.x + self.attack_rect.x + self.offset, self.rect.y + self.attack_rect.y, self.attack_rect.w, self.attack_rect.h)

    def getCollideBox(self):
        if not self.left:
            return pygame.Rect(self.rect.x + self.rect.w - self.rect_collide.right, self.rect.y + self.rect_collide.y, self.rect_collide.w, self.rect_collide.h)

        return pygame.Rect(self.rect.x + self.rect_collide.x, self.rect.y + self.rect_collide.y, self.rect_collide.w, self.rect_collide.h)
