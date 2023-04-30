import pygame
from setting import *
import level
import player
from game_data import level_0
from ui import UI


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.run = True
        self.gameMenu = True
        self.gameOver = False
        self.coin = 0
        self.win = pygame.display.set_mode((SC_WIDTH, SC_HEIGHT))
        self.music = pygame.mixer.Sound('../sounds/Pixel 4.mp3')
        self.sword_sd = pygame.mixer.Sound('../sounds/sword-effect.wav')
        self.ui = UI(self.win, self)
        self.camera = pygame.Rect(
            0, 0, SC_WIDTH, SC_HEIGHT)
        self.map1 = level.Level(TILE_SIZE, self.updateCoin)
        self.player = player.Player(
            150, 400, self.map1.checkAtLadder, self.sword_sd)
        self.map1.setPlayerBoxFunc(self.player.getCollideBox)
        self.map1.setup(level_0)
        self.player.setStartPos(self.map1.playerPos)

    def updateCoin(self, amount):
        self.coin += amount

    def updateCamera(self):
        self.camera.x = (self.player.rect.x +
                         self.player.animData.rect_collide.w/2) - SC_WIDTH/2
        self.camera.y = (self.player.rect.y +
                         self.player.animData.rect_collide.y/2) - SC_HEIGHT/2

        if self.camera.x < 0:
            self.camera.x = 0
        elif self.camera.x > LV_WIDTH - self.camera.w:
            self.camera.x = LV_WIDTH - self.camera.w

        if self.camera.y < 0:
            self.camera.y = 0
        elif self.camera.y > LV_HEIGHT - self.camera.h:
            self.camera.y = LV_HEIGHT - self.camera.h

    def update(self, deltaTime):
        self.player.update(deltaTime)
        self.updateCamera()
        self.map1.update(deltaTime)
        self.map1.checkPlayerCollision(self.player)
        self.map1.checkEnemyVsPlayer(self.player)

    def draw(self):
        self.win.fill((123, 154, 200))
        self.map1.draw(self.win, self.camera.x, self.camera.y)
        self.player.draw(self.win, self.camera.x, self.camera.y)
        self.ui.show_player_health(self.player.health, 100)
        self.map1.show_enemy_health(
            self.ui.show_enemy_health, self.camera.x, self.camera.y)
        self.ui.show_coins(self.coin)
        self.ui.show_attack_point(self.player.damage)

    def play(self):
        # to control speed of while loop
        clock = pygame.time.Clock()
        getTicksLastFrame = 0
        self.music.play(loops=-1)

        while self.run:
            if self.gameMenu:
                self.ui.play()
            else:
                # make sure while loop run <= 60 times/second
                t = pygame.time.get_ticks()
                deltaTime = (t - getTicksLastFrame)/1000
                getTicksLastFrame = t

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False

                self.update(deltaTime)
                self.draw()
                # need to update to display
                pygame.display.update()
                clock.tick(FPS)

        pygame.quit()


def main():
    game = Game()
    game.play()


# prevent run main function when don't run main file directly (ex: main is imported)
if __name__ == "__main__":
    main()
