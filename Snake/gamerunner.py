import pygame
from settings import Settings
from food import Food, create_food
from pygame.locals import *
from util import *
from snake import Snake, SnakeCell
from agent import *
import numpy as np


class GameRunner:
    def __init__(self, settings=Settings()) -> None:
        self.settings = settings
        self.game_going = True
        self.snake = Snake()
        self.food = Food()
        self.score_point = 0
        self.path = []
        self.clock = pygame.time.Clock()
        pygame.init()
        self.screen = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption("Snake")
        self.data = []
        self.file_name = 'agent2'

    def update_screen(self):
        pygame.display.set_caption(f"Snake {self.score_point}")
        # if self.score_point < 100:
        #     return
        self.screen.fill(self.settings.bg_color)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        draw_grid(self.screen, self.settings)
        pygame.display.flip()
        self.clock.tick(10*self.settings.snake_speed)

    def gameinit(self):
        self.game_going = True
        self.path_iter = iter(self.path)
        self.score_point = 0
        self.snake = Snake([
            SnakeCell(self.settings.row // 2, self.settings.col // 2, self.settings.snake_color)])
        self.food = create_food(self.snake, self.settings)
        self.update_screen()

    def running(self):

        # quit or restart listener
        if not self.game_going:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.gameinit()
                elif event.type == QUIT:
                    np.save(self.file_name, np.array(self.data))
                    exit(0)
            return

        # turn listener
        flag_get_key = False
        for event in pygame.event.get():
            if event.type == QUIT:
                np.save(self.file_name, np.array(self.data))
                exit(0)
            elif event.type == KEYDOWN and not flag_get_key:
                flag_get_key = True
                if event.key == K_LEFT:
                    self.snake.turn('left')
                if event.key == K_RIGHT:
                    self.snake.turn('right')
                if event.key == K_UP:
                    self.snake.turn('up')
                if event.key == K_DOWN:
                    self.snake.turn('down')

        # agent & turn 以下代码会用AI覆盖掉人的操作，也就是说蛇会自己走
        # 解除注释即可调用
        '''
        try:
            direction = next(self.path_iter)
            # print('try')
            if not isReach(move_point(self.snake.bodys[0], direction), self.snake.bodys[-1], self.snake.bodys[:-1]):
                # print('yes')
                self.path = []
                self.path_iter = iter(self.path)
                self.snake.turn(agent1(self.snake, self.food)[0])
            else:
                self.snake.turn(direction)
        except StopIteration:
            # print('try')
            self.path = agent(self.snake, self.food)
            self.path_iter = iter(self.path)
            direction = next(self.path_iter)
            if not isReach(move_point(self.snake.bodys[0], direction), self.snake.bodys[-1], self.snake.bodys[:-1]):
                # print('yes')
                self.path = []
                self.path_iter = iter(self.path)
                self.snake.turn(agent1(self.snake, self.food)[0])
            else:
                self.snake.turn(direction)
        '''

        eat_flag = self.snake.will_eat(self.food)
        if eat_flag:
            self.food = create_food(self.snake, self.settings)
            self.score_point += 1

        self.snake.move(eat_flag)

        crash = self.snake.is_selfcrash()
        if crash:
            self.game_going = 0
            print("You die, and please press space to restart")
            self.data.append(self.score_point)
            # 解除注释下面这句话会使得一死就重开
            # self.gameinit()

        self.update_screen()

    def start_client(self):
        self.gamegoing = True
        self.gameinit()
        while True:
            self.running()


if __name__ == '__main__':
    runner = GameRunner()
    runner.start_client()
