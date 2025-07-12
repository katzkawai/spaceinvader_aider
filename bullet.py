import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.image = pygame.Surface((4, 8))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
