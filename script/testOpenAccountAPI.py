import logging
import requests,unittest
from api.openAccountAPI import openAccountAPI
from api.loginAPI import loginAPI
from utils import common_assert
from utils import thirdParty


class testOpenAccountAPI(unittest.TestCase):
    phone1="13676158422"

    def setUp(self) -> None:
        self.session=requests.session()
        self.openAccountApi=openAccountAPI()
        self.loginApi=loginAPI()

    def tearDown(self) -> None:
        self.session.close()

    # 请求开户 - 成功
    def test01_request_account_success(self):
        response=self.loginApi.login(self.session,phone=self.phone1)
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        response=self.openAccountApi.request_account(self.session)
        logging.info("请求开户接口的响应数据为：{}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))



    # 第三方开户接口开户 - 成功
    def test02_thirdParty_account_success(self):
        response = self.loginApi.login(self.session, phone=self.phone1)
        logging.info("登录接口的响应数据为：{}".format(response.json()))
        common_assert(self, response, 200, 200, "登录成功")

        response = self.openAccountApi.request_account(self.session)
        logging.info("请求开户接口的响应数据为：{}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))

        form=response.json().get("description").get("form")
        response=thirdParty(form,self.session)
        self.assertEqual("UserRegister OK",response.text)




        # 由于项目多次使用到向第三方接口发送请求，故，以下代码可以封装，便于调用

        # soup=BeautifulSoup(html,"html.parser")
        #
        # # 获取第三方接口地址
        # thirdParty_account_url=soup.form["action"]
        #
        # # 创建一个空字典来准备存放数据
        # thirdParty_data={}
        # for input in soup.find_all("input"):
        #     # 提取到的input的name属性值作为字典的键，
        #     # 提取到的input的value属性值作为字典的值，
        #     # 组成thirdParty_data字典的键值对，以.setdefault方法写入字典
        #     thirdParty_data.setdefault(input["name"],input["value"])
        # logging.info("thirdParty_data={}".format(thirdParty_data))
        #
        # response=self.session.post(thirdParty_account_url,thirdParty_data)
        # logging.info("第三方开户接口的响应数据为：{}".format(response.text))
        # self.assertEqual("UserRegister OK",response.text)

