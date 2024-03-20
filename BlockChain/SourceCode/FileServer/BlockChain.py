from werkzeug.datastructures import FileStorage
from Block import Block
from SourceCode.FileServer.perInf import PersonalInformation
from SourceCode.FileServer.perInf import PersonalInformationEncoder
import time
import json
from flask import Flask, jsonify, request, render_template, redirect, send_from_directory
import os
import pytrie

import pymysql

from datetime import datetime


class BlockChain:
    def __init__(self):
        # 初始化链，添加创世区块
        self.chain = [self._create_genesis_block()]
        # 设置初始难度
        self.difficulty = 3
        # # 用户信息
        # self.personalinformation = []

    @staticmethod
    def _create_genesis_block():
        '''
        生成创世区块
        :return: 创世区块
        '''
        # timestamp = time.mktime(time.strptime('2018-06-11 00:00:00', '%Y-%m-%d %H:%M:%S'))
        # print(timestamp)
        # now = datetime.now()
        # print(now)
        block = Block(0, datetime.now(), [], '')
        return block

    def get_latest_block(self):
        '''
        获取链上最后一个也是最新的一个区块
        :return:最后一个区块
        '''
        return self.chain[-1]

    def add_personalInformation(self, personal):
        # 添加用户文件著作信息
        block = Block(self.chain[-1].index + 1, time.time(), personal, self.chain[-1].hash)
        block.mine_block(self.difficulty)
        self.chain.append(block)

        # 将该用户的文件hash值存储到字典树中
        t.__setitem__(block.hash, block.index)

    def verify_blockchain(self):
        '''
        校验区块链数据是否完整 是否被篡改过
        :return: 校验结果
        '''
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]  # 当前遍历到的区块
            previous_block = self.chain[i - 1]  # 当前区块的上一个区块
            if current_block.hash != current_block.calculate_hash():
                # 如果当前区块的hash值不等于计算出的hash值，说明数据有变动
                return False
            if current_block.previous_hash != previous_block.calculate_hash():
                # 如果当前区块记录的上个区块的hash值不等于计算出的上个区块的hash值 说明上个区块数据有变动或者本区块记录的上个区块的hash值被改动
                return False
        return True


app = Flask(__name__)
blockChain = BlockChain()
t = pytrie.Trie()


@app.route('/', methods=["GET"])
def methodEdge():
    return redirect('login')


@app.route('/block', methods=['GET'])
def get_blockchain():

    for line in request.values:
        print(line)
    arr = []
    for chain in blockChain.chain:
        l = {"index": chain.index, "timestamp": chain.timestamp, "current_hash": chain.hash,
             "previous_hash": chain.previous_hash}
        arr.append(l)
    return jsonify(arr)


@app.route('/block', methods=['POST'])
def check():
    print(request.values)
    id = request.values['id']
    name = request.values['name']
    email = request.values['email']
    number = request.values['number']
    sex = request.values['sex']
    timestamp = request.values['timestamp']
## _name, _sex, _number, _email, _file
    blockChain.chain.append(Block(str(int(id) + 1), timestamp, PersonalInformation(name, sex, number, email, ""), blockChain.chain[-1].hash))
    # ha = request.values['hash']
    # if request.values['method'] == 1:
    #     key = t.longest_prefix_value(ha, default=-1)
    #     # print(key)
    #     # print(blockChain.chain[key].hash)
    #     if key == -1 or blockChain.chain[key].hash != ha:
    #         return jsonify({'status': 'Not your file !'})
    #
    #     li = {"name": request.values['name'],
    #           "index": blockChain.chain[key].index,
    #           "timestamp": blockChain.chain[key].timestamp,
    #           "current_hash": blockChain.chain[key].hash,
    #           "previous_hash": blockChain.chain[key].previous_hash}
    #     return jsonify(li)
    # else:
    #     key = -1
    #     for chain in blockChain.chain:
    #         if chain.hash == ha:
    #             key = chain.index
    #             break
    #
    #     if key == -1 or blockChain.chain[key].hash != ha:
    #         return jsonify({'status': 'Not your file !'})
    #
    #     li = {"name": request.values['name'],
    #           "index": blockChain.chain[key].index,
    #           "timestamp": blockChain.chain[key].timestamp,
    #           "current_hash": blockChain.chain[key].hash,
    #           "previous_hash": blockChain.chain[key].previous_hash}
    #     return jsonify(li)
    return ""


