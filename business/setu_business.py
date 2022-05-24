import json
import os
from ssl import SSLError
from mirai import Image
from util import *

async def setu_cache(bot, event, msg):
    # print('bot in setu', bot)
    if msg == '存点色图' or msg == '缓存色图':
        local_setu = os.listdir('./setu')
        if len(local_setu) >= 3:
            await bot.send(event, '色图资源充分！别存了！')
            return
        await bot.send(event, '色图缓存中，请耐心等待……')
        for i in range(0,10):
            setu_path = './setu/'
            setu_name = 'setu' + str(i) + '.jpg'
            if setu_name not in local_setu:
                try:
                    success, status_code, text = down_setu(setu_name=setu_name, setu_path=setu_path)
                except SSLError:
                    await bot.send(event, '色图站挂了，缓存失败')
                    return
                if not success:
                    await bot.send(event, f'网络异常！\nstatus_code：{status_code}\nresponse：{text}')
                    return
        await bot.send(event, '色图缓存完成')

async def setu(bot, event, msg):
    setu_trigger_1 = ['来点', '来张', '来一点', '来一张']
    setu_trigger_2 = ['色图', '涩图', '猫猫']
    setu_trigger = [st1 + st2 for st1 in setu_trigger_1 for st2 in setu_trigger_2]
    if msg not in setu_trigger:
        return
    group_id = event.sender.group.id
    user_id = str(event.sender.id)
    if group_id in ALLOW_ALL:
        with open("records/setu_record.json", "r", encoding='utf-8') as f:
            setu_record = json.loads(f.read())
        if user_id in setu_record.keys():
            count = setu_record[user_id] + 1
        else:
            count = 1
        setu_record[user_id] = count
        with open('records/setu_record.json', 'w', encoding='utf-8') as f:
            f.write(pretty_json(setu_record))
    local_setu = os.listdir('./setu')
    if local_setu:
        message_chain=[]
        message_chain.append(Image(path='./setu/'+local_setu[0]))
        message_chain.append("剩余缓存" + str(len(local_setu) - 1) + "张色图")
        if event.sender.group.id == RTS_ID:
            # message_chain.append(At(target=1913603067))
            message_chain.append('，您已看过' + str(count) + '张色图')
            message_chain.append('，先生快来看色图')
        await bot.send(event, message_chain)
        os.remove('./setu/'+local_setu[0])
        return
    try:
        success, status_code, text = down_setu(setu_name='setu.jpg', setu_path='./setu/')
    except SSLError:
        await bot.send(event, '别看了，色图站挂啦')
        return
    if not success:
        await bot.send(event, f'网络异常！\nstatus_code：{status_code}\nresponse：{text}')
        return
    await bot.send(event, Image(path='./setu/setu.jpg'))
    os.remove('./setu/setu.jpg')

async def setu_send_all(bot, event, msg):
    if msg != '我要色色':
        return
    group_id = event.sender.group.id
    user_id = str(event.sender.id)
    local_setu = os.listdir('./setu')
    if local_setu:
        pass
    else:
        await bot.send(event, '当前没有缓存色图，开始缓存色图')
        for i in range(0,10):
            setu_path = './setu/'
            setu_name = 'setu' + str(i) + '.jpg'
            if setu_name not in local_setu:
                try:
                    success, status_code, text = down_setu(setu_name=setu_name, setu_path=setu_path)
                except SSLError:
                    await bot.send(event, '色图站挂了，缓存失败')
                    return
                if not success:
                    await bot.send(event, f'网络异常！\nstatus_code：{status_code}\nresponse：{text}')
                    return
        await bot.send(event, '色图缓存完成')
    local_setu = os.listdir('./setu')
    for setu_name in local_setu:
        await bot.send(event, Image(path='./setu/'+setu_name))
        os.remove('./setu/'+setu_name)
    if group_id in ALLOW_ALL:
        with open("records/setu_record.json", "r", encoding='utf-8') as f:
            setu_record = json.loads(f.read())
        if user_id in setu_record.keys():
            count = setu_record[user_id] + len(local_setu)
        else:
            count = len(local_setu)
        setu_record[user_id] = count
        with open('records/setu_record.json', 'w', encoding='utf-8') as f:
            f.write(pretty_json(setu_record))
    if event.sender.group.id == RTS_ID:
        # message_chain.append(At(target=【先生qq号】]))
        await bot.send(event, ('已输出所有缓存色图，您已看过' + str(count) + '张色图，先生快来看色图'))
