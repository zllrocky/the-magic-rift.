import pygame


class Mage:
    """Класс для управления летающим магом."""

    def __init__(self, tmr_game):
        """Инициализирует мага и магическую платформу, задает его начальную позицию."""
        self.screen = tmr_game.screen
        self.settings = tmr_game.settings
        self.screen_rect = tmr_game.screen.get_rect()

        """Загрузка и настройка мага"""
        self.image = pygame.image.load("images/mage.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()

        """Загрузка магической платформы"""
        self.platform_image = pygame.image.load(
            "images/magic_platform.png"
        ).convert_alpha()

        # Масштабируем платформу, чтобы она была чуть шире мага
        platform_width = int(self.rect.width * 1.3)  # 130% от ширины мага
        platform_height = int(self.rect.height * 0.4)  # Плоская
        self.platform_image = pygame.transform.scale(
            self.platform_image, (platform_width, platform_height)
        )
        self.platform_rect = self.platform_image.get_rect()

        # Ставим мага по центру внизу
        self.rect.midbottom = self.screen_rect.midbottom
        # Приподнять мага от края
        self.rect.y -= 40

        # Привязываем платформу к ногам мага
        # (Она будет центрирована по магу и стоять под его ногами)
        self.platform_rect.midtop = self.rect.midbottom

        # Сохранение вещественной координаты центра корабля.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Флаги перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Обновляет позицию мага и платформы с учетом флагов."""

        # Движение мага (с учетом настроек скорости)
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.mage_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.mage_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.mage_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.mage_speed

        # Обновление атрибута rect на основании self.x и self.y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Платформа всегда следует за ногами мага
        self.platform_rect.midtop = self.rect.midbottom
        # Можно чуть-чуть сместить платформу вверх, чтобы она "касалась" ног
        self.platform_rect.y -= 40

    def blitme(self):
        """Рисует платформу и мага в текущей позиции."""
        self.screen.blit(self.platform_image, self.platform_rect)
        self.screen.blit(self.image, self.rect)

    def center_mage(self):
        """Размещает корабль в центре нижней стороны."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
