import pygame
from pygame.sprite import Sprite


class Fireball(Sprite):
    """Класс для управления снарядами, выпущенными магом."""

    def __init__(self, tmr_game):
        super().__init__()
        self.screen = tmr_game.screen
        self.settings = tmr_game.settings

        # Работа с картинкой fireball
        self.image = pygame.image.load("images/fireball.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        # Появление fireball над головой мага
        self.rect.midtop = tmr_game.mage.rect.midtop

        # Позиция снаряда хранится в десятичном формате для плавности
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану."""
        # Обновление позиции снаряда в десятичном формате.
        self.y -= self.settings.fireball_speed
        self.rect.y = self.y

    def draw_fireball(self):
        """Вывод fireball на экран."""
        self.screen.blit(self.image, self.rect)
