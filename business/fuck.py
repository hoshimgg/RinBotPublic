import os
import random
from mirai import GroupMessage, Image
from util import *
from config import bot

def fuck_list(event, method, payload):
    if method == 'fucklist':
        group_id = event.sender.group.id
        qq_id = event.sender.id
        can_read, can_write, msg = auth(group_id, qq_id)
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

def do_fuck(event, company_sentences, precise):
    if not company_sentences:  # 该公司不在列表里
        return bot.send(event, '请先为该公司/群友提供迫害词句，发送/help以查看帮助')
    if precise:  # 提供了精准词汇
        company_sentences = [s for s in company_sentences if precise.lower() in s.lower()]
    if len(company_sentences) == 0:
        return bot.send(event, '精准失败')
    sen_cnt = len(company_sentences)
    sen_index = random.randint(0, sen_cnt-1)
    content = company_sentences[sen_index]
    if 'images' in content:
        if os.path.isfile(content):
            return bot.send(event, Image(path=content))
    return bot.send(event, content)

def save_fuck(event, company, sentence, company_sentences, sentence_json):
    if not company_sentences:  # 该公司不在列表里，新建一个key
        sentence_json[company] = []
    elif sentence in company_sentences:  # 出现重复
        return bot.send(event, '库中已有该词句！')
    sentence_json[company].append(sentence)
    with open('records/fuck_sentence.json', 'w', encoding='utf-8') as f:
        f.write(pretty_json(sentence_json))
    return bot.send(event, f'针对{company}的词句："{sentence}"学习成功！')

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

def save_fuck_new(event: GroupMessage, method, payload: str):
    if method != 'savefuck':
        return
    group_id = event.sender.group.id
    qq_id = event.sender.id
    can_read, can_write, msg = auth(group_id, qq_id)
    if not can_write:
        return bot.send(event, msg)
    if not payload:
        return bot.send(event, '请提供要迫害的对象和词句，发送/help以查看帮助')
    payload_list = payload.split(' ', 1)
    if len(payload_list) != 2:
        return bot.send(event, '请提供该对象的迫害词句，发送/help以查看帮助')
    company = get_true_name(payload_list[0])
    sentence = payload_list[1]
    with open('records/fuck_sentence.json', 'r', encoding='utf-8') as f:
        sentence_json: dict = json.loads(f.read())
    if company not in sentence_json.keys():
        sentence_json[company] = []
    company_sentences = sentence_json[company]
    if sentence in company_sentences:  # 出现重复
        return bot.send(event, '迫害库中已有该词句！')
    sentence_json[company].append(sentence)
    with open('records/fuck_sentence.json', 'w', encoding='utf-8') as f:
        f.write(pretty_json(sentence_json))
    return bot.send(event, f'针对{company}的词句："{sentence}"学习成功！')

def fuck_handler(event: GroupMessage, method, payload):
    if method != 'fuck':
        return
    group_id = event.sender.group.id
    qq_id = event.sender.id
    can_read, can_write, msg = auth(group_id, qq_id)
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
    return do_fuck(event, company_sentences, sentence)

def fuck_detect(event, msg):
    group_id = event.sender.group.id
    if group_id not in ALLOW_ALL+FUTSUU:
        return
    with open('records/fuck_sentence.json', 'r', encoding='utf-8') as f:
        sentence_json = json.loads(f.read())
    for company, sens in sentence_json.items():
        if msg in sens:
            with open('records/fuck_record.json', 'r', encoding='utf-8') as f:
                record = json.loads(f.read())
            if company in record.keys():
                count = record[company] + 1
                record[company] = count
            else:
                count = 1
                record[company] = count
            with open('records/fuck_record.json', 'w', encoding='utf-8') as f:
                f.write(pretty_json(record))
            action = '迫害' if group_id in FUTSUU else '乳'
            return bot.send(event, f'今日{action}{company}！（{count}/1）')
