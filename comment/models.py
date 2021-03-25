from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# 评论 Model
class Comment(models.Model):
    # 指向 ContentType 的模型
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    # 记录对应模型的 主键
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 评论内容
    text = models.TextField()
    # 评论时间
    comment_time = models.DateTimeField(auto_now_add=True)
    # 评论人
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Comment'
        ordering = ['-comment_time']