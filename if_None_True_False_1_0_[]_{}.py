a=None
# a=1
# a=0
# a=True
# a=False
# a=200
# a="我"
# a={}
# a=[]

# a为1、True、200、我、时，会执行；为False、0、None、{}、[]时不执行
if a:
    print("if a:执行了")

# a为None、0、False、{}、[]时，会执行
if not a:
    print("if not a:执行了")

# 只有a为None时，会执行
if a is None:
    print("if a is None:执行了")

