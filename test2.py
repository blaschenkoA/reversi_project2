import time

import pygame
import sqlite3
import sys
import os


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


if __name__ == '__main__':
    PLAER = False

    class PoleReversi:
        # Хранение данных поля
        # (расположение фишек, цвета фишек и доски: по умолчанию или выбранные пользователем в меню)
        def __init__(self, color_pole="#ffddf8", versy=1):
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

        def clik_hod(self, cell, v=False):
            if not cell or self.pole[cell[0]][cell[1]] != 3:
                return

            if v or self.versy or (not self.versy and self.hod == 1):

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
            colvo_3 = 0
            self.vozmozhnyj_hod()
            for i in self.pole:
                for j in i:
                    if j == 3:
                        colvo_3 += 1
            if not colvo_3:
                self.hod = self.opposite_hod(opposite)

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

                if i in range(8) and j in range(8) and self.pole[i][j] == opposite:
                    to_flip_ar.append((i, j))
                    i = i + row
                    j = j + column
                    while i in range(8) and j in range(8) and self.pole[i][j] == opposite:
                        to_flip_ar.append((i, j))
                        i = i + row
                        j = j + column
                    if i in range(8) and j in range(8) and self.pole[i][j] == self.hod:
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
            self.hod = 1
            if c1 == c2:
                con = sqlite3.connect("players.db")
                cur = con.cursor()
                cur.execute("""UPDATE players SET draw_games = ?
                                WHERE id = ?""", (PLAER[4] + 1, PLAER[0]))
                con.commit()
                con.close()
                return 3
            if c1 > c2:
                con = sqlite3.connect("players.db")
                cur = con.cursor()
                cur.execute("""UPDATE players SET won_games = ?
                                WHERE id = ?""", (PLAER[2] + 1, PLAER[0]))
                con.commit()
                con.close()
                return 1
            if c2 > c1:
                con = sqlite3.connect("players.db")
                cur = con.cursor()
                cur.execute("""UPDATE players SET lost_games = ?
                                WHERE id = ?""", (PLAER[3] + 1, PLAER[0]))
                con.commit()
                con.close()
                return 2

        def restart(self):
            self.pole = [[0 for i in range(8)] for j in range(8)]
            self.pole[3][3] = 2
            self.pole[4][4] = 2
            self.pole[3][4] = 1
            self.pole[4][3] = 1
            self.hod = 1

        def bot(self):
            self.vozmozhnyj_hod()
            variant = []
            for i in range(8):
                for j in range(8):
                    if self.pole[i][j] == 3:
                        variant.append((i, j))

            if not variant:
                return

            best_variant = []
            for i in [(0, 0), (0, 7), (7, 7), (7, 0)]:
                if i in variant:
                    best_variant.append([i, self.get_colvo(i)])
            if best_variant:
                self.clik_hod(sorted(best_variant, key=lambda x: x[1])[-1][0], True)
                return

            for i in [(0, 2), (0, 3), (0, 4), (0, 5), (7, 2), (7, 3), (7, 4), (7, 5),
                      (2, 0), (3, 0), (4, 0), (5, 0), (2, 7), (3, 7), (4, 7), (5, 7)]:
                if i in variant:
                    best_variant.append([i, self.get_colvo(i)])
            if best_variant:
                self.clik_hod(sorted(best_variant, key=lambda x: x[1])[-1][0], True)
                return

            for i in [(2, 2), (2, 3), (2, 4), (2, 5), (5, 2), (5, 3), (5, 4), (5, 5),
                      (3, 2), (3, 5), (4, 2), (4, 5)]:
                if i in variant:
                    best_variant.append([i, self.get_colvo(i)])
            if best_variant:
                self.clik_hod(sorted(best_variant, key=lambda x: x[1])[-1][0], True)
                return

            for i in [(1, 2), (1, 3), (1, 4), (1, 5), (6, 2), (6, 3), (6, 4), (6, 5),
                      (2, 1), (3, 1), (4, 1), (5, 1), (2, 6), (3, 6), (4, 6), (5, 6)]:
                if i in variant:
                    best_variant.append([i, self.get_colvo(i)])
            if best_variant:
                self.clik_hod(sorted(best_variant, key=lambda x: x[1])[-1][0], True)
                return

            for i in [(1, 1), (1, 0), (0, 1), (1, 6), (1, 7), (0, 6), (6, 6), (6, 7),
                      (7, 6), (6, 1), (6, 0), (7, 1)]:
                if i in variant:
                    best_variant.append([i, self.get_colvo(i)])
            if best_variant:
                self.clik_hod(sorted(best_variant, key=lambda x: x[1])[-1][0], True)
                return

    pygame.init()
    size = window_width, window_height = 900, 500
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    gameDisplay = pygame.display.set_mode((window_width, window_height))
    font1 = pygame.font.SysFont("arialblack", 13)  # шрифт для получаемого текста
    font2 = pygame.font.SysFont("arialblack", 17)  # шрифт для надписей "войти" и "регистрация"
    font3 = pygame.font.SysFont("arialblack", 13)  # шрифт для выведения ошибок
    font4 = pygame.font.SysFont("arialblack", 19)  # шрифт для надписи "выход" в меню
    text = ''

    board = PoleReversi("#C7CFD4")

    AUTORIZATION = True
    MENU = False
    GAME = False

    COLOR_B = "var2_b.png"
    COLOR_W = "var2_w.png"

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
            self.rect.x = 500
            self.rect.y = 430

        def update(self, *args):
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                board.restart()

    clock = pygame.time.Clock()
    crashed = False

    def display_the_background(png_name, x, y):
        bck = load_image(png_name)
        gameDisplay.blit(bck, (x, y))

    input_box = pygame.Rect(579, 216, 20, 20)  # прямоугольник для ввода текста
    sign_in_button = pygame.Rect(724, 368, 136, 27)  # кнопка "войти"
    reg_button = pygame.Rect(724, 422, 136, 27)  # тож кнопка "регистрация"

    sign_in_label = font2.render("Войти", True, "black")
    reg_label = font2.render("Регистрация", True, "black")
    error_label = font2.render("", True, "#D7D7D9")

    color_inactive = pygame.Color("#474747")  # темно-серый
    color_active = pygame.Color('white')
    color = color_inactive
    active = False

    while not crashed:
        if AUTORIZATION:
            pygame.display.set_caption('Авторизация')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # если нажали на прямоугольник для ввода текста (input_box)
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive

                    # если нажата кнопка "войти"
                    if sign_in_button.collidepoint(event.pos):
                        if text == "":
                            error_label = font3.render("Введите имя аккаунта", True, "red")
                        else:
                            con = sqlite3.connect("players.db")
                            cur = con.cursor()
                            data = cur.execute("""SELECT * FROM players
                                                        WHERE account_name = ?""", (text,)).fetchall()
                            con.commit()
                            con.close()
                            if data:
                                AUTORIZATION = False
                                MENU = True
                                PLAER = data[0]
                                pygame.display.set_caption('Меню')
                            else:
                                error_label = font3.render("Аккаунта с такими данными не существует", True, "red")

                    # если нажата кнопка "зарегистрироваться"
                    if reg_button.collidepoint(event.pos):
                        if text == "":
                            error_label = font3.render("Введите имя аккаунта", True, "red")
                        else:
                            con = sqlite3.connect("players.db")
                            cur = con.cursor()
                            data = cur.execute("""SELECT * FROM players
                                                        WHERE account_name = ?""", (text,)).fetchall()
                            if data:
                                error_label = font3.render("Такой аккаунт уже существует. Попробуйте войти",
                                                           True, "red")
                            else:

                                cur.execute('''INSERT INTO players(
                                           account_name, won_games, lost_games, draw_games) VALUES (?, ?, ?, ?)''',
                                            (text, 0, 0, 0))
                                con.commit()
                                con.close()
                                AUTORIZATION = False
                                MENU = True
                                pygame.display.set_caption('Меню')

                if event.type == pygame.KEYDOWN:
                    error_label = font3.render("", True, "red")
                    if active:
                        if event.key == pygame.K_RETURN:
                            text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            gameDisplay.fill("white")
            display_the_background("background.png", 0, 0)

            # рендер текста
            txt_surface = font1.render(text, True, color)

            width = max(278, txt_surface.get_width() + 10)
            # изменение размера прямоугольника, если текст слишком большой
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y - 1))
            pygame.draw.rect(screen, color, input_box, 2)

            pygame.draw.rect(screen, "#E6E6E6", sign_in_button)  # кнопка "войти"
            screen.blit(sign_in_label, (762, 371))

            pygame.draw.rect(screen, (254, 162, 244), reg_button)  # кнопка "регистрация"
            screen.blit(reg_label, (733, 423))

            screen.blit(error_label, (515, 470))

            pygame.display.update()

        if MENU:
            display_the_background("menu.png", 0, 0)

            my_event = pygame.USEREVENT + 1
            pygame.time.set_timer(my_event, 1)

            ai_game = pygame.Rect(100, 160, 189, 69)  # кнопка для игры вдвоем
            ai_game_background = pygame.Rect(115, 217, 160, 4)
            two_player_game = pygame.Rect(100, 260, 189, 69)  # кнопка для игры против бота
            two_player_game_background = pygame.Rect(115, 317, 160, 4)
            quit = pygame.Rect(790, 465, 90, 20) # кнопка выхода
            quit_background = pygame.Rect(780, 490, 90, 3)

            pygame.draw.rect(screen, "#FF96E8", ai_game, 2)
            pygame.draw.rect(screen, "#FF96E8", two_player_game, 2)

            quit_label = font4.render("Выйти", True, "white")
            screen.blit(quit_label, (790, 465))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if two_player_game.collidepoint(event.pos):
                        pygame.display.set_caption('Игра')  # ЕСЛИ С ЧЕЛОВЕКОМ
                        MENU = False
                        GAME = True
                        board.versy = 1
                    if ai_game.collidepoint(event.pos):
                        pygame.display.set_caption('Игра')  # ЕСЛИ С БОТОМ
                        MENU = False
                        GAME = True
                        board.versy = 0
                    if quit.collidepoint(event.pos):
                        pygame.quit()
                if event.type == my_event:
                    x, y = pygame.mouse.get_pos()
                    if two_player_game.collidepoint((x, y)):
                        pygame.draw.rect(screen, "white", two_player_game_background)
                    if ai_game.collidepoint((x, y)):
                        pygame.draw.rect(screen, "white", ai_game_background)
                    if quit.collidepoint((x, y)):
                        pygame.draw.rect(screen, "white", quit_background)

            pygame.display.update()
            clock.tick(1000)

        if GAME:
            for y in range(board.height):
                for x in range(board.width):
                    Fishki(all_sprites, x * board.cell_size + board.left + 1,
                           y * board.cell_size + board.top + 1)

            rectangle = pygame.Rect(830, 430, 60, 60)
            pygame.draw.rect(screen, "black", rectangle)

            quit_icon = load_image("quit.png")
            gameDisplay.blit(quit_icon, (830, 430))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rectangle.collidepoint(event.pos):
                        GAME = False
                        MENU = True
                    board.get_click(event.pos)

            Restart(all_sprites)
            screen.fill((0, 0, 0))
            all_sprites.update(event)
            board.render(screen)
            all_sprites.draw(screen)
            draw(screen)
            quit_icon = load_image("quit.png")
            gameDisplay.blit(quit_icon, (830, 430))

            pygame.display.flip()

            if board.hod == 2 and not board.versy:
                time.sleep(0.5)
                board.bot()

    pygame.quit()
