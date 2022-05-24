import requests
import json

session = requests.Session()
proxies = {
    'http': 'http://localhost:7890/',
    'https': 'http://localhost:7890/',
}

def pretty_json(json_data):
    return json.dumps(json_data, indent=4, separators=(',', ': '), ensure_ascii=False)

def streamline(content):
    return content.replace(' ', '').replace('\n', '')

def write(content):
    with open('temp.txt', 'w') as f:
        f.write(str(content))

def down_setu(setu_path: str, setu_name: str):
    url = 'https://tool.tsutsu.cc/api/setu/generate'
    response = session.post(url, proxies=proxies).json()
    setu_url = response['data']['image_url']
    print('setu_url:', setu_url)
    img_data = session.get(setu_url, proxies=proxies)
    if img_data.status_code != 200:
        return False, img_data.status_code, img_data.text
    with open(setu_path + setu_name, 'wb') as file:
        file.write(img_data.content)
    return True, None, None

def gen_compare(cur, pre):
    change = ''
    if cur > pre:
        trend = 1
    elif cur < pre:
        trend = -1
    else:
        trend = 0
    if cur != pre:
        change = '↑' if trend == 1 else '↓'
        change += str(format(abs(cur - pre), '.5f'))
    return trend, change

def gen_text(rate, pre_rate):
    CNYJPY = rate["CNYJPY"]
    pre_CNYJPY = pre_rate["CNYJPY"]
    display_CNYJPY = format(CNYJPY, '.5f')
    _, change = gen_compare(CNYJPY, pre_CNYJPY)
    result = f'1人民币={display_CNYJPY}日元 {change}\n'

    JPYCNY = rate["JPYCNY"]
    pre_JPYCNY = pre_rate["JPYCNY"]
    display_JPYCNY = format(JPYCNY, '.5f')
    trend, change = gen_compare(JPYCNY, pre_JPYCNY)
    result += f'1日元={display_JPYCNY}人民币 {change}\n'

    yueka = rate["yueka"]
    pre_yueka = pre_rate["yueka"]
    display_yueka = format(yueka, '.5f')
    _, change = gen_compare(yueka, pre_yueka)
    result += f'月卡：{display_yueka}元 {change}\n'
    
    dayueka = rate["dayueka"]
    pre_dayueka = pre_rate["dayueka"]
    display_dayueka = format(dayueka, '.5f')
    _, change = gen_compare(dayueka, pre_dayueka)
    result += f'大月卡：{display_dayueka}元 {change}\n'

    bili = rate["bili"]
    pre_bili = pre_rate["bili"]
    display_bili = format(bili, '.5f')
    _, change = gen_compare(bili, pre_bili)
    result += f'叔叔包年：{display_bili}元 {change}\n'

    cz648 = rate["cz648"]
    pre_cz648 = pre_rate["cz648"]
    display_cz648 = format(cz648, '.5f')
    _, change = gen_compare(cz648, pre_cz648)
    result += f'648：{display_cz648}元 {change}\n'

    # print('need_at in gen_text, utils', trend)
    return trend, result

def get_rate_text():
    url = 'https://vip.stock.finance.sina.com.cn/forex/api/jsonp.php/=/NewForexService.getDayKLine?symbol=fx_scnyjpy'
    response = session.get(url)
    jpurl = 'https://vip.stock.finance.sina.com.cn/forex/api/jsonp.php/=/NewForexService.getDayKLine?symbol=fx_sjpycny'
    jp_response = session.get(jpurl)
    CNYJPY = float(response.text[-11:].split('"')[0])
    JPYCNY = float(jp_response.text[-10:].split('"')[0])
    rate = {
        'CNYJPY': CNYJPY,
        'JPYCNY': JPYCNY,
        'yueka': 610 * JPYCNY,
        'dayueka': 1220 * JPYCNY,
        'cz648': 12000 * JPYCNY,
        'bili': 2300 * JPYCNY,
    }
    with open('records/exchange_rate.json', 'r', encoding='utf-8') as f:
        pre_rate = json.loads(f.read())
    with open('records/exchange_rate.json', 'w', encoding='utf-8') as f:
        f.write(pretty_json(rate))
    return gen_text(rate, pre_rate)

if __name__ == '__main__':
    down_setu(setu_name='setu.jpg', setu_path='./setu/')
