RTS_ID = 12345
TEST_ID = 12345
KXY_ID = 12345
MADOKA_ID = 12345

ALLOW_ALL = [RTS_ID, TEST_ID]
NAOREN = [KXY_ID]
FUTSUU = [MADOKA_ID]

WHITELIST = [12345, 12345, 12345, 12345, 12345]

def auth(group_id, sender_id):
    """Return：可读、可写、消息"""
    if sender_id == 992951869:
        return True, True, "好人"
    if sender_id in WHITELIST:
        return True, True, '白名单'
    if group_id in ALLOW_ALL:
        return True, True, '好群'
    if group_id in FUTSUU:
        return True, False, '您还不在白名单中，请联系星空凛'
    if group_id in NAOREN:
        return False, False, '恁都是孬人'
    return False, False, '该功能仅在特定群中生效！'
