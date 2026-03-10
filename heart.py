import pygame
from pygame.sprite import Sprite


class Heart(Sprite):
    """Класс для управления одной жизнью-сердцем."""

    def __init__(self, tmr_game):
        super().__init__()
        self.screen = tmr_game.screen

        # Загружаем изображение
        self.image = pygame.image.load("images/heart.png")
        self.image = pygame.transform.scale(self.image, (70, 50))

        self.rect = self.image.get_rect()
