from django.shortcuts import render,redirect

from utils import page
from blog import forms
from blog.models import Article



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
