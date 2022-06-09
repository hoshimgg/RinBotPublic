RTS = 12345
TEST = 12345
KXY = 12345
MADOKA = 12345

ALLOW_ALL = [RTS, TEST]
NAOREN = [KXY]
FUTSUU = [MADOKA]

RIN = 12345
PUELLA_MAGI_NICO = 12345
MENG_BAI = 12345
YU_XI = 12345
SAYAKA = 12345

MASTER = [RIN]
WHITELIST = [PUELLA_MAGI_NICO, MENG_BAI, YU_XI, SAYAKA]

def auth(group_id, sender_id):
    """Return：可读、可写、用户组、消息"""
    if sender_id in MASTER:
        return True, True, '主人', None
    if sender_id in WHITELIST:
        return True, True, '好人', None
    if group_id in ALLOW_ALL:
        return True, True, '好群', None
    if group_id in FUTSUU:
        return True, False, '普通群', '您还不在白名单中，请联系星空凛'
    if group_id in NAOREN:
        return False, False, '孬人', '恁都是孬人'
    return False, False, '路人', '该功能仅在特定群中生效！'
