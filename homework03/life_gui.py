import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI
import argparse
import pathlib


class GUI(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

        self.width = args.width
        self.height = args.height
        self.cell_size = args.cell_size
        self.speed = args.speed
        self.load_name = args.load_name
        self.load = args.load
        self.save_name = args.save_name
        self.screen_size = args.width, args.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = cell_width
        self.cell_height = cell_height

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

        if self.load:
            self.grid = GameOfLife.from_file(self.load_name).curr_generation
            self.life.curr_generation = GameOfLife.from_file(self.load_name).curr_generation
        else:
            self.grid = self.life.create_grid(randomize=True)

        pause = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:  # type: ignore
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if pause:
                            pause = False
                        else:
                            pause = True
                    if event.key == pygame.K_s:
                        self.life.save(self.save_name)
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button:
                        y, x = pygame.mouse.get_pos()
                        x = x // self.cell_size
                        y = y // self.cell_size
                        if self.grid[x][y]:
                            self.grid[x][y] = 0
                        else:
                            self.grid[x][y] = 1

            if self.life.is_max_generations_exceeded == False or self.life.is_changing == False:
                running = False

            if pause == True:
                self.draw_grid()
                self.draw_lines()
            else:
                self.draw_grid()
                self.draw_lines()
                self.life.step()
                self.grid = self.life.curr_generation
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_grid(self) -> None:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Settings")
    parser.add_argument(
        "--width", default=320, type=int, action="store", dest="width", help="Ширина поля"
    )
    parser.add_argument(
        "--height", default=240, type=int, action="store", dest="height", help="Высота поля"
    )
    parser.add_argument(
        "--size", default=20, type=int, action="store", dest="cell_size", help="Размер клеток"
    )
    parser.add_argument(
        "--speed", default=10, type=int, action="store", dest="speed", help="Скорость игры"
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
        cell_width = GameOfLife.from_file(args.load_name).rows
        cell_height = GameOfLife.from_file(args.load_name).cols
        width = cell_width * args.cell_size
        height = cell_height * args.cell_size
    else:
        cell_width = args.width // args.cell_size
        cell_height = args.height // args.cell_size

    if args.max:
        game = GameOfLife((cell_height, cell_width), max_generations=args.max)
    else:
        game = GameOfLife((cell_height, cell_width))

    ui = GUI(game)
    ui.run()
