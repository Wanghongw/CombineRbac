# -*- coding:utf-8 -*-
from django.conf.urls import url

from blog.views import auth,blog,article

urlpatterns = [


    url(r'^login/$', auth.login,name='login'),
    url(r'^index/$', auth.index,name='index'),


    url(r'^blog_show/', blog.blog_show,name='blog_show'),
    url(r'^blog_add/', blog.blog_add,name='blog_add'),
    url(r'^blog_edit/(?P<pk>\d+)/$', blog.BlogEdit.as_view(),name='blog_edit'),
    url(r'^blog_del/(?P<pk>\d+)/$', blog.blog_del,name='blog_del'),

    url(r'^article_show/', article.article_show,name='article_show'),
    url(r'^article_add/', article.article_add,name='article_add'),
    url(r'^article_edit/(?P<pk>\d+)/$', article.article_edit,name='article_edit'),
    url(r'^article_del/(?P<pk>\d+)/$', article.article_del,name='article_del'),

]
