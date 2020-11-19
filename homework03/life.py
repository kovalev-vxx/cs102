import pathlib
import random
import typing as tp
import copy

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
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for row in range(self.rows):
            row = []  # type: ignore
            for col in range(self.cols):
                if randomize == False:
                    row.append(0)  # type: ignore
                else:
                    row.append(random.randint(0, 1))  # type: ignore
            grid.append(row)
        return grid  # type: ignore

    def get_neighbours(self, cell: Cell) -> Cells:
        x, y = cell
        neighbours = []
        for i in range(x - 1, x + 2):
            for m in range(y - 1, y + 2):
                if i < 0:
                    continue
                if m < 0:
                    continue
                if i > self.rows - 1:
                    continue
                if m > self.cols - 1:
                    continue
                if not (i == x and m == y):
                    neighbours.append(self.curr_generation[i][m])
        return neighbours

    def get_next_generation(self) -> Grid:
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
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.generations <= self.max_generations:  # type: ignore
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        if self.prev_generation != self.curr_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
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
        with open(filename, "w") as save_file:
            for i in range(self.rows):
                for j in range(self.cols):
                    if j == self.cols - 1:
                        save_file.write(str(self.curr_generation[i][j]) + "\n")
                    else:
                        save_file.write(str(self.curr_generation[i][j]))
            save_file.close()
