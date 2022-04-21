import app

class rechargeAPI():
    def __init__(self):
        self.get_rechargeCode_url=app.BASE_URL+"/common/public/verifycode/{}"
        self.requestRecharge_url=app.BASE_URL+"/trust/trust/recharge"

    def get_rechargeCode(self,session,r):

        url=self.get_rechargeCode_url.format(str(r))
        response=session.get(url)
        return  response

    def requestRecharge(self,session,amount="10000",valicode="8888"):
        data={'paymentType':'chinapnrTrust',
              'amount':amount,
              'formStr':'reForm',
              'valicode':valicode}
        response=session.post(self.requestRecharge_url,data)
        return  response
