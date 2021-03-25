from django.shortcuts import render, redirect
from blog.models import Blog
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_date, \
    get_7_days_hot_blogs
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.urls import reverse


def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_dat'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_dat'] = get_yesterday_hot_date(blog_content_type)
    context['hot_data_for_7_days'] = get_7_days_hot_blogs()
    return render(request, "home.html", context)


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    # 使用系统自带用户系统
    # 使用authenticate方法进行验证
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message': '用户名或密码不正确！'})