@app.route('/upload_file/', methods=['POST'])
def upload_file():
    # file1 = requests_file.FileAdapter.__getattribute__('file1')
    file1: FileStorage = request.files.get('file1')

    # save file
    file1.save(f'static/{file1.filename}')
    print(str(os.path.abspath('static')) + str(f'/{file1.filename}'))
    blockChain.add_personalInformation(PersonalInformation(request.values['name'], time.strftime('%Y/%m/%d %H:%M'),
                                                           str(os.path.abspath('static')) + str(f'/{file1.filename}')))
    return jsonify({'status': 'ok', 'hash': blockChain.chain[-1].hash})

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')


    # for line in request.values:
    #     print(line)
    # print(type(request.values.get('name')))
    name = request.values.get('name')
    number = request.values.get('number')
    gridRadios = request.values.get('gridRadios')
    email = request.values.get('email')
    file = request.values.get('file')
    # listName = ['name', 'number', 'gridRadios', 'email', 'file']

    print(request.files)
    f = request.files['file']
    basePath = os.path.dirname(__file__)
    upload_path = os.path.join(basePath, 'static/files', f.filename)
    print(upload_path)
    f.save(upload_path)
    return redirect('upload')



    # for li in listName:
    #     print(request.values.get(li))

    return 'upload'


@app.route('/download', methods=['GET'])
def download():
    fileName = request.values.get('name')
    return send_from_directory('/files', fileName, as_attachment=True)



# 流式下载
# @app.route('/download/<filename>')
# def uploaded_file(filename):
#     def send_file():
#         store_path = os.path.join(UPLOAD_FOLDER,filename)
#         with open(store_path, 'rb') as targetfile:
#             while 1:
#                 data = targetfile.read(1 * 1024 * 1024)   # 每次读取1MB (可用限速)
#                 if not data:
#                     break
#                 yield data
#     response = Response(send_file(), content_type='application/octet-stream')
#     response.headers["Content-disposition"] = 'attachment; filename=%s' % filename   # 如果不加上这行代码，导致下图的问题
#     return response




@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    return 'search'

@app.route('/login', methods=['GET', 'POST'])
def loginInterface():
    # print(request.method)
    if request.method == 'GET':
        return render_template('login.html')

    error_msg = "密码错误！"

    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", charset='utf8', db='unicom')
    curser = conn.cursor(cursor=pymysql.cursors.DictCursor)


    sql = "select * from admin where username = %s and password = %s"
    curser.execute(sql, (str(request.form.get('Name')), str(request.form.get('Password'))))
    data_list = curser.fetchall()
    # print(data_list)


    conn.close()
    curser.close()
    # print(request.form)
    # return "xxx"

    if data_list == ():
        # flash("登录失败！")
        print("field!")
        return render_template('login.html', error_msg=error_msg)
    else:
        return redirect("user")


@app.route('/register', methods=["GET", "POST"])
def registerUser():
    if request.method == "GET":
        return render_template('signup.html')

    conn = pymysql.connect(host='127.0.0.1', port=3306, user="root", passwd="123456", charset='utf8', db='unicom')
    curser = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select max(id) from admin"
    curser.execute(sql)
    max_id = curser.fetchall()


    sql = "insert into admin (id, username, password, mobile) values (%s, %s, %s, %s)"
    curser.execute(sql, (max_id[0].get('max(id)') + 1, request.form.get('username'), request.form.get('password'), "150xxxxx"))
    conn.commit()

    conn.close()
    curser.close()

    return redirect('login')


@app.route('/user', methods=["GET"])
def userInterface():

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)