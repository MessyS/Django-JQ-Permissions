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

#重置密码
def reset(request):
    if request.method == 'POST':
        #获取表单信息
        name = request.POST.get('name')
        old_passwd = request.POST.get('old_passwd')
        new_passwd = request.POST.get('new_passwd')
        confirm_passwd = request.POST.get('confirm_passwd')

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
                return render(request, 'template/reset.html', {'ero': ero})

        # 旧密码核对
        join_time = user.date_joined[11:16]
        passwd = md5_salt(old_passwd,join_time)
        if passwd == user.passwd:
            # 两次新密码核对
            if new_passwd == confirm_passwd:
                now_time_s = time.strftime('%H:%M', time.localtime(time.time()))
                passwd = md5_salt(new_passwd, now_time_s)

                user.passwd = passwd
                user.save()
                return render(request, 'template/jump.html')
            else:
                ero = '两次密码不一样诶，请重新输入'
                usermsg = {
                    'name': name,
                    'oldpasswd': old_passwd
                }
                return render(request, 'template/reset.html', {'ero': ero, "usermeg": usermsg})
        else:
            ero = '原来的密码错了哦~~~请重新输入'
            usermsg = {
                'name': name,
            }
            return render(request, 'template/reset.html', {'ero': ero, "usermeg": usermsg})
    else:
        return render(request,'template/reset.html')
