import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', str(name))
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Тут указываешь вместо цветов по умолчанию те цвета
# которые пользователь выбрал в главном меню в виде переменной. (потом подключим)
COLOR_B = "var2_b.png"
COLOR_W = "var2_w.png"


class PoleReversi:
    # Хранение данных поля
    # (расположение фишек, цвета фишек и доски: по умолчанию или выбранные пользователем в меню)
    def __init__(self, color_pole=("#C7CFD4"), versy=1):
        self.pole = [[0 for i in range(8)] for j in range(8)]
        self.pole[3][3] = 2
        self.pole[4][4] = 2
        self.pole[3][4] = 1
        self.pole[4][3] = 1
        self.hod = 1
        self.color_pole = color_pole
        self.width = 8
        self.height = 8
        self.left = 10
        self.top = 10
        self.cell_size = 60
        self.versy = versy

    def vozmozhnyj_hod(self):  # Нахождение клеток, куда можно походить
        for i in range(8):
            for j in range(8):
                if self.pole[i][j] == 3:
                    self.pole[i][j] = 0
        for i in range(8):
            for j in range(8):
                if not self.pole[i][j]:  # проверка по вертикали вниз
                    if i != 7 and self.pole[i + 1][j] not in (0, 3, self.hod):
                        for i1 in range(i + 1, 8):
                            if self.pole[i1][j] in (0, 3):
                                break
                            if self.pole[i1][j] == self.hod:
                                self.pole[i][j] = 3
                                break
                if not self.pole[i][j]:  # проверка по вертикали вверх
                    if i != 0 and self.pole[i - 1][j] not in (0, 3, self.hod):
                        for i1 in range(i - 1, -1, -1):
                            if self.pole[i1][j] in (0, 3):
                                break
                            if self.pole[i1][j] == self.hod:
                                self.pole[i][j] = 3
                                break
                if not self.pole[i][j]:  # проверка по горизонтали влево
                    if j != 0 and self.pole[i][j - 1] not in (0, 3, self.hod):
                        for j1 in range(j - 1, -1, -1):
                            if self.pole[i][j1] in (0, 3):
                                break
                            if self.pole[i][j1] == self.hod:
                                self.pole[i][j] = 3
                                break
                if not self.pole[i][j]:  # проверка по горизонтали вправо
                    if j != 7 and self.pole[i][j + 1] not in (0, 3, self.hod):
                        for j1 in range(j + 1, 8):
                            if self.pole[i][j1] in (0, 3):
                                break
                            if self.pole[i][j1] == self.hod:
                                self.pole[i][j] = 3
                                break
                if not self.pole[i][j]:  # проверка по диагонали вправо-вниз
                    if j != 7 and i != 7 and self.pole[i + 1][j + 1] not in (0, 3, self.hod):
                        f = True
                        for i1 in range(i + 1, 8):
                            for j1 in range(j + 1, 8):
                                if i1 - i == j1 - j:
                                    if self.pole[i1][j1] in (0, 3):
                                        f = False
                                        break
                                    if self.pole[i1][j1] == self.hod:
                                        self.pole[i][j] = 3
                                        f = False
                                        break
                            if not f:
                                break
                if not self.pole[i][j]:  # проверка по диагонали вправо-вверх
                    if j != 7 and i != 0 and self.pole[i - 1][j + 1] not in (0, 3, self.hod):
                        f = True
                        for i1 in range(i - 1, -1, -1):
                            for j1 in range(j + 1, 8):
                                if i - i1 == j1 - j:
                                    if self.pole[i1][j1] in (0, 3):
                                        f = False
                                        break
                                    if self.pole[i1][j1] == self.hod:
                                        self.pole[i][j] = 3
                                        f = False
                                        break
                            if not f:
                                break
                if not self.pole[i][j]:  # проверка по диагонали влево-вниз
                    if j != 0 and i != 7 and self.pole[i + 1][j - 1] not in (0, 3, self.hod):
                        f = True
                        for i1 in range(i + 1, 8):
                            for j1 in range(j - 1, -1, -1):
                                if i1 - i == j - j1:
                                    if self.pole[i1][j1] in (0, 3):
                                        f = False
                                        break
                                    if self.pole[i1][j1] == self.hod:
                                        self.pole[i][j] = 3
                                        f = False
                                        break
                            if not f:
                                break
                if not self.pole[i][j]:  # проверка по диагонали влево-вверх
                    if j != 0 and i != 0 and self.pole[i - 1][j - 1] not in (0, 3, self.hod):
                        f = True
                        for i1 in range(i - 1, -1, -1):
                            for j1 in range(j - 1, -1, -1):
                                if i - i1 == j - j1:
                                    if self.pole[i1][j1] in (0, 3):
                                        f = False
                                        break
                                    if self.pole[i1][j1] == self.hod:
                                        self.pole[i][j] = 3
                                        f = False
                                        break
                            if not f:
                                break

    def render(self, screen):
        self.vozmozhnyj_hod()
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(self.color_pole),
                                 (x * self.cell_size + self.left,
                                  y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color(0, 0, 0),
                                 (x * self.cell_size + self.left,
                                  y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.clik_hod(cell)

    def get_cell(self, pos):
        for y in range(self.height):
            for x in range(self.width):
                x1 = x * self.cell_size + self.left
                y1 = y * self.cell_size + self.top
                if x1 < pos[0] < x1 + self.cell_size and y1 < pos[1] < y1 + self.cell_size:
                    return x, y
        return None

    def opposite_hod(self, cur_hod):  # функция просто возвращающая белый ход, если сейчас ход черных, и наоборот
        if cur_hod == 1:
            return 2
        else:
            return 1

    def clik_hod(self, cell):
        if not cell or self.pole[cell[0]][cell[1]] != 3:
            return

        self.pole[cell[0]][cell[1]] = self.hod

        opposite = self.opposite_hod(self.hod)

        lines_ar = ((1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1))

        for line in lines_ar:
            row = line[0]
            column = line[1]

            i = cell[0] + row
            j = cell[1] + column

            to_flip_ar = []  # координаты фишек, которые перевернутся

            if i in range(8) and j in range(8) and self.pole[i][j] == opposite:
                to_flip_ar.append((i, j))
                i = i + row
                j = j + column
                while i in range(8) and j in range(8) and self.pole[i][j] == opposite:
                    to_flip_ar.append((i, j))
                    i = i + row
                    j = j + column
                if i in range(8) and j in range(8) and self.pole[i][j] == self.hod:
                    for coords in to_flip_ar:
                        self.pole[coords[0]][coords[1]] = self.hod

        self.hod = opposite

    def get_colvo(self, cell):
        opposite = self.opposite_hod(self.hod)
        colvo = 0
        lines_ar = ((1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1))

        for line in lines_ar:
            row = line[0]
            column = line[1]
            i = cell[0] + row
            j = cell[1] + column
            to_flip_ar = []  # координаты фишек, которые могут перевернутся

            if self.pole[i][j] == opposite and i in range(8) and j in range(8):
                to_flip_ar.append((i, j))
                i = i + row
                j = j + column
                while self.pole[i][j] == opposite and i in range(8) and j in range(8):
                    to_flip_ar.append((i, j))
                    i = i + row
                    j = j + column
                if self.pole[i][j] == self.hod and i in range(8) and j in range(8):
                    colvo += len(to_flip_ar)

        return colvo

    def victory(self):
        c1, c2 = 0, 0
        for i in self.pole:
            for j in i:
                if j == 3:
                    return 0
                if j == 1:
                    c1 += 1
                if j == 2:
                    c2 += 1
        if c1 == c2:
            return 3
        if c1 > c2:
            return 1
        if c2 > c1:
            return 2

    def restart(self):
        self.pole = [[0 for i in range(8)] for j in range(8)]
        self.pole[3][3] = 2
        self.pole[4][4] = 2
        self.pole[3][4] = 1
        self.pole[4][3] = 1
        self.hod = 1


pygame.init()
pygame.display.set_caption('Игра')
screen = pygame.display.set_mode((900, 500))
all_sprites = pygame.sprite.Group()
VERSY = 0
color_pole = ("#C7CFD4")
board = PoleReversi(color_pole, VERSY)
running = True


class Fishki(pygame.sprite.Sprite):
    image_b = load_image(COLOR_B, -1)
    image_w = load_image(COLOR_W, -1)
    image_3 = load_image("color_3.png", -1)
    image_0 = load_image("color_0.png", -1)

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Fishki.image_0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        cell = board.get_cell((self.rect.x, self.rect.y))
        if board.pole[cell[0]][cell[1]] == 1:
            self.image = Fishki.image_b
        elif board.pole[cell[0]][cell[1]] == 2:
            self.image = Fishki.image_w
        elif board.pole[cell[0]][cell[1]] == 3:
            self.image = Fishki.image_3
        elif board.pole[cell[0]][cell[1]] == 0:
            self.image = Fishki.image_0


class Restart(pygame.sprite.Sprite):
    image = load_image('restart.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Restart.image
        self.rect = self.image.get_rect()
        self.rect.x = 830
        self.rect.y = 430

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            board.restart()


for y in range(board.height):
    for x in range(board.width):
        Fishki(all_sprites, x * board.cell_size + board.left + 1,
               y * board.cell_size + board.top + 1)
Restart(all_sprites)


def draw(screen):
    victory = board.victory()
    if not victory:
        font = pygame.font.Font(None, 40)
        if board.hod == 1:
            text = font.render("Ход черных", True, (255, 255, 255))
        else:
            text = font.render("Ход белых", True, (255, 255, 255))
        text_x = 600
        text_y = 75
        screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 25)
    s = 0
    for i in board.pole:
        for j in i:
            if j == 1:
                s += 1
    text = font.render(f"У черных {s} фишек", True, (255, 255, 255))
    text_x = 625
    text_y = 175
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 25)
    s = 0
    for i in board.pole:
        for j in i:
            if j == 2:
                s += 1
    text = font.render(f"У белых {s} фишек", True, (255, 255, 255))
    text_x = 625
    text_y = 200
    screen.blit(text, (text_x, text_y))

    if victory:
        font = pygame.font.Font(None, 40)
        if victory == 1:
            text = font.render(f"Выиграли черыне", True, (255, 255, 255))
        elif victory == 2:
            text = font.render(f"Выиграли белые", True, (255, 255, 255))
        else:
            text = font.render(f"Ничья", True, (255, 255, 255))
        text_x = 600
        text_y = 300
        screen.blit(text, (text_x, text_y))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    all_sprites.update(event)
    board.render(screen)
    all_sprites.draw(screen)
    draw(screen)
    pygame.display.flip()