import datetime
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

from blog.models import Blog
from read_statistics.models import ReadNum, ReadDetail
from django.utils import timezone
from django.db.models import Sum

# def read_statistics_once_read(request, obj):
#     """
#     是否 增加阅读数量
#     :param request: request
#     :param obj: Blog obj
#     :return: 返回生成的 key 并设置 Cookies 以便下次的校验
#     """
#     ct = ContentType.objects.get_for_model(obj)
#     key = "{}_{}_read".format(ct.model, obj.pk)
#     # 如果 COOKIES 不存在 则视为一次有效的点赞 则进行 阅读数量的 增加 记录 操作
#     # 如果 COOKIES 存在 则视为重复访问 直接返回 COOKIE
#     if not request.COOKIES.get(key):
#         if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
#             # 存在记录 直接获取 Blog 对应的数据对象
#             readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
#             print(readnum)
#         else:
#             # 不存在Blog数据对象 直接创建Blog数据对象
#             readnum = ReadNum(content_type=ct, object_id=obj.pk)
#         # 阅读数量 + 1
#         readnum.read_num += 1
#         readnum.save()
#
#         # 获取当前时间  只取日期
#         date = timezone.now().date()
#         # 判断 是否存在
#         # 存在 则 直接获取
#         # 不存在 则 创建
#         if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
#             readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date)
#         else:
#             readDetail = ReadDetail(content_type=ct, object_id=obj.pk, date=date)
#         # 对应 阅读数量 + 1
#         readDetail.read_num += 1
#         readDetail.save()
#     return key

# 使用 get_or_create 函数 简洁代码

today = timezone.now().date()


# 记录阅读数量
def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "{}_{}_read".format(ct.model, obj.pk)
    if not request.COOKIES.get(key):
        # get_or_create 返回一个元祖 没有则创建
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()


        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key


# 返回近七天的阅读量
def get_seven_days_read_data(content_type):
    read_nums = []
    dates = []
    # 获取 7 天的值
    for i in range(6, -1, -1):
        # 日期差量
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        # 聚合 计算
        # 返回一个 字典 {'read_num_sum' : 数值}
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums


# 今天 阅读最高的
def get_today_hot_data(content_type):
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')[0:7]
    return read_details

# 昨天 阅读最高的
def get_yesterday_hot_date(content_type):
    # 减去一天差量 获取到昨天
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')[0:8]
    return read_details


# 七天内 阅读最高的
def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date)\
        .values('id', 'title')\
        .annotate(read_num_sum=Sum('read_details__read_num'))\
        .order_by('-read_num_sum')[0:7]


    # 获取 7天热门阅读的的缓存数据
    host_blogs_for_7_days = cache.get('host_blogs_for_7_days')
    if host_blogs_for_7_days is None:
        host_blogs_for_7_days = blogs
        cache.set('host_blogs_for_7_days', host_blogs_for_7_days, 3600)
        print('计算中...')
    else:
        print('使用缓存了')

    print(host_blogs_for_7_days)


    return host_blogs_for_7_days