from django.db import models



class UserInfo(models.Model):
    """
    用户信息
    """
    username = models.CharField(max_length=33,verbose_name='用户名',unique=True)
    password = models.CharField(max_length=33,verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱',blank=True,null=True)


class Blog(models.Model):
    """
    个人博客
    """
    name = models.CharField(max_length=64,verbose_name='博客名称',unique=True)
    user = models.CharField(max_length=64,verbose_name='用户名',unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    文章表
    """
    category_choices = (
        (1,'未分类'),
        (2,'技术'),
        (3,'杂谈'),
        (4,'感悟'),
    )

    title = models.CharField('文章标题',max_length=128,unique=True)
    category = models.IntegerField('文章分类',choices=category_choices,default=1)
    content = models.TextField('文章内容')
    create_at = models.DateTimeField(auto_now_add=True,blank=True)

    blog = models.ForeignKey(to=Blog,verbose_name='所属博客')

    def __str__(self):
        return self.title
