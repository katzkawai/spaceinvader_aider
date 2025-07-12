import pygame
from settings import PLAYER_SPEED, BULLET_SPEED
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(400, 500))
    
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        
        # Bullet firing
        if keys[pygame.K_SPACE]:
            bullet = Bullet(self.rect.center, -BULLET_SPEED)
            self.groups()[0].add(bullet)
