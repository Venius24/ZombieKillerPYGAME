import pygame
import random
from settings import Settings

class Zombie(pygame.sprite.Sprite):
    """Класс, представляющий одного зомби."""
    def __init__(self, zk_game):
        """Инициализирует зомби и задает его начальную позицию."""
        super().__init__()
        self.screen = zk_game.screen
        self.settings = zk_game.settings

        # Задаем размеры и цвет зомби из settings
        self.width = 100
        self.height = 100
        self.color = self.settings.zombie_color  # Цвет зомби из settings

        # Создаем прямоугольник для зомби
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # Каждый новый зомби появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной горизонтальной позиции зомби
        self.x = float(self.rect.x)

    def check_edges(self):
        """Возвращает True, если зомби находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.top <= 0 or self.rect.bottom >= screen_rect.bottom:
            return True  # Zombie is at the top or bottom edge
        return False
    
    def check_end_edge(self):
        """Возвращает True, если зомби находится у левого края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.left <= 0:
            return True  # Zombie is at the left or right edge

    def update(self):
        self.rect.y += (
        self.settings.zombie_drop_speed
        * self.settings.zombie_direction
    )
        self.rect.x -= random.uniform(self.settings.zombie_min_speed, self.settings.zombie_max_speed)
        #print(f"Zombie x position: {self.rect.x}")

    def draw(self):
        """Рисует зомби на экране."""
        pygame.draw.rect(self.screen, self.color, self.rect)