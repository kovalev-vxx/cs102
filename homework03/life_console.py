import curses
import curses.ascii
from life import GameOfLife
from ui import UI
import pathlib
import argparse


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

        self.width = args.width
        self.height = args.height
        self.speed = args.speed
        self.load_name = args.load_name
        self.load = args.load
        self.save_name = args.save_name

    def run(self) -> None:
        screen = curses.initscr()
        y, x = screen.getmaxyx()

        if self.height > y or self.width > x:
            curses.endwin()
            print(f"\n Неправильное разрешение (размер терминала {x}x{y})\n")
        else:
            win = curses.newwin(self.height, self.width)
            win.keypad(True)
            curses.noecho()
            curses.curs_set(0)
            curses.mousemask(1)
            win.nodelay(True)

            self.draw_borders(win)

            if self.load:
                self.grid = GameOfLife.from_file(self.load_name).curr_generation
                self.life.curr_generation = GameOfLife.from_file(self.load_name).curr_generation
            else:
                self.grid = self.life.create_grid(randomize=True)

            key = 0
            while key != curses.ascii.ESC:
                win.timeout(self.speed)
                self.draw_grid(win)

                self.life.step()
                self.grid = self.life.curr_generation
                key = win.getch()

                if key == ord("s"):
                    self.life.save(self.save_name)
                    break

                if self.life.is_max_generations_exceeded == False or self.life.is_changing == False:
                    break

                if key == curses.KEY_MOUSE:
                    _, x, y, _, _ = curses.getmouse()
                    if self.grid[y - 1][x - 1]:
                        self.grid[y - 1][x - 1] = 0
                    else:
                        self.grid[y - 1][x - 1] = 1

                if key == curses.ascii.SP:
                    key = -1
                    while key != curses.ascii.SP:
                        self.draw_grid(win)
                        key = win.getch()
                        if key == curses.KEY_MOUSE:
                            _, x, y, _, _ = curses.getmouse()
                            if self.grid[y - 1][x - 1]:
                                self.grid[y - 1][x - 1] = 0
                            else:
                                self.grid[y - 1][x - 1] = 1
                        if key == curses.ascii.ESC:
                            break
                    continue

        curses.endwin()
        print(f"\n Число генераций - {self.life.generations - 1}\n")

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y - 1][x - 1]:
                    screen.addch(y, x, "\u25AA")
                else:
                    screen.addch(y, x, " ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Настройки GAME OF LIFE")
    parser.add_argument(
        "--width", default=50, type=int, action="store", dest="width", help="Ширина поля"
    )
    parser.add_argument(
        "--height", default=20, type=int, action="store", dest="height", help="Высота поля"
    )
    parser.add_argument(
        "--speed", default=150, type=int, action="store", dest="speed", help="Скорость игры"
    )
    parser.add_argument(
        "--max", type=float, action="store", dest="max", help="Максимальное число генерация"
    )
    parser.add_argument(
        "--save",
        default="save.txt",
        type=pathlib.Path,
        action="store",
        dest="save_name",
        help="Файл для сохранения",
    )
    parser.add_argument(
        "--load_name",
        default="save.txt",
        type=pathlib.Path,
        action="store",
        dest="load_name",
        help="Файл для загрузки",
    )
    parser.add_argument("--load", action="store", dest="load", help="Загрузить игру?")
    args = parser.parse_args()

    if args.load:
        args.width = GameOfLife.from_file(args.load_name).rows
        args.height = GameOfLife.from_file(args.load_name).cols
    if args.max:
        game = GameOfLife((args.height - 1, args.width - 1), max_generations=args.max)
    else:
        game = GameOfLife((args.height - 1, args.width - 1))

    console = Console(game)
    console.run()
