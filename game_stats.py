class GameStats:
    """Отслеживание статистики для игры The Magic Rift."""

    def __init__(self, tmr_game):
        """Инициализирует статистику."""
        self.settings = tmr_game.settings
        self.reset_stats()
        # Игра запускается в неактивном состоянии
        self.game_active = False
        # Рекорд не должен сбрасываться.
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.mages_left = self.settings.mage_limit
        self.score = 0
