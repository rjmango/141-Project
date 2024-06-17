import pygame
from states.state import State

class About2(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.bg = pygame.image.load("assets/bg/aboutus2.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (1920/2, 1280/2))

    def update(self, delta_time, actions):
        if actions["start"]:
            self.game.button_sfx.play()
            self.exit_state()
        self.game.reset_keys()
    
    def render(self, display):
        #load background
        display.blit(self.bg, (0,0))
