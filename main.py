import pygame
import sys
import random
from pygame.time import delay

pygame.init()

# основные инструменты
font = pygame.font.Font(None, 38)

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

width = 1350
height = 750

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake xenzia')

clock = pygame.time.Clock()

snake_block = 30
snake_speed = 5


def lvl_1():
    background = pygame.image.load('maps/bg_lvl1.jpg').convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    screen.blit(background, (0, 0))
    pygame.display.flip()


# функция окончания игры
def terminate():
    # фон проигрыша
    background = pygame.image.load('maps/Game over.jpg').convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    screen.blit(background, (0, 0))
    pygame.display.flip()
    # музыка
    pygame.mixer.music.load("gameover.mp3")
    pygame.mixer.music.play(1)
    delay(5700)
    # выход из программы
    pygame.quit()
    sys.exit()


# заставка
def start_screen():
    # фон
    background = pygame.image.load('maps/Re.jpg').convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    screen.blit(background, (0, 0))
    pygame.display.flip()
    # музыка
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1)
    delay(3000)


# функция рисует счет
def score(score):
    value = font.render("Score: " + str(score), True, black)
    screen.blit(value, [0, 0])


# функция рисует змейку
def snake_draw(snake_block, snake_list, speed_x, speed_y):
    if speed_x == -snake_block and speed_y == 0:
        head = pygame.image.load("maps/head_left.png").convert()
    if speed_x == snake_block and speed_y == 0:
        head = pygame.image.load("maps/head_right.png").convert()
    if speed_y == -snake_block and speed_x == 0:
        head = pygame.image.load("maps/head_up.png").convert()
    if (speed_y == snake_block and speed_x == 0) or (speed_x == 0 and speed_y == 0):
        head = pygame.image.load("maps/head_down.png").convert()
    print(speed_x, ' ', speed_y)
    return head


# обработчик нажатий
def movements_snake(speed_x, speed_y):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # стрелочки
            if event.key == pygame.K_LEFT and speed_x != snake_block:
                speed_x = -snake_block
                speed_y = 0
            elif event.key == pygame.K_RIGHT and speed_x != -snake_block:
                speed_x = snake_block
                speed_y = 0
            elif event.key == pygame.K_UP and speed_y != snake_block:
                speed_y = -snake_block
                speed_x = 0
            elif event.key == pygame.K_DOWN and speed_y != -snake_block:
                speed_y = snake_block
                speed_x = 0
            # WASD
            elif event.key == pygame.K_w and speed_y != snake_block:
                speed_y = -snake_block
                speed_x = 0
            elif event.key == pygame.K_a and speed_x != snake_block:
                speed_x = -snake_block
                speed_y = 0
            elif event.key == pygame.K_s and speed_y != -snake_block:
                speed_y = snake_block
                speed_x = 0
            elif event.key == pygame.K_d and speed_x != -snake_block:
                speed_x = snake_block
                speed_y = 0
            # выход из программы
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
    return [speed_x, speed_y]


# функция, которая ловит пересечения, ведущие к окончанию игры
def intersection(snake_list, snake_head):
    for i in snake_list[:-1]:
        if i == snake_head:
            return True
    # ______________________________________________________________ ДОПИСАТЬ ПЕРЕСЕЧЕНИЕ С ПРЕПЯТСТВИЯМИ НА УРОВНЕ


# главная функция
def game():
    # Начальные параметры
    game_over = False

    x = snake_block * 20
    y = snake_block * 10

    speed_x = 0
    speed_y = 0

    snake_list = []
    length = 1

    apple_x = random.randint(0, width // snake_block) * snake_block
    apple_y = random.randint(0, height // snake_block) * snake_block
    # основной цикл игры
    while not game_over:
        lvl_1()
        # смена скорости
        speed_x, speed_y = movements_snake(speed_x, speed_y)
        # проверка на выход за игровую зону
        if x > width:
            x = 0
        if x < 0:
            x = ((width - snake_block) // snake_block) * snake_block
        if y > height:
            y = snake_block
        if y < 0:
            y = ((720 - snake_block)//snake_block)*snake_block + snake_block + 1

        # смена координат
        x += speed_x
        y += speed_y
        # записываем координаты по спискам
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]
        apple = pygame.image.load('maps/apple.png').convert()
        head = snake_draw(snake_block, snake_list, speed_x, speed_y)
        head_size = head.get_rect(bottomright=(x, y))
        apple_size = apple.get_rect(bottomright=(apple_x, apple_y))
        screen.blit(apple, apple_size)
        screen.blit(head, head_size)
        pygame.display.update()

        # проверяем пересечение с препятствиями или с телом
        game_over = intersection(snake_list, snake_head)
        # проверяем пересечение головы с яблоком
        if apple_size.colliderect(head_size):
            apple_x = random.randint(0, width // snake_block) * snake_block
            apple_y = random.randint(0, height // snake_block) * snake_block
            length += 1
        # рисуем счет
        score(length - 1)
        pygame.display.update()
        clock.tick(snake_speed)
    # Game over
    terminate()


# запуск
start_screen()
game()

# ДОБАВИТЬ ТРИ УРОВНЯ СО СВОИМ ДИЗАЙНОМ И ПРЕПЯТСТВИЯМИ
# уравнять размеры яблока и змейки, доделать анимацию туловища и хвоста