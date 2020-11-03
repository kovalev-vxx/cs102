from typing import Tuple, List, Set, Optional
import random


def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: List[str], n: int) -> List[List[str]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    list = []
    while len(values) > n:
        part_list = values[:n]
        list.append(part_list)
        values = values[n:]
    list.append(values)
    return list


def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """

    row, col = pos
    return grid[row]


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    actual_col: List[str] = []
    row, col = pos
    for row in grid:
        for i in row[col]:
            actual_col.append(str(i))

    return actual_col


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    expected_block = []
    if col % 3 == 0:
        col += 3
    if row % 3 == 0:
        row += 3
    if row == 0:
        row += 1
    if col == 0:
        col += 1
    while row % 3 != 0:
        row += 1
    while col % 3 != 0:
        col += 1

    for i in grid[row - 3 : row]:
        for m in i[col - 3 : col]:
            expected_block.append(m)

    return expected_block


def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """

    for i in grid:
        for m in i:
            if m == ".":
                row = i.index(m)
                col = grid.index(i)
                pos = col, row
                return pos


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    row, col = pos
    values: Set[str] = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
    for i in grid[row]:
        values.discard(i)
    for i in grid:
        for m in i[col]:
            values.discard(m)
    for i in get_block(grid, pos):
        values.discard(i)

    return values


def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """

    for row in range(9):
        for col in range(9):
            if grid[row][col] == ".":
                for x in list(find_possible_values(grid, (row, col))):
                    grid[row][col] = x
                    solution = solve(grid)
                    if solution:
                        return solution
                    else:
                        grid[row][col] = "."
                return
    return grid


def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    values = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

    for row in range(9):
        for col in range(9):
            pos = row, col
            block = set()
            row_solution = set()
            col_solution = set()
            if not solution[row][col] in values:
                return False
            for i in get_block(solution, pos):
                block.add(i)
            if block != values:
                return False
            for i in solution[row]:
                row_solution.add(i)
            if row_solution != values:
                return False
            for i in solution:
                for m in i[col]:
                    col_solution.add(m)
            if col_solution != values:
                return False
    return True


def generate_sudoku(N: int) -> List[List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    max_sudoku_numbers = 81
    if N > max_sudoku_numbers:
        N = max_sudoku_numbers
    z = 0
    new_grid = []
    empty_grid = []
    for row in range(9):
        for col in range(9):
            empty_grid.append(".")
    random_grid = group(empty_grid, 9)
    solution = solve(random_grid)

    for i in solution:
        for m in i:
            new_grid.append(m)

    while z != max_sudoku_numbers - N:
        a = random.choice(new_grid)
        if a != ".":
            new_grid[new_grid.index((a))] = "."
            z += 1

    return group(new_grid, 9)


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
