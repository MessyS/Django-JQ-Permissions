from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect
from messy.models import *
import hashlib,time

#md5加密处理函数
def md5_salt(str,salt):
    passwd = str + salt
    md5_encode = hashlib.new('md5',passwd.encode('utf-8'))
    passwd = md5_encode.hexdigest()
    return passwd

#注册
def signUp(request):
    # 先判断GET，进行请求截断，节省服务器资源
    if request.method == 'GET':
        return render(request, 'template/signUp.html')
    if request.method == 'POST':
        #后端判断两次密码是否一致
        name = request.POST.get('name')
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')
        confirm_passwd = request.POST.get('confirm-passwd')

        #判断为空
        if name != '' and email != '' and passwd != '' and confirm_passwd != '':
            #判断密码重合
            if passwd == confirm_passwd:
                #加盐
                now_time_s = time.strftime('%H:%M', time.localtime(time.time()))
                passwd = md5_salt(passwd,now_time_s)

                now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                addUser = MUL(name=name,email=email,passwd=passwd,date_joined=now_time)
                addUser.save()
                return render(request,'template/jump.html')
            else:
                usermsg = {"name": name, 'email': email}
                ero = '两次密码不一致，请重新输入！'
                return render(request, 'template/signUp.html',{'ero':ero,'usermsg':usermsg})
        else:
            ero = '请输入内容！'
            usermsg = {"name":name,'email':email,"passwd":passwd,'confirm_passwd':confirm_passwd}
            return render(request, 'template/signUp.html', {'ero': ero,'usermsg':usermsg})
    else:
        return HttpResponse('请使用正确的方式访问本页面哟~')
