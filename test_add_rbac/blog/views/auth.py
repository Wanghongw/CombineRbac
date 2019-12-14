from django.shortcuts import render
from django.http import JsonResponse

from blog import models
from rbac.service.init_permission import init_permission


def login(request):
    data = {'code': None, 'msg': None}

    if request.method == 'GET':
        return render(request,'blog/login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 用项目的用户Model做校验
        user_obj = models.UserInfo.objects.filter(name=username,password=password).first()
        print(user_obj,type(user_obj))
        if user_obj:
            # 权限注入
            init_permission(user_obj,request)

            request.session['is_login'] = True
            request.session['user_id'] = user_obj.pk
            request.session['user'] = user_obj.name
            data['code']=1000
            return JsonResponse(data)

        else:
            data['code'] = 2000
            data['msg'] = '用户名或密码错误'

        return JsonResponse(data)


def index(request):

        return render(request,'blog/index.html')
        # return redirect('blog:index')

