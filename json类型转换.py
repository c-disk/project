import json
# 引入json模块
a = [1,2,3,4]
# 创建一个列表a。
b = json.dumps(a)
# 使用dumps()函数，将列表a转换为json格式的字符串，赋值给b。
print(b)
# 打印b。
print(type(b))
# 打印b的数据类型。
c = json.loads(b)
# 使用loads()函数，将json格式的字符串b转为列表，赋值给c。
print(c)
# 打印c。
print(type(c))
# 打印c的数据类型。