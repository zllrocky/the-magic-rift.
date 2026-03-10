import pygame.font
from heart import Heart


class Scoreboard:
    """Класс для вывода игровой информации."""

    def __init__(self, tmr_game):
        """Инициализирует атрибуты подсчета очков."""
        self.screen = tmr_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = tmr_game.settings
        self.stats = tmr_game.stats

        # Настройки шрифта для вывода счета.
        self.text_color = (218, 65, 32)
        self.font = pygame.font.SysFont(None, 30)
        # Подготовка исходного изображения.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

        self.tmr_game = tmr_game
        self.prep_hearts()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color)
        # Вывод счета в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Выводит счет на экран."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.hearts.draw(self.screen)

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"Best: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
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
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(level_str, True, self.text_color)

        # Уровень выводится под текущим счетом.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_hearts(self):
        """Создает группу сердец в зависимости от количества жизней."""
        self.hearts = pygame.sprite.Group()

        # Цикл пройдет столько раз, сколько жизней осталось в stats.mages_left
        for hearts_number in range(self.stats.mages_left):
            heart = Heart(self.tmr_game)
            # Расставляем их в ряд: 10 пикселей отступ + номер сердца * ширину
            heart.rect.x = 10 + hearts_number * (heart.rect.width + 5)
            heart.rect.y = 10  # Отступ от верхнего края
            self.hearts.add(heart)
