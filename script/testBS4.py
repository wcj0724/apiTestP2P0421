from bs4 import BeautifulSoup
html ="""
<html>
<head><title>黑马程序员</title></head>
<body>
<p id="test01">软件测试</p>
<p id="test02">2020年</p>
<a href="/api.html">接口测试</a>
<a href="/web.html">Web自动化测试</a>
<a href="/app.html">APP自动化测试</a>
</body>
</html>
"""

soup=BeautifulSoup(html,"html.parser")

print("p标签的名字",soup.p.name)
print("p标签的值",soup.p.string)
print("p标签的属性值",soup.p["id"])
print("所有p标签",soup.find_all("p"))
p=soup.find_all("p")
print("第2个p标签的属性值:",p[1]["id"])
print("第2个p标签的值:",p[1].string)



