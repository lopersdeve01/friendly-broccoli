from django.shortcuts import render

import paramiko
from io import StringIO


#     远程连接执行命令
# 创建SSH对象
# ssh = paramiko.SSHClient()
# # 允许连接不在know_hosts文件中的主机
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # 连接服务器
# ssh.connect(hostname='192.168.153.128', port=22, username='root', password=' #####')
# # 执行命令
# stdin, stdout, stderr = ssh.exec_command('df')
# # 获取命令结果
# result = stdout.read()
# # 关闭连接
# ssh.close()
# print(result.decode('utf-8'))


# #      上传文件
# transport = paramiko.Transport(('192.168.153.128', 22))
# transport.connect(username='root', password='#####')
# sftp = paramiko.SFTPClient.from_transport(transport)
#
#
# # 将location.py 上传至服务器 /tmp/test.py
# # sftp.put(r'E:\untitled\DJANGO\ip\warehouse\index.html', '/opt/index.html')
# sftp.get('/opt/requirements.txt', r'E:\untitled\DJANGO\ip\warehouse\requirements.txt')
#
# transport.close()

# #  私钥执行命令
# private_key = paramiko.RSAKey.from_private_key_file(r'C:/Users/Origin/.ssh/id_rsa')
# # 创建SSH对象
# ssh = paramiko.SSHClient()
# # 允许连接不在know_hosts文件中的主机
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # 连接服务器
# ssh.connect(hostname='192.168.153.128', port=22, username='root', pkey=private_key)
# # 执行命令
# stdin, stdout, stderr = ssh.exec_command('df')
# # 获取命令结果
# result = stdout.read()
# # 关闭连接
# ssh.close()
#
# print(result)


# #  私钥上传下载文件
# private_key = paramiko.RSAKey.from_private_key_file(r'C:/Users/Origin/.ssh/id_rsa')
# transport = paramiko.Transport(('192.168.153.128', 22))
# transport.connect(username='root', pkey=private_key)
# sftp = paramiko.SFTPClient.from_transport(transport)
# # 将location.py 上传至服务器 /tmp/test.py
# # sftp.put('xx.txt', '/opt/xx1.txt')
# # 将remove_path 下载到本地 local_path
# sftp.get('/opt/xx1.txt', 'xx1.txt')
# transport.close()




#   私钥存在内存
key = """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----"""

private_key = paramiko.RSAKey(file_obj=StringIO(key))
print('private_key',private_key)

# 创建SSH对象
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname='192.168.153.128', port=22, username='root', pkey=private_key)

# 执行命令
stdin, stdout, stderr = ssh.exec_command('df')
# 获取命令结果
result = stdout.read()

# 关闭连接
ssh.close()

print(result)