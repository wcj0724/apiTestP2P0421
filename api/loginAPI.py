import app
class loginAPI():
    def __init__(self):
        self.getImgCode_url=app.BASE_URL+"/common/public/verifycode1/"
        self.getSmsCode_url=app.BASE_URL+"/member/public/sendSms"
        self.register_url=app.BASE_URL+"/member/public/reg"
        self.login_url=app.BASE_URL+"/member/public/login"
        self.loginStatus_url=app.BASE_URL+"/member/public/islogin"

    # 获取图片验证码接口
    def getImgCode(self,session,r):
        url=self.getImgCode_url+str(r)
        response=session.get(url)
        return response

    # 获取短信验证码接口
    def getSmsCode(self,session,phone,imgVerifyCode):
        data={"phone":phone,
              "imgVerifyCode":imgVerifyCode,
              "type":"reg"}

        # 请求头类型为：Content-Type：application/x-www-form-urlencoded时，
        # 可以不加请求头headers的参数，
        # 因为默认：请求头类型就是application/x-www-form-urlencoded
        response=session.post(url=self.getSmsCode_url,headers=app.HEADERS,data=data)
        return response

    # 获注册接口
    def register(self,session,phone,password,verifycode="8888",phone_code="666666",dy_server="on",invite_phone=""):
        data={"phone":phone,
              "password":password,
              "verifycode":verifycode,
              "phone_code":phone_code,
              "dy_server":dy_server,
              "invite_phone":invite_phone}
        response=session.post(url=self.register_url,headers=app.HEADERS,data=data)
        return response

    # 登录接口
    def login(self,session,phone="13676158422",password="123456wcj"):
        data={"keywords":phone,
              "password":password}
        response=session.post(self.login_url,data=data)
        return response

    # 登录状态查询接口
    def loginStatus(self,session):
        response=session.post(self.loginStatus_url)
        return response



        