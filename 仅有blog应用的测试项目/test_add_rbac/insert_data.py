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

    category_choices = [4,2,3]
    dates = ['2011-12-12','2012-3-5','2018-12-5']
    blog_lst = [1,2,3]

    lst = []
    # 插入5个数据
    for i in range(7):

        random_title = ''.join(random.choices(string.ascii_letters, k=5))

        random_category = random.choice(category_choices)

        random_content = ''.join(random.choices(string.ascii_letters, k=9))

        random_date = random.choice(dates)

        random_blog = random.choice(blog_lst)

        customer_obj = models.Article(title=random_title,category=random_category,content=random_content,create_at=random_date,blog_id=random_blog)
        lst.append(customer_obj)

    models.Article.objects.bulk_create(lst)
