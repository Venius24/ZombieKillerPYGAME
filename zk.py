import pygame
import os, sys
import random
import time
from settings import Settings
from soldier import Soldier
from bullet import Bullet
from zombie import Zombie
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class ZombieKiller:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Zombie Killer")
        self.bg_color = self.settings.bg_color

        self.soldier = Soldier(self)
        self.bullets = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # ------------------------------------------------------------------
        # ВКЛАДКА 1.  Параметры «рандомизации»   ---------------------------
        # ------------------------------------------------------------------
        self.spawn_chance = 0.85   # 85 % ячеек будут заняты
        self.jitter_x     = 0.25   # смещение до 25 % ширины спрайта
        self.jitter_y     = 0.30   # смещение до 30 % высоты
        self.seed        = None   # поставь число, чтобы «запомнить» генерацию


        self._create_crowd()

        self.play_button = Button(self, "Play")

        
    

    def run_game(self):
        while True:
            self._check_events()
            self.soldier.update()

            if self.stats.game_active:
                self._check_crowd_edges()
                self._update_zombies()
                self._update_bullets()
                
            
            self._update_screen()  
            
            

    def _check_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                print(event.key)
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Обработка нажатий клавиш."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.soldier.moving_right = True
            self.soldier.moving_left = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.soldier.moving_right = False
            self.soldier.moving_left = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.soldier.moving_up = True
            self.soldier.moving_down = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.soldier.moving_down = True
            self.soldier.moving_up = False

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
    
    def _check_keyup_events(self, event):
        """Обработка отпускания клавиш."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.soldier.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.soldier.moving_left = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.soldier.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.soldier.moving_down = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            """Создание нового снаряда и включение его в группу bullets."""
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                self.bullets.remove(bullet)
        #print(len(self.bullets))
        self._check_bullet_zombie_collisions()


    def _check_bullet_zombie_collisions(self):
        # Проверка попаданий в пришельцев.
        # При обнаружении попадания удалить снаряд и пришельца.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.zombies, False, True)
        
        if not self.zombies:
          # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self._create_crowd()
            self.settings.increase_speed()

            # Увеличение уровня.
            self.stats.level += 1
            self.sb.prep_level()

        if collisions:
            for zombies in collisions.values():
                self.stats.score += self.settings.zombie_points * len(zombies)
            self.sb.prep_score()
            self.sb.check_high_score()

    # ------------------------------------------------------------------
    # ВКЛАДКА 2.  Создание толпы   -------------------------------w------
    # ------------------------------------------------------------------
    def _create_crowd(self) -> None:
        if self.seed is not None:
            random.seed(self.seed)

        probe = Zombie(self)
        w, h = probe.rect.size

        # --- настройки компоновки ----------------------------------------------------
        # (при желании вынесите их в self.settings, конфиг и т.д.)
        top_margin      = h       # отступ сверху
        bottom_margin   = h       # отступ снизу
        right_margin    = w       # отступ от правого края
        gap_x           = w * 0.7 # горизонтальный зазор между спрайтами
        gap_y           = h * 1 # вертикальный зазор

        avail_y = (
            self.settings.screen_height
            - top_margin
            - bottom_margin
        )
        # n строк:  n·h + (n‑1)·gap_y ≤ avail_y  →  
        rows = int((avail_y + gap_y) // (h + gap_y))

        soldier_w = self.soldier.rect.width
        left_margin = soldier_w + w * 8.1              # «коридор» перед солдатом

        avail_x = (
            self.settings.screen_width
            - left_margin
            - right_margin
        )
        # m колонок: m·w + (m‑1)·gap_x ≤ avail_x  →  
        cols = int((avail_x + gap_x) // (w + gap_x))

        # --- фактическое размещение --------------------------------------------------
        start_x = self.settings.screen_width - right_margin - w  # x первой (правой) колонки
        start_y = top_margin                                     # y первой (верхней) строки

        for row in range(rows):
            for col in range(cols):
                if random.random() > self.spawn_chance:
                    continue                           # пропускаем ячейку

                jitter_dx = (random.uniform(-self.jitter_x, self.jitter_x) * w)
                jitter_dy = (random.uniform(-self.jitter_y, self.jitter_y) * h)

                self._create_zombie(
                    row, col,
                    start_x=start_x + jitter_dx,      # немножко сдвигаем
                    start_y=start_y + jitter_dy,
                    gap_x=gap_x,
                    gap_y=gap_y,
                    sprite_w=w,
                    sprite_h=h,
                )

    # ------------------------------------------------------------------
    # ВКЛАДКА 3.  Создание конкретного зомби   -------------------------
    # ------------------------------------------------------------------
    def _create_zombie(
        self, row, col, *, start_x, start_y,
        gap_x, gap_y, sprite_w, sprite_h
    ):
        zombie = Zombie(self)

        zombie.rect.x = start_x - col * (sprite_w + gap_x)
        zombie.rect.y = start_y + row * (sprite_h + gap_y)

        # даём спрайту «приукраситься» (если ты это реализуешь)
        if hasattr(zombie, "randomize_look"):
            zombie.randomize_look()

        self.zombies.add(zombie)

    def _return_soldier(self):
        """Возвращает солдата в начальное положение."""
        self.soldier.rect.midleft = self.screen.get_rect().midleft  # Reset position
        self.soldier.x = float(self.soldier.rect.x)
        self.soldier.y = float(self.soldier.rect.y)
        self.soldier.moving_right = False
        self.soldier.moving_left = False
        self.soldier.moving_up = False
        self.soldier.moving_down = False

    def _update_screen(self):
        """Обновление экрана."""
        self.screen.fill(self.settings.bg_color)
        self.soldier.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Рисуем всех зомби вручную
        for zombie in self.zombies.sprites():
            zombie.draw()

        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()


        pygame.display.flip()


    def _check_crowd_edges(self):
        """Реагирует на достижение пришельцем края экрана."""      
        for zombie in self.zombies.sprites():
            if zombie.check_edges():
                self._change_zombie_direction()
                break
    
    def _change_zombie_direction(self):
        """Опускает весь флот и меняет направление флота."""
        self.settings.zombie_direction *= -1
        #print(f"Zombie direction changed to: {self.settings.zombie_direction}")

    def _update_zombies(self):
        self.zombies.update()

        if pygame.sprite.spritecollideany(self.soldier, self.zombies):
            self._soldier_hit()

        self._check_zombies_end()


    def _soldier_hit(self):
        if self.stats.soldier_health > 0:
            """Обрабатывает столкновение корабля с пришельцем."""
            self.stats.soldier_health -= 1
            self.sb.prep_soldiers()
            self.zombies.empty()
            self.bullets.empty()
            # Создание нового флота и размещение корабля в центре.
            self._create_crowd()
            self._return_soldier()
            # Пауза.
            time.sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_zombies_end(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for zombie in self.zombies.sprites():      
            if zombie.check_end_edge():
                # Происходит то же, что при столкновении с кораблем.
                self._soldier_hit()
                break
    
    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            # Указатель мыши скрывается.
            pygame.mouse.set_visible(False)

            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_soldiers()

            # Очистка
            self.zombies.empty()
            self.bullets.empty()

            self._create_crowd()
            self._return_soldier()


if __name__ == "__main__":
    zk = ZombieKiller()
    zk.run_game()