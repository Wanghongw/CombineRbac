from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.views import View

from utils import page
from blog.models import Blog,Article
from blog import models,forms

from rbac.service.init_permission import init_permission



data = {'code': None, 'msg': None}

def login(request):

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
            data['msg'] = '没有这个用户'

        return JsonResponse(data)



def index(request):

        return render(request,'blog/index.html')
        # return redirect('blog:index')


##################

def blog_show(request):
    # 查找所有的博客对象
    all_blogs = Blog.objects.all()

    current_page_num = request.GET.get('page', default=1)
    # 每页显示5条
    per_page_counts = 5
    # 总共显示11个页码
    page_number = 11
    total_count = all_blogs.count()
    page_obj = page.PageNation(request.path, current_page_num, total_count, request, per_page_counts,
                               page_number)

    all_blogs = all_blogs.order_by('-pk')[page_obj.start_num:page_obj.end_num]
    ret_html = page_obj.page_html()
    return render(request, 'blog/blog.html', {'all_blogs':all_blogs,'ret_html': ret_html})
    # 如果没查到数据的话，就返回一个空表格页面



def blog_add(request):
    if request.method == 'GET':
        form_obj = forms.BlogModelForm()
        return render(request, 'blog/my_form.html', {'form_obj':form_obj})
    elif request.method == 'POST':
        form_obj = forms.BlogModelForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('blog:blog_show')
        else:
            return render(request, 'blog/my_form.html', {'form_obj': form_obj})


class BlogEdit(View):

    def get(self,request,pk):
        blog_obj = Blog.objects.filter(pk=pk).first()
        form_obj = forms.BlogModelForm(instance=blog_obj)
        return render(request, 'blog/my_form.html', {'form_obj':form_obj})

    def post(self,request,pk):
        blog_obj = Blog.objects.filter(pk=pk).first()
        form_obj = forms.BlogModelForm(request.POST,instance=blog_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('blog:blog_show')
        else:
            return render(request, 'blog/my_form.html', {'form_obj':form_obj})

def blog_del(request,pk):
    Blog.objects.filter(pk=pk).delete()
    return redirect('blog:blog_show')


##########

def article_show(request):
    # 查找所有的文章对象
    all_articles = Article.objects.all()

    current_page_num = request.GET.get('page', default=1)
    # 每页显示5条
    per_page_counts = 5
    # 总共显示11个页码
    page_number = 11
    total_count = all_articles.count()
    page_obj = page.PageNation(request.path, current_page_num, total_count, request, per_page_counts,
                               page_number)

    all_articles = all_articles.order_by('-pk')[page_obj.start_num:page_obj.end_num]
    ret_html = page_obj.page_html()
    return render(request, 'blog/article.html', {'all_articles': all_articles, 'ret_html': ret_html})



def article_add(request):
    if request.method == 'GET':
        form_obj = forms.ArticleModelForm()
        return render(request,'blog/my_form.html',{'form_obj':form_obj})

    if request.method == 'POST':
        form_obj = forms.ArticleModelForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('blog:article_show')
        else:
            return render(request,'blog/my_form.html',{'form_obj':form_obj})

def article_edit(request,pk):
    if request.method == 'GET':
        article_obj = Article.objects.filter(pk=pk).first()
        form_obj = forms.ArticleModelForm(instance=article_obj)
        return render(request,'blog/my_form.html',{'form_obj':form_obj})

    if request.method == 'POST':
        article_obj = Article.objects.filter(pk=pk).first()
        form_obj = forms.ArticleModelForm(request.POST,instance=article_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('blog:article_show')
        else:
            return render(request,'blog/my_form.html',{'form_obj':form_obj})

def article_del(request,pk):
    Article.objects.filter(pk=pk).delete()
    return redirect('blog:article_show')
