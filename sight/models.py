from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from utils.models import CommonModel
from system.models import ImageRelated
from .choices import TicketTypes, EntryWay, TicketStatus
from accounts.models import User


class Sight(CommonModel):
    """ 景点基础信息 """
    name = models.CharField(verbose_name='名称', max_length=64)
    desc = models.CharField(verbose_name='描述', max_length=256)
    main_img = models.ImageField(verbose_name='主图', max_length=256, upload_to='%Y%m/sight')
    banner_img = models.ImageField(verbose_name='详情主图', max_length=256, upload_to='%Y%m/sight')
    # content = models.TextField(verbose_name='详细')
    content = RichTextField(verbose_name='详细')
    score = models.FloatField(verbose_name='评分', default=5)
    min_price = models.FloatField(verbose_name='最低价格', default=0)
    province = models.CharField(verbose_name='省份', max_length=32)
    city = models.CharField(verbose_name='城市', max_length=32)
    area = models.CharField(verbose_name='区/县', max_length=32, null=True, blank=True)
    town = models.CharField(verbose_name='乡/镇', max_length=32, null=True, blank=True)

    is_top = models.BooleanField(verbose_name='是否精选', default=False)
    is_hot = models.BooleanField(verbose_name='是否热门', default=False)

    images = GenericRelation(verbose_name='关联图片', to=ImageRelated, related_query_name='rel_sight_images')

    class Meta:
        db_table = 'sight'
        ordering = ['-updated_at']
        verbose_name = '景点信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @property
    def comment_count(self):
        """ 评论总数 """
        return self.comments.filter(is_valid=True).count()

    @property
    def image_count(self):
        """ 景点图片数量 """
        return self.images.filter(is_valid=True).count()


class Info(models.Model):
    """ 景点详情 """
    sight = models.OneToOneField(verbose_name='景点', to=Sight, on_delete=models.CASCADE)
    entry_explain = RichTextField(verbose_name='入园参考', max_length=1024, null=True, blank=True)
    play_way = RichTextField(verbose_name='特色玩法', null=True, blank=True)
    tips = RichTextField(verbose_name='温馨提示', null=True, blank=True)
    traffic = RichTextField(verbose_name='交通到达', null=True, blank=True)

    class Meta:
        db_table = 'sight_info'
        verbose_name = '景点详情'
        verbose_name_plural = verbose_name


class Ticket(CommonModel):
    """ 门票 """
    sight = models.ForeignKey(verbose_name='景点', to=Sight, related_name='tickets', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='名称', max_length=128)
    desc = models.CharField(verbose_name='描述', max_length=64, null=True, blank=True)
    types = models.SmallIntegerField(
        verbose_name='类型',
        choices=TicketTypes.choices,
        default=TicketTypes.ADULT,
        help_text='默认为成人票',
    )
    price = models.FloatField(verbose_name='价格（原价）')
    discount = models.FloatField(verbose_name='折扣', default=10)
    total_stock = models.PositiveIntegerField(verbose_name='总库存', default=0)
    remain_stock = models.PositiveIntegerField(verbose_name='剩余库存', default=0)
    expire_date = models.IntegerField(verbose_name='有效期', default=1)
    return_policy = models.CharField(verbose_name='退改政策', max_length=64, default='条件退')
    has_invoice = models.BooleanField(verbose_name='是否提供发票', default=True)
    entry_way = models.SmallIntegerField(
        verbose_name='入园方式',
        choices=EntryWay.choices,
        default=EntryWay.BY_TICKET,
    )
    tips = RichTextField(verbose_name='预定须知', null=True, blank=True)
    remark = RichTextField(verbose_name='其他说明', null=True, blank=True)
    status = models.SmallIntegerField(
        verbose_name='状态',
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN
    )

    class Meta:
        db_table = 'sight_ticket'
        ordering = ['id']
        verbose_name = '景点门票'
        verbose_name_plural = verbose_name

    @property
    def sell_price(self):
        """ 销售价=原价*折扣 """
        return self.price * self.discount / 10


class Comment(CommonModel):
    """ 评论及回复 """
    user = models.ForeignKey(verbose_name='评论用户', to=User, related_name='comments', on_delete=models.CASCADE)
    sight = models.ForeignKey(verbose_name='景点', to=Sight, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='评论内容', null=True, blank=True)
    is_top = models.BooleanField(verbose_name='是否置顶', default=False)
    love_count = models.IntegerField(verbose_name='点赞次数', default=0)
    score = models.FloatField(verbose_name='评分', default=5)

    ip_address = models.CharField('IP地址', blank=True, null=True, max_length=64)
    is_public = models.SmallIntegerField('是否公开', default=1)
    reply = models.ForeignKey(
        'self', blank=True, null=True,
        related_name='reply_comment',
        verbose_name='回复',
        on_delete=models.CASCADE)

    images = GenericRelation(ImageRelated,
                             verbose_name='关联的图片',
                             related_query_name="rel_comment_images")

    class Meta:
        db_table = 'sight_comment'
        ordering = ['-love_count', '-created_at']
        verbose_name = '景点评论'
        verbose_name_plural = verbose_name
