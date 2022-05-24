import datetime
import json
import os
import requests
import psutil
from mirai import At, Mirai, Shutdown, Startup, WebSocketAdapter, Image
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from requests.exceptions import SSLError
from util import *

scheduler = AsyncIOScheduler()

session = requests.Session()
proxies = {
    'http': ' http://localhost:7890/',
    'https': 'http://localhost:7890/',
}

adapter = WebSocketAdapter(verify_key='Hoshizora1', host='localhost', port=6090)
bot = Mirai(715859163, adapter)

def pretty_json(json_data):
    return json.dumps(json_data, indent=4, separators=(',', ': '), ensure_ascii=False)

@bot.on(Startup)
def start_scheduler(_):
    scheduler.start() # 启动定时器

@bot.on(Shutdown)
def stop_scheduler(_):
    scheduler.shutdown(True) # 结束定时器

@scheduler.scheduled_job(CronTrigger(hour='*', minute='0/10'))
async def timer():
    mem = psutil.virtual_memory().percent
    # print(mem)
    await bot.send_group_message(737445521, f'星空凛为您报时: {datetime.datetime.now()}\n内存占用率: {mem}%')
    if mem > 98:
        await bot.send_group_message(1109364022, '服务器内存占用已超98%！服务器可能即将崩溃！请群友们速速call国歌!')

@scheduler.scheduled_job(CronTrigger(hour=4, minute=10))
async def auto_cache_setu():
    for i in range(0,10):
        setu_path = './setu/'
        setu_name = 'setu' + str(i) + '.jpg'
        try:
            down_setu(setu_name=setu_name, setu_path=setu_path)
        except SSLError:
            await bot.send_group_message(1109364022, '色图站又挂了！')

@scheduler.scheduled_job(CronTrigger(hour=23, minute=41))
async def report_setu_record():
    with open('setu_record.json', 'r',  encoding='utf-8') as f:
        setu_record = json.loads(f.read())
    message_chain = []
    for key, value in setu_record.items():
        message_chain.append(At(target = int(key)))
        message_chain.append(f'，您今天看了{value}张色图\n')
    with open('setu_record.json', 'w',  encoding='utf-8') as f:
        f.write(pretty_json({}))
    await bot.send_group_message(1109364022, message_chain)

@scheduler.scheduled_job(CronTrigger(hour=4, minute=10))
async def clear_record():
    print('clear_record')
    with open('record.json', 'w', encoding='utf-8') as f:
        f.write(pretty_json({}))

@scheduler.scheduled_job(CronTrigger(hour=0, minute=10, second=3))
async def daka():
    status_code, result = do_daka()
    if status_code == 200 and result['e'] == 0:
        await bot.send_group_message(866839618, f'打卡成功！\nstatus_code：{status_code}\nresponse：{str(result)}')
    else:
        await bot.send_group_message(866839618, f'打卡失败！\nstatus_code：{status_code}\nresponse：{str(result)}')

@scheduler.scheduled_job(CronTrigger(hour='*', minute='30'))
async def cron_rate():
    trend, rate = get_rate_text()
    # print('need_at in cron_rate, keep_alive', need_at)
    message_chain = [rate]
    if trend == 1:
        trend_txt = '涨' 
    elif trend == -1:
        trend_txt = '跌'
    else:
        trend_txt = '平'
    message_chain.append(f'日元丁真，鉴定为{trend_txt}')
    # message_chain.append(At(target = 3504879459))
    # message_chain.append('\nhttps://www.apple.com/jp/shop/buy-giftcard/giftcard')
    await bot.send_group_message(1109364022, message_chain)

if __name__ == '__main__':
    bot.run(port=9000)
    # val = os.system('htop')
    # print(val)
    # mem = psutil.virtual_memory().percent
    # print(mem)
