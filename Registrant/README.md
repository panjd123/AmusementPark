# RUC-Registrant

为了帮助广大经常忘填疫情防控通的RUCer，selenium 实现的 RUC 疫情防控通电脑端自动登记脚本出现在了 github 上（雾

### 所用库

1. selenium
2. win10toast

### 基本使用指南

1. 下载 Edge 驱动，并将对应的 exe 文件添加到系统变量 `path` 中，详见可百度 "selenium Edge"
2. 在 setting.json 中输入账号密码信息用于登录
3. 运行 main.pyw
4. 提示：如果出现黑框，可以百度 "selenium 黑框"

登记失败会报错提醒，可能的原因有：账号密码错误，昨天忘记登记，导致部分信息缺失；网速太慢；网站改版

#### setting.json 说明

thresh_time : 通知停留在屏幕上的时间，单位：秒

log : 只对 main_plus.py 生效，0 表示低通知，即只在失败时通知；1 表示高通知，即登记失败，今日已登记，本次登记成功都通知，默认值为 1

silent: 原本是用来指定 headless，但是实测发现 headless 极不稳定，所以现在采用把窗口移动到 -2000 的位置

### 注意

脚本没有模拟定位的功能
用 Edge 是因为经过测试，只有 Edge 可以在不翻墙的前提下正常获取到定位信息
