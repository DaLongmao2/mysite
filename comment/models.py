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
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='comments')

    # 下一级回复 记录某条回复的最顶级是谁？
    root = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING, related_name='root_comment')
    # 回复的评论 的 ID？
    parent = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING, related_name='parent_comment')
    # 回复谁的 ？ 可以通过 parent 进行反查 但是太麻烦了
    reply_to = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name='replies')

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'Comment'
        ordering = ['-comment_time']

