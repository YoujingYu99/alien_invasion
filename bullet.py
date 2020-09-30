import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''a class that manages the bullets'''

    def __init__(self,ai_settings, screen, ship):
        '''create a bullet object at the ship'''
        super().__init__()
        self.screen = screen

        #create a rectangle at (0,0) then move it to the ship
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #save the y axis of bullet as floating point numbers
        self.y = float(self.rect.y)

        self.colour = ai_settings.bullet_colour
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        '''move bullet up'''
        #update the y-axis of bullet position
        self.y -= self.speed_factor
        #update the rect value of bullet position
        self.rect.y = self.y

    def draw_bullet(self):
        '''draw bullet on screen'''
        pygame.draw.rect(self.screen, self.colour, self.rect)
