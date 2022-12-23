class PoleReversi:
    # Хранение данных поля
    # (расположение фишек, цвета фишек и доски: по умолчанию или выбранные пользователем в меню)
    def __init__(self, color_b=(0, 0, 0), color_w=(255, 255, 255), color_pole=(138, 246, 214)):
        self.pole = [[0 for i in range(8)] for j in range(8)]
        self.pole[3][3] = 1
        self.pole[4][4] = 1
        self.pole[3][4] = 2
        self.pole[4][3] = 2
        self.hod = 1
        self.color_b, self.color_w, self.color_pole = color_b, color_w, color_pole

    def vozmozhnyj_hod(self):  # Нахождение клеток, куда можно походить
        for i in range(8):
            for j in range(8):
                if not self.pole[i][j]:  # проверка по вертикали вниз
                    if i != 7 and self.pole[i + 1][j] != 0 and self.pole[i + 1][j] != self.hod:
                        for i1 in range(i + 1, 8):
                            if self.pole[i1][j] in (0, 3):
                                break
                            if self.pole[i1][j] == self.hod:
                                self.pole[i][j] = 3
                                break
                if not self.pole[i][j]:  # проверка по вертикали вверх
                    if i != 0 and self.pole[i - 1][j] != 0 and self.pole[i - 1][j] != self.hod:
                        for i1 in range(i - 1, 0, -1):
                            if self.pole[i1][j] in (0, 3):
                                break
                            if self.pole[i1][j] == self.hod:
                                self.pole[i][j] = 3
                                break
                if not self.pole[i][j]:  # проверка по горизонтали влево
                    if j != 0 and self.pole[i][j - 1] != 0 and self.pole[i][j - 1] != self.hod:
                        for j1 in range(j - 1, 0, -1):
                            if self.pole[i][j1] in (0, 3):
                                break
                            if self.pole[i][j1] == self.hod:
                                self.pole[i][j] = 3
                                break
                if not self.pole[i][j]:  # проверка по горизонтали вправо
                    if j != 7 and self.pole[i][j + 1] != 0 and self.pole[i][j + 1] != self.hod:
                        for j1 in range(j + 1, 8):
                            if self.pole[i][j1] in (0, 3):
                                break
                            if self.pole[i][j1] == self.hod:
                                self.pole[i][j] = 3
                                break
                if not self.pole[i][j]:  # проверка по диагонали вправо-вниз
                    if j != 7 and i != 7 and self.pole[i + 1][j + 1] != 0 and\
                            self.pole[i + 1][j + 1] != self.hod:
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
                    if j != 7 and i != 0 and self.pole[i - 1][j + 1] != 0 and \
                            self.pole[i - 1][j + 1] != self.hod:
                        f = True
                        for i1 in range(i - 1, 0, -1):
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
                    if j != 0 and i != 7 and self.pole[i + 1][j - 1] != 0 and \
                            self.pole[i + 1][j - 1] != self.hod:
                        f = True
                        for i1 in range(i + 1, 8):
                            for j1 in range(j - 1, 0, -1):
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
                    if j != 0 and i != 0 and self.pole[i - 1][j - 1] != 0 and \
                            self.pole[i - 1][j - 1] != self.hod:
                        f = True
                        for i1 in range(i - 1, 0, -1):
                            for j1 in range(j - 1, 0, -1):
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