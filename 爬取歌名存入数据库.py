import pymysql
import requests
import openpyxl

# rows = [['歌曲名', '专辑名', '播放时长', '播放链接']]
rows = []
url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
for x in range(5):

    params = {
        'ct': '24',
        'qqmusic_ver': '1298',
        'new_json': '1',
        'remoteplace': 'sizer.yqq.song_next',
        'searchid': '64405487069162918',
        't': '0',
        'aggr': '1',
        'cr': '1',
        'catZhida': '1',
        'lossless': '0',
        'flag_qc': '0',
        'p': str(x + 1),
        'n': '20',
        'w': '周杰伦',
        'g_tk': '5381',
        'loginUin': '0',
        'hostUin': '0',
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': 'utf-8',
        'notice': '0',
        'platform': 'yqq.json',
        'needNewCode': '0'
    }
    # 将参数封装为字典
    res_music = requests.get(url, params=params)
    # 调用get方法，下载这个列表
    json_music = res_music.json()
    # 使用json()方法，将response对象，转为列表/字典
    list_music = json_music['data']['song']['list']
    # 一层一层地取字典，获取歌单列表
    for music in list_music:
        # # list_music是一个列表，music是它里面的元素
        # print(music['name'])
        # # 以name为键，查找歌曲名
        # print('所属专辑：' + music['album']['name'])
        # # 查找专辑名
        # print('播放时长：' + str(music['interval']) + '秒')
        # # 查找播放时长
        # print('播放链接：https://y.qq.com/n/yqq/song/' + music['file']['media_mid'] + '.html\n\n')
        # # 查找播放链接
        name = music['name']
        album = music['album']['name']
        interval = music['interval']
        interval = f'{int(interval)//60}分{int(interval)%60}秒'
        link = 'https://y.qq.com/n/yqq/song/' + music['file']['media_mid'] + '.html'
        music_row = [name,album,interval,link]
        rows.append(music_row)

# wb = openpyxl.Workbook()
# sheet = wb.active
# sheet.title = 'jay'
# for row in rows:
#     sheet.append(row)
# wb.save(r'C:\Users\djp\Desktop\歌词.xlsx')

#连接数据库
db = pymysql.connect(
    'localhost',
    'root',
    '1208525117',
    'test_db'
)
#创建游标对象
cursor = db.cursor()
for row in rows:
    try:
        sql = "INSERT INTO 歌词(歌曲名, 专辑名, 播放时长, 播放链接) VALUES ('{}', '{}', '{}', '{}')".format(row[0],row[1],row[2],row[3])
        cursor.execute(sql)
    except:
        pass
    db.commit()
db.close()

