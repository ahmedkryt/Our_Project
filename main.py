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

snake_block = 40
snake_speed = 5

tile_images = {
    'wall': pygame.image.load('small_kam_2.png'),
    'empty': pygame.image.load('trava.png')
}

tile_width = tile_height = 50


# функция окончания игры
def terminate():
    # фон проигрыша
    background = pygame.image.load('Res/Game over.jpg').convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    screen.blit(background, (0, 0))
    pygame.display.flip()
    # музыка
    pygame.mixer.music.load("Res/gameover.mp3")
    pygame.mixer.music.play(1)
    delay(300)
    # выход из программы
    pygame.quit()
    sys.exit()


# заставка
def start_screen():
    # фон
    background = pygame.image.load('Res/Re.jpg').convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    screen.blit(background, (0, 0))
    pygame.display.flip()
    # музыка
    pygame.mixer.music.load("Res/music.mp3")
    pygame.mixer.music.play(-1)
    delay(3000)


# класс змейки
class Snake:
    def __init__(self, b, s):
        self.snake_block = b
        self.snake_speed = s

    # функция рисует счет
    def score(self, score):
        value = font.render("Score: " + str(score), True, black)
        screen.blit(value, [0, 0])

    # функция рисует змейку
    def snake_draw(self, snake_block, snake_coords, duration, body_pictures):
        turn = [pygame.image.load("Res/body_bottomleft.png").convert(),
                pygame.image.load("Res/body_bottomright.png").convert(),
                pygame.image.load("Res/body_topleft.png").convert(),
                pygame.image.load("Res/body_topright.png").convert()]
        flag = False
        if duration == 'up':
            pass
        if duration == 'down':
            body_pictures[-1] = pygame.image.load("Res/head_down.png").convert()
            for i in turn:
                if i in body_pictures:
                    flag = True
                    break
            if not flag:
                for i in reversed(range(1, len(snake_coords) - 1)):
                    body_pictures[i] = pygame.image.load("Res/body_vertical.png").convert()
                body_pictures[0] = pygame.image.load("Res/tail_up.png").convert()

        if duration == 'left':
            head = pygame.image.load("Res/head_left.png").convert()

        if duration == 'right':
            head = pygame.image.load("Res/head_right.png").convert()

        return body_pictures

    # обработчик нажатий
    def movements_snake(self, speed_x, speed_y, duration):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # стрелочки
                if event.key == pygame.K_LEFT and speed_x != snake_block:
                    speed_x = -snake_block
                    speed_y = 0
                    duration = 'left'
                elif event.key == pygame.K_RIGHT and speed_x != -snake_block:
                    speed_x = snake_block
                    speed_y = 0
                    duration = 'right'
                elif event.key == pygame.K_UP and speed_y != snake_block:
                    speed_y = -snake_block
                    speed_x = 0
                    duration = 'up'
                elif event.key == pygame.K_DOWN and speed_y != -snake_block:
                    speed_y = snake_block
                    speed_x = 0
                    duration = 'down'
                # WASD
                elif event.key == pygame.K_w and speed_y != snake_block:
                    speed_y = -snake_block
                    speed_x = 0
                    duration = 'up'
                elif event.key == pygame.K_a and speed_x != snake_block:
                    speed_x = -snake_block
                    speed_y = 0
                    duration = 'left'
                elif event.key == pygame.K_s and speed_y != -snake_block:
                    speed_y = snake_block
                    speed_x = 0
                    duration = 'down'
                elif event.key == pygame.K_d and speed_x != -snake_block:
                    speed_x = snake_block
                    speed_y = 0
                    duration = 'right'
                # выход из программы
                elif event.key == pygame.K_ESCAPE:
                    terminate()
        return [speed_x, speed_y, duration]

    # функция, которая ловит пересечения, ведущие к окончанию игры
    def intersection(self, snake_list, snake_head):
        for i in snake_list[:-1]:
            if i == snake_head:
                return True
        # ______________________________________________________________ ДОПИСАТЬ ПЕРЕСЕЧЕНИЕ С ПРЕПЯТСТВИЯМИ НА УРОВНЕ


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Trava(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(trava_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Kamni(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(kamni_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


player = None
running = True
trava_group = SpriteGroup()
kamni_group = SpriteGroup()
hero_group = SpriteGroup()


def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Trava('empty', x, y)
            elif level[y][x] == '#':
                Kamni('wall', x, y)
    return new_player, x, y


level_map = load_level("map3.txt")
hero, max_x, max_y = generate_level(level_map)


# главная функция
def game():
    # Начальные параметры
    game_over = False

    x = snake_block * 20
    y = snake_block * 12

    speed_x = 0
    speed_y = 0
    duration = 'down'

    snake_coords = [[x, y-snake_block*2], [x, y-snake_block], [x, y]]

    body_pictures = [pygame.image.load('Res/tail_up.png').convert(),
                     pygame.image.load('Res/body_vertical.png').convert(),
                     pygame.image.load('Res/head_down.png').convert()]

    body_rect = [body_pictures[0].get_rect(bottomright=(snake_coords[0][0], snake_coords[1][1])),
                 body_pictures[1].get_rect(bottomright=(snake_coords[0][0], snake_coords[1][1])),
                 body_pictures[2].get_rect(bottomright=(snake_coords[0][0], snake_coords[1][1]))]
    length = 3

    apple_x = random.randint(0, width // snake_block) * snake_block
    apple_y = random.randint(0, height // snake_block) * snake_block

    snake = Snake(snake_block, snake_speed)
    # основной цикл игры
    while not game_over:

        apple = pygame.image.load('Res/apple.png').convert()

        body_pictures = snake.snake_draw(snake_block, snake_coords, duration, body_pictures)
        for i in reversed(range(len(body_pictures))):
            rect = body_pictures[i].get_rect(bottomright=(snake_coords[i][0], snake_coords[i][1]))
            body_rect[i] = rect
            screen.blit(body_pictures[i], rect)
        apple_size = apple.get_rect(bottomright=(apple_x, apple_y))
        screen.blit(apple, apple_size)
        pygame.display.update()

        # проверяем пересечение с препятствиями или с телом
        #game_over = intersection(snake_coords, snake_head)
        # проверяем пересечение головы с яблоком
        if apple_size.colliderect(body_rect[-1]):
            apple_x = random.randint(0, width // snake_block) * snake_block
            apple_y = random.randint(0, height // snake_block) * snake_block
            length += 1
        # рисуем счет
        snake.score(length - 3)
        # смена скорости
        speed_x, speed_y, duration = snake.movements_snake(speed_x, speed_y, duration)
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
        if speed_x != 0 and speed_y != 0:
            # записываем координаты по спискам
            snake_head = [x, y]
            snake_coords.append(snake_head)
            del (snake_coords[0])
            pygame.display.update()
            clock.tick(snake_speed)
        for i in kamni_group:
            if body_rect[-1].colliderect(i):
                game_over = True
        pygame.display.update()
        trava_group.draw(screen)
        kamni_group.draw(screen)
        clock.tick(snake_speed)

    # Game over
    terminate()


# запуск
start_screen()
game()

# уравнять размеры яблока и змейки, доделать анимацию туловища и хвоста