from django.test import TestCase

# Create your tests here.
import time

from datetime import datetime
data='2019-11-07 08:28:19.168798+00:00'
data1=data[:-13]
print(data1)
t3=time.mktime(time.strptime(data1,'%Y-%m-%d %H:%M:%S'))
print('t3',t3)
# t2=time.localtime(t3+3600*8)
# print('t2',t2)
print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(t3+3600*8)))
# print(datetime.now())
# print(time.localtime(t3))
# t1=time.localtime(time.mktime(time.gmtime(t3)))
# print(t1)

# print(t2)
# print(time.strftime("%Y-%m-%d %H:%M:%S",t1))
# print(time.strftime("%Y-%m-%d %H:%M:%S",t2))

# data='2019-11-07 08:28:19'

# t4=

# 3600*8



