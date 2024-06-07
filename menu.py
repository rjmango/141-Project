import pygame, spritesheet
from states.state import State

class Menu(State):
    def __init__(self, game):
        # Buttons
        # start_img = pygame.image.load("assets/buttons/start-button.png").convert_alpha()
        # about_img = pygame.image.load("assets/buttons/about-button.png").convert_alpha()

        State.__init__(self, game)

        #Load Background animation
        # each frame is 1024x1536
        background_animation = pygame.image.load("assets/bg/mingwindow-bg.png").convert_alpha()
        self.background_spritesheet = spritesheet.SpriteSheet(background_animation)

        #create animation list
        self.animation_list = []
        self.animation_steps = 14
        self.last_update = pygame.time.get_ticks()
        self.animation_delay = 150
        self.frame = 0

        for x in range(self.animation_steps):
            self.animation_list.append(self.background_spritesheet.get_image(x, 1536, 1024, 0.625, None))


    def update(self, delta_time, actions):
        if actions["start"]:
            print("Enter")
        self.animate()



    def render(self):
        #load background
        self.screen.blit(self.animation_list[self.frame], (0,0))

        #update background
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_delay:
            self.frame = (self.frame + 1) % self.animation_steps
            self.last_update = current_time