import requests
# from testinformation import testinf
from flask import jsonify
import time


post_data = {
    'name': 'Alice',
    'hash': ''
}

resp = requests.post('http://127.1.1.1:5000/upload/',
                     files={
                         'file1': ('2.jpg', open('2.jpg', 'rb'))
                     },
                     data=post_data)
# 返回上传文件的hash值
print(resp.json())
