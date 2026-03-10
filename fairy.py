import pygame
from pygame.sprite import Sprite


class Fairy(Sprite):
    """Класс, представляющий одного фею."""

    def __init__(self, tmr_game):
        """Инициализирует фею и задает его начальную позицию."""
        super().__init__()
        self.screen = tmr_game.screen
        self.settings = tmr_game.settings
        self.screen_rect = tmr_game.screen.get_rect()

        # Загрузка изображения пришельца и назначение атрибута rect.
        self.image = pygame.image.load("images/fairy_fae.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

        # Каждый новая фея появляется сверху по центру.
        self.rect.midtop = self.screen_rect.midtop
        self.rect.y += 150

        # Сохранение точной горизонтальной позиции пришельца.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Перемещает фейку влево или вправо."""
        self.x += self.settings.fairy_speed * self.settings.fleet_direction
        self.rect.x = self.x
