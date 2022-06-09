import requests
import time

session = requests.Session()
session.trust_env = False

url = 'https://'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}
cookies = {

}
payload = {
    'created': int(time.time()),
}

def do_daka():
    payload['date'] = time.strftime(r'"%Y%m%d"', time.localtime()) 
    payload['created'] = int(time.time())
    response = session.post(url, headers=headers, data=payload, cookies=cookies)
    return(response.status_code, response.json())

if __name__ == '__main__':
    print(do_daka())
