import requests
from bs4 import BeautifulSoup

menu = []
for i in range(10):
    k = i*25
    URL = f'https://movie.douban.com/top250?start={k}&filter='
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    infos = soup.find_all('div', class_='item')
    for info in infos:
        rank = '排行榜第' + info.find('em').text + '位：'
        link = '链接：' + info.find('a')['href']
        names = info.find_all('span', class_='title')
        try:
            name = '电影名：' + names[0].text + names[1].text + info.find('span', class_='other').text
        except:
            name = '电影名：' + names[0].text + info.find('span', class_='other').text
        name = ''.join(name.split())
        score = '评分：' + info.find('span', class_='rating_num').text
        try:
            say = '推荐语：' + info.find('p', class_='quote').text
        except:
            pass
        say = ''.join(say.split())
        menu.append([rank, name, score, say, link])

file = open(r'C:\Users\djp\Desktop\test\豆瓣电影.txt', 'w',encoding='utf-8')
for i in range(len(menu)):
    s = str(menu[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
    s = s.replace("'", '').replace(',', '') + '\n'+'\n'  # 去除单引号，逗号，每行末尾追加换行符
    file.write(s)
file.close()
print("保存文件成功")












