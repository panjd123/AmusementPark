import pygame
from settings import Settings
from point import Point
from direct import Direct


def draw_grid(screen, settings: Settings = Settings()):
    for r in range(settings.row):
        pygame.draw.line(screen, settings.cell_color,
                         (0, r * settings.cell_height), (settings.screen_width, r * settings.cell_height))
    for c in range(settings.col):
        pygame.draw.line(screen, settings.cell_color,
                         (c * settings.cell_width, 0), (c * settings.cell_width, settings.screen_height))


def draw_rect(screen, point, color=(-1, -1, -1), settings: Settings = Settings()):
    left = point.col * settings.cell_width
    top = point.row * settings.cell_height
    if color == (-1, -1, -1):
        pygame.draw.rect(screen, point.color, (left, top,
                         settings.cell_width, settings.cell_height))
    else:
        pygame.draw.rect(
            screen, color, (left, top, settings.cell_width, settings.cell_height))


def draw_cir(screen, point, color=(-1, -1, -1), settings: Settings = Settings()):
    left = point.col * settings.cell_width
    top = point.row * settings.cell_height
    if color == (-1, -1, -1):
        pygame.draw.ellipse(screen, point.color, (left, top,
                            settings.cell_width, settings.cell_height), 0)
    else:
        pygame.draw.ellipse(
            screen, color, (left, top, settings.cell_width, settings.cell_height), 0)


def inEdge(col, row, settings=Settings()):
    if col < 0 or col > settings.col - 1 or row < 0 or row > settings.row - 1:
        return False
    return True


def dis(p1, p2):
    return abs(p1.col-p2.col)+abs(p1.row-p2.row)


def move_point(pt: Point, i=-1, settings: Settings = Settings()):
    direct = Direct()
    p = pt.copy()
    if i != -1:
        p.row += direct.direct_row[i]
        p.col += direct.direct_col[i]
    if p.col < 0:
        p.col = settings.col - 1
    if p.col > settings.col - 1:
        p.col = 0
    if p.row < 0:
        p.row = settings.row - 1
    if p.row > settings.row - 1:
        p.row = 0
    return p
