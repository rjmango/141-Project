import pygame, spritesheet
from states.state import State

class Finish_Screen(State):
    def __init__(self, game):
        State.__init__(self, game)

        #Load Background animation
        # each frame is 1152x768
        background_animation = pygame.image.load(f'assets/bg/congrats-{self.game.stars}star.png').convert_alpha()
        self.background_spritesheet = spritesheet.SpriteSheet(background_animation)

        #create animation list
        self.animation_list = []
        self.animation_steps = 51
        self.last_update = pygame.time.get_ticks()
        self.animation_delay = 150
        self.frame = 0

        self.text = self.game.bigFont.render(f'{self.game.final_time[0]}:{self.game.final_time[1]}:{self.game.final_time[2]}', False, (0,0,0))
        self.textRect = self.text.get_rect()
        self.textRect.center = 526 // 2, 390

        for x in range(self.animation_steps):
            frame = pygame.transform.scale(self.background_spritesheet.get_image(x, 1152, 768, 0.625, None), (self.game.GAME_W, self.game.GAME_H))
            self.animation_list.append(frame)
    
    def update(self, delta_time, actions):
        if actions["start"]:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('assets/sfx/menu-bgm.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.8)
            self.exit_state()
        self.animate()
        self.game.reset_keys()
    
    def render(self, display):
        #load background
        display.blit(self.animation_list[self.frame], (0,0))
        display.blit(self.text, self.textRect)

    def animate(self):
        #update background
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_delay:
            if self.frame == self.animation_steps - 1:
                self.frame = (self.frame - 1)
            elif self.frame == self.animation_steps - 2:
                self.frame = (self.frame + 1)
            else:
                self.frame = (self.frame + 1) % self.animation_steps
                self.last_update = current_time
