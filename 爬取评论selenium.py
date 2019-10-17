from selenium import webdriver
import time

#静默模式
# from selenium.webdriver.chrome.options import Options # 从options模块中调用Options类
#
# chrome_options = Options() # 实例化Option对象
# chrome_options.add_argument('--headless') # 把Chrome浏览器设置为静默模式
# driver = webdriver.Chrome(options = chrome_options)

#实例化
driver = webdriver.Chrome()

driver.get('https://y.qq.com/n/yqq/song/000xdZuV2LcQ19.html')
time.sleep(2)
more = driver.find_element_by_class_name('js_get_more_hot')
more.click()
list_1 = driver.find_element_by_class_name('js_hot_list').find_elements_by_class_name('comment__text')
for comment in list_1:
    print(comment.text)
    print('')
driver.close()
