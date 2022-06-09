import os
import random
from typing import Dict
from mirai import GroupMessage, Image
from util import *
from config import *


def fuck_list(event, method, payload):
    if method == 'fucklist':
        group_id = event.sender.group.id
        qq_id = event.sender.id
        can_read, can_write, who, msg = auth(group_id, qq_id)
        if not can_read:
            return bot.send(event, msg)
        with open('records/synonym.json', 'r', encoding='utf-8') as f:
            synonym = json.loads(f.read())
        for key, synonym_list in synonym.items():
            synonym_list = [s.lower() for s in synonym_list]
            if payload.lower() in synonym_list:
                payload = key
        with open('records/fuck_sentence.json', 'r', encoding='utf-8') as f:
            sentence_json = json.loads(f.read())
        company_sentences = sentence_json.get(payload, None)
        if not company_sentences:
            return bot.send(event, '请先为该公司/群友提供嘲讽词句，发送/help以查看帮助')
        company_sentences_str = ''
        message_chain = []
        for sentence in company_sentences:
            if 'images' in sentence and os.path.isfile(sentence):
                message_chain.append(Image(path=sentence))
            else:
                company_sentences_str += sentence + '\n'
        message_chain.insert(0, company_sentences_str)
        return bot.send(event, message_chain)


def record_fuck(company, group_id):
    with open('records/fuck_record.json', 'r', encoding='utf-8') as f:
        record = json.loads(f.read())
    group_record = record[str(group_id)] if str(group_id) in record.keys() else {}
    count = group_record[company] + 1 if company in group_record.keys() else 1
    group_record[company] = count
    record[str(group_id)] = group_record
    with open('records/fuck_record.json', 'w', encoding='utf-8') as f:
        f.write(pretty_json(record))
    action = '乳' if group_id == RTS else '迫害'
    return f'今日{action}{company}！（{count}/1）'


def do_fuck(event, company, company_sentences, precise):
    group_id = event.sender.group.id
    if not company_sentences:  # 该公司不在列表里
        return bot.send(event, '请先为该公司/群友提供迫害词句，发送/help以查看帮助')
    if precise:  # 提供了精准词汇
        company_sentences = [
            s for s in company_sentences if precise.lower() in s.lower()]
    if len(company_sentences) == 0:
        return bot.send(event, '精准失败')
    sen_cnt = len(company_sentences)
    sen_index = random.randint(0, sen_cnt-1)
    content = company_sentences[sen_index]
    msg_chain = []
    if 'images' in content and os.path.isfile(content):
        msg_chain.append(Image(path=content))
    else:
        msg_chain.append(content) 
    msg_chain += ['\n--------\n', record_fuck(company, group_id)]
    return bot.send(event, msg_chain)


def get_true_name(company):
    with open('records/synonym.json', 'r', encoding='utf-8') as f:
        synonym = json.loads(f.read())
    for key, synonym_list in synonym.items():
        synonym_list = [s.lower() for s in synonym_list]
        company = company.lower()
        if company in synonym_list:
            company = key.lower()
            break
    return company


def is_repeat(company, sentence):
    with open('records/fuck_sentence.json', 'r', encoding='utf-8') as f:
        sentence_json: Dict[str, list] = json.loads(f.read())
    if company not in sentence_json.keys(): 
        sentence_json[company] = []
    if sentence in sentence_json[company]:  # 出现重复
        return True, sentence_json, '迫害库中已有该词句！'
    return False, sentence_json, '没有重复'


def save_fuck(company, sentence, group_id):
    is_repeat_, sentence_json, repeat_msg = is_repeat(company, sentence)
    if is_repeat_:
        return repeat_msg
    sentence_json[company].append(sentence)
    with open('records/fuck_sentence.json', 'w', encoding='utf-8') as f:
        f.write(pretty_json(sentence_json))
    return f'针对{company}的词句："{sentence}"学习成功！' + '\n--------\n' + record_fuck(company, group_id)


def save_fuck_qq(event: GroupMessage, method, payload: str):
    if method != 'savefuck':
        return
    group_id = event.sender.group.id
    qq_id = event.sender.id
    can_read, can_write, who, msg = auth(group_id, qq_id)
    if not can_write:
        return bot.send(event, msg)
    if not payload:
        return bot.send(event, '请提供要迫害的对象和词句，发送/help以查看帮助')
    payload_list = payload.split(' ', 1)
    if len(payload_list) != 2:
        return bot.send(event, '请提供该对象的迫害词句，发送/help以查看帮助')
    company = get_true_name(payload_list[0])
    sentence = payload_list[1]
    return bot.send(event, save_fuck(company, sentence, group_id))


def fuck_handler(event: GroupMessage, method, payload):
    if method != 'fuck':
        return
    group_id = event.sender.group.id
    qq_id = event.sender.id
    can_read, can_write, who, msg = auth(group_id, qq_id)
    if not can_read:
        return bot.send(event, msg)
    if not payload:
        return bot.send(event, '请提供要迫害的对象，发送/help以查看帮助')
    payload_list = payload.split(' ', 1)
    company = get_true_name(payload_list[0])
    with open('records/fuck_sentence.json', 'r', encoding='utf-8') as f:
        sentence_json = json.loads(f.read())
    company_sentences = sentence_json.get(company, None)
    sentence = payload_list[1] if len(payload_list) == 2 else None
    return do_fuck(event, company, company_sentences, sentence)


def fuck_detect(event, msg):
    # print('in fuck_detect', msg)
    group_id = event.sender.group.id
    qq_id = event.sender.id
    can_read, can_write, who, auth_msg = auth(group_id, qq_id)
    if not can_read:
        return None
    # print('in fuck_detect, can read', msg)
    with open('records/fuck_sentence.json', 'r', encoding='utf-8') as f:
        sentence_json = json.loads(f.read())
    for company, sens in sentence_json.items():
        if msg in sens:
            # print('检测到迫害')
            return bot.send(event, record_fuck(company, group_id))


def pre_save_img(event: GroupMessage, method, payload):
    if method != 'fuckimg':
        return
    print('in pre_save_img')
    group_id = event.sender.group.id
    qq_id = event.sender.id
    can_read, can_write, who, msg = auth(group_id, qq_id)
    if not can_write:
        return bot.send(event, msg)
    if not payload:
        return bot.send(event, '请提供要迫害的对象和词句，发送/help以查看帮助')
    payload_list = payload.split(' ', 1)
    if len(payload_list) != 2:
        return bot.send(event, '请提供图片文件名（不含后缀），发送/help以查看帮助')
    print('in pre_save_img', 'at get_true_name')
    company = get_true_name(payload_list[0])
    filename = payload_list[1]
    save_path = f'images/{filename}.jpg'
    is_repeat_, sentence_json, repeat_msg = is_repeat(company, save_path)
    print('in pre_save_img', 'at is_repeat')
    if is_repeat_: 
        return bot.send(event, repeat_msg)
    FUCK_IMG['is_saving'] = True
    FUCK_IMG['company'] = company
    FUCK_IMG['save_path'] = save_path
    FUCK_IMG['group_id'] = group_id
    return bot.send(event, '请发送一张图片：')


async def save_img(event: GroupMessage):
    group_id = event.sender.group.id
    images = event.message_chain[Image]
    if len(images) == 0:
        await bot.send(event, '请发送一张图片！')
        return
    await images[0].download(filename=FUCK_IMG['save_path'], determine_type=False)
    await bot.send(event, '图片保存成功！')
    await bot.send(event, save_fuck(FUCK_IMG['company'], FUCK_IMG['save_path'], group_id))
    FUCK_IMG['is_saving'] = False
