import pathlib
import random
import typing as tp
import copy
from pprint import pprint

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
            self,
            size: tp.Tuple[int, int],
            randomize: bool = True,
            max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment

        random_grid = []

        if randomize == False:
            for row in range(self.rows):
                for col in range(self.cols):
                    random_grid.append(0)
        else:
            for row in range(self.rows):
                for col in range(self.cols):
                    random_grid.append(random.randint(0, 1))

        grid = []
        while random_grid:
            part_list = random_grid[: self.cols]
            grid.append(part_list)
            random_grid = random_grid[self.cols:]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:

        x, y = cell
        neighbours = []

        if x == 0 and y == 0:
            for i in range(x, x + 2):
                for j in range(y, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(self.curr_generation[i][j])

        elif x == 0 and 0 < y < self.cols - 1:
            for i in range(x, x + 2):
                for j in range(y - 1, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(self.curr_generation[i][j])

        elif 0 < x < self.rows - 1 and y == 0:
            for i in range(x - 1, x + 2):
                for j in range(y, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(self.curr_generation[i][j])

        elif x == self.rows - 1 and y == self.cols - 1:
            for i in range(x - 1, x + 1):
                for j in range(y - 1, y + 1):
                    if not (i == x and j == y):
                        neighbours.append(self.curr_generation[i][j])

        elif x == self.rows - 1 and 0 < y < self.cols - 1:
            for i in range(x - 1, x + 1):
                for j in range(y - 1, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(self.curr_generation[i][j])

        elif 0 < x < self.rows - 1 and y == self.cols - 1:
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 1):
                    if not (i == x and j == y):
                        neighbours.append(self.curr_generation[i][j])

        elif x == 0 and y == self.cols - 1:
            for i in range(x, x + 2):
                for j in range(y - 1, y + 1):
                    if not (i == x and j == y):
                        neighbours.append(self.curr_generation[i][j])

        elif x == self.rows - 1 and y == 0:
            for i in range(x - 1, x + 1):
                for j in range(y, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(self.curr_generation[i][j])
        else:
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if not (i == x and j == y):
                        neighbours.append(self.curr_generation[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        copy_grid = copy.deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                if sum(self.get_neighbours((i, j))) == 3 and self.curr_generation[i][j] == 0:
                    copy_grid[i][j] = 1
                elif self.curr_generation[i][j] and (1 < sum(self.get_neighbours((i, j))) < 4):
                    copy_grid[i][j] = 1
                else:
                    copy_grid[i][j] = 0
        return copy_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations <= self.max_generations:  # type: ignore
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation != self.curr_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as file:
            lst = file.readlines()
        digits = [int(c) for c in open(filename).read() if c in "01"]

        rows = (len(lst[0])) - 1
        cols = len(lst)
        life = GameOfLife((rows, cols))

        grid = []
        while digits:
            part_list = digits[:rows]
            grid.append(part_list)
            digits = digits[rows:]
        life.curr_generation = grid
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        save_file = open(filename, "w")
        for i in range(self.rows):
            for j in range(self.cols):
                if j == self.cols - 1:
                    save_file.write(str(self.curr_generation[i][j]) + "\n")
                else:
                    save_file.write(str(self.curr_generation[i][j]))
        save_file.close()
        pass

