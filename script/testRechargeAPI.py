import logging
import random

import requests,unittest
from api.rechargeAPI import rechargeAPI
from api.loginAPI import loginAPI
from utils import common_assert
from utils import thirdParty


class testRechargeAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.session=requests.session()
        self.loginApi=loginAPI()
        self.rechargeApi=rechargeAPI()

    def tearDown(self) -> None:
        self.session.close()

    # 获取充值验证码 - 成功
    # （随机小数）
    def test01_get_recharge_random_float_success(self):
        response = self.loginApi.login(self.session)
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        r=random.random()
        response=self.rechargeApi.get_rechargeCode(self.session,r)
        logging.info("获取充值验证码接口的响应数据为：{}".format(response.text))
        self.assertEqual(200,response.status_code)




    # 获取充值验证码 - 成功
    # （随机整数）
    def test02_get_recharge_random_int_success(self):
        response = self.loginApi.login(self.session)
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        r=random.randint(1000000,9999999)
        response=self.rechargeApi.get_rechargeCode(self.session,r)
        logging.info("获取充值验证码接口的响应数据为：{}".format(response.text))
        self.assertEqual(200,response.status_code)

    # 获取充值验证码 - 成功
    # （随机数为空）
    def test03_get_recharge_random_isNULL_success(self):
        response = self.loginApi.login(self.session)
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        response=self.rechargeApi.get_rechargeCode(self.session,"")
        logging.info("获取充值验证码接口的响应数据为：{}".format(response.text))
        self.assertEqual(404,response.status_code)


    # 充值 - 成功
    # （全部参数正确）
    def test04_recharge_success(self):
        response = self.loginApi.login(self.session,phone="18281626378",password="0724wcjWCJ.,")
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        r=random.random()
        response=self.rechargeApi.get_rechargeCode(self.session,r)
        logging.info("获取充值验证码接口的响应数据为：{}".format(response.text))
        self.assertEqual(200,response.status_code)

        response=self.rechargeApi.requestRecharge(self.session)
        logging.info("请求充值接口的响应数据为：{}".format(response.json()))
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))



    # 充值 - 失败
    # （验证码错误）

    def test05_recharge_Code_isError_fail(self):
        response = self.loginApi.login(self.session)
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        r=random.random()
        response=self.rechargeApi.get_rechargeCode(self.session,r)
        logging.info("获取充值验证码接口的响应数据为：{}".format(response.text))
        self.assertEqual(200,response.status_code)

        response=self.rechargeApi.requestRecharge(self.session,"100000000","9999")
        logging.info("请求充值接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "验证码错误")

    # 充值 - 失败
    # （充值金额为空）

    def test06_recharge_amount_isNULL_fail(self):
        response = self.loginApi.login(self.session)
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        r=random.random()
        response=self.rechargeApi.get_rechargeCode(self.session,r)
        logging.info("获取充值验证码接口的响应数据为：{}".format(response.text))
        self.assertEqual(200,response.status_code)

        response=self.rechargeApi.requestRecharge(self.session,"")
        logging.info("请求充值接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 100, "充值金额不能为空")

    # 第三方充值接口-充值成功
    # （全部参数正确）
    def test07_thirdParty_recharge_success(self):
        response = self.loginApi.login(self.session,phone="18281626378",password="0724wcjWCJ.,")
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        r = random.random()
        response = self.rechargeApi.get_rechargeCode(self.session, r)
        logging.info("获取充值验证码接口的响应数据为：{}".format(response.text))
        self.assertEqual(200, response.status_code)

        response = self.rechargeApi.requestRecharge(self.session)
        logging.info("请求充值接口的响应数据为：{}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))


        form = response.json().get("description").get("form")
        response = thirdParty(form, self.session)
        self.assertEqual("NetSave OK",response.text)


