import random
import typing as tp

import pygame
from pygame.locals import *
import copy

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("gray"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("gray"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()

        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT: # type: ignore
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """

        random_grid = []

        if randomize == False:
            for row in range(self.cell_height):
                for col in range(self.cell_width):
                    random_grid.append(0)
        else:
            for row in range(self.cell_height):
                for col in range(self.cell_width):
                    random_grid.append(random.randint(0, 1))

        grid = []
        while random_grid:
            part_list = random_grid[: self.cell_width]
            grid.append(part_list)
            random_grid = random_grid[self.cell_width :]
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for x in range(self.cell_height):
            for y in range(self.cell_width):
                if self.grid[x][y]:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size),
                    )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        x, y = cell
        neighbours = []

        if x == 0 and y == 0:
            for i in range(x, x + 2):
                for j in range(y, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(self.grid[i][j])

        elif x == 0 and 0 < y < self.cell_width - 1:
            for i in range(x, x + 2):
                for j in range(y - 1, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(self.grid[i][j])

        elif 0 < x < self.cell_height - 1 and y == 0:
            for i in range(x - 1, x + 2):
                for j in range(y, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(self.grid[i][j])

        elif x == self.cell_height - 1 and y == self.cell_width - 1:
            for i in range(x - 1, x + 1):
                for j in range(y - 1, y + 1):
                    if not (i == x and j == y):
                        neighbours.append(self.grid[i][j])

        elif x == self.cell_height - 1 and 0 < y < self.cell_width - 1:
            for i in range(x - 1, x + 1):
                for j in range(y - 1, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(self.grid[i][j])

        elif 0 < x < self.cell_height - 1 and y == self.cell_width - 1:
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 1):
                    if not (i == x and j == y):
                        neighbours.append(self.grid[i][j])

        elif x == 0 and y == self.cell_width - 1:
            for i in range(x, x + 2):
                for j in range(y - 1, y + 1):
                    if not (i == x and j == y):
                        neighbours.append(self.grid[i][j])

        elif x == self.cell_height - 1 and y == 0:
            for i in range(x - 1, x + 1):
                for j in range(y, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(self.grid[i][j])
        else:
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(self.grid[i][j])

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """

        copy_grid = copy.deepcopy(self.grid)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if sum(self.get_neighbours((i, j))) == 3 and self.grid[i][j] == 0:
                    copy_grid[i][j] = 1
                elif self.grid[i][j] and (1 < sum(self.get_neighbours((i, j))) < 4):
                    copy_grid[i][j] = 1
                else:
                    copy_grid[i][j] = 0
        return copy_grid


if __name__ == "__main__":
    game = GameOfLife(160, 120, 20, 10)
    game.run()
    print(123)
