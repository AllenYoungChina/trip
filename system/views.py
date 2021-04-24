import json

from django import http
from django.core.cache import cache
from django.views.generic import FormView

from utils.response import ServerErrorJsonResponse, BadRequestJsonResponse
from .models import Slider
from .forms import SendSmsCodeForm


def slider_list(request):
    """ 轮播图接口 """
    data = {
        'meta': {},
        'objects': [],
    }
    queryset = Slider.objects.filter(is_valid=True)
    for item in queryset:
        data['objects'].append({
            'id': item.id,
            'name': item.name,
            'img_url': item.img.url,
            'target_url': item.target_url,
        })
    return http.JsonResponse(data=data)


def cache_set(request):
    """ 缓存写入 """
    pass


def cache_get(request):
    """ 缓存读取 """
    pass


class SmsCodeView(FormView):
    """ 发送短信验证码 """
    form_class = SendSmsCodeForm

    def form_valid(self, form):
        """ 表单通过验证时调用 """
        data = form.send_sms_code()
        if data is not None:
            return http.JsonResponse(data=data, status=201)
        else:
            return ServerErrorJsonResponse()

    def form_invalid(self, form):
        """ 表单未通过验证时调用 """
        err_list = json.loads(form.errors.as_json())
        return BadRequestJsonResponse(err_list=err_list)
