import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import schedule
import time

def wea(weather):
    day = weather.find('h1').text[:3]
    state = weather.find(class_='wea').text
    tem = weather.find(class_='tem').text.replace('\n', '')
    ifo = (f'{day}  天气：{state}  气温：{tem}')
    return ifo

def wea_spiaer():
    headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    url='http://www.weather.com.cn/weather/101301212.shtml'
    res=requests.get(url,headers=headers)
    res.encoding='utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    weather = soup.find('ul',class_='t').find('li',class_='on')
    today = wea(weather)
    weather = soup.find('ul',class_='t').find('li',class_='lv3')
    tom = wea(weather)
    return f'{today}\n{tom}'

def mail():
    mailhost='smtp.qq.com'
    #把qq邮箱的服务器地址赋值到变量mailhost上，地址需要是字符串的格式。
    qqmail = smtplib.SMTP()
    #实例化一个smtplib模块里的SMTP类的对象，这样就可以SMTP对象的方法和属性了
    qqmail.connect(mailhost,25)
    #连接服务器，第一个参数是服务器地址，第二个参数是SMTP端口号。
    account = '1208525117@qq.com'
    #获取邮箱账号
    password = 'kyaatsrevjolfeef'
    #获取邮箱密码
    qqmail.login(account,password)
    #登录邮箱，第一个参数为邮箱账号，第二个参数为邮箱密码
    receiver= '1208525117@qq.com'
    #获取收件人的邮箱
    content= wea_spiaer()
    #输入你的邮件正文
    message = MIMEText(content, 'plain', 'utf-8')
    #实例化一个MIMEText邮件对象，该对象需要写进三个参数，分别是邮件正文，文本格式和编码.
    subject = '天气'
    #用input()获取邮件主题
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = Header(account)
    #在等号的右边，是实例化了一个Header邮件头对象，该对象需要写入两个参数，分别是邮件主题和编码，然后赋值给等号左边的变量message['Subject']。

    #发送邮件，调用了sendmail()方法，写入三个参数，分别是发件人，收件人，和字符串格式的正文。
    try:
        qqmail.sendmail(account, receiver, message.as_string())
        print ('邮件发送成功')
    except:
        print ('邮件发送失败')
    qqmail.quit()
    #退出邮箱

def job():
    wea_spiaer()
    mail()

schedule.every().day.at("14:59").do(job)
#部署每天的8：30执行函数的任务
while True:
    schedule.run_pending()
    time.sleep(1)