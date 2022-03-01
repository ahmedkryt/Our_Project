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

width = 1150
height = 750

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake xenzia')

clock = pygame.time.Clock()

snake_block = 50
FPS = 5

tile_images = {
    'wall': pygame.image.load('small_kam_2.png'),
    'empty': pygame.image.load('trava.png')
}

tile_width = tile_height = 50


# функция окончания игры
def terminate():
    # фон проигрыша
    background = pygame.image.load('Res/Game over.jpg').convert_alpha()
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
    background = pygame.image.load('Res/Re.jpg').convert_alpha()
    background = pygame.transform.smoothscale(background, screen.get_size())
    screen.blit(background, (0, 0))
    pygame.display.flip()
    # музыка
    pygame.mixer.music.load("Res/music.mp3")
    pygame.mixer.music.play(-1)
    delay(3000)


# класс змейки
class Snake:
    def __init__(self, b):
        self.snake_block = b

    # функция рисует счет
    def score(self, score):
        value = font.render("Score: " + str(score), True, black)
        screen.blit(value, [0, 0])

    # функция рисует змейку
    def snake_draw(self, snake_coords, direction, body_pictures, old_direction):
        direct = {
            'body_left': ['left-up', 'down-right'],
            'body_right': ['right-up', 'down-left'],
            'top_left': ['up-right', 'left-down'],
            'top_right': ['right-down', 'up-left']
        }

        flag = False
        if direction != old_direction:
            if (direction + '-' + old_direction) in direct['body_left']:
                body_pictures[-2] = pygame.image.load("Res/body_bottomleft.png").convert_alpha()
            if (direction + '-' + old_direction) in direct['body_right']:
                body_pictures[-2] = pygame.image.load("Res/body_bottomright.png").convert_alpha()
            if (direction + '-' + old_direction) in direct['top_left']:
                body_pictures[-2] = pygame.image.load("Res/body_topleft.png").convert_alpha()
            if (direction + '-' + old_direction) in direct['top_right']:
                body_pictures[-2] = pygame.image.load("Res/body_topright.png").convert_alpha()
            flag = True

        if direction == 'up':
            body_pictures[-1] = pygame.image.load("Res/head_up.png").convert_alpha()
            if not flag:
                for i in reversed(range(1, len(snake_coords) - 1)):
                    body_pictures[i] = pygame.image.load("Res/body_vertical.png").convert_alpha()
                body_pictures[0] = pygame.image.load("Res/tail_down.png").convert_alpha()
            else:
                for i in reversed(range(2, len(snake_coords) - 1)):
                    body_pictures[i] = pygame.image.load("Res/body_vertical.png").convert_alpha()
                if old_direction == 'left':
                    body_pictures[0] = pygame.image.load("Res/tail_right.png").convert_alpha()
                else:
                    body_pictures[0] = pygame.image.load("Res/tail_left.png").convert_alpha()

        if direction == 'down':
            body_pictures[-1] = pygame.image.load("Res/head_down.png").convert_alpha()
            if not flag:
                for i in reversed(range(1, len(snake_coords) - 1)):
                    body_pictures[i] = pygame.image.load("Res/body_vertical.png").convert_alpha()
                body_pictures[0] = pygame.image.load("Res/tail_up.png").convert_alpha()
            else:
                for i in reversed(range(2, len(snake_coords) - 1)):
                    body_pictures[i] = pygame.image.load("Res/body_vertical.png").convert_alpha()
                if old_direction == 'left':
                    body_pictures[0] = pygame.image.load("Res/tail_right.png").convert_alpha()
                else:
                    body_pictures[0] = pygame.image.load("Res/tail_left.png").convert_alpha()

        if direction == 'left':
            body_pictures[-1] = pygame.image.load("Res/head_left.png").convert_alpha()
            if not flag:
                for i in reversed(range(1, len(snake_coords) - 1)):
                    body_pictures[i] = pygame.image.load("Res/body_horizontal.png").convert_alpha()
                body_pictures[0] = pygame.image.load("Res/tail_right.png").convert_alpha()
            else:
                for i in reversed(range(2, len(snake_coords) - 1)):
                    body_pictures[i] = pygame.image.load("Res/body_horizontal.png").convert_alpha()
                if old_direction == 'up':
                    body_pictures[0] = pygame.image.load("Res/tail_down.png").convert_alpha()
                else:
                    body_pictures[0] = pygame.image.load("Res/tail_up.png").convert_alpha()

        if direction == 'right':
            body_pictures[-1] = pygame.image.load("Res/head_right.png").convert_alpha()
            if not flag:
                for i in reversed(range(1, len(snake_coords) - 1)):
                    body_pictures[i] = pygame.image.load("Res/body_horizontal.png").convert_alpha()
                body_pictures[0] = pygame.image.load("Res/tail_left.png").convert_alpha()
            else:
                for i in reversed(range(2, len(snake_coords) - 1)):
                    body_pictures[i] = pygame.image.load("Res/body_horizontal.png").convert_alpha()
                if old_direction == 'up':
                    body_pictures[0] = pygame.image.load("Res/tail_down.png").convert_alpha()
                else:
                    body_pictures[0] = pygame.image.load("Res/tail_up.png").convert_alpha()
            if flag:
                old_direction = direction

        return [body_pictures, old_direction]

    # обработчик нажатий
    def movements_snake(self, speed_x, speed_y, direction, old_direction):
        old_direction = direction
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # стрелочки
                if event.key == pygame.K_LEFT and speed_x != snake_block:
                    speed_x = -snake_block
                    speed_y = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and speed_x != -snake_block:
                    speed_x = snake_block
                    speed_y = 0
                    direction = 'right'
                elif event.key == pygame.K_UP and speed_y != snake_block:
                    speed_y = -snake_block
                    speed_x = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN and speed_y != -snake_block:
                    speed_y = snake_block
                    speed_x = 0
                    direction = 'down'
                # WASD
                elif event.key == pygame.K_w and speed_y != snake_block:
                    speed_y = -snake_block
                    speed_x = 0
                    direction = 'up'
                elif event.key == pygame.K_a and speed_x != snake_block:
                    speed_x = -snake_block
                    speed_y = 0
                    direction = 'left'
                elif event.key == pygame.K_s and speed_y != -snake_block:
                    speed_y = snake_block
                    speed_x = 0
                    direction = 'down'
                elif event.key == pygame.K_d and speed_x != -snake_block:
                    speed_x = snake_block
                    speed_y = 0
                    direction = 'right'
                # выход из программы
                elif event.key == pygame.K_ESCAPE:
                    terminate()
        return [speed_x, speed_y, direction, old_direction]

    # функция, которая ловит пересечения, ведущие к окончанию игры
    def intersection(self, body, snake_or_apple):
        for i in body[:-1]:
            if i.colliderect(snake_or_apple):
                return True

        for i in kamni_group:
            if snake_or_apple.colliderect(i):
                return True
        return False


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


