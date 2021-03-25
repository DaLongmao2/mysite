from django.db.models.fields import exceptions
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

# 封装
class ReadNumExpandMethod():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0



class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)

    # 指向 ContentType 的模型
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    # 记录对应模型的 主键
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')



class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)

    # 指向 ContentType 的模型
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    # 记录对应模型的 主键
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

