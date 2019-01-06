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

#登录
def logIn(request):
    if request.method == 'GET':
        return render(request,'template/logIn.html')

    elif request.method == 'POST':
        # 获取表单信息
        name = request.POST.get('name')
        passwd = request.POST.get('password')
        next = request.POST.get('next')

        #查询是否存在用户（用户名）
        nameExist = MUL.objects.filter(name__exact=name).exists()
        if nameExist != 0:
            user = MUL.objects.get(name=name)
        else:
            #查询是否存在用户（邮箱）
            emailExist = MUL.objects.filter(email__exact=name).exists()
            if emailExist != 0:
                user = MUL.objects.get(email=name)
            else:
                ero = '用户好像不存在诶╮(╯﹏╰）╭立即注册？'
                return render(request, 'template/logIn.html', {'ero': ero})

        # 加盐
        join_time = user.date_joined[11:16]
        passwd = md5_salt(passwd,join_time)

        if passwd == user.passwd:
            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            user.last_login = now_time
            user.save()
            if next != '':
                next = next
            else:
                next = '/manager/'
            response =  HttpResponseRedirect(next)
            response.set_cookie('username',name, 3600)
            return response
        else:
            ero = '用户名或密码错误！'
            return render(request, 'template/logIn.html', {'ero': ero, 'username': name})
    else:
        return HttpResponse('请使用正确的方式访问本页面哟~~~')

#登出（删除cookie）
def logOut(request):
    response = render(request, 'template/jump.html')
    response.delete_cookie('username')
    return response
