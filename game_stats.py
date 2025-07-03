from settings import Settings

class GameStats():
    """Отслеживание статистики для игры Alien Invasion."""
    def __init__(self, zk_game):
        """Инициализирует статистику."""
        self.settings = zk_game.settings     
        self.reset_stats()

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.soldier_health = self.settings.soldier_health