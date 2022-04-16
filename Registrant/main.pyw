from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import time
from sys import exit
from win10toast import ToastNotifier


def printExit(text, tim, driver, ex=0):
    toaster = ToastNotifier()
    toaster.show_toast("Registrant",
                       text,
                       duration=tim)
    driver.quit()
    exit(ex)


class Registrant():
    def __init__(self, driver_kind='Edge', url="", silent=True, student_ID=None, password=None):
        '''
        ### Parameters
        student_ID & password : you can also use Registrant().set_ID_password() to set

        driver_kind : {'Edge', 'Firefox', 'Chrome'}, default='Edge'

        silent : bool, default=True
            Not to open the browser window
        '''
        self.student_ID = student_ID
        self.password = password
        self.silent = silent
        self.url = url

        if driver_kind == 'Firefox':
            self.options = webdriver.FirefoxOptions()
            self.initOptions()
            self.driver = webdriver.Firefox(options=self.options)
        elif driver_kind == 'Chrome':
            self.options = webdriver.ChromeOptions()
            self.initOptions()
            self.driver = webdriver.Chrome(options=self.options)
        elif driver_kind == 'Edge':
            self.options = webdriver.EdgeOptions()
            # self.initOptions()
            self.driver = webdriver.Edge(options=self.options)
        else:
            raise ValueError

    def initOptions(self):
        '''
        浏览器启动参数
        '''
        # self.options.headless = self.silent
        self.options.add_argument('--disable-images')

    def set_ID_password(self, student_ID=None, password=None):
        self.student_ID = student_ID
        self.password = password

    def register(self, thresh_time, log):
        try:
            if not (self.student_ID and self.password):
                raise ValueError
        except ValueError:
            printExit('未输入账号密码', thresh_time, self.driver, 1)

        if self.silent:
            self.driver.set_window_rect(-2000, 0)
        self.driver.get(self.url)

        try:
            # account -> password -> login
            self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div[2]/div[1]/input').send_keys(self.student_ID)
            self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div[2]/div[2]/input').send_keys(self.password)
            self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]').click()

            # Daily report
            WebDriverWait(driver=self.driver, timeout=10,
                          poll_frequency=0.5).until(lambda driver: driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/section/div/div[3]/div/ul/li/span'))
            self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div[1]/div/section/div/div[3]/div/ul/li/span').click()

            # Location
            WebDriverWait(driver=self.driver, timeout=10,
                          poll_frequency=0.2).until(lambda driver: driver.find_element(By.XPATH, '/html/body/div[1]/div/div/section/div[4]/ul/li[9]/div'))
            self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div/div/section/div[4]/ul/li[9]/div').click()

            # until page-loading-container.style = 'display: none;'
            WebDriverWait(driver=self.driver, timeout=10,
                          poll_frequency=0.2).until(lambda driver: driver.find_element(
                              By.XPATH, '/html/body/div[3]').get_attribute('style') == "display: none;")
            # Submit
            self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div/div/section/div[5]/div/a').click()
        except:
            printExit('填报失败：尝试提交前失败', thresh_time, self.driver, 1)
        try:
            WebDriverWait(driver=self.driver, timeout=1,
                          poll_frequency=0.2).until(lambda driver: driver.find_element(
                              By.XPATH, '/html/body/div[4]/div/div[2]/div[2]'))
            self.driver.find_element(
                By.XPATH, '/html/body/div[4]/div/div[2]/div[2]').click()
        except:
            try:
                self.driver.find_element(
                    By.XPATH, '//*[@id="wapat"]/div/div[2]/div')
            except:
                printExit('填报失败：提交后失败', thresh_time, self.driver, 1)
            else:
                if log:
                    printExit('今日已填报', thresh_time, self.driver, 0)
        else:
            if log:
                printExit('填报成功', thresh_time, self.driver, 0)
        self.driver.quit()
        exit(0)

    def __call__(self, thresh_time, log):
        self.register(thresh_time, log)


if __name__ == '__main__':
    with open('./settings.json', 'r', encoding='utf8') as fp:
        settings = json.load(fp)
    time.sleep(settings['delay_time'])
    if settings['log']:
        toaster = ToastNotifier()
        toaster.show_toast("Registrant",
                           '启动',
                           duration=settings['thresh_time'])
    reg = Registrant(url=settings['url'],
                     silent=settings['silent'], student_ID=settings['student_ID'], password=settings['password'])
    reg.register(settings['thresh_time'], settings['log'])
