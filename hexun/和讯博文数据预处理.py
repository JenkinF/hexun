import numpy as npy
from matplotlib import pylab
from dao.database_connection import DBConnection
import wordcloud as wc
import pandas as pda
import jieba

pylab.rcParams['font.sans-serif'] = ['SimHei']

'''
1.从数据库读取数据
'''


def get_data():
    conn = DBConnection.connect()
    sql = "SELECT * FROM articles"
    data = pda.read_sql(sql, conn)
    DBConnection.disconnect(conn)
    return data


'''
2.缺失值处理
缺值情况：评论数大于0，但是点击量等于0，说明点击量缺失
处理方法：将点击量设置为平均数
'''


def missing_value_handle(data):
    count = 0
    for i in range(len(data["id"])):
        if data["article_comment_count"][i] != 0 and data["article_click_count"][i] == 0:
            data["article_click_count"][i] = 6471
            count += 1
    print("共处理{}条缺值数据".format(count))
    return data


'''
3.生成词云图
'''


def get_world_cloud(data):
    name = ""
    for i in data["article_name"]:
        arr = jieba.cut(i)
        for j in arr:
            name += j + " "
    font = r'C:\Windows\Fonts\simhei.ttf'
    mywc = wc.WordCloud(collocations=False, font_path=font, background_color="white").generate(name)
    pylab.imshow(mywc)
    pylab.axis("off")
    pylab.savefig("./wordCloud.jpg", dpi=200)
    pylab.show()


'''
4.异常值处理
异常情况：点分布不均匀
        评论数大于点击数
处理方法：去除分布集中外的点
        将评论数和点击数置为平均数
'''


def abnormal_value_handle(data):
    count = 0
    da = data.values
    # 数据量较小，采用改值处理
    for i in range(len(da)):
        if da[i][2] > 20000:
            da[i][2] = 6471
            count += 1
        if da[i][3] > 400:
            da[i][3] = 30
            count += 1
        if da[i][3] > da[i][2]:
            da[i][2] = 6471
            da[i][3] = 30
            count += 1
    print("共处理{}条异常数据".format(count))
    # 绘制散点图
    click_count = da.T[2]
    comment_count = da.T[3]
    pylab.plot(comment_count, click_count, "o")
    pylab.xlabel("评论数")
    pylab.ylabel("点击量")
    pylab.show()
    return da


'''
5.数据分析
'''


def data_analysis(data):
    click_counts = data.T[2]
    comment_counts = data.T[3]
    # 最值
    click_max = click_counts.max()
    click_min = click_counts.min()
    comment_max = comment_counts.max()
    comment_min = comment_counts.min()
    # 极差
    click_range = click_max - click_min
    comment_range = comment_max - comment_min
    # 组距
    click_dist = click_range // 10
    comment_dist = comment_range // 10
    # 绘制直方图
    # 点击量
    click_hist = npy.arange(click_min, click_max, click_dist)
    pylab.hist(click_counts.astype(int), click_hist)
    pylab.xlabel("点击量")
    pylab.ylabel("博文数")
    # pylab.hist(click_count, 10)
    pylab.show()

    # 评论数
    comment_hist = npy.arange(comment_min, comment_max, comment_dist)
    pylab.hist(comment_counts.astype(int), comment_hist)
    pylab.xlabel("评论数")
    pylab.ylabel("博文数")
    # pylab.hist(comment_count_list, 10)
    pylab.show()
    # 所有文章中，点击量越多文章数越少,递减
    # 评论数规律同上


if __name__ == '__main__':
    data = get_data()
    get_world_cloud(data)
    print(data.describe())
    data = missing_value_handle(data)
    data = abnormal_value_handle(data)
    data_analysis(data)
