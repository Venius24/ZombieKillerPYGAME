import pygame

class Bullet(pygame.sprite.Sprite):
    """Класс для управления снарядами, выпущенными солдатом."""
    
    def __init__(self, zk_game):
        """Создание снаряда в позиции солдата."""
        super().__init__()
        self.screen = zk_game.screen
        self.settings = zk_game.settings
        self.color = self.settings.bullet_color

        # Создание снаряда в позиции солдата
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                 self.settings.bullet_height)
        self.rect.midright = zk_game.soldier.rect.midright

        # Позиция снаряда
        self.x = float(self.rect.x)

    def update(self):
        """Перемещение снаряда вверх по экрану."""
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        """Вывод снаряда на экран."""
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)
        