# Спрайты фона
class Trava(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(trava_group)
        screen.fill(white)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# Спрайты препятствий
class Kamni(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(kamni_group)
        screen.fill(white)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


trava_group = SpriteGroup()
kamni_group = SpriteGroup()


# подготовавливаем файл уровня
def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Trava('empty', x, y)
            elif level[y][x] == '#':
                Kamni('wall', x, y)


level_map = load_level("map1.txt")
generate_level(level_map)

# главная функция
def game():
    # Начальные параметры
    game_over = False
    lvl = 1
    x = snake_block * 5
    y = snake_block * 6

    speed_x = 0
    speed_y = 0
    direction = 'down'
    old_direction = direction

    snake_coords = [[x, y-snake_block*2], [x, y-snake_block], [x, y]]

    body_pictures = [pygame.image.load('Res/tail_up.png').convert_alpha(),
                     pygame.image.load('Res/body_vertical.png').convert_alpha(),
                     pygame.image.load('Res/head_down.png').convert_alpha()]

    body_rect = [body_pictures[0].get_rect(bottomright=(snake_coords[0][0], snake_coords[0][1])),
                 body_pictures[1].get_rect(bottomright=(snake_coords[1][0], snake_coords[1][1])),
                 body_pictures[2].get_rect(bottomright=(snake_coords[2][0], snake_coords[2][1]))]
    length = 3
    snake = Snake(snake_block)
    apple_x = random.randint(1, width//snake_block) * snake_block
    apple_y = random.randint(1, height//snake_block) * snake_block
    apple = pygame.image.load('Res/apple.png').convert_alpha()
    apple_size = apple.get_rect(bottomright=(apple_x, apple_y))
    while snake.intersection(body_rect, apple_size) is True:
        apple_x = random.randint(1, width // snake_block) * snake_block
        apple_y = random.randint(1, height // snake_block) * snake_block
        apple_size = apple.get_rect(bottomright=(apple_x, apple_y))
    # основной цикл игры
    while not game_over:
        # получаем список с картинками для тела
        body_pictures, old_direction = snake.snake_draw(snake_coords, direction, body_pictures, old_direction)
        # проверяем пересечение с препятствиями или с телом
        #game_over = snake.intersection(body_rect, body_rect[-1])
        # проверка на выход за игровую зону
        if x > width:
            x = 0
        if x < 0:
            x = ((width - snake_block) // snake_block) * snake_block
        if y > height:
            y = snake_block
        if y < 0:
            y = ((720 - snake_block)//snake_block)*snake_block + snake_block + 1

        apple_size = apple.get_rect(bottomright=(apple_x, apple_y))
        if apple_size.colliderect(body_rect[-1]):
            apple_x = random.randint(1, width // snake_block) * snake_block
            apple_y = random.randint(1, height // snake_block) * snake_block
            length += 1
            if lvl == 2:
                trava_group.empty()
                kamni_group.empty()
                level_map = load_level("map2.txt")
                generate_level(level_map)
            elif lvl == 3:
                trava_group.empty()
                kamni_group.empty()
                level_map = load_level("map3.txt")
                generate_level(level_map)
        while snake.intersection(body_rect, apple_size) is True:
            apple_x = random.randint(1, width // snake_block) * snake_block
            apple_y = random.randint(1, height // snake_block) * snake_block
            apple_size = apple.get_rect(bottomright=(apple_x, apple_y))
        # рисуем
        if 40 > length >= 20:
            lvl = 2
        if length > 40:
            lvl = 3

        trava_group.draw(screen)
        kamni_group.draw(screen)
        snake.score(length - 3)
        screen.blit(apple, apple_size)
        for i in reversed(range(len(body_pictures))):
            rect = body_pictures[i].get_rect(bottomright=(snake_coords[i][0], snake_coords[i][1]))
            body_rect[i] = rect
            screen.blit(body_pictures[i], rect)
        pygame.display.update()

        # смена координат
        # обрабатываем нажатие
        speed_x, speed_y, direction, old_direction = snake.movements_snake(speed_x, speed_y, direction, old_direction)
        x += speed_x
        y += speed_y
        if speed_x != 0 or speed_y != 0:
            # записываем координаты по спискам
            snake_head = [x, y]
            snake_coords.append(snake_head)
            del (snake_coords[0])
        clock.tick(FPS)

    # Game over
    terminate()


# запуск
start_screen()
game()

# реализовать переход между уровнями, реализовать рост змейки, подогнать размер картинок