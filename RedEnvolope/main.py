import time
from typing import List

import keyboard
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def is_element_exist(driver, element, method='by_id', timeout=0, frequency=0.2):
    """
    监听 element_text 是否在 timeout 时间内存在 , 结果以列表形式返回

    element_text: list 或 str 格式,当是 list 格式时表示是否存在其中任意一个

    可选method有: 'by_text', 'by_id'
    """
    def exist(driver: WebDriver) -> List[WebElement]:
        if method == 'by_text':
            def find(text): return driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("'+text+'")')
        elif method == 'by_id':
            def find(id): return driver.find_elements(By.ID, id)
        else:
            raise ValueError

        if isinstance(element, str):
            return find(element)
        else:
            for ele in element:
                if find(ele):
                    return find(ele)
            return []
    if timeout:
        try:
            WebDriverWait(driver, timeout, frequency).until(exist)
        except TimeoutException:
            return []
        else:
            return exist(driver)
    else:
        return exist(driver)


class RedEnvelope():
    def __init__(self):
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "MIUI",
            "platformVersion": "12",
            "appPackage": "com.tencent.mm",
            "appActivity": ".ui.LauncherUI",
            "newCommandTimeout": 6000,
            "noReset": True
        }
        self.driver = webdriver.Remote(
            'http://127.0.0.1:4723/wd/hub', desired_capabilities=self.desired_caps)
        actions = TouchAction(self.driver)
        self.password = '不告诉你'
        self.grab_flag = True

    def login(self):
        if not is_element_exist(self.driver, ['com.tencent.mm:id/g6c', 'com.tencent.mm:id/f30'], 'by_id', 10):
            print('微信启动失败')
            return

        if is_element_exist(self.driver, 'com.tencent.mm:id/g6c'):
            print('检测到微信被登出，正在重新登录')
            if is_element_exist(self.driver, 'com.tencent.mm:id/g66'):
                self.driver.find_element(
                    By.ID, 'com.tencent.mm:id/g66').click()
                if is_element_exist(self.driver, 'com.tencent.mm:id/iwl', timeout=1):
                    self.driver.find_element(
                        By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]").click()
                    self.login_with_password()
                else:
                    print('等待用密码登录入口超时')
        else:
            print('登录微信成功 (由保持登录记录)')

    def login_with_password(self):
        print('正在用密码登录')
        if is_element_exist(self.driver, 'com.tencent.mm:id/cd6', timeout=1):
            self.driver.find_element(
                By.ID, 'com.tencent.mm:id/cd6').send_keys(self.password)
            self.driver.find_element(By.ID, 'com.tencent.mm:id/g5v').click()
        else:
            print('等待密码输入框超时')
        if is_element_exist(self.driver, 'com.tencent.mm:id/f30', 'by_id', 10):
            print('登录微信成功 (由键入密码)')

    def main(self):
        print('session:', self.driver.session_id)
        print('正在启动微信')
        self.login()
        self.add_hotkey_stop_grab()

    def add_hotkey_stop_grab(self):
        def stop_grab():
            self.grab_flag = False

        keyboard.add_hotkey('ctrl+alt+r', stop_grab)
        print('激活了热键 ctrl+alt+r 以结束抢红包')

    def grab(self):
        # 如果要实现稳定多会话抢红包, 得再删除没有抢到的红包（不会显示消息:你已领取xx的红包）
        self.grab_from_message()
        return

        '''多会话'''
        # b4r 微信->每个会话窗口
        pers = is_element_exist(self.driver, 'com.tencent.mm:id/b4r')
        if pers:
            for per in pers:
                message = per.find_element(By.ID, 'com.tencent.mm:id/cyv').text
                if '[微信红包]' in message:
                    per.click()
                    self.grab_from_message()
                    break
        else:
            self.grab_from_message()

    def grab_from_message(self):
        try:
            tick = time.time()
            spot_flag = False
            messages = is_element_exist(
                self.driver, 'com.tencent.mm:id/b47', timeout=1)
            for i, message in zip(range(len(messages)), messages[::-1]):
                if is_element_exist(message, 'com.tencent.mm:id/y4'):
                    # print('哇，发现一个红包!')
                    spot_flag = True
                    tick2 = time.time()
                    env_app = is_element_exist(
                        message, 'com.tencent.mm:id/xs')
                    # print(str(i)+': check env_append:', time.time()-tick2)
                    if not env_app:
                        print('抢它!')
                        message.click()
                        bottom = is_element_exist(
                            self.driver, 'com.tencent.mm:id/gix', timeout=1, frequency=0)
                        if bottom:
                            bottom[0].click()
                            dh = is_element_exist(
                                self.driver, 'com.tencent.mm:id/gcq', timeout=2, frequency=0)
                            if dh:
                                print('抢到 '+dh[0].text+' 元')
                            else:
                                print('没抢到,就差一点')
                        else:
                            print('没抢到')
                        bt = is_element_exist(
                            self.driver, ['com.tencent.mm:id/k6t', 'com.tencent.mm:id/giw'], timeout=1)
                        if bt:
                            bt[0].click()

                        '''多会话'''
                        # self.actions.long_press(message)
                        # self.actions.perform()
                        # self.driver.find_element(
                        #     By.XPATH, "//android.widget.LinearLayout[@resource-id='com.tencent.mm:id/hyf']/android.widget.LinearLayout[1]").click()

                    else:
                        pass
                        '''气氛组'''
                        # if env_app[0].text == '已领取':
                        #     print('哦，是领过的')
                        # elif env_app[0].text == '已被领完':
                        #     print('啊，是没抢到的')
                        # else:
                        #     print('咦，这是什么')

                # print('message:'+str(i)+'/' +
                #       str(len(messages))+':'+str(time.time()-tick))

            '''结合MIUI实现多会话'''
            if spot_flag:
                bt = is_element_exist(
                    self.driver, 'com.tencent.mm:id/fz', timeout=1, frequency=0)
                if bt:
                    bt[0].click()
                self.driver.find_element(
                    By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]").click()

        except StaleElementReferenceException:
            return

    def grab_start(self, frequcency=0):
        print('抢红包:开始')
        self.grab_flag = True
        while self.grab_flag:
            self.grab()
            time.sleep(frequcency)
        print('抢红包:结束')


if __name__ == '__main__':
    R = RedEnvelope()
    R.main()
