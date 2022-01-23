import pygame


# отработка WASD
def movements_snake(self):
    x_head, y_head = self.hero.get_position()
    if pygame.key.get_pressed()[pygame.K_a]:
        x_head -= 1
    if pygame.key.get_pressed()[pygame.K_d]:
        x_head += 1
    if pygame.key.get_pressed()[pygame.K_w]:
        y_head -= 1
    if pygame.key.get_pressed()[pygame.K_s]:
        y_head += 1
    if self.labyrinth.is_free((x_head, y_head)):
        self.hero.set_position((x_head, y_head))


# отработка стрелочек
def movements_snake2(self):
    x_head, y_head = self.hero.get_position()
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        x_head -= 1
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        x_head += 1
    if pygame.key.get_pressed()[pygame.K_UP]:
        y_head -= 1
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        y_head += 1
    if self.labyrinth.is_free((x_head, y_head)):
        self.hero.set_position((x_head, y_head))
