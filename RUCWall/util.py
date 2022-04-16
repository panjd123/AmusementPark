import jieba
import stylecloud
import json
import requests
from queue import Queue
from threading import Thread
import numpy as np
from timeit import default_timer as timer
from time import sleep
import pandas as pd
import time


def strip2json(rom_text, st="([{"):
    '''对 get 得到的信息预处理后转成 json 格式'''
    text_st = rom_text.find(st)
    if text_st == -1:
        raise IndexError
    rom_text = rom_text[text_st+1:-2]
    json_text = json.loads(rom_text)
    return json_text


def getPost(page):
    '''以 json 格式返回第 page 页的主贴'''
    rom_text = requests.get(
        f"http://weixiao.nickboy.cc/wall/content/gh_3852826aa4ab?&page={page}&callback=jsonp").text
    return strip2json(rom_text)


def getComment(cid):
    '''以 list[json] 格式返回 cid 号帖子下的所有评论'''
    comment = []
    try:
        for page in range(1, 1000):
            rom_text = requests.get(
                f"http://weixiao.nickboy.cc/wall/comments/gh_3852826aa4ab?&cid={cid}&page={page}&callback=jsonp").text
            comment.extend(strip2json(rom_text))
            if page % 10 == 0:
                print(f"running on id:{cid} page:{page}")
    except IndexError:
        pass
    if not comment:
        comment.append(dict())
    for c in comment:
        c.update({'cid': cid})
    return comment


def getPostByOneThread(Q: Queue, pages):
    postes = []
    try:
        for i, page in enumerate(pages):
            postes.extend(getPost(page))
            if i % 10 == 9:
                print(f"{round(i/len(pages)*100,2)}%")
    except IndexError:
        print(f"Pass last page. now:{page}")
        pass
    Q.put(postes)


def getCommentByOneThread(Q: Queue, cids):
    postes = []
    for i, cid in enumerate(cids):
        postes.extend(getComment(cid))
        if i % 10 == 9:
            print(f"{round(i/len(cids)*100,2)}%")
    Q.put(postes)


def isStop(crawl):
    stop = True
    for thread in crawl:
        stop &= thread.is_running
    return stop


class MyThread(Thread):
    def __init__(self, _target, _args):
        super().__init__(target=_target, args=_args, daemon=True)
        self.is_running = False

    def myStart(self):
        self.is_running = True
        self.start()
        self.is_running = False


def getPostByThreads(stPage, edPage, threadNum, output_file="post.csv"):
    '''开始页，结束页，线程数，保存到的csv文件名'''
    Q = Queue()
    threadcrawl = []
    for i in range(0, threadNum):
        t = MyThread(_target=getPostByOneThread, _args=(
            Q, np.arange(stPage+i, edPage+1, threadNum),))
        t.myStart()
        threadcrawl.append(t)

    for t in threadcrawl:
        t.join()

    postes = []
    while not Q.empty():
        postes.extend(Q.get())

    df = pd.DataFrame(postes)
    df['time'] = df['time'].apply(lambda x: time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(x)))
    df.to_csv(output_file, encoding='gb18030')


def getCommentByThreads(cids, threadNum, output_file="comment.csv"):
    '''cid的列表，线程数，保存到的csv文件名'''
    cids = np.array(cids)
    Q = Queue()
    threadcrawl = []
    for i in range(0, threadNum):
        t = MyThread(_target=getCommentByOneThread, _args=(
            Q, cids[i::threadNum],))
        t.myStart()
        threadcrawl.append(t)

    for t in threadcrawl:
        t.join()

    comment = []
    while not Q.empty():
        comment.extend(Q.get())

    df = pd.DataFrame(comment)
    # df['time'] = df['time'].apply(lambda x: time.strftime(
    #     "%Y-%m-%d %H:%M:%S", time.localtime(x)))
    df.to_csv(output_file, encoding='gb18030')


def loadContent():
    '''加载 csv 数据并合并成一个大 text'''
    text = ""

    # df = pd.read_csv(f"comment_all.csv", encoding="gb18030")
    # args = (df['removed'].values != 1)
    # val = df.iloc[args]['content'].values.astype(str)
    # text += " ".join(val)+" "

    df = pd.read_csv(f"post_all.csv", encoding="gb18030")
    # args = (df['removed'].values == 1)
    val = df['content'].values.astype(str)
    text += " ".join(val)+" "
    return text


def ciyun(text: str, output_file='ciyun.png'):
    '''用 text 生成词云'''
    stop_word = []
    with open('stop_words.txt',
              encoding="utf-8") as f:
        l = f.readlines()
        for word in l:
            stop_word.append(word.strip())
    stop_word.append("楼")
    stop_word.append("真的")
    stop_word.append("想")
    stop_word.append("说")
    stop_word.append("没")
    stop_word.append("感觉")
    stop_word.append("更")
    stop_word.append("一点")
    stop_word.append("好像")
    stop_word.append("确实")
    stop_word.append("东西")
    stop_word.append("挺")
    stop_word.append("太")
    stop_word.append("做")
    stop_word.append("中")
    stop_word.append("希望")

    # stop_word.append("老师")
    # stop_word.append("同学")
    # stop_word.append("学生")
    # stop_word.append("男生")
    # stop_word.append("女生")
    # stop_word.append("楼主")
    # stop_word.append("朋友")
    # stop_word.append("学校")
    # stop_word.append("人大")
    # stop_word.append("有人")
    # stop_word.append("uu")
    # stop_word.append("lz")

    # stop_word.append("请问")
    # stop_word.append("求问")
    # stop_word.append("问问")
    # stop_word.append("问")
    # stop_word.append("建议")
    # stop_word.append("蹲")
    # stop_word.append("谢谢")

    result = jieba.cut(text, cut_all=True)
    result = " ".join(result)
    # print(result)
    stylecloud.gen_stylecloud(
        text=result,
        size=1024,
        font_path='msyh.ttc',
        palette='cartocolors.qualitative.Pastel_7',
        gradient='horizontal',
        icon_name='fab fa-weixin',
        output_name=output_file,
        stopwords=True,
        custom_stopwords=stop_word
    )


if __name__ == '__main__':
    tic = timer()

    '''先获取所有的主贴，cids 同时也获取到了'''
    # maxPage = 4775
    # getPostByThreads(1, maxPage, 5)

    # df = pd.read_csv('post_all.csv', encoding='gb18030')
    # args = df['r_count'].values > 0
    # cids = df.iloc[args, 1].values
    # n = len(cids)

    '''防止断了全完蛋，分了20个批次爬评论'''
    bat = 20
    # s = 0
    # t = n//bat
    # for i in range(bat):
    #     if i in [2, 15, 17]:
    #         getCommentByThreads(cids[s:t], 4, f"comment{i}_new.csv")
    #     s += n//bat
    #     t += n//bat

    '''把20个评论拼起来'''
    # comment = pd.read_csv(f"comment0.csv", encoding="gb18030")
    # for i in range(1, bat):
    #     df = pd.read_csv(f"comment{i}.csv", encoding="gb18030")
    #     comment = comment.append(df)
    # comment.to_csv("comment.csv", encoding="gb18030")

    '''主贴和评论还可以再拼起来'''
    # df1 = pd.read_csv(f"comment_all.csv", encoding="gb18030")
    # df2 = pd.read_csv(f"post_all.csv", encoding="gb18030")
    # df1.append(df2).to_csv("all.csv", encoding="gb18030")

    '''画个词云图'''
    # text = loadContent()
    # print(len(text))
    # ciyun(text)

    toc = timer()
    print(toc-tic)

# 11
