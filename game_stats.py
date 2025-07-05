from settings import Settings

class GameStats():
    """Отслеживание статистики для игры Alien Invasion."""
    def __init__(self, zk_game):
        """Инициализирует статистику."""
        self.settings = zk_game.settings
        self.game_active = False
        self.high_score = 0
        

        self.reset_stats()

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.soldier_health = self.settings.soldier_health
        self.score = 0
        self.level = 1