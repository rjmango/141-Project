import pygame, button
from states.state import State
from states.loading_screen import Loading_Screen

class Difficulty(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.load_assets()

        #time which the cat last flickered
        self.last_update = pygame.time.get_ticks()

        #buttons
        self.buttons = [ button.Button(0,0, self.easy, 5),
                         button.Button(0,0, self.medium, 5),
                         button.Button(0,0, self.hard, 5)
                       ]

        #button highlighted value
        self.highlighted = 1

    def update(self, delta_time, actions):
        if actions["start"]:
            self.game.button_sfx.play()
            new_state = Loading_Screen(self.game)
            self.exit_state()
            self.exit_state()
            new_state.enter_state()

            pygame.mixer.music.stop()
            pygame.mixer.music.load('assets/sfx/loading-bgm.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.8)

        if actions["right"]:
            self.game.difficulty = (self.game.difficulty + 1) % 3

        if actions["left"]:
            self.game.difficulty = (self.game.difficulty - 1) % 3
        self.game.reset_keys()
        self.animate()

    def render(self, display):
        display.blit(self.bg, (0,0))

        if self.highlighted:
            self.buttons[self.game.difficulty].draw(display)

    def load_assets(self):
        self.bg = pygame.image.load("assets/bg/selectdiff-bg.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (self.game.GAME_W, self.game.GAME_H))

        self.easy = pygame.image.load("assets/buttons/easy-highlight.png").convert_alpha()
        self.medium = pygame.image.load("assets/buttons/medium-highlight.png").convert_alpha()
        self.hard = pygame.image.load("assets/buttons/hard-highlight.png").convert_alpha()

    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= 500:
            self.highlighted = (self.highlighted + 1) % 2
            self.last_update = current_time
