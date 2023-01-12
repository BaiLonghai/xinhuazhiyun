#-*-coding:utf_8-*-
import random
import string
import time
#输入生成密码位数
password_digits = 16
#输入生成密码个数
password_num = int(input('输入生成密码个数(默认为1):') or "1")
#定义密码组成字符
digits = string.digits
uppercase = string.ascii_uppercase
lowercase = string.ascii_lowercase
non_alphanumeric='!@#&*$^'
#字符数量限制
digits_num = random.randint(1,6)
uppercase_num = random.randint(1,password_digits-digits_num-1)
lowercase_num =random.randint(1,password_digits-digits_num-uppercase_num)
non_alphanumeric_num=password_digits-digits_num-uppercase_num-lowercase_num
#生成字符串


for i in range(password_num):
    password = random.sample(digits,digits_num) + random.sample(uppercase,uppercase_num)+ random.sample(lowercase,lowercase_num)+random.sample(non_alphanumeric,non_alphanumeric_num)
    random.shuffle(password)
    #列表转字符串
    new_password = ''.join(password)
    print("密码为：",new_password)
    #写入到日志文件，防止历史密码丢失
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    filename = 'passwd.txt'
    with open(filename, 'a') as file_object:
        file_object.write(str(now_time)+"\t"+new_password+"\n")
input('Press Enter to exit...')

