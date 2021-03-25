from django.contrib.auth.models import User
from django.db import models
# from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum
from read_statistics.models import ReadNumExpandMethod, ReadDetail


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

    class Meta:
        db_table = 'BlogType'

# 博客
class Blog(models.Model, ReadNumExpandMethod):
    # 使用 django 自带用户系统
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # content = RichTextField()
    content = RichTextUploadingField()
    read_details = GenericRelation(ReadDetail)
    create_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    # 第一种
    # def blog_read_num(self):
    #     try:
    #         return self.blogreadnum.read_num
    #     except:
    #         return 0

    def __str__(self):
        return "<Blog: %s >" % self.title

    class Meta:
        db_table = 'Blog'
        # 排序
        ordering = ['-create_time']


# 阅读数量 第一中解决方案
# class BlogReadNum(models.Model):
#     read_num = models.IntegerField(default=0)
#     blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)
#
#     def __str__(self):
#         return "<BlogReadNum: %s >" % self.read_num
#
#     class Meta:
#         db_table = 'BlogReadNum'

# 使用系统自带的 ContentType 的
