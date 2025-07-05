import pygame
import pygame.font
from pygame.sprite import Group
from settings import Settings
from soldier import Soldier
from game_stats import GameStats
from button import Button
from zombie import Zombie   
from bullet import Bullet

class Scoreboard():
    """Класс для вывода игровой информации."""     
    def __init__(self, zk_game):
        """Инициализирует атрибуты подсчета очков."""
        self.zk_game = zk_game
        self.screen = zk_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = zk_game.settings
        self.zk_settings = zk_game.settings  # Assuming `zk_game` is passed to the Scoreboard
        self.stats = zk_game.stats
        # Настройки шрифта для вывода счета.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Подготовка исходного изображения.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_soldiers()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""    
        rounded_score = round(self.stats.score, -1)
        score_str = "score {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
        self.text_color, self.settings.button_color)
        # Вывод счета в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "high {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
        self.text_color, self.zk_settings.button_color)
        # Рекорд выравнивается по центру верхней стороны.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Проверяет, появился ли новый рекорд."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


    def prep_level(self):
        """Преобразует уровень в графическое изображение."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
        self.text_color, self.settings.button_color)
        # Уровень выводится под текущим счетом.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_soldiers(self):
        """Сообщает количество оставшихся кораблей."""   
        self.soldiers = Group()
        for soldier_number in range(self.stats.soldier_health):
            soldier = Soldier(self.zk_game)
            soldier.rect.x = 10 + soldier_number * soldier.rect.width
            soldier.rect.y = 10
            self.soldiers.add(soldier)


    def show_score(self):
        """Выводит счет на экран."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.soldiers.draw(self.screen)
        
