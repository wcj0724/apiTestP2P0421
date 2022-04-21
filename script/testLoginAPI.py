import logging
import random
import unittest
from time import sleep
from parameterized import parameterized
from utils import read_imgCode_data, read_register_data, read_params_data

import requests

from api.loginAPI import loginAPI
from utils import common_assert


class testLoginAPI(unittest.TestCase):
    imgVerifyCode = "8888"
    password = "123456wcj"
    phone_code = "666666"
    dy_server = "on"
    phone1 = "13676158422"

    def setUp(self) -> None:
        self.loginApi = loginAPI()
        self.session = requests.session()
        self.phone = "136" + str(random.randint(10000000, 99999999))

    def tearDown(self) -> None:
        self.session.close()

    # 参数化--获取图片验证码，参数化测试用例数据
    # 注意：务必地启动整个类，否则会失败！！！
    # @parameterized.expand(read_imgCode_data("imgCode_data.json"))
    @parameterized.expand(read_params_data("imgCode_data.json", "imgCode_data", "type,status_code"))
    def test01_params_get_imgCode_random_float_success(self, type, status_code):
        r=""
        if type == "float":
            r = random.random()
        elif type == "int":
            r = random.randint(0, 100000)
        elif type == "char":
            r = "".join(random.sample("abcdefghijk", 8))
        response = self.loginApi.getImgCode(self.session, r)
        logging.info("获取图片验证码接口的响应数据为：{}".format(response))
        self.assertEqual(status_code, response.status_code)

    # 获取图片验证码 - 成功（随机小数）
    def test01_get_imgCode_random_float_success(self):
        r = random.random()
        response = self.loginApi.getImgCode(self.session, r)
        logging.info("获取图片验证码接口的响应数据为：{}".format(response))

        self.assertEqual(200, response.status_code)

    # 获取图片验证码 - 成功（随机整数）
    def test02_get_imgCode_random_int_success(self):
        r = random.randint(0, 100000)
        response = self.loginApi.getImgCode(self.session, r)
        self.assertEqual(200, response.status_code)

    # 获取图片验证码 - 失败（随机数为空）
    def test03_get_imgCode_random_isNull_success(self):
        response = self.loginApi.getImgCode(self.session, "")

        self.assertEqual(404, response.status_code)

    # 获取图片验证码 - 失败（随机数为字符串）
    def test04_get_imgCode_random_isStr_success(self):
        # 生成指定长度的随机字符串
        # 随机挑选8个字符出来组成列表
        r = random.sample("abcdefghijk", 8)
        logging.info(r)
        # 将前面得到的列表变成字符串
        r_str = "".join(r)
        logging.info(r_str)
        response = self.loginApi.getImgCode(self.session, r_str)

        self.assertEqual(400, response.status_code)

    # 获取短信验证码 - 成功（全部参数正确）
    def test05_get_SmsCode_success(self):
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        logging.info(self.phone)
        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode=self.imgVerifyCode)
        logging.info("获取短信验证码接口的响应数据为：{}".format(response.json()))

        common_assert(self, response, 200, 200, "短信发送成功")

    # 获取短信验证码 - 失败（手机号为空）
    def test06_get_SmsCode_phoneIsNull_fail(self):
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone="", imgVerifyCode=self.imgVerifyCode)
        logging.info("获取短信验证码接口的响应数据为：{}".format(response.json()))

        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

    # 获取短信验证码 - 失败（验证码为空）
    def test07_get_SmsCode_imgVerifyCodeIsNull_fail(self):
        logging.info(self.phone)
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode="")
        logging.info("获取短信验证码接口的响应数据为：{}".format(response.json()))

        common_assert(self, response, 200, 100, "图片验证码错误")

    # 获取短信验证码 - 失败（图片验证码错误）
    def test08_get_SmsCode_imgVerifyCode_Error_fail(self):
        logging.info(self.phone)

        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode="9999")
        logging.info("获取短信验证码的响应数据为：{}".format(response.json()))

        common_assert(self, response, 200, 100, "图片验证码错误")

    # 参数化-注册-成功（必填参数正确）
    # 注意：务必地启动整个类，否则会失败！！！
    # @parameterized.expand(read_register_data("register_data.json"))
    @parameterized.expand(read_params_data("register_data.json", "register_data", "phone,password,verifycode,phone_code,dy_server,invite_phone,status_code,status,description"))
    def test09_params_register_required_success(self,phone,password,verifycode,phone_code,dy_server,invite_phone,status_code,status,description):
        logging.info("注册的手机号为:{}".format(phone))
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=phone, imgVerifyCode=verifycode)

        common_assert(self, response, 200, 200, "短信发送成功")

        response = self.loginApi.register(self.session, phone,password,verifycode,phone_code,dy_server,invite_phone)
        logging.info("注册接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, status_code,status,description)

    # 注册-成功（必填参数正确）
    def test09_register_optional_success(self):
        logging.info("注册成功的手机号为：{}".format(self.phone))
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode=self.imgVerifyCode)

        common_assert(self, response, 200, 200, "短信发送成功")

        response = self.loginApi.register(self.session, phone=self.phone, password=self.password,
                                          invite_phone="")
        logging.info("注册接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "注册成功")

    # 注册-成功（全部参数正确）
    def test10_register_optional_success(self):
        logging.info("注册成功的手机号为：{}".format(self.phone))
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode=self.imgVerifyCode)

        common_assert(self, response, 200, 200, "短信发送成功")

        response = self.loginApi.register(self.session, phone=self.phone, password=self.password,
                                          invite_phone="18281626378")
        logging.info("注册接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "注册成功")

    # 注册 - 失败（手机号为空）
    def test11_register_phoneIsNull_fail(self):
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode=self.imgVerifyCode)
        common_assert(self, response, 200, 200, "短信发送成功")

        response = self.loginApi.register(self.session, phone="", password=self.password)
        logging.info("注册接口的响应数据为：{}".format(response.json()))

        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

    # 注册 - 失败（密码为空）
    def test12_register_passwordIsNull_fail(self):
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode=self.imgVerifyCode)

        common_assert(self, response, 200, 200, "短信发送成功")

        response = self.loginApi.register(self.session, phone=self.phone, password="")
        logging.info("注册接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "密码不能为空")

    # 注册 - 失败（图片验证码为空）
    def test13_register_imgCodeIsNull_fail(self):
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode=self.imgVerifyCode)
        logging.info("注册接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "短信发送成功")

        response = self.loginApi.register(self.session, phone=self.phone, password=self.password, verifycode="")
        logging.info("注册接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "验证码不能为空!")

    # 注册 - 失败（短信验证码为空）
    def test14_register_smsCodeIsNull_fail(self):
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode=self.imgVerifyCode)

        common_assert(self, response, 200, 200, "短信发送成功")

        response = self.loginApi.register(self.session, phone=self.phone, password=self.password,
                                          verifycode=self.imgVerifyCode, phone_code="")
        logging.info("注册接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "短信验证码不能为空")

    # 注册 - 失败（不同意协议）
    def test15_register_disagreenProtocol_fail(self):
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode=self.imgVerifyCode)

        common_assert(self, response, 200, 200, "短信发送成功")

        response = self.loginApi.register(self.session, phone=self.phone, password=self.password,
                                          verifycode=self.imgVerifyCode, phone_code=self.phone_code, dy_server="off")
        logging.info("注册接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "请同意我们的条款")
        self.assertEqual(100, response.json().get("status"))

    # 注册 - 失败（图片验证码错误）
    def test16_register_imgCodeError_fail(self):
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode=self.imgVerifyCode)

        common_assert(self, response, 200, 200, "短信发送成功")

        response = self.loginApi.register(self.session, phone=self.phone, password=self.password, verifycode="9999")
        logging.info("注册接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "验证码错误!")

    # 注册 - 失败（短信验证码错误）
    def test17_register_smsCodeError_fail(self):
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode=self.imgVerifyCode)

        common_assert(self, response, 200, 200, "短信发送成功")

        response = self.loginApi.register(self.session, phone=self.phone, password=self.password,
                                          verifycode=self.imgVerifyCode, phone_code="777777")
        logging.info("注册接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "验证码错误")

    # 注册 - 失败（手机号已存在）
    def test18_register_phoneIsExist_fail(self):
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode=self.imgVerifyCode)

        common_assert(self, response, 200, 200, "短信发送成功")

        response = self.loginApi.register(self.session, phone="18281626378", password=self.password)
        logging.info("注册接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "手机已存在!")

    # 注册 - 失败（邀请人手机号未注册）
    def test19_register_invite_phoneIsNotExist_fail(self):
        r = random.random()
        response = self.loginApi.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)

        response = self.loginApi.getSmsCode(self.session, phone=self.phone, imgVerifyCode=self.imgVerifyCode)

        common_assert(self, response, 200, 200, "短信发送成功")

        response = self.loginApi.register(self.session, phone=self.phone, password=self.password,
                                          invite_phone="18281626377")
        logging.info("注册接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "推荐人不存在")

    # 登录-成功
    # （全部参数正确）
    def test20__login_success(self):
        response = self.loginApi.login(self.session, self.phone1)
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

    # 登录-失败
    # （手机号为空）
    def test21_login_phoneIsNull_fail(self):
        response = self.loginApi.login(self.session, "")
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "用户名不能为空")

    # 登录-失败
    # （密码为空）
    def test22_login_passwordIsNull_fail(self):
        response = self.loginApi.login(self.session, self.phone1, "")
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "密码不能为空")

    # 登录 - 失败
    # （手机号不存在）
    def test23_login_phoneIsNotExist_fail(self):
        response = self.loginApi.login(self.session, "18281626377")
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "用户不存在")

    # 登录 - 失败
    # （密码错误1次，2次，3次，错误3次之后需要等1分钟输入正确密码才能登录成功）

    def test24_login_passwordIsError_threeTimes_fail(self):
        response = self.loginApi.login(self.session, self.phone1, "123456wcj1")
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")

        response = self.loginApi.login(self.session, self.phone1, "123456wcj1")
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")

        response = self.loginApi.login(self.session, self.phone1, "123456wcj1")
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        response = self.loginApi.login(self.session, self.phone1, "123456wcj1")
        common_assert(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        logging.info("登录接口的响应数据为：{}".format(response.json()))

        # 等待60s之后
        sleep(65)

        response = self.loginApi.login(self.session, self.phone1, "123456wcj")
        common_assert(self, response, 200, 200, "登录成功")
        logging.info("登录接口的响应数据为：{}".format(response.json()))

    # 判断是否登录
    # （登录）
    def test25_register_optional_success(self):
        response = self.loginApi.login(self.session, self.phone1)
        common_assert(self, response, 200, 200, "登录成功")

        response = self.loginApi.loginStatus(self.session)
        logging.info("登录状态查询接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "OK")

    # 判断是否登录
    # （未登录）
    def test26_register_optional_success(self):
        response = self.loginApi.loginStatus(self.session)
        logging.info("登录状态查询接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 250, "您未登陆！")
