from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from utils.models import CommonModel
from accounts.models import User
from order.choices import OrderStatus, OrderTypes


class Order(CommonModel):
    """ 订单 """
    sn = models.CharField(verbose_name='订单编号', max_length=32)
    user = models.ForeignKey(verbose_name='关联用户', to=User, related_name='orders', on_delete=models.CASCADE)
    buy_count = models.IntegerField(verbose_name='购买数量', default=1)
    buy_amount = models.FloatField(verbose_name='总价')

    to_user = models.CharField(verbose_name='收货人', max_length=32)
    to_area = models.CharField(verbose_name='省市区', max_length=32, default='')
    to_address = models.CharField(verbose_name='详细地址', max_length=256, default='')
    to_phone = models.CharField(verbose_name='手机号码', max_length=32)

    remark = models.CharField(verbose_name='备注', max_length=255, null=True, blank=True)

    # 快递信息
    express_type = models.CharField(verbose_name='快递', max_length=32, null=True, blank=True)
    express_no = models.CharField(verbose_name='单号', max_length=32, null=True, blank=True)

    status = models.SmallIntegerField(
        verbose_name='订单状态',
        choices=OrderStatus.choices,
        default=OrderStatus.SUBMIT
    )
    types = models.SmallIntegerField(
        verbose_name='',
        choices=OrderTypes.choices,
        default=OrderTypes.SIGHT_TICKET
    )

    class Meta:
        db_table = 'order'
        ordering = ['id']


class OrderItem(CommonModel):
    """ 订单明细 """
    user = models.ForeignKey(verbose_name='关联用户', to=User, related_name='order_items', on_delete=models.CASCADE)
    order = models.ForeignKey(verbose_name='关联订单', to=Order, related_name='order_items', on_delete=models.CASCADE)
    # 商品快照
    flash_name = models.CharField(verbose_name='商品名称', max_length=128)
    flash_img = models.ImageField(verbose_name='商品的主图')
    flash_price = models.FloatField(verbose_name='兑换价格')
    flash_origin_price = models.FloatField(verbose_name='原价')
    flash_discount = models.FloatField(verbose_name='折扣')

    count = models.PositiveIntegerField(verbose_name='购买数量')
    amount = models.FloatField(verbose_name='总额')

    status = models.SmallIntegerField(
        verbose_name='状态',
        choices=OrderStatus.choices,
        default=OrderStatus.SUBMIT
    )
    remark = models.CharField(verbose_name='备注', max_length=255, null=True, blank=True)

    # 复合关联
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'order_item'


class Payment(CommonModel):
    """ 支付凭证 """
    user = models.ForeignKey(verbose_name='关联用户', to=User, related_name='payments', on_delete=models.CASCADE)
    order = models.ForeignKey(verbose_name='关联订单', to=Order, related_name='payments', on_delete=models.CASCADE)
    amount = models.FloatField(verbose_name='金额', help_text='支付实际的金额')
    sn = models.CharField(verbose_name='流水号', max_length=32)
    third_sn = models.CharField(verbose_name='第三方单号', max_length=128, null=True, blank=True)

    status = models.SmallIntegerField(verbose_name='支付状态', default=1)

    meta = models.CharField(verbose_name='其他数据', max_length=128, null=True, blank=True)
    remark = models.CharField(verbose_name='备注信息', max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'order_payment'
