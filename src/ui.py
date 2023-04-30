import pygame
from button import Button


class UI:
    def __init__(self, surface, game):

        # setup
        self.game = game
        self.display_surface = surface
        self.menu = True
        self.opts = False

        # health
        self.player_health_bar = pygame.image.load(
            '../images/Knight/health_bar.png').convert_alpha()
        self.bar_max_width = 152
        self.bar_height = 4

        self.enemy_health_bar = pygame.image.load(
            '../images/healthbar.png').convert_alpha()
        self.e_bar_max_width = 63
        self.e_bar_height = 4

        # coins
        self.coin = pygame.image.load(
            '../images/assets/Coin/01.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(240, 35))
        self.font = pygame.font.Font('../font/MoRk DuNgEon.ttf', 20)

        # sword
        self.sword = pygame.image.load(
            '../images/Knight/sword7.png').convert_alpha()
        self.sword_rect = self.coin.get_rect(topleft=(60, 61))

        self.BG = pygame.image.load("../images/menu-asset/Background.png")

    def show_player_health(self, current, full):
        topleft = (54, 39)
        self.display_surface.blit(self.player_health_bar, (20, 10))
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(
            topleft, (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

    def show_enemy_health(self, topleft, current, full):
        self.display_surface.blit(
            self.enemy_health_bar, (topleft[0] - 12, topleft[1] - 4), (30, 50, 114-30, 10))
        current_health_ratio = current / full
        current_bar_width = self.e_bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(
            topleft, (current_bar_width, self.e_bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surf = self.font.render(str(amount), False, '#ffffff')
        coin_amount_rect = coin_amount_surf.get_rect(
            midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)

    def show_attack_point(self, amount):
        self.display_surface.blit(self.sword, self.sword_rect)
        sword_amount_surf = self.font.render(str(amount), False, '#ffffff')
        sword_amount_rect = sword_amount_surf.get_rect(
            midleft=(self.sword_rect.right + 4, self.sword_rect.centery + 10))
        self.display_surface.blit(sword_amount_surf, sword_amount_rect)

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("../font/MoRk DuNgEon.ttf", size)

    def playGame(self):
        self.game.gameMenu = False

    def options(self):
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        self.display_surface.fill("white")

        OPTIONS_TEXT = self.get_font(45).render(
            "This is the OPTIONS self.display_surface.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(500, 260))
        self.display_surface.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(500, 460),
                              text_input="BACK", font=self.get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(self.display_surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    self.opts = False
                    self.menu = True

        pygame.display.update()

    def main_menu(self):
        self.display_surface.blit(self.BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("../images/menu-asset/Play Rect.png"), pos=(500, 250),
                             text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("../images/menu-asset/Options Rect.png"), pos=(500, 400),
                                text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("../images/menu-asset/Quit Rect.png"), pos=(500, 550),
                             text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

        self.display_surface.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(self.display_surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.playGame()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.opts = True
                    self.menu = False
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()

        pygame.display.update()

    def play(self):
        if self.menu:
            self.main_menu()
        elif self.opts:
            self.options()
