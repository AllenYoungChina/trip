from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from utils.models import CommonModel

from accounts.models import User


class Slider(CommonModel):
    """ 轮播图 """
    name = models.CharField(verbose_name='名称', max_length=32)
    desc = models.CharField(verbose_name='描述', max_length=100, null=True, blank=True)
    types = models.SmallIntegerField(verbose_name='展示位置', default=10)
    img = models.ImageField(verbose_name='图片地址', max_length=255, upload_to='%Y%m/slider')
    reorder = models.SmallIntegerField(verbose_name='排序字段', default=0, help_text='数字越大越靠前')
    start_time = models.DateTimeField(verbose_name='生效起始时间', null=True, blank=True)
    end_time = models.DateTimeField(verbose_name='生效结束时间', null=True, blank=True)
    target_url = models.CharField(verbose_name='跳转地址', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'system_slider'
        ordering = ['-reorder']


class ImageRelated(CommonModel):
    """ 图片关联 """
    img = models.ImageField(verbose_name='图片', max_length=256, upload_to='%Y%m/file')
    summary = models.CharField(verbose_name='图片说明', max_length=32, blank=True, null=True)
    user = models.ForeignKey(verbose_name='上传用户', to=User, null=True, on_delete=models.CASCADE)
    content_type = models.ForeignKey(verbose_name='图片类型', to=ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField(verbose_name='图片ID')
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    class Meta:
        db_table = 'system_image_related'
