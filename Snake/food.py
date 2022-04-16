from point import Point
from util import draw_rect
from settings import Settings
from random import randint


class Food(Point):
    def copy(self):
        return Food(self.row, self.col, self.color)

    def draw(self, screen):
        draw_rect(screen, self)


def create_food(snake, settings: Settings):
    while True:
        new_food = Food(randint(0, settings.row - 1),
                        randint(0, settings.col - 1), settings.food_color)
        is_crash = snake.is_crash(new_food)
        if not is_crash:
            return new_food
