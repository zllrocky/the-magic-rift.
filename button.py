import pygame.font


class Button:

    def __init__(self, tmr_game):
        """Инициализирует атрибуты кнопки."""
        self.screen = tmr_game.screen
        self.screen_rect = self.screen.get_rect()

        # Загружаем картинку кнопки вместо рисования прямоугольника
        self.image = pygame.image.load("images/button.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (350, 250))

        # Получаем прямоугольник и центрируем его
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

    def draw_button(self):
        """Отображение кнопки на экране."""
        # Просто рисуем картинку
        self.screen.blit(self.image, self.rect)
