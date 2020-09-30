class Settings():
    '''save all the class in the game'''

    def __init__(self):
        '''set the initial mode'''
        #set the screen
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_colour = (230,230,230)
        self.ship_limit = 3

        #set the bullet
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (60,60,60)
        self.bullets_allowed = 3

        #set the aliens
        self.alien_drop_factor = 10

        #increase the speed of game
        self.speedup_scale = 1.1
        #increase score of aliens
        self.score_scale = 1.5

        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        ''' initialise settings that change with game'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        #fleet dir = 1 means moving right, -1 means moving left
        self.fleet_direction = 1

        #keeping score
        self.alien_points = 50

    def increase_speed(self):
        '''set to a higher speed and score'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
