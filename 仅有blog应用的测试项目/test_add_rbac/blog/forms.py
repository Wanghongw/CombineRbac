# -*- coding:utf-8 -*-
from django import forms
from django.forms import widgets

from blog import models


class BlogModelForm(forms.ModelForm):
    class Meta:
        model = models.Blog

        fields = '__all__'

        error_messages = {
            'name': {
                'required': '这个字段不能为空',
            },
            'user': {
                'required': '这个字段不能为空！',
            }
        }

    def __init__(self,*args,**kwargs):

        super(BlogModelForm, self).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':'form-control',
            })



class ArticleModelForm(forms.ModelForm):

    class Meta:
        model = models.Article

        fields = '__all__'

        exclude = ['create_at']

        error_messages = {
            'title': {
                'required': '这个字段不能为空',
            },
            'category': {
                'required': '这个字段不能为空！',
            },
            'blog': {
                'required': '这个字段不能为空',
            },
            'content': {
                'required': '这个字段不能为空',
            },

        }

    def __init__(self,*args,**kwargs):

        super(ArticleModelForm, self).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':'form-control',
            })


