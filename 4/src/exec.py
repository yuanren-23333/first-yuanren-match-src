import itertools
import base64
import json

import execjs
import requests
from bs4 import BeautifulSoup

with open('md5.js') as f:
    jscode = f.read()

url_temp = 'http://match.yuanrenxue.com/api/match/4?page={page}'
s = execjs.compile(jscode)


def get_md5(raw):
    return s.call('hex_md5', raw)


def getdata(page):
    url = url_temp.format(page=page)
    # requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
    response = requests.get(url)

    # response.json()でJSONデータに変換して変数へ保存
    jsonData = response.json()

    return jsonData


def get_masking_class(key, value):
    s_bytes = (key + value).encode('ascii')
    base64_bytes = base64.b64encode(s_bytes)
    s_base64 = base64_bytes.decode('ascii')
    return get_md5(s_base64.replace('=', ''))


def get_nums(html, display_filter):
    nums_bs4 = BeautifulSoup(html, 'lxml').find_all('td')

    def get_num_images(num_bs4):
        imgs_bs4 = num_bs4.find_all('img')
        imgs_bs4_display = list(filter(lambda img_bs4: display_filter not in img_bs4['class'], imgs_bs4))
        true_list = [-1] * len(imgs_bs4_display)
        for i in range(len(imgs_bs4_display)):
            true_postision = i + int(imgs_bs4_display[i]['style'].replace('left:', '').replace('px', '')) // 11
            assert true_postision >= 0 and true_list[true_postision] == -1
            true_list[true_postision] = imgs_bs4_display[i]['src']

        return true_list

    return map(get_num_images, nums_bs4)


def get_png_number_mapping():
    with open('num_dict.json') as f:
        png_number_mapping = json.load(f)
    return png_number_mapping


def get_nums_list(data, dic):
    for num in get_nums(data['info'], get_masking_class(data['key'], data['value'])):
        yield int(''.join([str(dic[n]) for n in num]))


png_number_mapping = get_png_number_mapping()


def get_single_page_list(page):
    data = getdata(page)
    return get_nums_list(data, png_number_mapping)


list_of_page_nums_list = map(get_single_page_list, range(1, 6))
page_sum = map(sum, list_of_page_nums_list)
ans = sum(page_sum)

print(ans)
