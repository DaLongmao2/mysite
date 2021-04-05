from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from blog.models import Blog, BlogType
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_date, \
    get_7_days_hot_blogs
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegForm


def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    context['read_nums'] = read_nums
    context['dates'] = dates
    context['blogs'] = Blog.objects.all()
    context['blog_types'] = BlogType.objects.all()
    context['today_hot_dat'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_dat'] = get_yesterday_hot_date(blog_content_type)
    context['hot_data_for_7_days'] = get_7_days_hot_blogs()
    return render(request, "home.html", context)


def login(request):
    # username = request.POST.get('username', '')
    # password = request.POST.get('password', '')
    # # 使用系统自带用户系统
    # # 使用authenticate方法进行验证
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    # user = auth.authenticate(request, username=username, password=password)
    # if user is not None:
    #     auth.login(request, user)
    #     return redirect(referer)
    # else:
    #     return render(request, 'error.html', {'message': '用户名或密码不正确！'})
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登录
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('next_to'), reverse('home'))


def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)