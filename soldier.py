import pygame
import os
from settings import Settings

class Soldier():
    def __init__(self, zk_game):
        self.screen = zk_game.screen
        self.screen_rect = zk_game.screen.get_rect()
        self.settings = zk_game.settings
        image_path = os.path.join(os.path.dirname(__file__), 'images/soldier.bmp')
        self.image = pygame.image.load(image_path).convert_alpha()

        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        
        self.rect.midleft = self.screen_rect.midleft

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        

    def update(self):
        """Обновление позиции солдата."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.soldier_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.soldier_speed
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= self.settings.soldier_speed  # Движение вверх уменьшает y
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.settings.soldier_speed  # Движение вниз увеличивает y

        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)