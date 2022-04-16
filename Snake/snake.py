from point import Point, SnakeCell
from settings import Settings
from util import draw_rect, move_point
from direct import Direct


class Snake:
    def __init__(self, bodys=[SnakeCell()], settings=Settings()) -> None:
        self.bodys = bodys
        self.direct_id = 1
        self.settings = settings
        self.direct = Direct()

    def __str__(self) -> str:
        return f'snake_head: {self.bodys[0].row} {self.bodys[0].col}'

    def turn(self, id):
        if isinstance(id, str):
            id = self.direct.direct_id_dict[id]
        if id >= 2 and self.direct_id <= 1:
            self.direct_id = id
        elif id <= 1 and self.direct_id >= 2:
            self.direct_id = id

    def will_eat(self, food):
        new_head = move_point(self.bodys[0], self.direct_id)
        return new_head == food

    def is_selfcrash(self):
        for body in self.bodys[1:]:
            if body == self.bodys[0]:
                return True
        return False

    def is_crash(self, target: Point):
        for body in self.bodys:
            if body == target:
                return True
        return False

    def move(self, longer_flag):
        self.bodys.insert(0, self.bodys[0].copy())
        self.bodys[0] = move_point(self.bodys[0], self.direct_id)
        if not longer_flag:
            self.bodys.pop()

    def draw(self, screen):
        for body in self.bodys:
            draw_rect(screen, body)
        draw_rect(screen, self.bodys[0], self.settings.head_color)
