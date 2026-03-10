class Settings:
    """Класс для хранения всех настроек игры The Magic Rift."""

    def __init__(self):
        """Инициализирует статические настройки игры."""
        # Параметры экрана
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (204, 153, 204)

        # Статика
        self.mage_limit = 3
        self.fleet_drop_speed = 15
        self.fireballs_allowed = 5
        self.speedup_scale = 1.1

        # Запускаем создание динамических настроек
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.mage_speed = 1.5
        self.fireball_speed = 3.0
        self.fairy_speed = 1.0
        self.score_scale = 1.5
        self.fleet_direction = 1

        # Подсчет очков
        self.fairy_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости."""
        self.mage_speed *= self.speedup_scale
        self.fireball_speed *= self.speedup_scale
        self.fairy_speed *= self.speedup_scale
        self.fairy_points = int(self.fairy_points * self.score_scale)
