import os, time, pygame
# Load our scenes
from states.title import Title

class Game():
        def __init__(self):
            pygame.init()
            pygame.display.set_caption("MiMiz")
            self.GAME_W,self.GAME_H = 1920/2, 1280/2
            self.SCREEN_WIDTH = pygame.display.Info().current_w * 6 // 8
            self.SCREEN_HEIGHT = self.SCREEN_WIDTH * 2//3
            self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
            self.running, self.playing = True, True
            self.actions = {"left": False, "right": False, "up" : False, "down" : False, "action1" : False, "action2" : False, "start" : False}
            self.dt, self.prev_time = 0, 0
            self.cat, self.difficulty = 0, 0
            self.state_stack = []
            self.load_assets()
            self.load_states()
            self.load_sfx()

            #GAME RESULTS:
            self.stars = 1
            self.final_time = [0,0,0]
            
            
            pygame.mixer.music.load('assets/sfx/menu-bgm.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.8)


            print(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        def game_loop(self):
            while self.playing:
                self.get_dt()
                self.get_events()
                self.update()
                self.render()

        def get_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.playing = False
                        self.running = False
                    elif event.key == pygame.K_LEFT:
                        self.actions['left'] = True
                    elif event.key == pygame.K_RIGHT:
                        self.actions['right'] = True
                    elif event.key == pygame.K_UP:
                        self.actions['up'] = True
                    elif event.key == pygame.K_DOWN:
                        self.actions['down'] = True
                    elif event.key == pygame.K_p:
                        self.actions['action1'] = True
                    elif event.key == pygame.K_o:
                        self.actions['action2'] = True    
                    elif event.key == pygame.K_RETURN:
                        self.actions['start'] = True  

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.actions['left'] = False
                    elif event.key == pygame.K_RIGHT:
                        self.actions['right'] = False
                    elif event.key == pygame.K_UP:
                        self.actions['up'] = False
                    elif event.key == pygame.K_DOWN:
                        self.actions['down'] = False
                    elif event.key == pygame.K_p:
                        self.actions['action1'] = False
                    elif event.key == pygame.K_o:
                        self.actions['action2'] = False
                    elif event.key == pygame.K_RETURN:
                        self.actions['start'] = False  

        def update(self):
            self.state_stack[-1].update(self.dt,self.actions)

        def render(self):
            self.state_stack[-1].render(self.game_canvas)
            # Render current state to the screen
            render = pygame.transform.scale(self.game_canvas, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.screen.blit(render, (0,0))
            pygame.display.flip()


        def get_dt(self):
            now = time.time()
            self.dt = now - self.prev_time
            self.prev_time = now

        # def draw_text(self, surface, text, color, x, y):
        #     text_surface = self.font.render(text, True, color)
        #     #text_surface.set_colorkey((0,0,0))
        #     text_rect = text_surface.get_rect()
        #     text_rect.center = (x, y)
        #     surface.blit(text_surface, text_rect)

        def load_assets(self):
            # Create pointers to directories 
            self.font = pygame.font.Font('assets/slkscr.ttf', 50)
            self.bigFont = pygame.font.Font('assets/slkscr.ttf', 42)
            self.assets_dir = os.path.join("assets")
            # self.sprite_dir = os.path.join(self.assets_dir, "sprites")
            # self.font_dir = os.path.join(self.assets_dir, "font")
            # self.font= pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 20)

        def load_states(self):
            self.title_screen = Title(self)
            self.state_stack.append(self.title_screen)

        def reset_keys(self):
            for action in self.actions:
                self.actions[action] = False

        def load_sfx(self):
            self.button_sfx = pygame.mixer.Sound('assets/sfx/buttonselectsfx.mp3')
            self.collect_sfx = pygame.mixer.Sound('assets/sfx/collect-food.mp3')
            self.final_sfx = pygame.mixer.Sound('assets/sfx/final-screen.mp3')
            self.loading_bgm = pygame.mixer.Sound('assets/sfx/loading-bgm.mp3')
            self.maze_bgm = pygame.mixer.Sound('assets/sfx/maze-bgm.mp3')
            self.menu_bgm = pygame.mixer.Sound('assets/sfx/menu-bgm.mp3')
            self.door_sfx = pygame.mixer.Sound('assets/sfx/open-door.mp3')

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()