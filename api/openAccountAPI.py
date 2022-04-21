import app

class openAccountAPI():
    def __init__(self):
        self.request_account_url=app.BASE_URL+"/trust/trust/register"

    def request_account(self,session):
        response=session.post(self.request_account_url)
        return response

    # 不需要定义第三方借口
    # def thirdParty_account(self,session,url):
    #     response=session.post(url=url)
    #     return  response
