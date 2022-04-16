from re import T
from snake import Direct, Snake
from settings import Settings
from food import Food
import numpy as np
from util import dis, inEdge
from collections import deque


def agent(snake: Snake, food: Food):
    # return agent1_edge(snake, food)
    return agent2(snake, food)


def agent1(snake: Snake, food: Food):
    options = []

    for i in range(0, 4):
        if i == snake.direct_id ^ 1:
            continue
        tmp_head = snake.bodys[0].copy()
        tmp_head.row += snake.direct.direct_row[i]
        tmp_head.col += snake.direct.direct_col[i]
        if tmp_head.col < 0:
            tmp_head.col = snake.settings.col - 1
        if tmp_head.col > snake.settings.col - 1:
            tmp_head.col = 0
        if tmp_head.row < 0:
            tmp_head.row = snake.settings.row - 1
        if tmp_head.row > snake.settings.row - 1:
            tmp_head.row = 0
        if snake.is_crash(tmp_head) or not isReach(tmp_head, food, snake.bodys):
            continue
        options.append((i, dis(tmp_head, food)))

    if options:
        options = np.array(options)
        return [options[np.argmin(options[:, 1]), 0]]
    else:
        return [snake.direct_id]


def agent1_edge(snake: Snake, food: Food):
    options = []

    for i in range(0, 4):
        if i == snake.direct_id ^ 1:
            continue
        tmp_head = snake.bodys[0].copy()
        tmp_head.row += snake.direct.direct_row[i]
        tmp_head.col += snake.direct.direct_col[i]
        if tmp_head.col < 0:
            continue
            tmp_head.col = snake.settings.col - 1
        if tmp_head.col > snake.settings.col - 1:
            continue
            tmp_head.col = 0
        if tmp_head.row < 0:
            continue
            tmp_head.row = snake.settings.row - 1
        if tmp_head.row > snake.settings.row - 1:
            continue
            tmp_head.row = 0
        if snake.is_crash(tmp_head):
            continue
        options.append((i, dis(tmp_head, food)))

    if options:
        options = np.array(options)
        return [options[np.argmin(options[:, 1]), 0]]
    else:
        return [snake.direct_id]


def BFS(snake: Snake, food: Food, settings: Settings = Settings()):
    fromDirect = np.ones((settings.row, settings.col))*-1
    fromDirect = fromDirect.astype(int)
    vis = np.zeros((settings.row, settings.col))
    block = np.zeros((settings.row, settings.col))
    for body in snake.bodys:
        x, y = body.row, body.col
        block[x][y] = 1
    direct = Direct()
    q = deque()
    s, t = snake.bodys[0].row, snake.bodys[0].col
    q.append((s, t, len(snake.bodys)-1))
    cnt = 0
    while q:
        cnt += 1
        if cnt > settings.search_area:
            break
        u, v, l = q.popleft()
        if l >= 0:
            block[snake.bodys[l].row][snake.bodys[l].col] = False
        for i in range(4):
            x = u + direct.direct_row[i]
            y = v + direct.direct_col[i]
            if not inEdge(x, y) or vis[x][y] or block[x][y]:
                continue
            q.append((x, y, l-1))
            vis[x][y] = 1
            fromDirect[x][y] = i
            if food.row == x and food.col == y:
                continue
    x, y = food.row, food.col
    if not vis[x][y]:
        return False
    path = []
    while not (x == snake.bodys[0].row and y == snake.bodys[0].col):
        path.append(fromDirect[x][y])
        fr = fromDirect[x][y]
        x -= direct.direct_row[fr]
        y -= direct.direct_col[fr]
    path.reverse()
    return path


def isReach(p1, p2, block_points, settings: Settings = Settings()):
    vis = np.zeros((settings.row, settings.col), dtype=bool)
    block = np.zeros((settings.row, settings.col), dtype=bool)
    for body in block_points:
        x, y = body.row, body.col
        block[x][y] = True
    direct = Direct()
    q = deque()
    s, t = p1.row, p1.col
    q.append((s, t))
    vis[s][t] = True
    cnt = 0
    while q:
        cnt += 1
        if cnt > settings.search_area:
            break
        u, v = q.popleft()
        for i in range(4):
            x = u + direct.direct_row[i]
            y = v + direct.direct_col[i]
            if not inEdge(x, y) or vis[x][y] or block[x][y]:
                continue
            q.append((x, y))
            vis[x][y] = True
            if p2.row == x and p2.col == y:
                continue
    x, y = p2.row, p2.col
    # if not vis[x][y]:
    #     print('---------------')
    #     print(vis)
    #     for p in block_points:
    #         print(p)
    #     print('****')
    #     print(p1)
    #     print('****')
    #     print(p2)
    #     # input()
    return vis[x][y]


def agent2(snake: Snake, food: Food):
    ret = BFS(snake, food)
    if not ret:
        return agent1(snake, food)
    else:
        return ret
