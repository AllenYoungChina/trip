from django.db import models


class CommonModel(models.Model):
    """ 公共模型类 """
    is_valid = models.BooleanField(verbose_name='是否有效', default=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        # 设置当前模型类为抽象类
        abstract = True
