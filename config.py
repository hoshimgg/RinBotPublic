from mirai import Mirai, WebSocketAdapter

adapter = WebSocketAdapter(verify_key='password', host='localhost', port=6090)
bot = Mirai(12345, adapter)
