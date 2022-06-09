import datetime
from importlib.resources import path
import json

import psutil
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from mirai import At, Image
from requests.exceptions import SSLError

from config import *
from util import *

scheduler = AsyncIOScheduler()


@scheduler.scheduled_job(CronTrigger(hour='*', minute='0/10'))
async def timer():
    mem = psutil.virtual_memory().percent
    # print(mem)
    await bot.send_group_message(TEST, f'小泉花阳为您报时: {datetime.datetime.now()}\n内存占用率: {mem}%')
    if mem > 98:
        await bot.send_group_message(RTS, '服务器内存占用已超98%！服务器可能即将崩溃！请群友们速速call!')


@scheduler.scheduled_job(CronTrigger(hour=4))
async def auto_cache_setu():
    for i in range(0, 10):
        setu_path = './setu/'
        setu_name = 'setu' + str(i) + '.jpg'
        try:
            down_setu(setu_name, setu_path)
        except SSLError:
            await bot.send_group_message(TEST, '色图站又挂了！')


@scheduler.scheduled_job(CronTrigger(hour=0))
async def report_record():
    message_chain = []
    with open('records/setu_record.json', 'r',  encoding='utf-8') as f:
        setu_record = json.loads(f.read())
    for key, value in setu_record.items():
        message_chain.append(At(target=int(key)))
        message_chain.append(f'，您今天看了{value}张色图\n')
    with open('records/setu_record.json', 'w',  encoding='utf-8') as f:
        f.write(pretty_json({}))
    await bot.send_group_message(RTS, message_chain)

    with open('records/fuck_record.json', 'r',  encoding='utf-8') as f:
        fuck_record = json.loads(f.read())
    for group_id, group_record in fuck_record.items():
        message_chain = []
        for name, fuck_cnt in group_record.items():
            message_chain.append(f'今日{name}被迫害了{fuck_cnt}次\n')
        await bot.send_group_message(int(group_id), message_chain)
    with open('records/fuck_record.json', 'w', encoding='utf-8') as f:
        f.write(pretty_json({}))


@scheduler.scheduled_job(CronTrigger(hour=0, minute=10, second=3))
async def daka():
    status_code, result = do_daka()
    if status_code == 200 and result['e'] == 0:
        await bot.send_group_message(123456, f'打卡成功！\nstatus_code：{status_code}\nresponse：{str(result)}')
    else:
        await bot.send_group_message(123456, f'打卡失败！\nstatus_code：{status_code}\nresponse：{str(result)}')


@scheduler.scheduled_job(CronTrigger(hour='0-2/2, 6-23/2'))
async def cron_rate():
    trend, rate = get_rate_text()
    if trend == 1:
        trend_txt = '涨'
    elif trend == -1:
        trend_txt = '跌'
    else:
        trend_txt = '平'
    message_chain = [f'日元丁真，鉴定为{trend_txt}\n', rate]
    # message_chain.append(At(target = 123456))
    # message_chain.append('\nhttps://www.apple.com/jp/shop/buy-giftcard/giftcard')
    await bot.send_group_message(RTS, message_chain)

@scheduler.scheduled_job(CronTrigger(day_of_week='sun', hour='23', minute='59'))
async def thank_hard_work():
    img = Image(path='images/nanimoshimasenn.png')
    await bot.send_group_message(RTS, img)
    await bot.send_group_message(KXY, img)
    await bot.send_group_message(MADOKA, img)
