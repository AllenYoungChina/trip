from django.urls import path

from . import views

urlpatterns = [
    # 统计报表
    path('', views.index, name='index')
]
