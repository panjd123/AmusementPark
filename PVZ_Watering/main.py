from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import win32gui
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pyautogui
import time


def avhash(img):
    '''返回图片对应的感知哈希值'''
    img = cv2.resize(img, (8, 8))
    img = img.astype(float)
    avg = np.mean(img)
    hash = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            hash.append(img[i][j] < avg)
    return hash


def cmphash(hash1, hash2):
    '''返回两个hash间不相同位的数量'''
    if len(hash1) != len(hash2):
        print("Error:They can't be compared.")
        return
    ret = 0
    for i in range(len(hash1)):
        ret += (hash1[i] != hash2[i])
    return ret


class AllHwnd:
    '''用于观察获取pvz窗口句柄和窗口名'''
    hwnd_title = dict()

    def get_hwnd(self, hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    def __init__(self):
        win32gui.EnumWindows(self.get_hwnd, 0)
        for h, t in self.hwnd_title.items():
            if t != "":
                print(h, t)


class Pos:
    '''植物位置和需求'''
    plantpos = (0, 0)
    iconpos = (0, 0)
    kind = 0

    def __init__(self, a, b, c, d, dx, dy, _kind=0) -> None:
        self.plantpos = (a+dx, b+dy)
        self.iconpos = (c+dx, d+dy)
        self.kind = _kind


class ToolsCmp:
    '''图标对比'''
    imgs = []
    imgshash = []
    root = ""

    def __init__(self, root: str) -> None:
        self.root = root
        self.imgs.append(cv2.imread(
            self.root+"images/water.jpg", cv2.IMREAD_GRAYSCALE))
        self.imgs.append(cv2.imread(
            self.root+"images/fer.jpg", cv2.IMREAD_GRAYSCALE))
        self.imgs.append(cv2.imread(
            self.root+"images/spray.jpg", cv2.IMREAD_GRAYSCALE))
        self.imgs.append(cv2.imread(
            self.root+"images/music.jpg", cv2.IMREAD_GRAYSCALE))
        for img in self.imgs:
            self.imgshash.append(avhash(img))

    def judge_kind(self, img0) -> int:
        hash0 = avhash(img0)
        ls = []
        for hash in self.imgshash:
            ls.append(cmphash(hash0, hash))
        if min(ls) < 5:
            return ls.index(min(ls))
        else:
            return -1


class MyPVZ:
    '''程序主体'''
    pos = []
    root = ""
    windowx = 0
    windowy = 0
    tick = dict()
    toolpos = []

    def __init__(self, root: str = "./Python/PVZ_watering/") -> None:
        '''根据运行环境修改root'''
        self.root = root
        self.toolscmp = ToolsCmp(root)

    def get_ori(self) -> None:
        '''获取窗口位置和截图'''
        hwnd = win32gui.FindWindow(None, "Plants vs. Zombies")
        self.windowx, self.windowy = win32gui.GetWindowRect(hwnd)[0:2]
        self.windowx += 2
        self.windowy += 32  # 边框
        app = QApplication(sys.argv)
        screen = QApplication.primaryScreen()
        img = screen.grabWindow(hwnd).toImage()
        img.save(self.root+"data/ori.jpg", quality=95)
        for i in range(0, 8):
            self.toolpos.append((i*70+50+self.windowx, 50+self.windowy))

    def cv(self) -> None:
        '''图像处理'''
        grayimg = cv2.imread(self.root+"data/ori.jpg", cv2.IMREAD_GRAYSCALE)
        # 高斯模糊
        gaussedimg = cv2.GaussianBlur(grayimg, (1, 1), 0)
        # 二值化
        thresh = cv2.threshold(gaussedimg, 250, 255, 0)[1]
        # 边缘检测及可视化
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img = cv2.imread(self.root+"data/ori.jpg")
        # img = cv2.drawContours(cv2.imread(root+"data/ori.jpg"),
        #                        contours, -1, (255, 0, 0), 2)
        # 外接矩形检测提示框
        self.pos = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if 37 <= w <= 39 and 36 <= h <= 38:
                d = 2
                # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                self.pos.append(Pos(x-30, y+35, x+w//2, y+h//2, self.windowx, self.windowy,
                                    self.toolscmp.judge_kind(grayimg[y+d:y+h-3*d, x+d:x+w-d])))
        # 去重并对植物按位置排序
        self.pos = list(dict.fromkeys(self.pos))
        self.pos.sort(
            key=lambda plant: plant.plantpos[0]//80*100+plant.plantpos[1]//90)

    def auto(self) -> None:
        '''模拟鼠标操作'''
        # water_dx, water_dy = 82//2, 94//2
        for i, plant in enumerate(self.pos):
            # 提示框内容无对应标记：提示框识别失误拦截
            if plant.kind == -1:
                continue
            wx, wy = self.toolpos[plant.kind]
            x, y = plant.plantpos
            # 防止重复操作
            if (x//80, y//90) in self.tick and time.time()-self.tick[(x//80, y//90)] < 2:
                continue
            # if plant.kind == 0:
            # x += water_dx
            # y += water_dy
            pyautogui.click(wx, wy)
            pyautogui.moveTo(x, y)
            pyautogui.click(x, y)
            self.tick.update({(x//80, y//90): time.time()})

    def start(self) -> None:
        '''开启脚本'''
        while True:
            tick = time.time()
            self.get_ori()
            self.cv()
            # print("图像处理耗时", time.time()-tick)
            self.auto()


print('开始允许')
mypvz = MyPVZ("./")
mypvz.start()
