class GameStats():
    '''follow the game statistics'''

    def __init__(self, ai_settings):
        '''initialise statistical info'''
        self.ai_settings = ai_settings
        self.reset_stats()
        #set the game to inactive state initially
        self.game_active = False
        #highest score will not be reset
        self.high_score = 0

    def reset_stats(self):
        '''initialise stats that may change'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
