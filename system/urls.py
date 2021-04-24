from django.urls import path

from .views import slider_list, cache_set, cache_get, SmsCodeView

urlpatterns = [
    path('slider/list/', slider_list, name='slider_list'),
    path('cache/set/', cache_set, name='cache_set'),
    path('cache/get/', cache_get, name='cache_get'),
    # 发送验证码
    path('send/sms/', SmsCodeView.as_view(), name='send_sms'),
]
