import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from ship import Ship
from button import Button
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
    #initialise the game
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
        ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #create the "Play" button
    play_button = Button(ai_settings, screen, "Play")
    #creat a ship, a bullet group and an alien group
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #create an object that stores game statistics and a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    #start the main loop
    while True:

        #monitor the mouse and keyboard activities
        gf.check_events(ai_settings, screen, stats, sb, play_button,
            ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship,
                aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
            play_button)

run_game()
