import pygame, button
from states.state import State
from states.difficulty import Difficulty

class Select(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.load_assets()

        #buttons
        self.buttons =  [ button.Button(0, 0, self.ragdoll, 5),
                          button.Button(0, 0, self.siamiese, 5),
                          button.Button(0, 0, self.tilapia, 5),
                          button.Button(0, 0, self.tuxedo, 5)
                        ]

        #time which the cat last flickered
        self.last_update = pygame.time.get_ticks()

        #check if cat is highlighted
        self.highlighted = 1

    def update(self, delta_time, actions):
        if actions["start"]:
            self.game.button_sfx.play()
            next_state = Difficulty(self.game)
            next_state.enter_state()

        if actions["right"]:
            self.game.cat = (self.game.cat + 1) % 4

        if actions["left"]:
            self.game.cat = (self.game.cat - 1) % 4

        self.game.reset_keys()
        self.animate()

    def render(self, display):
        display.blit(self.bg, (0,0))

        if self.highlighted:
            self.buttons[self.game.cat].draw(display)

    def load_assets(self):
        #background image
        self.bg = pygame.image.load("assets/bg/select-cat.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (self.game.GAME_W, self.game.GAME_H))

        #cat images
        self.ragdoll = pygame.image.load("assets/characters/ragdoll-highlight.png").convert_alpha()
        self.siamiese = pygame.image.load("assets/characters/siamese-highlight.png").convert_alpha()
        self.tilapia = pygame.image.load("assets/characters/tilapia-highlight.png").convert_alpha()
        self.tuxedo = pygame.image.load("assets/characters/tuxedo-highlight.png").convert_alpha()
    
    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= 500:
            self.highlighted = (self.highlighted + 1) % 2
            self.last_update = current_time