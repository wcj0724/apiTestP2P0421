import logging
import unittest,requests
from api.authenticationAPI import authenticationAPI
from api.loginAPI import loginAPI
from utils import common_assert


class testAuthenticationAPI(unittest.TestCase):
    password1="123456wcj"
    phone1="13676158422"
    phone2="13615143700"
    phone3="13689170780"
    realname="李小小"
    card_id="510522199709068608"
    def setUp(self) -> None:
        self.session=requests.session()
        self.authenticationApi=authenticationAPI()
        self.loginApi=loginAPI()

    def tearDown(self) -> None:
        self.session.close()

    # 认证 - 成功
    # （全部参数正确）
    def test01_authentication_success(self):
        response = self.loginApi.login(self.session,phone=self.phone1)
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        response=self.authenticationApi.authentication(self.session,self.realname,self.card_id)
        logging.info("认证接口的响应数据为：{}".format(response.json()))
        common_assert(self,response,200,200,"提交成功!")


    # 认证 - 失败
    # （姓名为空）
    def test02_authentication_realnameIsNull_fail(self):
        response = self.loginApi.login(self.session,phone=self.phone3)
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        response=self.authenticationApi.authentication(self.session,"",self.card_id)
        logging.info("认证接口的响应数据为：{}".format(response.json()))
        common_assert(self,response,200,100,"姓名不能为空")


    # 认证 - 失败
    # （身份证号为空）
    def test02_authentication_card_idIsNull_fail(self):
        response = self.loginApi.login(self.session,phone=self.phone2)
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        response=self.authenticationApi.authentication(self.session,self.realname,"")
        logging.info("认证接口的响应数据为：{}".format(response.json()))
        common_assert(self,response,200,100,"身份证号不能为空")



    # 获取认证信息 - 成功
    def test03_get_authentication_success(self):
        response = self.loginApi.login(self.session, phone=self.phone1)
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        response = self.authenticationApi.get_authentication(self.session)
        logging.info("获取认证信息接口的响应数据为：{}".format(response.json()))
        self.assertEqual(200, response.status_code)
        # self.assertEqual("-2", response.json().get("realname_status"))
        self.assertIn('510****608',response.json().get("card_id"))




    # 获取认证信息 - 失败
    def test04_get_authentication_fail(self):
        response = self.loginApi.login(self.session, phone=self.phone2)
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        response = self.authenticationApi.get_authentication(self.session)
        logging.info("获取认证信息接口的响应数据为：{}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

