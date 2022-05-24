import json
import random
import requests
import traceback
import numpy as np  # 这行不能删
from config import bot
from mirai import At, GroupMessage, Startup, Image
from urllib.parse import urlencode
from requests.exceptions import SSLError
from util import *
from business import *

session = requests.Session()
proxies = {
    'http': 'http://localhost:7890/',
    'https': 'https://localhost:7890/',
}

def hello(event, msg):
    if msg == '您好':
        return bot.send(event, 'Hello, World!')

async def pixiv_image(event, msg):
    if msg == '来点二次元' or msg == '来张二次元':
        # pixiv_url = 'https://www.pixiv.net/ajax/top/illust?mode=all&lang=zh'
        # pixiv_response = session.get(pixiv_url, proxies=proxies)
        # print(pixiv_response)
        pixiv_url = 'https://api.pixiv.cx/rank/?'
        pixiv_params = {
            'format': 'json',
            'mode': 3
        }
        pixiv_response = session.get(pixiv_url, params=pixiv_params, verify=False)
        if pixiv_response.status_code != 200:
            await bot.send(f'出现网络问题：<{pixiv_response.status_code}>\n{pixiv_response.text}\n请访问{pixiv_url}查看')
        pixiv_response = pixiv_response.json()
        setu_url = pixiv_response['url']
        print(setu_url)
        img_data = session.get(setu_url, verify=False)
        with open('setu.jpg', 'wb') as file:
            file.write(img_data.content)
        await bot.send(event, Image(path='setu.jpg'))

async def erciyuan(bot, event, msg):
    if msg == '来点二次元' or msg == '来张二次元':
        url = 'http://iw233.cn/api/Random.php'
        response = session.get(url)
        with open('setu.jpg', 'wb') as file:
            file.write(response.content)
        await bot.send(event, Image(path='setu.jpg'))

def web_summary(event, msg: str):
    msg = streamline(msg)
    if msg.startswith('http'):
        return bot.send(event, get_url_brief(msg))

def calc(event, method, payload: str):
    if method == 'calc':
        group_id = event.sender.group.id
        qq_id = event.sender.id
        can_read, can_write, msg = auth(group_id, qq_id)
        if not can_write:
            return bot.send(event, msg)
        payload = payload.replace('（', '(').replace('）', ')')
        result = eval(pre_process(payload))
        return bot.send(event, str(result))

def help(event, method, _):
    group_id = event.sender.group.id
    if method == 'help':
        if group_id in ALLOW_ALL:
            with open('help/help.txt') as f:
                help_msg = f.read()
        elif group_id in NAOREN:
            with open('help/help_kxy.txt') as f:
                help_msg = f.read()
        else:
            with open('help/help_out.txt') as f:
                help_msg = f.read()
        return bot.send(event, help_msg)

def daka(event, method, _):
    if method == 'daka':
        status_code, result = do_daka()
        if status_code == 200 and result['e'] == 0:
            return bot.send(event, f'打卡成功！\nstatus_code：{status_code}\nresponse：{str(result)}')
        else:
            return bot.send(event, f'打卡失败！\nstatus_code：{status_code}\nresponse：{str(result)}')

def subscribe(event, method, _):
    if method == '订阅':
        group_id = event.sender.group.id
        if group_id in NAOREN:
            return bot.send(event, '下面有请松原花音，当然也有可能她死了')

def command_handler(event, msg):
    if msg[0] == '/':
        msg_list = msg[1:].split(' ', 1)
        method = msg_list[0]
        payload = msg_list[1] if len(msg_list) == 2 else None
        funcs = [calc, save_fuck_new, fuck_handler, fuck_list, help, daka, subscribe]
        for func in funcs:
            result = func(event, method, payload)
            if result:
                return result
        return bot.send(event, '指令错误！请发送/help查看可用指令')

def baidu(event, msg: str):
    ask_msg = None
    end_char = ['是啥', '是谁', '是什么']
    start_char = ['啥是', '啥叫', '什么是', '啥事', '为什么']
    for char in end_char:
        if msg.endswith(char):
            ask_msg = msg[:-len(char)]
            break
    for char in start_char:
        if msg.startswith(char):
            print('char', char)
            ask_msg = msg[len(char):]
            print('ask_msg', ask_msg)
            break
    if ask_msg:
        param = {
            'wd': ask_msg,
        }
        search_url = f'可能百度：https://www.baidu.com/s?{urlencode(param)}'
        return bot.send(event, search_url)

def go_along(event, msg):
    bzd = ['bzd', '不知道'], '那您真bgj'
    yg = ['yg', '也管'], '你啥都管'
    bgj = ['bgj', '不管经', '不管斤'], 'bgj'
    wdl = ['wdl', '无敌了', 'tql', '太强了', '太nm强了', 'lb'], 'qs'
    question_mark = ['?', '？'], '？'
    kaibai = ['算了', '就这样吧', '开摆', '躺平了', '我不想努力了', '野熊', '野熊吧', '懒得改了', '可是懒', '懒呗', '懒', '摆烂'], '开摆！'
    exclamation_mark = ['!', '！'], msg
    go_along_list = [bzd, yg, bgj, wdl, question_mark, kaibai]
    if random.random() < 1/4:
        for go_alone in go_along_list:
            if msg in go_alone[0]:
                return bot.send(event, go_alone[1])
    if msg[-1] in exclamation_mark[0]:
        return bot.send(event, exclamation_mark[1])

def exchange_rate(event, msg):
    if msg == '查汇率':
        _, rate = get_rate_text()
        return bot.send(event, rate)

async def bilibili(bot, event, msg: str):
    if msg.startswith('BV') or msg.startswith('bv'):
        url = f'https://www.bilibili.com/video/{msg}'
        await bot.send(event, url)
        await bot.send(event, get_url_brief(url))

def message_handler(event, msg):
    # print('in method: message_handler')
    if len(streamline(msg)) < 1:
        return
    methods = [hello, web_summary, command_handler, baidu, go_along, exchange_rate, fuck_detect]
    for method in methods:
        result = method(event, msg)
        if result:
            return result

async def send_img(bot, event, msg):
    if msg.startswith('发图'):
        success, save_msg = save_img(msg[2:].strip())
        if success:
            await bot.send(event, Image(path='temp.jpg'))
        else:
            await bot.send(event, save_msg)

async def asynchronous_handler(event, msg):
    # print('in method: asynchronous_handler')
    if len(streamline(msg)) < 1:
        return
    methods = [setu, setu_cache, erciyuan, send_img, setu_send_all, bilibili]
    for method in methods:
        # print('bot in qq', bot)
        await method(bot, event, msg)

@bot.on(GroupMessage)
async def on_group_message(event: GroupMessage):
    msg_chain_code = event.message_chain.as_mirai_code()
    print(msg_chain_code)
    msg = str(event.message_chain)
    try:
        return message_handler(event, msg)
    except Exception as e:
        traceback.print_exc()
        return bot.send(event, '内部错误：' + repr(e))

@bot.on(GroupMessage)
async def on_asynchronous_message(event: GroupMessage):
    msg = str(event.message_chain)
    try:
        await asynchronous_handler(event, msg)
    except Exception as e:
        traceback.print_exc()
        return bot.send(event, '内部错误：' + repr(e))

@bot.on(Startup)
async def startup(_):
    await bot.send_group_message(TEST_ID, '哈哈 俺启动辣！')

if __name__ == '__main__':
    bot.run()
