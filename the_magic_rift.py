import sys
import pygame
from time import sleep

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from mage import Mage
from fireball import Fireball
from fairy import Fairy
from death_effect import DeathEffect
from button import Button


class TheMagicRift:

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        # Запускаем полноэкранный режим
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # Обновляем настройки ширины и высоты, чтобы они соответствовали реальному экрану
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # Группа для хранения эффектов смерти
        self.death_effects = pygame.sprite.Group()

        # Создание экземпляра для хранения игровой статистики.
        # и панели результатов.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.play_button = Button(self)
        self.mage = Mage(self)
        self.fireballs = pygame.sprite.Group()
        self.fairys = pygame.sprite.Group()

        self._create_fleet()

        pygame.display.set_caption("The Magic Rift")

        # === ЗАГРУЗКА ФОНА ===
        # Загружаем файл
        self.bg_image = pygame.image.load("images/background.jpg").convert()

        # Масштабируем картинку под РЕАЛЬНЫЙ размер экрана
        self.bg_image = pygame.transform.scale(
            self.bg_image, (self.settings.screen_width, self.settings.screen_height)
        )
        self.bg_rect = self.bg_image.get_rect()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()  # Проверяет ввод полученный от игрока

            if self.stats.game_active:
                self.mage.update()  # Обновляет позицию мага
                self._update_fireballs()  # Обновляет позицию всех выпущенных снарядов
                self._update_fairys()  # Обновляет позицию каждой фейки
                self.death_effects.update()  # Обновляет эффект смерти

            self._update_screen()  # Обновление и вывод экрана

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Добавляем проверку клика:
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.mage.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.mage.moving_left = True
        elif event.key == pygame.K_UP:
            self.mage.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.mage.moving_down = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_fireball()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.mage.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.mage.moving_left = False
        elif event.key == pygame.K_UP:
            self.mage.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.mage.moving_down = False

    def _fire_fireball(self):
        """Создание нового снаряда и включение его в группу fireballs."""
        if len(self.fireballs) < self.settings.fireballs_allowed:
            new_fireball = Fireball(self)
            self.fireballs.add(new_fireball)

    def _update_fireballs(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов.
        self.fireballs.update()
        # Удаление снарядов, вышедших за край экрана.
        for fireball in self.fireballs.copy():
            if fireball.rect.bottom <= 0:
                self.fireballs.remove(fireball)

        self._check_fireball_fairy_collisions()

        if not self.fairys:
            # Уничтожение существующих снарядов и создание нового флота
            self.fireballs.empty()
            self.settings.increase_speed()
            # ПОВЫШАЕМ УРОВЕНЬ (Добавляй сюда!)
            self.stats.level += 1
            self.sb.prep_level()  # Рисуем новую цифру уровня
            # Создаем новых врагов
            self._create_fleet()

    def _check_fireball_fairy_collisions(self):
        """Обработка коллизий снарядов с фейками."""
        # Проверка попаданий (True, True означает удалить и пулю, и фейку)
        collisions = pygame.sprite.groupcollide(self.fireballs, self.fairys, True, True)

        if collisions:
            for hit_fairies in collisions.values():
                self.stats.score += self.settings.fairy_points * len(hit_fairies)

        self.sb.prep_score()
        self.sb.check_high_score()

        # collisions — это словарь {пуля: [список_сбитых_феек]}
        for hit_fairies in collisions.values():
            for fairy in hit_fairies:
                # Создаем эффект смерти в центре убитой фейки!
                new_effect = DeathEffect(self, fairy.rect.center)
                self.death_effects.add(new_effect)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        # Проверяем: попал ли клик в прямоугольник кнопки
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        # Запускаем только если нажали на кнопку И игра сейчас НЕ активна
        if button_clicked and not self.stats.game_active:
            # СБРАСЫВАЕМ СКОРОСТЬ ДО НАЧАЛЬНОЙ
            self.settings.initialize_dynamic_settings()
            # Сбрасываем статистику (жизни и т.д.)
            self.stats.reset_stats()

            # Очищаем всё старое
            self.fairys.empty()
            self.fireballs.empty()
            self.death_effects.empty()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_hearts()

            # Возвращаем мага в центр
            self.mage.center_mage()

            # Создаем новый врагов
            self._create_fleet()

            # Включаем игру и скрываем указатель мыши, чтобы не мешал в бою
            self.stats.game_active = True
            pygame.mouse.set_visible(False)

    def _update_fairys(self):
        """Обновляет позиции всех пришельцев во флоте."""
        self._check_fleet_edges()
        self.fairys.update()

        # Проверка коллизий "фея — маг".
        if pygame.sprite.spritecollideany(self.mage, self.fairys):
            self._mage_hit()
        # Проверить, добрались ли феи до нижнего края экрана.
        self._check_fairys_bottom()

    def _mage_hit(self):
        """Обрабатывает столкновение мага с феей."""
        # Уменьшение mages_left.
        if self.stats.mages_left > 1:
            self.stats.mages_left -= 1
            self.sb.prep_hearts()

            # Очистка списков пришельцев и снарядов.
            self.fairys.empty()
            self.fireballs.empty()
            self.death_effects.empty()

            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.mage.center_mage()

            # Пауза
            sleep(0.5)
        else:
            # КОНЕЦ ИГРЫ
            self.stats.mages_left = 0
            self.stats.game_active = False  # Вот этот стоп-кран!
            pygame.mouse.set_visible(True)  # Показываем курсор

    def _create_fleet(self):
        """Создание флота вторжения."""
        # Создание пришельца.
        fairy = Fairy(self)
        fairy_width, fairy_height = fairy.rect.size

        # Считаем количество феек в ряду
        available_space_x = self.settings.screen_width - (2 * fairy_width)
        number_fairy_x = available_space_x // (2 * fairy_width)

        # Считаем количество рядов
        # Вычитаем 3 высоты фейки (сверху) и высоту мага (снизу)
        mage_height = self.mage.rect.height
        available_space_y = (
            self.settings.screen_height - (4 * fairy_height) - mage_height
        )
        number_rows = available_space_y // (2 * fairy_height)

        # Создание армии феек
        for row_number in range(number_rows):
            for fairy_number in range(number_fairy_x):
                self._create_fairy(fairy_number, row_number)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for fairy in self.fairys.sprites():
            if fairy.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает феечек и меняет направление"""
        for fairy in self.fairys.sprites():
            fairy.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fairy(self, fairy_number, row_number):
        """Создание пришельца и размещение его в ряду."""
        fairy = Fairy(self)
        fairy_width, fairy_height = fairy.rect.size

        # Установка позиции X
        fairy.x = fairy_width + 2 * fairy_width * fairy_number
        fairy.rect.x = fairy.x

        # Установка позиции Y (чтобы ряды шли один под другим)
        fairy.rect.y = fairy_height + 2 * fairy_height * row_number

        self.fairys.add(fairy)

    def _check_fairys_bottom(self):
        """Проверяет, добрались ли феи до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for fairy in self.fairys.sprites():
            if fairy.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с магом.
                self._mage_hit()
                break

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.blit(self.bg_image, self.bg_rect)
        self.mage.blitme()

        # Рисуем каждый фаербол
        for fireball in self.fireballs.sprites():
            fireball.draw_fireball()
        self.fairys.draw(self.screen)
        self.death_effects.draw(self.screen)

        # Вывод информации о счете.
        self.sb.show_score()

        # Рисуем кнопку Play только если игра стоит на паузе
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()


if __name__ == "__main__":
    # Создание экземпляра и запуск игры.
    tmr = TheMagicRift()
    tmr.run_game()
