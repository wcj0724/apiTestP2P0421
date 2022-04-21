import time,app,unittest
from lib.HTMLTestRunner_PY3 import HTMLTestRunner
from script.testLoginAPI import testLoginAPI
from script.testAuthenticationAPI import testAuthenticationAPI
from script.testOpenAccountAPI import testOpenAccountAPI
from script.testRechargeAPI import testRechargeAPI

suite=unittest.TestSuite()
suite1=unittest.TestLoader().loadTestsFromTestCase(testLoginAPI)
suite2=unittest.TestLoader().loadTestsFromTestCase(testAuthenticationAPI)
suite3=unittest.TestLoader().loadTestsFromTestCase(testOpenAccountAPI)
suite4=unittest.TestLoader().loadTestsFromTestCase(testRechargeAPI)
suite.addTests([suite1,suite2,suite3,suite4])

# report_file=app.BASE_DIR+"/report/report-{}.html".format(time.strftime("%Y%m%d-%H%M%S"))
report_file=app.BASE_DIR+"/report/report.html"
with open(report_file,"wb") as f:
    runner=HTMLTestRunner(f,title="P2P金融项目接口测试报告")
    runner.run(suite)
