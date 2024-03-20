import matplotlib.pyplot as plt
import numpy as np

# 这两行代码解决 plt 中文显示的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 输入统计数据
waters = ('10', '100', '1000', '10000', '100000')
buy_number_line = [0.0281681, 0.3109219, 3.178538599999996, 47.7877703, 2547.3840185999998]
buy_number_trie = [0.0263431, 0.2951456, 3.1406598, 36.468672, 1412.4293027]

bit = 10
for i in range(len(buy_number_line)):
    buy_number_line[i] /= bit
    buy_number_trie[i] /= bit
    bit *= 10

bar_width = 0.3 # 条形宽度
index_trie = np.arange(len(waters)) # 男生条形图的横坐标
index_line = index_trie + bar_width # 女生条形图的横坐标

# 使用两次 bar 函数画出两组条形图
plt.bar(index_trie, height=buy_number_trie, width=bar_width, color='b', label='字典树查询')
plt.bar(index_line, height=buy_number_line, width=bar_width, color='g', label='线性查询')

plt.legend() # 显示图例
plt.xticks(index_trie + bar_width/2, waters) # 让横坐标轴刻度显示 waters 里的饮用水， index_trie + bar_width/2 为横坐标轴刻度的位置
plt.ylabel('平均每次查询时间(s)') # 纵坐标轴标题
plt.title('字典树查询和线性查询性能对比') # 图形标题

plt.show()