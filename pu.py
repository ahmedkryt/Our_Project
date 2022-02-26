import pygame

pygame.init()

W, H = 1160, 600

screen = pygame.display.set_mode((W, H))
# pygame.display.set_caption("Изображения")
# pygame.display.set_icon(pygame.image.load("maps/fon.jpeg"))

# фон
fon_surf = pygame.image.load("maps/fon.jpeg")
fon_rect = fon_surf.get_rect(center=(W // 2, H // 2))

screen.blit(fon_surf, fon_rect)
pygame.display.update()

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (239, 228, 176)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    running = True
    x_pos = 0
    v = 20  # пикселей в секунду
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (0, 255, 0), (int(x_pos), 340), 5)
        x_pos += v * clock.tick() / 220  # v * t в секундах
        pygame.display.flip()

    clock.tick(FPS)
    pygame.quit()

