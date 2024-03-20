import requests
from flask import jsonify
import time

post_data = {
    'name': '',
    'hash': ''
}
num = 100
List_hash = []
name = []
file_name = []
path = 'C:/Users/13248/Desktop/Data/'
f = open(f'{path}{num}.txt', 'r+')
for line in f.readlines():
    line = line.strip('\n')
    # print(line.split(' ')[0], line.split(' ')[1])
    name.append(line.split(' ')[0])
    file_name.append(line.split(' ')[1])


for i in range(num):
    # print(file_name[i], f'{path}{num}/{file_name[i]}')
    print(f'正在上传第 {i} 个区块')
    resp = requests.post('http://127.1.1.1:5000/upload/',
                         files={
                             'file1': (file_name[i], open(path + f'{num}/' + file_name[i], 'rb'))
                         },
                         data=post_data)
    List_hash.append(resp.json()['hash'])

    # 返回上传文件的hash值
    print(resp.json())

#
# # 测试 num 个用户数据字典树查询所用的时间
# post_data = {
#     'name': '',
#     'hash': '',
#     'method': 1
# }
#
# start = time.perf_counter()
#
# for i in range(num):
#     post_data['name'] = name[i]
#     post_data['hash'] = List_hash[i]
#     resp = requests.post('http://127.1.1.1:5000/', data=post_data)
#
# end = time.perf_counter()
#
# print(f'使用字典树索引的时间: {end - start}')
#
#
# # 测试 num 个用户数据普通查询所用的时间
# post_data['method'] = 2
#
# start = time.perf_counter()
#
# for i in range(num - 1, -1, -1):
#     resp = requests.post('http://127.1.1.1:5000/', data=post_data)
#
# end = time.perf_counter()
#
# print(f'普通搜索的时间: {end - start}')
#
#
