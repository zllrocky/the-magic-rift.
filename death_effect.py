import pygame
from pygame.sprite import Sprite


class DeathEffect(Sprite):

    def __init__(self, tmr_game, center_pos):
        super().__init__()
        self.screen = tmr_game.screen

        # Загружаем все 4 кадра в список
        self.frames = []
        for i in range(1, 5):
            img = pygame.image.load(f"images/death_{i}.png").convert_alpha()
            # Масштабируем под размер фейки (60x60 или чуть больше для эффекта)
            img = pygame.transform.scale(img, (80, 80))
            self.frames.append(img)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = center_pos  # Ставим ровно в центр бывшей фейки

        # Таймер для смены кадров
        self.last_tick = pygame.time.get_ticks()
        self.animation_speed = 70

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_tick > self.animation_speed:
            self.last_tick = now
            self.frame_index += 1

            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]
            else:
                self.kill()
