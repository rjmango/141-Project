import pygame, spritesheet, random, prims
from states.state import State
from states.finish_screen import Finish_Screen

TILESIZE = 64
PLAYERSIZE = 64
import random


MAP = prims.maze_array

class Game_World(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.newMap()
        self.load_assets()
        self.generateFood()

        #Generate player
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 14)
            if MAP[x][y] == 0:
                self.player = Player(game, self, y, x)
                MAP[x][y] = 3
                break
        
        #Generate exits
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 14)
            if MAP[x][y] == 0:
                End(self, self.game, y, x)
                MAP[x][y] = 3
                break

        self.time = [0,0,0]
        self.second = 0
        self.text = self.game.font.render(f'{self.time[0]}:{self.time[1]}:{self.time[2]}', False, (255,0,0))
        self.textRect = self.text.get_rect()
        self.textRect.center = self.game.GAME_W // 2, 600

        self.rating = [[[0, 0, 30], [0, 0, 40], [0, 0, 50]],        #EASY 3 2 1
                       [[0, 0, 40], [0, 0, 50], [0, 1,00]] ,        #MEDIUM 3 2 1 
                       [[0, 0, 50], [0, 1, 00] , [0, 1, 10]] ]      #HARD 3 2 1
          
        self.start = False
        self.playing = True

    def generateFood(self):
        self.current_food = 0
        self.food_count = 4 + 5 * self.game.difficulty
        
        i = self.food_count
        while(i != 0):
            x = random.randint(0,14)
            y = random.randint(0, 9)
            if x == 0 and y == 0:
                pass
            elif x == 14 and y == 9:
                pass
            elif MAP[y][x] == 0:
                Food(self, self.game, x,y)
                MAP[y][x] = 2
                i -= 1

    def newMap(self):
        self.all_sprites = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()
        self.finish = pygame.sprite.Group()
        for i in range (0, int(self.game.GAME_W/TILESIZE)):
            for j in range (0, int(self.game.GAME_H/TILESIZE)):
                Background(self,i,j)

        for i in range(10):
            for j in range(15):
                if MAP[i][j] == 1:
                    Wall(self, j, i)

    def update(self, delta_time, actions):
        if not self.playing:
            self.game.final_time = self.time
            for i in range(3):
                print(self.time, self.rating[self.game.difficulty][i])
                if self.time < self.rating[self.game.difficulty][i]:
                    self.game.stars = 3 - i
                    print(self.game.stars)
                    break
            pygame.mixer.music.stop()
            pygame.mixer.music.load('assets/sfx/final-screen.mp3')
            pygame.mixer.music.play(2)
            pygame.mixer.music.set_volume(0.8)
            new_state = Finish_Screen(self.game)
            self.exit_state()
            new_state.enter_state()



        self.second += delta_time
        if self.start and self.second > 1:
            self.second = 0
            self.time[2] += 1
            if self.time[2] == 60:
                self.time[2] = 0
                self.time[1] += 1
            if self.time[1] == 60: 
                self.time[1] = 0
                self.time[0] += 1
            self.text = self.game.font.render(f'{self.time[0]}:{self.time[1]}:{self.time[2]}', False, (0,0,0))

        self.player.update(delta_time, actions)
        self.foods.update(delta_time)
        self.finish.update(delta_time)
        
    def render(self, display):
        display.blit(self.grass_img, (0,0))
        self.background.draw(display)
        self.finish.draw(display)
        self.player.render(display)
        self.walls.draw(display)
        self.foods.draw(display)
        display.blit(self.text, self.textRect)
    
    def load_assets(self):
        self.grass_img = pygame.image.load("assets/map/grass-map.png").convert_alpha()
        self.grass_img = pygame.transform.scale(self.grass_img, (self.game.GAME_W, self.game.GAME_H))

