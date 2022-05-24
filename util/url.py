from bs4 import BeautifulSoup
import requests

proxies = {
    'http': 'http://localhost:7890/',
    'https': 'https://localhost:7890/',
}

def write(content):
    with open('result.html', 'a') as f:
        f.write(content)

def streamline(content):
    return content.replace(' ', '').replace('\n', '')

def get_title(soup):
    if soup.title:
        title = soup.title.string if soup.title.string else ''
    else:
        title = ''
    # print('soup.title.string:', title, len(title))
    if len(streamline(title)) < 1:
        og_title = soup.find('meta', property='og:title')
        title = og_title.get('content') if og_title else ''
        # print('og:title:', title)
    if len(streamline(title)) < 1:
        og_site_name = soup.find('meta', property='og:site_name')
        title = og_site_name.get('content') if og_site_name else ''
    if len(streamline(title)) < 1:
        title = '无法获取标题！'
    return title

def get_url_brief(url):
    if 'localhost' in url or '127.0.0.1' in url or '[::1]' in url:
        return '谁是孬人'
    try:
        response = requests.get(url, proxies=proxies, timeout=(3, 5), stream=True)
    except requests.exceptions.ConnectionError:
        return '网络连接错误！'
    file_size = response.headers.get('Content-Length', 0)
    # print(file_size)
    if int(file_size) > 50000:
        return '文件过大！'
    # print(response)
    html = response.content
    if len(html) <= 1:
        return '无法爬取该页面！'
    # print(html)
    soup = BeautifulSoup(html, features="lxml")
    # print('标题：', soup.title.string)
    content = ''
    # print(soup.prettify())
    title = get_title(soup)
    body = soup.body
    if body:
        for string in body.strings:
            # print(string)
            string = string.strip() + '\n'
            # write(string)
            if len(string) > 15 and streamline(string) != streamline(title) and 'with JavaScript enabled' not in string:
                content += string
    else:
        content = ''
    if len(streamline(content)) < 1:
        content = '无法获取摘要！'
    return '标题：' + title + '\n' + \
            '摘要：' + content[:180]

def save_img(url):
    if 'localhost' in url or '127.0.0.1' in url or '[::1]' in url:
        return False, '谁是孬人'
    try:
        response = requests.get(url, proxies=proxies, timeout=(3, 5), stream=True)
    except requests.exceptions.ConnectionError:
        return False, '网络连接错误！'
    file_size = response.headers.get('Content-Length', 0)
    if int(file_size) > 10*1e3*1e3: ## 10MB
        return False, '文件过大！'
    with open('temp.jpg', 'wb') as file:
        file.write(response.content)
    return True, '下载成功'

if __name__ == '__main__':
    print(get_url_brief('https://ieeexplore.ieee.org/Xplore/home.jsp'))
