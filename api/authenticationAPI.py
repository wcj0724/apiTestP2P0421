
import app


class authenticationAPI():

    def __init__(self):
        self.authentication_url=app.BASE_URL+"/member/realname/approverealname"
        self.get_authentication_url=app.BASE_URL+"/member/member/getapprove"

    # 认证接口
    def authentication(self,session,realname,card_id):
        data={"realname":realname,
              "card_id":card_id}

        # 请求头类型为：Content-Type：multipart/form-data时，不需要加请求头headers的参数
        # 只需要在后面多传一种数据格式：files={"x":"y"}
        response=session.post(self.authentication_url,data=data,files={"x":"y"})
        return response

    # 获取认证信息接口
    def get_authentication(self,session):
        response=session.post(self.get_authentication_url)
        return response

