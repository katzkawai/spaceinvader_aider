import pygame
from player import Player
from settings import WIDTH, HEIGHT, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    # Sprite groups
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    
    player = Player()
    all_sprites.add(player)
    
    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update
        all_sprites.update(keys)
        bullets.update()
        
        # Draw
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        bullets.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()

if __name__ == "__main__":
    main()
