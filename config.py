from mirai import Mirai, WebSocketAdapter
from util import *

adapter = WebSocketAdapter(verify_key='12345', host='localhost', port=6090)
bot = Mirai(12345, adapter)

FUCK_IMG = {
    'is_saving': False,
    'company': '测试',
    'save_path': 'images/test.jpg',
    'group_id': TEST
}

HELP_BASE = [
    '- 来点色图：来点色图（感谢つつ：tsutsu.cc）（不可以色色！）',
    '- 来点二次元：随机Pixiv图（感谢Yueer：yueer.moe）',
    '- 存点色图：缓存10张色图（耗时较长）',
    '- 我要色色：输出所有缓存色图（不可以色色！）',
    '- /daka：帮助master完成每日健康打卡',
    '- 查汇率：查日元汇率及原神、叔叔充值折算',
    '- 发图 图片URL：发送图片',
]
HELP_READ = [
    '- /fuck 迫害对象：进行随机迫害',
    '- /fuck 迫害对象 精准词句：进行精准迫害',
    '- /fucklist 迫害对象：输出全部迫害语句',
]
HELP_WRITE = [
    '- /calc 数学表达式：计算表达式（感谢司机技术支持，别瞎玩）',
    '- /savefuck 迫害对象 词句：学习迫害该词句',
    '- /fuckimg 迫害对象 文件名：图片迫害',
]
