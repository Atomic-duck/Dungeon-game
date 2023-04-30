import pygame
import os
import tiles
from support import import_csv_layout, import_cut_graphics, import_folder, import_sprite
from setting import TILE_SIZE
from enemy import Skeleton, Goblin, Wizard
import boss
import assets


class Level(pygame.sprite.Sprite):
    def __init__(self, tile_size, updateCoin) -> None:
        super().__init__()
        self.tile_size = tile_size
        self.getPlayerBox = None
        self.playerPos = None
        self.enemies = []
        self.boundaries = []
        self.crates = []
        self.assets = []

        self.background1 = pygame.image.load(
            os.path.join('../images/', 'background1.png')).convert_alpha()
        self.background2 = pygame.image.load(
            os.path.join('../images/Caves/', 'background4b.png')).convert_alpha()
        self.background3 = pygame.image.load(
            os.path.join('../images/Caves/', 'background3.png')).convert_alpha()
        self.background4 = pygame.image.load(
            os.path.join('../images/Caves/', 'background2.png')).convert_alpha()
        self.background5 = pygame.image.load(
            os.path.join('../images/Caves/', 'background1.png')).convert_alpha()

        self.coin_frames = import_folder('../images/assets/Coin')
        self.potion_frames = import_sprite(
            '../images/assets/Potions/potion.png', 8, 24, 24, 72)
        self.statue_frames = import_sprite(
            '../images/assets/Salt.png', 1, 112, 224, 112)

        self.updateCoin = updateCoin

    def setPlayerBoxFunc(self, getPlayerBox):
        self.getPlayerBox = getPlayerBox

    def import_asset(self):
        self.goblin_asset = [
            pygame.image.load(
                os.path.join('../images/Monsters_Creatures_Fantasy/Goblin/', 'Idle.png')).convert_alpha(),
            pygame.image.load(
                os.path.join('../images/Monsters_Creatures_Fantasy/Goblin/', 'Run.png')).convert_alpha(),
            pygame.image.load(
                os.path.join('../images/Monsters_Creatures_Fantasy/Goblin/', 'Attack.png')).convert_alpha(),
            pygame.image.load(
                os.path.join('../images/Monsters_Creatures_Fantasy/Goblin/', 'Death.png')).convert_alpha(),
            pygame.image.load(
                os.path.join('../images/Monsters_Creatures_Fantasy/Goblin/', 'TakeHit.png')).convert_alpha()]

        self.skeleton = [
            pygame.image.load(
                os.path.join('../images/Monsters_Creatures_Fantasy/Skeleton/', 'Idle.png')).convert_alpha(),
            pygame.image.load(
                os.path.join('../images/Monsters_Creatures_Fantasy/Skeleton/', 'Walk.png')).convert_alpha(),
            pygame.image.load(
                os.path.join('../images/Monsters_Creatures_Fantasy/Skeleton/', 'Attack.png')).convert_alpha(),
            pygame.image.load(
                os.path.join('../images/Monsters_Creatures_Fantasy/Skeleton/', 'Shield.png')).convert_alpha(),
            pygame.image.load(
                os.path.join('../images/Monsters_Creatures_Fantasy/Skeleton/', 'Death.png')).convert_alpha(),
            pygame.image.load(
                os.path.join('../images/Monsters_Creatures_Fantasy/Skeleton/', 'TakeHit.png')).convert_alpha()
        ]

    def setup(self, level_map):
        self.import_asset()
        self.layer_group = self.setupLayer(level_map)
        for enemy in self.enemies:
            enemy.setBoundary(self.boundaries)

    def setupLayer(self, level_map):
        layer_group = {}

        ##### Layer #####
        for layer in level_map:
            if layer == 'player':
                continue
            elif layer == 'enemy_pos' or layer == 'asset':
                pos_layout = import_csv_layout(
                    level_map[layer]['csv_path'])
                self.create_enemies(pos_layout)
            else:
                terrain_layout = import_csv_layout(
                    level_map[layer]['csv_path'])
                if level_map[layer]['animated'] is False:
                    layer_group[layer] = self.create_static_tile_group(
                        terrain_layout, level_map[layer]['img_path'], layer)

        return layer_group

    def create_enemies(self, pos_layout):
        for r_idx, row in enumerate(pos_layout):
            for c_idx, cell in enumerate(row):
                if cell != '-1':
                    x_pos = c_idx*self.tile_size
                    y_pos = r_idx*self.tile_size

                    if cell == '0':
                        self.playerPos = (
                            x_pos + TILE_SIZE/2, y_pos + TILE_SIZE)
                    elif cell == '1':
                        ene = Skeleton(x_pos + TILE_SIZE/2,
                                       y_pos + TILE_SIZE, self.getPlayerBox)
                        ene.setup_sub(self.skeleton)
                        self.enemies.append(ene)
                    elif cell == '2':
                        ene = Goblin(x_pos + TILE_SIZE/2, y_pos +
                                     TILE_SIZE, self.getPlayerBox)
                        ene.setup_sub(self.goblin_asset)
                        self.enemies.append(ene)
                    elif cell == '4':
                        self.boss = boss.Boss(
                            x_pos + TILE_SIZE/2, y_pos + TILE_SIZE, self.getPlayerBox)
                    elif cell == '5':
                        self.enemies.append(Wizard(
                            x_pos + TILE_SIZE/2, y_pos + TILE_SIZE, self.getPlayerBox))
                    elif cell == '6':
                        self.boundaries.append(
                            tiles.Tile((x_pos, y_pos), TILE_SIZE))
                    elif cell == '15':
                        self.crates.append(assets.Crate(x_pos + TILE_SIZE/2,
                                                        y_pos + TILE_SIZE))
                    elif cell == '14':
                        self.assets.append(assets.Statue(x_pos + TILE_SIZE/2,
                                                         y_pos + TILE_SIZE, 112, self.statue_frames))

    def create_static_tile_group(self, layout, img_path, type):
        sprite_group = pygame.sprite.Group()
        surs = None
        if img_path != '':
            surs = import_cut_graphics(img_path)

        for r_idx, row in enumerate(layout):
            for c_idx, cell in enumerate(row):
                x_pos = c_idx*self.tile_size
                y_pos = r_idx*self.tile_size
                if cell != '-1':
                    if type == 'terrain' or type == 'ladder':
                        sprite_group.add(tiles.StaticTile(
                            (x_pos, y_pos), self.tile_size, surs[int(cell)]))

        return sprite_group

    def checkCoinCollision(self):
        for asset in self.assets:
            coinDirect = asset.getDirect()
            v_res = True if asset.rect.bottom >= asset.y else False
            if v_res:
                if abs(coinDirect.x) < 0.2:
                    coinDirect.x = 0
                if abs(coinDirect.y) < 1:
                    coinDirect.y = 0
                asset.setDirect(coinDirect.x * 0.5,
                                coinDirect.y * -0.4 - asset.weight)

    def checkPlayerCollision(self, player):
        self.checkCollision(player)
        for asset in self.assets:
            if player.getCollideBox().colliderect(asset.getCollideBox()):
                if asset.type == 'coin':
                    self.updateCoin(1)
                    asset.eaten = True
                elif asset.type == 'potion':
                    player.updateHealth(asset.heal)
                    asset.eaten = True
                elif asset.type == 'statue' and not asset.blessed and pygame.key.get_pressed()[pygame.K_e]:
                    player.allow_pray = True
                    player.updateAttack(asset.attack)
                    asset.blessed = True

    def checkCollision(self, obj):
        v_res = self.vertical_ground_collision(obj)
        h_res = self.horizontal_ground_collision(obj)
        return v_res, h_res

    def vertical_ground_collision(self, obj):
        layers = ['terrain']
        for layer in layers:
            terrain_tiles = self.layer_group[layer]
            objRect = obj.getCollideBox()
            objDirect = obj.getDirect()
            objRect.x -= objDirect.x

            tiles = terrain_tiles.sprites()
            for i in range(len(tiles)):
                tile = tiles[i]
                if tile.rect.colliderect(objRect) and objDirect.y > 0:
                    objRect.bottom = tile.rect.top
                    obj.setOnGround(True)
                    obj.setRectDisplay(objRect.x + objDirect.x, objRect.y)
                    obj.setDirect(objDirect.x, 0)
                    return True

            l = len(tiles) - 1
            for i in range(len(tiles)):
                tile = tiles[l-i]
                if tile.rect.colliderect(objRect) and objDirect.y < 0:
                    objRect.top = tile.rect.bottom + 2
                    obj.setRectDisplay(objRect.x + objDirect.x, objRect.y)
                    obj.setDirect(objDirect.x, 0)
                    return True

        obj.setOnGround(False)
        return False

    def horizontal_ground_collision(self, obj):
        layers = ['terrain']
        for layer in layers:
            terrain_tiles = self.layer_group[layer]
            objRect = obj.getCollideBox()
            objDirect = obj.getDirect()
            objRect.y -= objDirect.y

            for tile in terrain_tiles.sprites():
                if tile.rect.colliderect(objRect) and objRect.bottom > tile.rect.top:
                    if obj.direct.x > 0:
                        objRect.right = tile.rect.left - 2
                    elif obj.direct.x < 0:
                        objRect.left = tile.rect.right + 2

                    obj.setRectDisplay(objRect.x, objRect.y + objDirect.y)
                    return True

        return False

    def checkAtLadder(self, obj):
        ladder_tiles = self.layer_group['ladder']
        objRect = obj.getCollideBox()

        for tile in ladder_tiles.sprites():
            if tile.rect.colliderect(objRect):
                return True

        return False

    def update(self, deltaTime):
        self.boss.update(deltaTime)
        for enemy in self.enemies:
            enemy.update(deltaTime)
        for crate in self.crates:
            crate.update(deltaTime)
            if crate.state == 'destroy':
                for i in range(crate.coin_num):
                    crate.coin_num -= 1
                    self.assets.append(
                        assets.Coin(crate.getCenterPos(), crate.bottom_yPos, 16, self.coin_frames))

                for i in range(crate.potion_num):
                    crate.potion_num -= 1
                    self.assets.append(
                        assets.Potion(crate.getCenterPos(), crate.bottom_yPos, 24, self.potion_frames))

        for asset in self.assets:
            asset.update(deltaTime)

        for name, layer in self.layer_group.items():
            layer.update(deltaTime)

        self.enemies = [enemy for enemy in self.enemies if not enemy.delete]
        self.assets = [asset for asset in self.assets if not asset.delete]
        self.crates = [crate for crate in self.crates if not crate.delete]

        self.checkCoinCollision()

        # self.water.update(deltaTime)

    def checkEnemyVsPlayer(self, player):
        player.attack(self.boss)
        self.boss.attack(player)
        for crate in self.crates:
            player.attack(crate)
        for enemy in self.enemies:
            player.attack(enemy)
            enemy.attack(player)

    def show_enemy_health(self, show_health, cx, cy):
        show_health((self.boss.rect.centerx + 50 - cx, self.boss.rect.y - 20 - cy),
                    self.boss.health, self.boss.max_health)

        for enemy in self.enemies:
            if enemy.visible:
                show_health((enemy.rect.centerx - 25 - cx, enemy.rect.y - 20 - cy),
                            enemy.health, enemy.max_health)

    def drawBackground(self, win, cx, cy):
        win.blit(self.background5, (-cx*0.3, -cy * 0.3))
        win.blit(self.background4, (-cx*0.5, -cy * 0.5))
        win.blit(self.background3, (-cx*0.8, -cy*0.8))
        win.blit(self.background1, (-cx, -cy))

    def draw(self, win, cx, cy):
        self.drawBackground(win, cx, cy)
        for name, layer in self.layer_group.items():
            for tile in layer:
                tile.draw(win, cx, cy)

        for crate in self.crates:
            crate.draw(win, cx, cy)

        for enemy in self.enemies:
            enemy.draw(win, cx, cy)

        for asset in self.assets:
            asset.draw(win, cx, cy)

        self.boss.draw(win, cx, cy)
