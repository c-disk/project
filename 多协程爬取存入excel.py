from gevent import monkey
monkey.patch_all()
import requests,gevent,openpyxl
from bs4 import BeautifulSoup
from gevent.queue import Queue
from fake_useragent import UserAgent

headers = {
    'user-agent': UserAgent().random
}

work = Queue()
for i in range(1,11):
        for j in range(1,11):
            if i != 10:
                url = f'http://www.boohee.com/food/group/{i}?page={j}'
                work.put_nowait(url)
            else:
                url = f'http://www.boohee.com/food/view_menu?page={j}'
                work.put_nowait(url)

def excel(foodlist,food_list):
    wb = openpyxl.Workbook()
    del wb['Sheet']  #删除默认的Sheet表
    for food in foodlist:
        wb.create_sheet(food)
    for i in range(1,11):
        j = i-1
        for row in food_list[i]:
            sheet = wb[foodlist[j]]
            sheet.append(row)
    wb.save(r'C:\Users\djp\Desktop\食物热量.xlsx')

def spider(foodlist,food_list):
    while not work.empty():
        url = work.get_nowait()
        res = requests.get(url,headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        if url[-1] == '1':
            food = soup.find(class_='widget-food-list').find('h3').text.replace('\n','')
            foodlist.append(food)
        if  url[-8] != 'u':
            if url[-8] != '?':
                key = int(url[-8])
            else:
                try:
                    key = int(url[-9])
                except:
                    key = 10
        else:
            key = 10
        items = soup.find_all(class_='item clearfix')
        for item in items:
            title = item.find(class_='text-box').find('h4').text.replace('\n','')
            link = 'http://www.boohee.com/'+ item.find(class_='text-box').find('h4').find('a')['href']
            hot = item.find(class_='text-box').find('p').text
            food_list[key].append([title,hot,link])

foodlist=[]
food_list = {}
for i in range(1,11):
    food_list[i] = []

task_list = []
for i in range(5):
    task = gevent.spawn(spider,foodlist,food_list)
    task_list.append(task)
gevent.joinall(task_list)
excel(foodlist,food_list)
