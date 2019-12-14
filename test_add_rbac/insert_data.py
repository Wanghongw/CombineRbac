# -*- coding:utf-8 -*-
import os
import random
import string

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_add_rbac.settings")
    import django
    django.setup()

    # 插入数据
    from blog import models

    # 往博客表中插入数据
    blog_lst = ['火之国','水之国','风之国','雷之国','土之国']
    name_lst = ['whw','wanghw','naruto','sasuke','madara']

    b_lst = []
    for bid,blog in enumerate(blog_lst):
        blog_obj = models.Blog(name=blog,user=name_lst[bid])
        b_lst.append(blog_obj)
    models.Blog.objects.bulk_create(b_lst)

    # 往文章表中插入数据
    category_choices = [4,2,3]
    dates = ['2011-12-12','2012-3-5','2018-12-5']
    blog_id_lst = [1,2,3,4,5]
    lst = []
    # 插入50个数据
    for i in range(50):
        random_title = ''.join(random.choices(string.ascii_letters, k=5))
        random_category = random.choice(category_choices)
        random_content = ''.join(random.choices(string.ascii_letters, k=9))
        random_date = random.choice(dates)
        random_blog = random.choice(blog_id_lst)

        customer_obj = models.Article(title=random_title,category=random_category,content=random_content,create_at=random_date,blog_id=random_blog)
        lst.append(customer_obj)

    models.Article.objects.bulk_create(lst)
