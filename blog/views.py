from django.contrib.contenttypes.models import ContentType

from comment.models import Comment
from read_statistics.utils import read_statistics_once_read
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Blog, BlogType
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from comment.forms import CommentForm


# 发帖  删帖   登录  注册  评论  阅读量   热门帖子  收藏
from read_statistics.models import ReadNum


def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.BLOG_PAGES_NUM)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number
    # 　分页列表　拼接　判断
    page_range_list = list(range(max(currentr_page_num - 1, 1), currentr_page_num)) + \
                      list(range(currentr_page_num, min(currentr_page_num + 1, paginator.num_pages) + 1))
    # 添加省略标记
    if page_range_list[0] - 1 >= 2:
        page_range_list.insert(0, '...')
    if paginator.num_pages - page_range_list[-1] >= 2:
        page_range_list.append('...')
    # 添加首页 和 尾页
    if page_range_list[0] != 1:
        page_range_list.insert(0, 1)
    if page_range_list[-1] != paginator.num_pages:
        page_range_list.append(paginator.num_pages)
    # blogs_types = BlogType.objects.all()
    # blogs_types_all_list = []
    # for blog_type in blogs_types:
    #     blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
    #     blogs_types_all_list.append(blog_type)

    blog_dates = Blog.objects.dates('create_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_data in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_data.year, create_time__month=blog_data.month).count()
        blog_dates_dict[blog_data] = blog_count

    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['page_range_list'] = page_range_list
    context['blog_dates'] = blog_dates_dict
    return context


# 博客列表
def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


# 博客 类型 分类
def blog_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    # 查询所有该分类的文章
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_with_type.html', context)


# 博客 时间 分类
def blogs_with_date(request, year, month):
    # 查询所有该分类的文章
    blogs_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blogs_with_date.html', context)


# 博客内容
def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    # 获取 ContentType 表中对应的 blog 对象
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, root=None)
    # if not request.COOKIES.get('blog_%s_read' % blog_pk):
        # 第一种方法
        # if BlogReadNum.objects.filter(blog=blog).count():
        #     readnum = BlogReadNum.objects.get(blog=blog)
        # else:
        #     readnum = BlogReadNum(blog=blog)
        # readnum.read_num += 1
        # readnum.save()
    # response.set_cookie('blog_%s_read' % blog_pk, 'true', expires=datetime)
    # 阅读数量
    read_cookie = read_statistics_once_read(request, blog)
    # 上一页
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    # 下一页
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    # Blog
    context['blog'] = blog

    # 返回评论内容
    context['comments'] = comments
    # 返回 CommentForm 实例化表单
    context['comments_form'] = CommentForm(initial={'content_type': blog_content_type.model, 'object_id': blog_pk, 'reply_comment_id': 0})
    response = render(request, "blog/blog_detail.html", context)
    # max_age 过期时间 多少秒之后
    # expires 指定时间过期
    response.set_cookie(read_cookie, 'true')
    return response

