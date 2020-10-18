import itertools

import execjs
import requests


with open('md5.js') as f:
    jscode = f.read()

url_temp = 'http://match.yuanrenxue.com/api/match/1?page={page}&m={m}'
s = execjs.compile(jscode)


def get_md5():
    time = execjs.eval('Date.parse(new Date())')
    mwqqppz = str(time)
    ans = s.call('hex_md5', mwqqppz)
    op = '%E4%B8%A8'
    print(ans, mwqqppz)
    return ans + op + str(time // 1000)


def getlist(page):
    url = url_temp.format(page=page, m=get_md5())
    # requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
    response = requests.get(url)

    # response.json()でJSONデータに変換して変数へ保存
    jsonData = response.json()
    return [d.get('value') for d in jsonData.get('data')]


def Average(lst):
    return sum(lst) / len(lst)


print(Average(list(itertools.chain.from_iterable(map(getlist, range(1, 6))))))
