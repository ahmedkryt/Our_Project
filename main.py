import pygame
import random

pygame.init()

# основные инструменты
font = pygame.font.Font(None, 38)

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

width = 1360
height = 750

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake xenzia')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 10


# функция рисует счет
def score(score):
    value = font.render("Score: " + str(score), True, black)
    screen.blit(value, [0, 0])


# функция рисует змейку
def snake_draw(snake_block, snake_list):
    for i in snake_list:
        pygame.draw.rect(screen, black, [i[0], i[1], snake_block, snake_block])


# обработчик нажатий
def movements_snake(speed_x, speed_y):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # стрелочки
            if event.key == pygame.K_LEFT:
                speed_x = -snake_block
                speed_y = 0
            elif event.key == pygame.K_RIGHT:
                speed_x = snake_block
                speed_y = 0
            elif event.key == pygame.K_UP:
                speed_y = -snake_block
                speed_x = 0
            elif event.key == pygame.K_DOWN:
                speed_y = snake_block
                speed_x = 0
            # WASD
            elif event.key == pygame.K_w:
                speed_y = -snake_block
                speed_x = 0
            elif event.key == pygame.K_a:
                speed_x = -snake_block
                speed_y = 0
            elif event.key == pygame.K_s:
                speed_y = snake_block
                speed_x = 0
            elif event.key == pygame.K_d:
                speed_x = snake_block
                speed_y = 0
            # выход из программы
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
    return [speed_x, speed_y]
    # ___________________________________________________________УБРАТЬ ВОЗМОЖНОСТЬ ИДТИ В ОБРАТНОМ НАПРАВЛЕНИИ(В СЕБЯ)


# функция, которая ловит пересечения, ведущие к окончанию игры
def intersection(snake_list, snake_head):
    for i in snake_list[:-1]:
        if i == snake_head:
            return True
    # ______________________________________________________________ ДОПИСАТЬ ПЕРЕСЕЧЕНИЕ С ПРЕПЯТСТВИЯМИ НА УРОВНЕ


# основной цикл
def game():
    # Начальные параметры
    game_over = False

    x = width / 2
    y = height / 2

    speed_x = 0
    speed_y = 0

    snake_list = []
    length = 1

    apple_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    apple_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
    # ____________________________________________________________________________ПЕРЕСМОТРЕТЬ ГЕНЕРАЦИЮ КООРДИНАТ,
    # __________________________________________________________ГОЛОВА И ЯБЛОКО НЕРОВНО ВСТРЕЧАЮТСЯ ПРИ ПЕРЕСЕЧЕНИИ
    while not game_over:
        screen.fill(white)

        # смена скорости
        speed_x, speed_y = movements_snake(speed_x, speed_y)
        # проверка на выход за игровую зону
        if x >= width or x < 0 or y >= height or y < 0:
            pass
        # ______________________________________________________________ДОПИСАТЬ ПЕРЕМЕЩЕНИЕ ЗМЕЙКИ ПРИ ВЫХОДЕ ЗА ЭКРАН
        # смена координат
        x += speed_x
        y += speed_y
        # записываем координаты по спискам
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]
        # создаем прямоугольники головы и яблока
        head = pygame.Rect(x, y, snake_block, snake_block)
        apple = pygame.Rect(apple_x, apple_y, snake_block, snake_block)
        # рисуем яблоко и змейку
        pygame.draw.rect(screen, green, apple)
        snake_draw(snake_block, snake_list)
        # проверяем пересечение с препятствиями или с телом
        game_over = intersection(snake_list, snake_head)
        # проверяем пересечение головы с яблоком
        if apple.colliderect(head):
            apple_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            apple_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length += 1
        # рисуем счет
        score(length - 1)
        pygame.display.update()
        clock.tick(snake_speed)
    pygame.quit()
    quit()


game()

# ДОБАВИТЬ ТРИ УРОВНЯ СО СВОИМ ДИЗАЙНОМ И ПРЕПЯТСТВИЯМИ
# ДОБАВИТЬ ЗАСТАВКУ В НАЧАЛЕ ИГРЫ
