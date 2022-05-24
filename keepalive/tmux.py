import os
import time

def monitor():
    last_line = os.popen('tmux capturep -p -t qq | tail -n 1')
    last_line = last_line.read().strip()
    if last_line != '$':
        print('没死')
        return
    print('死了，这就重启')
    os.system('tmux send -t qq "python3 qq.py" ENTER')

if __name__ == '__main__':
    while True:
        monitor()
        print('5min后进行下一次检查')
        time.sleep(60*5)
