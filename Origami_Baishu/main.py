from bs4 import BeautifulSoup as soup
from requests import get, post
import unicodedata
import numpy as np
from tqdm import tqdm

'''合并标题'''


def joint(span):
    ret = ""
    for s in span:
        ret += unicodedata.normalize('NFKD', s.text)
    ret = ret.replace('?', '')
    ret = ret.replace('!', '')
    ret = ret.replace('/', '')
    ret = ret.replace('%', '')
    ret = ret.replace('&', '')
    ret = ret.replace('\\', '')
    ret = ret.replace('|', '')
    ret = ret.replace('<', '')
    ret = ret.replace('>', '')
    ret = ret.replace('\'', '')
    return ret


def get_articles(url="http://mp.weixin.qq.com/s/OnsGIlYEidDki_taZwx7ZQ"):
    html = get(url).text
    bs = soup(html, 'lxml')
    rom = bs.find(
        'div', attrs={'class': 'rich_media_content'}).findAll('p')[3:-4]
    articles_html = []
    for r in rom:
        if r.a:
            articles_html.append(r)
    print('识别到', len(articles_html), '篇文章')
    articles = [[joint(article_html.a.findAll('span')), article_html.a['href']]
                for article_html in articles_html]
    return articles


def get_block_dic():
    articles = get_articles()
    img_dic = set()
    block_dic = set()
    articles = np.array(articles)
    for article in articles[np.random.choice(len(articles), 100, replace=False)]:
        bs = soup(get(article[1]).text, 'lxml')
        imgs = bs.findAll('img', {"data-s": "300,640"})
        for i, img in enumerate(imgs):
            src = img['data-src']
            if src in img_dic:
                block_dic.add(src)
                continue
            img_dic.add(src)
    np.save('block', block_dic)
    print(block_dic)


articles = get_articles()
img_dic = set()
block_dic = np.load('block.npy', allow_pickle=True)
block_dic = block_dic.tolist()
articles = np.array(articles)
for article in tqdm(articles):
    bs = soup(get(article[1]).text, 'lxml')
    imgs = bs.findAll('img', {"data-s": "300,640"})
    target = 0
    for i, img in enumerate(imgs):
        src = img['data-src']
        # print(src,src in block_dic)
        if src in block_dic:
            target = i-1
            break

    # print(target,imgs[target])
    src = imgs[target]['data-src']
    with open('./img/{}.png'.format(article[0]), 'wb') as f:
        f.write(get(src).content)
