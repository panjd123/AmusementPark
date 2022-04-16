import random
import pygame
import numpy as np
from pygame.locals import *


def get_point(num):
    if num == 3:
        return 3
    if num == 4:
        return 6
    if num == 5:
        return 10
    if num >= 6:
        return 2 * num


class Xiaoxiaole:
    WIDTH = 500
    HEIGHT = 500
    SCREEN_SIZE = (WIDTH, HEIGHT)
    GRID_NUM = 8
    GRID_SIZE = 48
    GEM_SIZE = int(GRID_SIZE * 0.8)
    X_MARGIN = (WIDTH - GRID_SIZE * GRID_NUM) // 2
    Y_MARGIN = (HEIGHT - GRID_SIZE * GRID_NUM) // 2
    LINE_COLOR = (255, 165, 0)
    BACKGROUND_COLOR = (255, 255, 220)
    GEMS_KIND = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (122, 122, 122)]
    GEM_KIND_NUM = len(GEMS_KIND)
    gems = np.zeros((GRID_NUM, GRID_NUM), int)
    the_pos = (0, 0)
    to_pos = (-1, -1)
    flag_unchanged = False
    points = 0
    sparkles = np.zeros((GRID_NUM, GRID_NUM))
    DROP_TIME = 80
    OBSERVE_TIME = 300
    SPARKLE_TIMES = 4
    SPARKLE_TIME = 80
    TRY_TIME = 16
    lst_gems = gems.copy()
    lst_points = points
    health = 10

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('消消乐 当前分数为:' + str(points))

    # myfont = pygame.font.Font(None, 30)
    # textImage = myfont.render("The expected score of optimal operation is:", True, (0, 0, 0))
    # screen.blit(textImage, (0, 0))

    def __init__(self, _OBSERVE_TIME=300, _SPARKLE_TIMES=4):
        if _SPARKLE_TIMES % 2 == 1:
            _SPARKLE_TIMES += 1
        self.OBSERVE_TIME = _OBSERVE_TIME
        self.SPARKLE_TIMES = _SPARKLE_TIMES

    def init_gems(self):
        for i in range(self.GRID_NUM):
            for j in range(self.GRID_NUM):
                numx = [0, 0, 0, 0]
                numy = [0, 0, 0, 0]
                for k in range(1, 3):
                    if i - k >= 0:
                        numx[self.gems[i - k][j]] += 1
                    if j - k >= 0:
                        numy[self.gems[i][j - k]] += 1
                gem = random.randint(0, self.GEM_KIND_NUM - 1)
                while numx[gem] >= 2 or numy[gem] >= 2:
                    gem = random.randint(0, self.GEM_KIND_NUM - 1)
                self.gems[i][j] = gem
        self.lst_gems = self.gems.copy()

    def swap_pos(self, pos1, pos2):
        x, y = pos1
        s, t = pos2
        self.gems[x][y], self.gems[s][t] = self.gems[s][t], self.gems[x][y]

    def legal_movement(self, pos):
        i, j = pos
        if pos == (-1, -1):
            return False
        num = 1
        for k in range(-1, -3, -1):
            if 0 <= i + k < self.GRID_NUM and self.gems[i + k][j] == self.gems[i][j]:
                num += 1
            else:
                break
        for k in range(1, 3, 1):
            if 0 <= i + k < self.GRID_NUM and self.gems[i + k][j] == self.gems[i][j]:
                num += 1
            else:
                break
        if num >= 3:
            return True
        num = 1
        for k in range(-1, -3, -1):
            if 0 <= j + k < self.GRID_NUM and self.gems[i][j + k] == self.gems[i][j]:
                num += 1
            else:
                break
        for k in range(1, 3, 1):
            if 0 <= j + k < self.GRID_NUM and self.gems[i][j + k] == self.gems[i][j]:
                num += 1
            else:
                break
        if num >= 3:
            return True
        return False

    def legal_movement_2(self, pos1, pos2):
        self.swap_pos(pos1, pos2)
        ret = self.legal_movement(pos2)
        ret |= self.legal_movement(pos1)
        self.swap_pos(pos1, pos2)
        return ret

    def draw_background(self):
        self.screen.fill(self.BACKGROUND_COLOR)

    def draw_block(self, block, color=(255, 0, 0), size=2):
        pygame.draw.rect(self.screen, color, block, size)

    def draw_grids(self):
        for col in range(self.GRID_NUM + 1):
            pygame.draw.line(self.screen, self.LINE_COLOR, (self.X_MARGIN + col * self.GRID_SIZE, self.Y_MARGIN),
                             (self.X_MARGIN + col * self.GRID_SIZE, self.HEIGHT - self.Y_MARGIN), 2)
        for row in range(self.GRID_NUM + 1):
            pygame.draw.line(self.screen, self.LINE_COLOR, (self.X_MARGIN, self.Y_MARGIN + row * self.GRID_SIZE),
                             (self.WIDTH - self.X_MARGIN, self.Y_MARGIN + row * self.GRID_SIZE), 2)

    def draw_gems(self):
        for i in range(self.GRID_NUM):
            for j in range(self.GRID_NUM):
                if self.gems[i][j] != -1:
                    pygame.draw.circle(self.screen, self.GEMS_KIND[self.gems[i][j]], (
                        self.X_MARGIN + self.GRID_SIZE * (i + 0.5), self.Y_MARGIN + self.GRID_SIZE * (j + 0.5)),
                                       self.GEM_SIZE / 2)

    def redraw(self):
        self.draw_background()
        self.draw_grids()
        self.draw_gems()
        # self.screen.blit(self.textImage, (self.X_MARGIN//3, self.Y_MARGIN//3))
        pygame.display.flip()
        pygame.display.set_caption('消消乐 当前分数为:' + str(self.points) + "   还有" + str(self.health) + "轮机会")

    def get_block(self, pos):
        x, y = pos
        return (x - self.X_MARGIN) // self.GRID_SIZE, (y - self.Y_MARGIN) // self.GRID_SIZE

    def sparkle_del(self, d=1):
        tmp = self.gems.copy()
        for k in range(self.SPARKLE_TIMES + d):
            # 5times then del -1 1 -1 1 -1
            for i in range(self.GRID_NUM):
                for j in range(self.GRID_NUM):
                    if self.sparkles[i][j] == 1:
                        if self.gems[i][j] == -1:
                            self.gems[i][j] = tmp[i][j]
                        else:
                            self.gems[i][j] = -1
            self.redraw()
            pygame.time.wait(self.SPARKLE_TIME)
        self.sparkles = np.zeros((self.GRID_NUM, self.GRID_NUM))

    def calculate(self):
        flag = False
        # vis = np.zeros(self.GRID_NUM, self.GRID_NUM)
        fax = [[(j, i) for i in range(self.GRID_NUM)] for j in range(self.GRID_NUM)]
        szx = np.ones((self.GRID_NUM, self.GRID_NUM))
        fay = [[(j, i) for i in range(self.GRID_NUM)] for j in range(self.GRID_NUM)]
        szy = np.ones((self.GRID_NUM, self.GRID_NUM))
        for i in range(self.GRID_NUM):
            for j in range(self.GRID_NUM):
                if i + 1 < self.GRID_NUM and self.gems[i][j] == self.gems[i + 1][j] and self.gems[i][j] != -1:
                    fax[i + 1][j] = fax[i][j]
                    szx[fax[i][j][0]][fax[i][j][1]] += 1
                if j + 1 < self.GRID_NUM and self.gems[i][j] == self.gems[i][j + 1] and self.gems[i][j] != -1:
                    fay[i][j + 1] = fay[i][j]
                    szy[fay[i][j][0]][fay[i][j][1]] += 1
        for i in range(self.GRID_NUM):
            for j in range(self.GRID_NUM):
                my_szx = szx[fax[i][j][0]][fax[i][j][1]]
                my_szy = szy[fay[i][j][0]][fay[i][j][1]]
                if my_szx >= 3 or my_szy >= 3:
                    self.sparkles[i][j] = 1
                    flag = True
                if fax[i][j] == (i, j) and my_szx >= 3:
                    self.points += my_szx
                if fay[i][j] == (i, j) and my_szy >= 3:
                    self.points += my_szy
        pygame.display.set_caption('消消乐 当前分数为:' + str(self.points))
        return flag

    def calculate_cal(self):
        ret = 0
        fax = [[(j, i) for i in range(self.GRID_NUM)] for j in range(self.GRID_NUM)]
        szx = np.ones((self.GRID_NUM, self.GRID_NUM))
        fay = [[(j, i) for i in range(self.GRID_NUM)] for j in range(self.GRID_NUM)]
        szy = np.ones((self.GRID_NUM, self.GRID_NUM))
        for i in range(self.GRID_NUM):
            for j in range(self.GRID_NUM):
                if i + 1 < self.GRID_NUM and self.gems[i][j] == self.gems[i + 1][j] and self.gems[i][j] != -1:
                    fax[i + 1][j] = fax[i][j]
                    szx[fax[i][j][0]][fax[i][j][1]] += 1
                if j + 1 < self.GRID_NUM and self.gems[i][j] == self.gems[i][j + 1] and self.gems[i][j] != -1:
                    fay[i][j + 1] = fay[i][j]
                    szy[fay[i][j][0]][fay[i][j][1]] += 1
        for i in range(self.GRID_NUM):
            for j in range(self.GRID_NUM):
                my_szx = szx[fax[i][j][0]][fax[i][j][1]]
                my_szy = szy[fay[i][j][0]][fay[i][j][1]]
                if my_szx >= 3 or my_szy >= 3:
                    self.gems[i][j] = -1
                if fax[i][j] == (i, j) and my_szx >= 3:
                    ret += my_szx
                if fay[i][j] == (i, j) and my_szy >= 3:
                    ret += my_szy
        return ret

    def drop_it(self):
        vis = np.zeros(self.GRID_NUM)
        flag = False
        for i in range(self.GRID_NUM):
            for j in range(self.GRID_NUM):
                if self.gems[i][j] == -1 and vis[i] == 0:
                    vis[i] = 1
                    for k in range(j, 0, -1):
                        self.gems[i][k] = self.gems[i][k - 1]
                    self.gems[i][0] = random.randint(0, self.GEM_KIND_NUM - 1)
                    flag = True
        return flag

    def drop(self):
        while True:
            if not self.drop_it():
                break
            self.redraw()
            pygame.time.wait(self.DROP_TIME)

    def drop_cal(self):
        while True:
            if not self.drop_it():
                break

    def update(self):
        while self.calculate():
            self.sparkle_del()
            self.redraw()
            self.drop()
            pygame.time.wait(self.OBSERVE_TIME)

    def update_cal(self):
        ret = 0
        while True:
            cal = self.calculate_cal()
            if cal == 0:
                return ret
            ret += cal
            self.drop_cal()

    def sparkle_2(self, pos1, pos2):
        x, y = pos1
        s, t = pos2
        self.sparkles[x][y] = 1
        self.sparkles[s][t] = 1
        self.sparkle_del(0)
        self.sparkles[x][y] = 0
        self.sparkles[s][t] = 0

    def module_move(self, pos1, pos2):
        self.swap_pos(pos1, pos2)
        ret = self.update_cal()
        return ret

    def try_move(self, auto_move=False):
        tmp = self.gems.copy()
        dx = (0, 0, 1, -1)
        dy = (1, -1, 0, 0)
        best_pos1 = (-1, -1)
        best_pos2 = (-1, -1)
        mx = 0
        if self.to_pos != (-1, -1):
            return
        for i in range(self.GRID_NUM):
            for j in range(self.GRID_NUM):
                for h in range(4):
                    k = i + dx[h]
                    u = j + dy[h]
                    if 0 <= k < self.GRID_NUM and 0 <= u < self.GRID_NUM and self.legal_movement_2((i, j), (k, u)):
                        adv = 0
                        for t in range(self.TRY_TIME):
                            adv += self.module_move((i, j), (k, u))
                            self.gems = tmp.copy()
                        adv /= self.TRY_TIME
                        print(i, j, adv)
                        if mx < adv:
                            best_pos1, best_pos2 = (i, j), (k, u)
                            mx = adv
        print("best:", best_pos1, best_pos2, mx)
        self.sparkle_2(best_pos1, best_pos2)
        self.gems = tmp
        if auto_move:
            self.move(best_pos1, best_pos2)
        return mx

    def move(self, pos1, pos2):
        self.health -= 1
        self.lst_points = self.points
        self.lst_gems = self.gems.copy()
        self.sparkle_2(pos1, pos2)
        if self.to_pos == (-1, -1):
            self.swap_pos(pos1, pos2)
            if self.legal_movement(pos2) or self.legal_movement(pos1):
                self.update()
        self.redraw()

    def unmove(self):
        if not np.array_equal(self.gems, self.lst_gems):
            self.gems = self.lst_gems.copy()
            self.points = self.lst_points
            self.redraw()
            self.health += 1
            self.points = self.lst_points

    def runner(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit(0)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if self.X_MARGIN <= x <= self.WIDTH - self.X_MARGIN and \
                        self.Y_MARGIN <= y <= self.HEIGHT - self.Y_MARGIN:
                    self.the_pos = self.get_block(event.pos)
                    self.flag_unchanged = True
                else:
                    self.try_move()
            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                x, y = event.pos
                if self.X_MARGIN <= x <= self.WIDTH - self.X_MARGIN and \
                        self.Y_MARGIN <= y <= self.HEIGHT - self.Y_MARGIN:
                    self.unmove()
            elif event.type == MOUSEBUTTONDOWN and event.button == 2:
                x, y = event.pos
                if not self.X_MARGIN <= x <= self.WIDTH - self.X_MARGIN and \
                        self.Y_MARGIN <= y <= self.HEIGHT - self.Y_MARGIN:
                    for i in range(self.health):
                        self.SPARKLE_TIMES = 4
                        self.OBSERVE_TIME = 100
                        self.DROP_TIME = 100
                        self.try_move(True)
            elif event.type == MOUSEMOTION:
                x, y = event.pos
                now_pos = self.get_block(event.pos)
                if self.flag_unchanged and pygame.mouse.get_pressed(3)[0] \
                        and now_pos != self.the_pos and self.X_MARGIN <= x <= self.WIDTH - self.X_MARGIN and \
                        self.Y_MARGIN <= y <= self.HEIGHT - self.Y_MARGIN:
                    self.flag_unchanged = False
                    self.to_pos = now_pos
                    self.swap_pos(self.the_pos, self.to_pos)
                if self.flag_unchanged is False and pygame.mouse.get_pressed(3)[0] and now_pos == self.the_pos \
                        and self.X_MARGIN <= x <= self.WIDTH - self.X_MARGIN and \
                        self.Y_MARGIN <= y <= self.HEIGHT - self.Y_MARGIN:
                    self.flag_unchanged = True
                    self.swap_pos(self.the_pos, self.to_pos)
                    self.to_pos = (-1, -1)
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if self.legal_movement(self.the_pos) or self.legal_movement(self.to_pos):
                    self.lst_points = self.points
                    self.health -= 1
                    self.update()
                elif self.to_pos != (-1, -1):
                    self.swap_pos(self.the_pos, self.to_pos)
                self.to_pos = (-1, -1)
        self.redraw()

    def run_game(self):
        self.init_gems()
        while True:
            self.runner()


xiaoxiaole = Xiaoxiaole(300, 6)
xiaoxiaole.run_game()
