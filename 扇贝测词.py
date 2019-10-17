import requests
from fake_useragent import UserAgent
from time import sleep
import csv

headers = {
        'referer': 'https://www.shanbay.com/vocabtest/welcome/',
        # 请求来源，携带的信息比“origin”更丰富，本案例中其实是不需要加这个参数的，只是为了演示
        'user-agent':UserAgent().chrome
        # 标记了请求从什么设备，什么浏览器上发出
}

#选择词库
res = requests.get('https://www.shanbay.com/api/v1/vocabtest/category/?_=1568303089339',headers=headers)
json = res.json()
i = 0
for word_type in json['data']:
    print(f'{i}:{word_type[1]}',end=' ')
    i+=1
print('')
choice_0 = int(input('第 1 步，请从以上选择出题范围：(输入选择数字)'))
print('已选择:'+json['data'][choice_0][1])
print('')
choice_0 = json['data'][choice_0][0]

#随机抽取50个单词
url = 'https://www.shanbay.com/api/v1/vocabtest/vocabularies/?category='+ choice_0
res = requests.get(url,headers=headers)
json = res.json()
i = 0
word_list = []
for words in json['data']:
    word = words['content']
    print(f'{i}.{word}')
    i += 1
    word_list.append(word)
choice_1 = input('第 2 步，请从以上选择你认识的单词：（输入数字,用逗号隔开）')
print('')
choices = choice_1.split(',')

#选择认识的单词
print('第 3 步，单词测试，请选择正确的词义')
know_list = []
bingo_list = []
error_list = []
chinese = []
for choice in choices:
    know_list.append(word_list[int(choice)])
for konw_word in know_list:
    for words in json['data']:
        if words['content'] == konw_word:
            print(konw_word)
            i = 0
            for define in words['definition_choices']:
                print(f'{i}.'+define['definition'])
                i+=1
            choice_2 = int(input('请选择正确的词义:(输入选择数字)'))
            if words['definition_choices'][choice_2]['pk'] == words['pk']:
                print('bingo!')
                print('')
                bingo_list.append(konw_word)
                sleep(0.5)
            else:
                print('error~')
                print('')
                error_list.append(konw_word)
                for pk_go in words['definition_choices']:
                    if pk_go['pk'] ==  words['definition_choices'][choice_2]['pk']:
                        chinese.append(pk_go['definition'])
                sleep(0.5)

#生成报告
know = len(choices)
unknow = 50 - know
bingo = len(bingo_list)
error = len(error_list)
print('-'*30)
print(f'50个单词，认识{know}个单词，不认识{unknow}个单词，掌握{bingo}个单词，错了{error}个单词')
print(f'错题集：{error_list}')

with open('C:\\Users\\djp\\Desktop\\扇贝错题集.csv','w',newline='',encoding='utf-8')as file:
    writer = csv.writer(file)
    writer.writerow(error_list)
    writer.writerow(chinese)

