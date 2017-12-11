import pymysql

'''
数据库连接类
'''


class DBConnection(object):
    # 连接参数
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '*******',
        'db': 'hexun',
        'charset': 'utf8'
    }

    def __init__(self):
        pass

    # 连接数据库
    @classmethod
    def connect(cls):
        try:
            conn = pymysql.connect(
                host=cls.config['host'],
                port=cls.config['port'],
                user=cls.config['user'],
                password=cls.config['password'],
                db=cls.config['db'],
                charset=cls.config['charset']
            )
            return conn
        except Exception as e:
            print("连接失败：{}".format(e))

    # 断开连接
    @classmethod
    def disconnect(cls, conn):
        if conn:
            try:
                conn.close()
            except Exception as e:
                # print(f"关闭失败：{e}")
                print("关闭失败：{}".format(e))
