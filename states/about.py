import pygame, spritesheet
from states.state import State
from states.about2 import About2

class About(State):
    def __init__(self, game):
        State.__init__(self, game)

        #Load Background animation
        # each frame is 1344x896
        background_animation = pygame.image.load("assets/bg/aboutussprite1.png").convert_alpha()
        self.background_spritesheet = spritesheet.SpriteSheet(background_animation)

        #create animation list
        self.animation_list = []
        self.animation_steps = 48
        self.last_update = pygame.time.get_ticks()
        self.animation_delay = 75
        self.frame = 0

        for x in range(self.animation_steps):
            frame = pygame.transform.scale(self.background_spritesheet.get_image(x, 1344, 896, 0.625, None), (self.game.GAME_W, self.game.GAME_H))
            self.animation_list.append(frame)
    
    def update(self, delta_time, actions):
        if actions["start"]:
            self.game.button_sfx.play()
            new_state = About2(self.game)
            self.exit_state()
            new_state.enter_state()
        self.animate()
        self.game.reset_keys()
    
    def render(self, display):
        #load background
        display.blit(self.animation_list[self.frame], (0,0))

    def animate(self):
        #update background
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_delay:
            self.frame = (self.frame + 1) % self.animation_steps
            self.last_update = current_time
