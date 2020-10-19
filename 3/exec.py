import requests, statistics

switch_url = 'http://match.yuanrenxue.com/logo'
api_url = 'http://match.yuanrenxue.com/api/match/3?page={page}'

def get_sessionid():
    headers = {'Referer': 'http://match.yuanrenxue.com/match/3', 'Accept-Language': 'zh-CN,zh'}
    r = requests.post(switch_url, headers = headers)
    return r.headers['Set-Cookie'].split(';')[0].split('=')[1]

def make_header(sessionid):
    return  {'Referer': 'http://match.yuanrenxue.com/match/3', 'Accept-Language': 'zh-CN,zh', 'Cookie': 'sessionid=' + sessionid}

def switch_on(sessionid):
    headers = make_header(sessionid)
    requests.post(switch_url, headers = headers)

def solve():
    ans = []
    sessionid = get_sessionid()
    for i in range(5):
        switch_on(sessionid)

        # 访问api
        url = api_url.format(page = i + 1)
        response = requests.get(url, headers = make_header(sessionid))

        data = response.json().get('data')
        for j in range(len(data)):
            ans.append(data[j].get('value'))
    print(statistics.mode(ans))

solve()