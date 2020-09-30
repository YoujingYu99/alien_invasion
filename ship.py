import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self,ai_settings,screen):
        '''initialise ship and set its initial position'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #load the image and get the rectangle
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #put each new ship at the bottom center of the page
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #add floating numbers to the centerx
        self.center = float(self.rect.centerx)

        #move sign
        self.moving_right = False
        self.moving_left = False

    def update(self):
        ''' adjust the position of ship based on sign'''
        #update the center value, not rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        #update rect based on self.center
        self.rect.centerx = self.center

    def blitme(self):
        '''draw ships at positions'''
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        ''' put ship at center of the screen'''
        self.center = self.screen_rect.centerx