class Player(pygame.sprite.Sprite):
    def __init__(self,game, game_world, x, y):
        self.game = game
        self.world = game_world
        self.groups = self.world.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.load_sprites()
        self.position_x, self.position_y = x * TILESIZE, y * TILESIZE
        self.size_x, self.size_y = PLAYERSIZE, PLAYERSIZE
        self.current_frame, self.last_frame_update = 0,0
        self.image = pygame.transform.scale(self.curr_image, (self.size_x,self.size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position_x, self.position_y)
        self.rect.width = PLAYERSIZE - 10
        self.rect.height = PLAYERSIZE - 20
        
    def update(self,delta_time, actions):
        self.direction_x, self.direction_y = 0, 0 
        # Get the direction from inputs
        if actions["right"]:
            self.direction_x = 1
            self.world.start = True
        elif actions["left"]:
            self.direction_x = -1
            self.world.start = True
        elif actions["down"]:
            self.direction_y = 1
            self.world.start = True
        elif actions["up"]:
            self.direction_y = -1
            self.world.start = True

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
        self.world.all_sprites.draw(display)
        # pygame.draw.rect(display, (255,255,255), self.rect, 2)

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
        if self.last_frame_update > .09:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame +1) % len(self.curr_anim_list)
            self.curr_image = self.curr_anim_list[self.current_frame]

    def load_sprites(self):
        self.front_sprites, self.back_sprites, self.right_sprites, self.left_sprites = [],[],[],[]
        
        self.front_animation = pygame.image.load(f'assets/characters/cat/cat{self.game.cat}-front.png')
        self.back_animation = pygame.image.load(f'assets/characters/cat/cat{self.game.cat}-back.png')
        self.left_animation = pygame.image.load(f'assets/characters/cat/cat{self.game.cat}-left.png')
        self.right_animation = pygame.image.load(f'assets/characters/cat/cat{self.game.cat}-right.png')

        self.front_spritesheet = spritesheet.SpriteSheet(self.front_animation)
        self.back_spritesheet = spritesheet.SpriteSheet(self.back_animation)
        self.left_spritesheet = spritesheet.SpriteSheet(self.left_animation)
        self.right_spritesheet = spritesheet.SpriteSheet(self.right_animation)

        for i in range(15):
            self.front_sprites.append(self.front_spritesheet.get_image(i, 1600, 1600, 1, None))
            self.back_sprites.append(self.back_spritesheet.get_image(i, 1600, 1600, 1, None))

        for i in range(4):
            self.left_sprites.append(self.left_spritesheet.get_image(i, 1600, 1600, 1, None))
            self.right_sprites.append(self.right_spritesheet.get_image(i, 1600, 1600, 1, None))

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
        wall_bg = ["bush1", "bush2a", "bush2b", "fence", "fence", "trash", "house1a", "house2a"]        
        bg_index = random.randint(0, len(wall_bg)-1)
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        #background image and surface
        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.bg = pygame.image.load(f'assets/map/obstacle/{wall_bg[bg_index]}.png')
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
        wall_bg = ["grass1", "grass2", "grass3", "ground2", "tiletile", "tiletile2", "tiletile3", "tiletile4"]        
        bg_index = random.randint(0, len(wall_bg)-1)
        self.groups = game.background
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        #background image and surface
        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.bg = pygame.image.load(f'assets/map/bg/{wall_bg[bg_index]}.png')
        self.bg = pygame.transform.scale(self.bg, (TILESIZE, TILESIZE))
        self.image.blit(self.bg, (0,0))
        self.rect = self.image.get_rect()

        #coordinates
        self.x = x
        self.y = y

        #rectangle
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Food(pygame.sprite.Sprite):
    def __init__(self, game_world, game, x, y):
        self.groups = game_world.foods
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.current_frame, self.last_frame_update = 0, 0
        self.world = game_world
        self.game = game
        self.load_sprites()

        self.image = pygame.transform.scale(self.curr_img, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self, delta_time):
        self.collidePlayer()
        self.last_frame_update += delta_time
        if self.last_frame_update > .09:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame +1) % len(self.food_sprites)
            self.curr_img = self.food_sprites[self.current_frame]
        self.image = pygame.transform.scale(self.curr_img, (TILESIZE, TILESIZE))

    def collidePlayer(self):
        hits = pygame.sprite.spritecollide(self, self.world.all_sprites, False)
        if hits:
            self.game.collect_sfx.play()
            self.kill()
            self.world.current_food += 1
        if self.world.current_food == self.world.food_count:
            self.game.door_sfx.play()


    def load_sprites(self):
        food_types = ['cake', 'popsicle', 'cake2', 'donut']
        cat = self.game.cat
        self.food_sprites = []
        self.food_bg = pygame.image.load(f'assets/map/food/{food_types[cat]}.png')
        self.food_spritesheet = spritesheet.SpriteSheet(self.food_bg)

        for i in range(6):
            self.food_sprites.append(self.food_spritesheet.get_image(i, 1600, 1600, 1, None))
            
        self.curr_img = self.food_sprites[0]

class End(pygame.sprite.Sprite):
    def __init__(self, game_world, game, x, y):
        self.groups = game_world.finish
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.current_frame, self.last_frame_update = 0, 0
        self.world = game_world
        self.game = game
        self.load_sprites()

        self.image = pygame.transform.scale(self.curr_img, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self, delta_time):
        self.collidePlayer()

        self.last_frame_update += delta_time
        if self.world.current_food == self.world.food_count:
            if self.last_frame_update > .09 and self.current_frame != len(self.door_sprites) - 1:
                self.last_frame_update = 0
                self.current_frame = self.current_frame +1 % len(self.door_sprites)
                self.curr_img = self.door_sprites[self.current_frame]
            elif self.current_frame == len(self.door_sprites) - 1:
                self.curr_img = len(self.door_sprites) - 1
                self.curr_img = self.door_sprites[-1]
            self.image = pygame.transform.scale(self.curr_img, (TILESIZE, TILESIZE))

    def collidePlayer(self):
        hits = pygame.sprite.spritecollide(self, self.world.all_sprites, False)
        if hits:
            if self.world.current_food == self.world.food_count:
                self.world.playing = False

    def load_sprites(self):
        self.door_sprites = []
        self.door_bg = pygame.image.load(f'assets/map/finish-door.png')
        self.door_spritesheet = spritesheet.SpriteSheet(self.door_bg)

        for i in range(15):
            self.door_sprites.append(self.door_spritesheet.get_image(i, 64, 64, 1, None))
            
        self.curr_img = self.door_sprites[0]