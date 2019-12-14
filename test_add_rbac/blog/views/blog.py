from django.views import View
from django.shortcuts import render,redirect

from blog import forms
from utils import page
from blog.models import Blog


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
