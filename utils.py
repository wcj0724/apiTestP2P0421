import pymysql
import logging
import json

from bs4 import BeautifulSoup

import app
from logging.handlers import TimedRotatingFileHandler
def init_logging():
    # 创建日志器
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)
    # 创建控制台处理器
    sh=logging.StreamHandler()
    # 创建文件处理器
    logfile=app.BASE_DIR+"/log/p2p.log"
    fh=TimedRotatingFileHandler(logfile,
                                when='M',
                                interval=5,
                                backupCount=7,
                                encoding='utf-8')
    # 创建日志格式化器
    fmt = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
    formatter=logging.Formatter(fmt)

    # 添加日志格式化器到日志处理器中
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)

    # 添加日志处理器到日志器中
    logger.addHandler(sh)
    logger.addHandler(fh)
# init_logging()
# logging.info("info日志打印生效了哦！！！！！！")
# # 比info级别高的debug信息会显示出来
# logging.error("error日志打印生效了哦！！！！！！")
# # 比info级别低的debug信息不会显示
# logging.debug("debug日志打印生效了哦！！！！！！")

def common_assert(self,response,code,status,description):
    self.assertEqual(code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(description, response.json().get("description"))

def thirdParty(form,session):
    soup=BeautifulSoup(form,"html.parser")

    # 获取第三方接口地址
    thirdParty_url=soup.form["action"]
    logging.info("thirdParty_url={}".format(thirdParty_url))

    # 创建一个空字典来准备存放数据
    thirdParty_data={}
    for input in soup.find_all("input"):
        # 提取到的input的name属性值作为字典的键，
        # 提取到的input的value属性值作为字典的值，
        # 组成thirdParty_data字典的键值对，以.setdefault方法写入字典
        thirdParty_data.setdefault(input["name"],input["value"])
    logging.info("thirdParty_data={}".format(thirdParty_data))

    response=session.post(thirdParty_url,thirdParty_data)
    logging.info("第三方接口的响应数据为：{}".format(response.text))

    return response

class DButil():
    __conn=None
    __cursor=None
    @classmethod
    def __get_conn(cls,database):
        if cls.__conn is None:
            cls.__conn=pymysql.connect(host="localhost",
                                       port=3306,
                                       user="root",
                                       password="0724",
                                       database=database)
        return cls.__conn

    @classmethod
    def __get_cursor(cls):
        if cls.__cursor is None:
            cls.__cursor=cls.__get_conn(app.DB_wang).cursor()
        return cls.__cursor

    @classmethod
    def __close(cls):
        if cls.__cursor:
            cls.__cursor.close()
            cls.__cursor=None
        if cls.__conn:
            cls.__conn.close()
            cls.__conn=None

    @classmethod
    def delete(cls,database,sql):
        conn = cls.__get_conn(database)
        try:
            cursor=cls.__get_cursor()
            cursor.execute(sql)
            if sql.split()[0].lower()=="select":
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            cls.__close()

# class DButils:
#     @classmethod
#     def get_conn(cls,database):
#         conn = pymysql.connect(host="localhost",
#                                port=3306,
#                                user="root",
#                                password="0724",
#                                database=database,
#                                autocommit=True)
#         return conn
#
#
#     @classmethod
#     def close(cls,cursor=None,conn=None):
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()
#
#     @classmethod
#     def delete(cls,db_name,sql):
#         try:
#             conn = cls.get_conn(db_name)
#             cursor = conn.cursor()
#             cursor.execute(sql)
#         except Exception as e:
#             print(e)
#             conn.rollback()
#         finally:
#             cls.close(cursor,conn)


# 参数化方法--读取获取图片验证码接口要使用的数据
def read_imgCode_data(file):
    imgCode_data_file=app.BASE_DIR+"/data/"+file
    test_case_data=[]
    with open(imgCode_data_file,encoding="utf-8") as f:
        test_data=json.load(f)
        img_test_data=test_data.get("imgCode_data")
        for data in img_test_data:
            test_case_data.append((data.get("type"),data.get("status_code")))
        print("test_case_data={}".format(test_case_data))
    return test_case_data


# 参数化方法--读取注册接口要使用的数据
def read_register_data(file):
    register_data_file=app.BASE_DIR+"/data/"+file
    test_case_data=[]
    with open(register_data_file,encoding="utf-8") as f:
        test_data=json.load(f)
        register_test_data=test_data.get("register_data")
        for data in register_test_data:
            test_case_data.append((data.get("phone"),data.get("password"),data.get("verifycode"),data.get("phone_code"),data.get("dy_server"),data.get("invite_phone"),data.get("status_code"),data.get("status"),data.get("description")))
        print("test_case_data={}".format(test_case_data))
    return test_case_data


# 参数化方法--读取任何接口要使用的数据
# 嵌套循环
# file--------文件名，例如："imgCode_data.json"
# data_desc--数据.json文件里面的第一行，例如："imgCode_data"
# params----数据.json文件里面的,所有要读取的参数组成的字符串，以英文逗号相连接（中间不要出现空格！！）
#           例如："type,status_code"
def read_params_data(file,data_desc,params):
    params_data_file=app.BASE_DIR+"/data/"+file
    test_case_data=[]
    with open(params_data_file,encoding="utf-8")as f:
        test_params_data=json.load(f)
        test_params_list=test_params_data.get(data_desc)
        for data in test_params_list:
            params_list=[]
            for param in params.split(","):
                params_list.append(data.get(param))
            test_case_data.append(params_list)
    logging.info("test_case_data={}".format(test_case_data))
    return test_case_data




if __name__ =="__main__":
        # read_imgCode_data("imgCode_data.json")
        # read_register_data("register_data.json")
        read_params_data("imgCode_data.json", "imgCode_data", "type,status_code")

        # sql = "insert into user value('13977778888');"
        # DButils.delete("wang",sql)
        # DButil.delete("wang", sql)





