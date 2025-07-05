class Settings:
    def __init__(self):
        self.screen_width = 1980
        self.screen_height = 1020
        self.bg_color = (20, 150, 50)
        self.button_color = (255, 255, 100)

        
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

        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        self.increase_speed


    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.soldier_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.zombie_speed_factor = 1.0 
        self.zombie_direction = 1 #1 - вверх, -1 - вниз 
        self.zombie_points = 1
        self.score_scale = 1.5  # Коэффициент увеличения очков за зомби
        


    def increase_speed(self):
        """Увеличивает настройки скорости."""
        self.soldier_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.zombie_speed_factor *= self.speedup_scale

        self.zombie_points = int(self.zombie_points * self.score_scale)

        print("score", self.zombie_points)
