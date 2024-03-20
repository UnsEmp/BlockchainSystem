import random
import time
import os


def fun(Name_num):
    # 生成总的姓名数
    #     Name_num = 10
    List_name = []
    List_file = []

    for i in range(Name_num):
        print(f'{str(Name_num)}中: 第 {i} 个人')
        name = ''

        # 生成每个人的姓名长度
        name_len = random.randint(4, 11)
        # print(name_len)
        # time.sleep(0.01)

        # 生成每个人的姓名
        for j in range(name_len):
            name = f"{name}{chr(ord('a') + random.randint(0, 25))}"
        List_name.append(name)

        # 生成每个人的文件
        path = f'UserFile/{str(Name_num)}'
        # 判断这个文件夹是否存在
        if not os.path.exists(path):
            os.makedirs(path)

        path = f'UserFile/{str(Name_num)}/{name}.txt'
        # 判断这个文件之前是否存在
        if not os.path.exists(path):
            fo = open(path, 'w')
            for j in range(random.randint(0, 1e3)):
                file = random.randint(0, 1e3)
                fo.write(str(file))

        List_file.append(f'{name}.txt')
    return List_name, List_file


# print(random.randint(0,9))
# print(List)
t = 10
while t <= 1e3:
    f = open(f'{str(t)}.txt', 'w')

    List_name, List_file = fun(t)

    for i in range(len(List_name)):
        f.write(List_name[i] + ' ' + List_file[i] + '\n')
    f.close()
    print(f'{str(t)}.txt' + ' finish !')
    t *= 10
