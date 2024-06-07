import pygame, spritesheet, button
from states.state import State
from states.about import About
from states.select import Select

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.load_assets()

        #create animation list
        self.animation_list = []
        self.animation_steps = 14
        self.last_update = pygame.time.get_ticks()
        self.animation_delay = 150
        self.frame = 0

        for x in range(self.animation_steps):
            self.animation_list.append(self.background_spritesheet.get_image(x, 1536, 1024, 0.625, None))

        #pointer to current hovered button
        self.hovered_button = 0
        self.pointed = 0

        #time which the button last flickered
        self.last_btn_update = pygame.time.get_ticks()

        # buttons
        self.buttons = [ [ button.Button( 0, 0, self.start_hovered1, 5),
                           button.Button( 0, 0, self.start_hovered2, 5)
                         ],
                         [ button.Button( 0, 0, self.about_hovered1, 5), 
                           button.Button( 0, 0, self.about_hovered2, 5)
                         ],
                         [ button.Button( 0, 0 , self.quit_hovered1, 5), 
                           button.Button( 0, 0 , self.quit_hovered2, 5),
                         ]
                       ]

        self.god_btn = button.Button( 0, 0, self.god_img, 5)
       
    def update(self, delta_time, actions):
        if actions["start"]:
            self.game.button_sfx.play()
            if self.hovered_button == 0:
                new_state = Select(self.game)
                new_state.enter_state()
            elif self.hovered_button == 1:
                new_state = About(self.game)
                new_state.enter_state()
            elif self.hovered_button == 2:
                self.game.running = False
                self.game.playing = False

        if actions["down"]:
            self.hovered_button = (self.hovered_button + 1) % 3

        if actions["up"]:
            self.hovered_button = (self.hovered_button - 1) % 3

        self.animate()
        self.animate_button()
        self.game.reset_keys()

    def render(self, display):
        #load background
        display.blit(self.animation_list[self.frame], (0,0))
        display.blit(self.logo, (0,0))

        self.god_btn.draw(display)
        self.buttons[self.hovered_button][self.pointed].draw(display)

    def animate(self):
        #update background
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_delay:
            self.frame = (self.frame + 1) % self.animation_steps
            self.last_update = current_time

    def animate_button(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_btn_update >= 500:
            self.pointed = (self.pointed + 1) % 2
            self.last_btn_update = current_time
    
    def load_assets(self):
        
        #Load Background animation
        # each frame is 1024x1536
        background_animation = pygame.image.load("assets/bg/mingwindow-bg.png").convert_alpha()
        self.background_spritesheet = spritesheet.SpriteSheet(background_animation)

        #logo
        self.logo = pygame.image.load("assets/buttons/MIMIZ.png").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (self.game.GAME_W, self.game.GAME_H))

        # Buttons
        self.god_img = pygame.image.load("assets/buttons/title-buttons.png").convert_alpha()
 
        #hovered buttons
        self.start_hovered1 = pygame.image.load("assets/buttons/start-hovered1.png").convert_alpha()
        self.start_hovered2 = pygame.image.load("assets/buttons/start-hovered2.png").convert_alpha()
        self.about_hovered1 = pygame.image.load("assets/buttons/about-hovered1.png").convert_alpha()
        self.about_hovered2 = pygame.image.load("assets/buttons/about-hovered2.png").convert_alpha()
        self.quit_hovered1 = pygame.image.load("assets/buttons/quit-hovered1.png").convert_alpha()
        self.quit_hovered2 = pygame.image.load("assets/buttons/quit-hovered2.png").convert_alpha()
