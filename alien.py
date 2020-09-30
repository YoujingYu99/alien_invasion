import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''A class of individual aliens'''

    def __init__(self, ai_settings, screen):
        '''initialise aliens and set initial positions'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #load alien image
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        #each alien is at the top left corner of the screen initially
        self.x = self.rect.width
        self.y = self.rect.height

        #save the floating point number of the alien position
        self.x = float(self.rect.x)

    def check_edges(self):
        '''if alien at screen edge, return True'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True



    def update(self):
        '''move alien to the left or right'''
        self.x += (self.ai_settings.alien_speed_factor *
            self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        '''draw aliens at set positions'''
        self.screen.blit(self.image, self.rect)
