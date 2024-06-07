import pygame
from states.state import State

TILESIZE = 64
PLAYERSIZE = 40

MAP = [   [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
          [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
          [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
          [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
          [1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0],
          [1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
          [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
          [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
          [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
          [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0] ]

class Game_World(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.newMap()
        self.player = Player(game, self)
        self.load_assets()
    
    def newMap(self):
        self.all_sprites = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        print(int(self.game.GAME_W/TILESIZE), int(self.game.GAME_H/TILESIZE))
        for i in range (0, int(self.game.GAME_W/TILESIZE)):
            for j in range (0, int(self.game.GAME_H/TILESIZE)):
                Background(self,i,j)

        for i in range(10):
            for j in range(15):
                print(MAP[i][j], end = " ")
                if MAP[i][j] == 1:
                    Wall(self, j, i)
            print()

    def update(self, delta_time, actions):
        self.player.update(delta_time, actions)
        
    def render(self, display):
        display.blit(self.grass_img, (0,0))
        self.background.draw(display)
        self.walls.draw(display)
        self.player.render(display)
    
    def load_assets(self):
        self.grass_img = pygame.image.load("assets/map/grass-map.png").convert_alpha()
        self.grass_img = pygame.transform.scale(self.grass_img, (self.game.GAME_W, self.game.GAME_H))


class Player(pygame.sprite.Sprite):
    def __init__(self,game, game_world):
        self.game = game
        self.world = game_world
        self.groups = self.world.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.load_sprites()
        self.position_x, self.position_y = 0,0
        self.size_x, self.size_y = PLAYERSIZE, PLAYERSIZE
        self.current_frame, self.last_frame_update = 0,0
        self.image = pygame.transform.scale(self.curr_image, (self.size_x,self.size_y))
        self.rect = self.image.get_rect(center = (10,10))
        self.rect.width = PLAYERSIZE - 10
        self.rect.height = PLAYERSIZE - 5
        
    def update(self,delta_time, actions):
        
        self.direction_x, self.direction_y = 0, 0 
        # Get the direction from inputs
        if actions["right"]:
            self.direction_x = 1
        elif actions["left"]:
            self.direction_x = -1
        elif actions["down"]:
            self.direction_y = 1
        elif actions["up"]:
            self.direction_y = -1

        # Update the position
        self.position_x += 200 * delta_time * self.direction_x
        self.position_y += 200 * delta_time * self.direction_y
        self.rect.topleft = (self.position_x, self.position_y)

        self.collide_with_walls('x')
        self.collide_with_walls('y')

        if self.position_x < 0:
            self.position_x = 0
        if self.position_x + self.size_x > self.game.GAME_W:
            self.position_x = self.game.GAME_W - self.size_x
        if self.position_y < 0:
            self.position_y = 0
        if self.position_y + self.size_y > self.game.GAME_H:
            self.position_y = self.game.GAME_H - self.size_y
            
        # Animate the sprite
        self.animate(delta_time, self.direction_x, self.direction_y)

    def render(self, display):
        self.image = pygame.transform.scale(self.curr_image, (self.size_x,self.size_y))
        # display.blit(self.image, (self.position_x,self.position_y))
        self.world.all_sprites.draw(display)
        pygame.draw.rect(display, (255,255,255), self.rect, 2)

    def animate(self, delta_time, direction_x, direction_y):

        # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        # If no direction is pressed, set image to idle and return
        if not (direction_x or direction_y): 
            self.curr_image = self.curr_anim_list[0]
            return
        # If an image was pressed, use the appropriate list of frames according to direction
        if direction_x:
            if direction_x > 0: self.curr_anim_list = self.right_sprites
            else: self.curr_anim_list = self.left_sprites
        if direction_y:
            if direction_y > 0: self.curr_anim_list = self.front_sprites
            else: self.curr_anim_list = self.back_sprites
        # Advance the animation if enough time has elapsed
        if self.last_frame_update > .15:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame +1) % len(self.curr_anim_list)
            self.curr_image = self.curr_anim_list[self.current_frame]

    def load_sprites(self):
        self.front_sprites, self.back_sprites, self.right_sprites, self.left_sprites = [],[],[],[]
        # Load in the frames for each direction
        for i in range(1,5):
            self.front_sprites.append(pygame.image.load("assets/characters/player/player_front" + str(i) +".png"))
            self.back_sprites.append(pygame.image.load("assets/characters/player/player_back" + str(i) +".png"))
            self.right_sprites.append(pygame.image.load("assets/characters/player/player_right" + str(i) +".png"))
            self.left_sprites.append(pygame.image.load("assets/characters/player/player_left" + str(i) +".png"))
        # Set the default frames to facing front
        self.curr_image = self.front_sprites[0]
        self.curr_anim_list = self.front_sprites


    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.world.walls, False)
            if hits:
                if self.direction_x > 0:
                    self.position_x = hits[0].rect.left - self.rect.width
                if self.direction_x < 0:
                    self.position_x = hits[0].rect.right
                # self.direction_x = 0
                self.rect.x = self.position_x

        elif dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.world.walls, False)
            if hits:
                if self.direction_y > 0:
                    self.position_y = hits[0].rect.top - self.rect.height
                if self.direction_y < 0:
                    self.position_y = hits[0].rect.bottom
                # self.direction_y = 0
                self.rect.y = self.position_y

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        #background image and surface
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.bg = pygame.image.load("assets/map/tiles/bush2a.png")
        self.bg = pygame.transform.scale(self.bg, (TILESIZE, TILESIZE))
        self.image.blit(self.bg, (0,0))
        self.rect = self.image.get_rect()

        #coordinates
        self.x = x
        self.y = y

        #rectangle
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class Background(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.background
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        #background image and surface
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.bg = pygame.image.load("assets/map/tiles/grass2.png")
        self.bg = pygame.transform.scale(self.bg, (TILESIZE, TILESIZE))
        self.image.blit(self.bg, (0,0))
        self.rect = self.image.get_rect()

        #coordinates
        self.x = x
        self.y = y

        #rectangle
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        