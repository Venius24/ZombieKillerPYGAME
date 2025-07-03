class Settings:
    def __init__(self):
        self.screen_width = 1980
        self.screen_height = 1020
        self.bg_color = (20, 150, 5)

        
        self.soldier_speed = 6
        self.soldier_health = 3

        self.zombie_min_speed = 0.7
        self.zombie_max_speed = 0.5
        self.zombie_drop_speed = 2
        self.zombie_direction = 1 #1 - вверх, -1 - вниз 
        self.zombie_color = (215, 200, 50)
        self.zombie_crowd_size = 5

        self.bullets_allowed = 15
        self.bullet_speed = 5
        self.bullet_width = 50
        self.bullet_height = 10
        self.bullet_color = (230, 100, 150)
