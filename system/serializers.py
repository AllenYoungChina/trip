from utils.serializers import BaseSerializer


class BaseImageSerializer(BaseSerializer):
    """ 序列化图片信息返回 """
    def to_dict(self):
        image = self.obj
        return {
            'img': image.img.url,
            'summary': image.summary
        }
