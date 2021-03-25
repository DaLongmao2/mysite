from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class LikeCount(models.Model):  
    # 点赞数
    liked_num = models.IntegerField(default=0)

    # 指向 ContentType 的模型
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    # 记录对应模型的 主键
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'LikeCount'


class LikeRecord(models.Model):
    # 点赞人
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # 点赞时间
    liked_time = models.DateTimeField(auto_now_add=True)

    # 指向 ContentType 的模型
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    # 记录对应模型的 主键
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'LikeRecord'
