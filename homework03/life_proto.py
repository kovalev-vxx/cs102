import random
import typing as tp

import pygame
from pygame.locals import *
from pprint import pprint

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
        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()

        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.draw_grid()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

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
            for row in range(self.cell_width):
                for col in range(self.cell_height):
                    random_grid.append(0)
        else:
            for row in range(self.cell_width):
                for col in range(self.cell_height):
                    random_grid.append(random.randint(0, 1))

        grid = []
        while random_grid:
            part_list = random_grid[:self.cell_width]
            grid.append(part_list)
            random_grid = random_grid[self.cell_width:]
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        grid = self.grid
        for x in range(self.cell_width):
            for y in range(self.cell_height):
                if grid[y][x]:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        pass



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

        grid = self.grid

        if x == 0 and y == 0:
            for i in range(x, x + 2):
                for j in range(y, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(grid[i][j])

        elif x == 0 and 0 < y < self.cell_width - 1:
            for i in range(x, x + 2):
                for j in range(y - 1, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(grid[i][j])

        elif 0 < x < self.cell_height - 1 and y == 0:
            for i in range(x - 1, x + 2):
                for j in range(y, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(grid[i][j])

        elif x == self.cell_height - 1 and y == self.cell_width - 1:
            for i in range(x - 1, x + 1):
                for j in range(y - 1, y + 1):
                    if not (i == x and j == y):
                        neighbours.append(grid[i][j])

        elif x == self.cell_height - 1  and 0 < y < self.cell_width - 1:
            for i in range(x - 1, x + 1):
                for j in range(y - 1, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(grid[i][j])

        elif 0 < x < self.cell_height - 1 and y == self.cell_width - 1:
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 1):
                    if not (i == x and j == y):
                        neighbours.append(grid[i][j])

        elif x == 0 and y == self.cell_width - 1:
            for i in range(x, x + 2):
                for j in range(y - 1, y + 1):
                    if not (i == x and j == y):
                        neighbours.append(grid[i][j])

        elif x == self.cell_height - 1 and y == 0:
            for i in range(x - 1, x + 1):
                for j in range(y, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(grid[i][j])
        else:
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(grid[i][j])

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """

        copy_grid = self.grid
        pprint(copy_grid)





        pass


if __name__ == '__main__':
    game = GameOfLife(160, 120, 20)

    game.run()