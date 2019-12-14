# -*- coding:utf-8 -*-
#自定义分页
#官方推荐,页码数为奇数
class PageNation:
    def __init__(self,base_url,current_page_num,total_counts,request,per_page_counts=10,page_number=5,):
        '''
        :param base_url:   分页展示信息的基础路径
        :param current_page_num:  当前页页码
        :param total_counts:  总的数据量
        :param per_page_counts:  每页展示的数据量
        :param page_number:  显示页码数
        '''
        self.base_url = base_url
        self.current_page_num = current_page_num
        self.total_counts = total_counts
        self.per_page_counts = per_page_counts
        self.page_number = page_number
        self.request = request
        try:
            self.current_page_num = int(self.current_page_num)

        except Exception:
            self.current_page_num = 1

        half_page_range = self.page_number // 2
        # 计算总页数~~divmod方法返回商跟余数！
        self.page_number_count, a = divmod(self.total_counts, self.per_page_counts)
        if self.current_page_num < 1:
            self.current_page_num = 1
        #有余数的话，说明还有一页有遗留的数据，需要给总的页数加1
        if a:
            self.page_number_count += 1

        ######################################################## 当前页码为0的话~会有问题，下面这样的标记有做处理！
        if self.current_page_num > self.page_number_count:
            self.current_page_num = self.page_number_count

        if self.page_number_count <= self.page_number:
            self.page_start = 1
            self.page_end = self.page_number_count
        else:
            # 当前页小于定制的页数的一半的话~就是前面的几页，前面只显示到第一条数据就好了！
            if self.current_page_num <= half_page_range:
                self.page_start = 1
                self.page_end = page_number
            # 当前页大于定制的页数的一半的话~就是后面的几页，后面顶头了，最后只显示最后一条的数据就好了！
            elif self.current_page_num + half_page_range >= self.page_number_count:
                # 起始页码等于~总页数减去显示的页码数+1~~不加1的话会多添加一个标签!
                self.page_start = self.page_number_count - self.page_number + 1
                self.page_end = self.page_number_count
            else:
                self.page_start = self.current_page_num - half_page_range
                self.page_end = self.current_page_num + half_page_range

        ## 下面的逻辑是：搜索时保存搜索条件的逻辑！！！
        ## 后面的 循环生成html标签 会用到urlencode()方法！注意后面格式化标签字符串的方法！
        import copy
        # request.GET['page'] = 2 #This QueryDict instance is immutable
        from django.http.request import QueryDict
        # print(type(request))
        # print(request)
        # print(request.GET)
        # request.GET方法返回的是一个QueryDict类型的数据，
        # 它有一个urlencode()方法，可以将它里面的键值对转换成 ?condition=qq&wd=1&page=3的格式！
        # 这样的格式发送GET请求后浏览器能认识

        # 深拷贝后可以改了，避免浏览器请求的地址堆叠
        # 因为深拷贝调用了__deepcopy__方法，看QueryDict的源码可知这个方法把不可变的那个属性又改成了True使之可变
        # （一开始_mutable为True，init方法mutable设置成False......这个过程得知道！）
        self.params = copy.deepcopy(self.request.GET)
        # params['page'] = current_page_num
        # query_str = params.urlencode()


    #数据切片依据,起始位置
    @property
    def start_num(self):
        ################################################ 这里有个问题：如果没有数据的话,必须给 self.current_page_num = 1~~
        ################################################
        if self.current_page_num == 0:
            self.current_page_num = 1
        start_num = (self.current_page_num - 1) * self.per_page_counts
        return start_num

    #数据切片依据,终止位置
    @property
    def end_num(self):
        end_num = self.current_page_num * self.per_page_counts
        return end_num

    # 拼接HTMl标签
    def page_html(self):
        tab_html = ''
        tab_html += '<nav aria-label="Page navigation" class="pull-right"><ul class="pagination">'
        # 首页
        self.params['page'] = 1
        showye = '<li><a href="{0}?{1}" aria-label="Previous" ><span aria-hidden="true">首页</span></a></li>'.format(
            self.base_url, self.params.urlencode())
        tab_html += showye
        # 上一页
        if self.current_page_num == 1:
            previous_page = '<li disabled><a href="#" aria-label="Previous" ><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            previous_page = '<li><a href="{0}?page={1}" aria-label="Previous" ><span aria-hidden="true">&laquo;</span></a></li>'.format(
                self.base_url, self.current_page_num - 1)
        tab_html += previous_page

        ## 循环生成页码标签！
        for i in range(self.page_start, self.page_end + 1):
            self.params['page'] = i

            if self.current_page_num == i:

                one_tag = '<li class="active"><a href="{0}?{2}">{1}</a></li>'.format(self.base_url, i,self.params.urlencode()) #?condition=qq&wd=1&page=3
            else:
                one_tag = '<li><a href="{0}?{2}">{1}</a></li>'.format(self.base_url, i,self.params.urlencode())
            tab_html += one_tag

        # 下一页
        if self.current_page_num == self.page_number_count:
            next_page = '<li disabled><a href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            next_page = '<li><a href="{0}?page={1}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(self.base_url, self.current_page_num + 1)
        tab_html += next_page
        # 尾页
        self.params['page'] = self.page_number_count
        weiye = '<li><a href="{0}?{1}" aria-label="Previous" ><span aria-hidden="true">尾页</span></a></li>'.format(
            self.base_url, self.params.urlencode())
        tab_html += weiye

        tab_html += '</ul></nav>'

        return tab_html
