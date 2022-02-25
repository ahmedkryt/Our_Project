import pygame
import sys



def load_image(file_name):
    file_name = 'maps/' + file_name
    return pygame.image.load(file_name).convert_alpha()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image("Re.jpg"), (width, height))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
size = width, height = 743, 627

# музыка
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode(size)
FPS = 30
clock = pygame.time.Clock()

start_screen()

tile_width = tile_height = 50

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            print(event.key)
    clock.tick(FPS)
    pygame.display.flip()
