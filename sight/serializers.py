from utils.serializers import BaseListPageSerializer, BaseSerializer
from system.serializers import BaseImageSerializer


class SightListSerializer(BaseListPageSerializer):
    """ 景点列表序列化 """
    def get_obj(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'main_img': obj.main_img.url,
            'score': obj.score,
            'province': obj.province,
            'min_price': obj.min_price,
            'city': obj.city,
            'comment_count': obj.comment_count,
        }


class SightDetailSerializer(BaseSerializer):
    """ 景点详情序列化 """
    def to_dict(self):
        obj = self.obj
        return {
            'id': obj.id,
            'name': obj.name,
            'desc': obj.desc,
            'img': obj.banner_img.url,
            'content': obj.content,
            'score': obj.score,
            'province': obj.province,
            'area': obj.area,
            'town': obj.town,
            'min_price': obj.min_price,
            'city': obj.city,
            'comment_count': obj.comment_count,
            'image_count': obj.image_count,
        }


class CommentListSerializer(BaseListPageSerializer):
    """ 评论列表序列化 """
    def get_obj(self, obj):
        user = obj.user
        images = []
        for image in obj.images.filter(is_valid=True):
            # 使用图片序列化类序列化图片信息的返回
            images.append(BaseImageSerializer(obj=image).to_dict())
        return {
            'user': {
                'pk': user.pk,
                'nickname': user.nickname,
            },
            'pk': obj.pk,
            'content': obj.content,
            'is_top': obj.is_top,
            'love_count': obj.love_count,
            'score': obj.score,
            'is_public': obj.is_public,
            # images是一个列表，元素为每个图片信息组成的字典
            'images': images,
            # 将Python的Datetime类型的数据转化为字符串
            'created_at': obj.created_at.strftime('%Y-%m-%d')
        }


class TicketListSerializer(BaseListPageSerializer):
    """ 门票列表序列化 """
    def get_obj(self, obj):
        return {
            'pk': obj.pk,
            'name': obj.name,
            'desc': obj.desc,
            'types': obj.types,
            'price': obj.price,
            'sell_price': obj.sell_price,
            'total_stock': obj.total_stock,
            'remain_stock': obj.remain_stock,
        }


class SightInfoSerializer(BaseSerializer):
    """ 景点介绍序列化 """
    def to_dict(self):
        obj = self.obj
        return {
            'pk': obj.sight.pk,  # 景点的ID
            'entry_explain': obj.entry_explain,
            'play_way': obj.play_way,
            'tips': obj.tips,
            'traffic': obj.traffic,
        }


class TicketDetailSerializer(BaseSerializer):
    """ 门票详情序列化 """
    def to_dict(self):
        obj = self.obj
        return {
            'pk': obj.pk,
            'name': obj.name,
            'desc': obj.desc,
            'types': obj.types,
            'price': obj.price,
            'sell_price': obj.sell_price,
            'discount': obj.discount,
            'expire_date': obj.expire_date,
            'return_policy': obj.return_policy,
            'has_invoice': obj.has_invoice,
            'entry_way': obj.get_entry_way_display(),
            'tips': obj.tips,
            'remark': obj.remark,
        }
