import pygame
import random
from pygame.locals import *
from game.player import Player
from bullet import Bullet

# Game constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
ENEMY_ROWS = 5
ENEMY_COLS = 10
ENEMY_SPEED = 2
BULLET_SPEED = 10  # Match settings.py value

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 20))
        self.image.fill((255, 255, 255))  # White enemy
        self.rect = self.image.get_rect(topleft=(x, y))


class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.health = 10
        self.image = pygame.Surface((60, 30))
        self.image.fill((0, 0, 255))  # Blue barrier
        self.rect = self.image.get_rect(topleft=(x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    player = Player()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    barriers = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    
    # Create enemies grid
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            x = 100 + col * 50
            y = 50 + row * 40
            enemy = Enemy(x, y)
            enemies.add(enemy)
            all_sprites.add(enemy)
    
    # Create barriers
    for i in range(3):
        barrier = Barrier(200 + i*200, HEIGHT - 150)
        barriers.add(barrier)
        all_sprites.add(barrier)
    
    enemy_direction = 1
    game_started = False
    game_over = False
    score = 0
    running = True
    
    while running:
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE and not game_started:
                    game_started = True
        
        keys = pygame.key.get_pressed()
        
        if game_started and not game_over:
            # Update player and handle shooting
            player.update(keys)
            if player.bullet:
                bullets.add(player.bullet)
                all_sprites.add(player.bullet)
                player.bullet = None
            
            # Enemy movement
            move_down = False
            for enemy in enemies:
                enemy.rect.x += ENEMY_SPEED * enemy_direction
                if enemy.rect.right >= WIDTH or enemy.rect.left <= 0:
                    move_down = True
            
            if move_down:
                enemy_direction *= -1
                for enemy in enemies:
                    enemy.rect.y += 20
            
            # Enemy shooting (random chance)
            if random.random() < 0.01:  # 1% chance per frame
                shooter = random.choice(list(enemies))
                bullet = Bullet(shooter.rect.center, BULLET_SPEED)
                bullets.add(bullet)
                all_sprites.add(bullet)
            
            # Update bullets
            bullets.update()
            
            # Collision detection
            # Player bullets hit enemies
            hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
            for hit in hits:
                score += 100
            
            # Enemy bullets hit player
            if pygame.sprite.spritecollide(player, bullets, True):
                game_over = True
                result_text = "Game Over"
            
            # Bullets hit barriers
            pygame.sprite.groupcollide(bullets, barriers, True, False)
            
            # Check win condition
            if not enemies:
                game_over = True
                result_text = "Clear!"
            
            # Check if enemies reached bottom
            for enemy in enemies:
                if enemy.rect.bottom > HEIGHT - 100:
                    game_over = True
                    result_text = "Game Over"
        
        # Draw all sprites
        all_sprites.draw(screen)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        if game_over:
            text = font.render(result_text, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text, text_rect)
        elif not game_started:
            start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
            start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(start_text, start_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
