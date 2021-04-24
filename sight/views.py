import json

from django import http
from django.core.cache import cache
from django.views.generic import ListView, DetailView
from django.db.models import Q

from utils import constants
from .models import Sight, Comment, Ticket, Info
from . import serializers
from utils.response import NotFoundJsonResponse


class SightListView(ListView):
    """ 2.1 景点列表接口 """
    paginate_by = 5  # 分页，每页放5条数据

    def get_queryset(self):
        """ 重写查询方法 """
        query = Q(is_valid=True)
        # 1. 热门景点
        is_hot = self.request.GET.get('is_hot', None)
        if is_hot:
            query = Q(is_hot=True) & query
        # 2. 精选景点
        is_top = self.request.GET.get('is_top', None)
        if is_top:
            query = Q(is_top=True) & query
        # 3. 按景点名称搜索
        name = self.request.GET.get('name', None)
        if name:
            query = Q(name__icontains=name) & query
        queryset = Sight.objects.filter(query)
        return queryset

    def get_paginate_by(self, queryset):
        """ 从前端控制每页数据条数 """
        page_size = self.request.GET.get('limit', None)
        return page_size or self.paginate_by

    def render_to_response(self, context, **response_kwargs):
        """ 重写返回方式（默认返回模板） """
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.SightListSerializer(page_obj=page_obj).to_dict()
            return http.JsonResponse(data=data)
        else:
            return NotFoundJsonResponse()


class SightListCacheView(ListView):
    """ 2.1 景点列表接口（从redis缓存获取数据） """
    paginate_by = 20  # 分页，每页放5条数据

    def get_queryset(self):
        """ 重写查询方法 """
        query = Q(is_valid=True)
        # 1. 热门景点
        is_hot = self.request.GET.get('is_hot', None)
        if is_hot:
            query = Q(is_hot=True) & query
        # 2. 精选景点
        is_top = self.request.GET.get('is_top', None)
        if is_top:
            query = Q(is_top=True) & query
        queryset = Sight.objects.filter(query)
        return queryset

    def get_paginate_by(self, queryset):
        """ 从前端控制每页数据条数 """
        page_size = self.request.GET.get('limit', None)
        return page_size or self.paginate_by

    def render_to_response(self, context, **response_kwargs):
        """ 重写返回方式（默认返回模板） """
        query = Q(is_valid=True)
        # 1. 热门景点
        is_hot = self.request.GET.get('is_hot', None)
        if is_hot:
            try:
                data = cache.get(constants.INDEX_SIGHT_HOT_KEY)
                if data:
                    return http.JsonResponse(json.loads(data))
            except Exception as e:
                print(e)
        # 2. 精选景点
        is_top = self.request.GET.get('is_top', None)
        if is_top:
            try:
                data = cache.get(constants.INDEX_SIGHT_TOP_KEY)
                if data:
                    return http.JsonResponse(json.loads(data))
            except Exception as e:
                print(e)

        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.SightListSerializer(page_obj=page_obj).to_dict()
            return http.JsonResponse(data=data)
        else:
            return NotFoundJsonResponse()


class SightDetailView(DetailView):
    """ 2.2 景点详情接口 """
    def get_queryset(self):
        return Sight.objects.all()

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['object']
        if page_obj is not None:
            if page_obj.is_valid is False:
                return NotFoundJsonResponse
            data = serializers.SightDetailSerializer(page_obj).to_dict()
            return http.JsonResponse(data=data)
        return NotFoundJsonResponse()


class SightCommentListView(ListView):
    """ 2.3 景点评论列表接口 """
    paginate_by = 10

    def get_queryset(self):
        # 根据景点ID查询景点
        sight_id = self.kwargs.get('pk', None)
        sight = Sight.objects.filter(pk=sight_id, is_valid=True).first()
        if sight:
            return sight.comments.filter(is_valid=True)
        # 如果景点不存在，返回一个空的查询结果集
        return Comment.objects.none()

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.CommentListSerializer(page_obj=page_obj).to_dict()
            return http.JsonResponse(data=data)
        return NotFoundJsonResponse()


class SightTicketListView(ListView):
    """ 2.4 景点门票列表接口 """
    paginate_by = 10

    def get_queryset(self):
        # 根据景点ID查询景点
        sight_id = self.kwargs.get('pk', None)
        return Ticket.objects.filter(is_valid=True, sight__id=sight_id)

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.TicketListSerializer(page_obj=page_obj).to_dict()
            return http.JsonResponse(data=data)
        return NotFoundJsonResponse()


class SightInfoDetailView(DetailView):
    """ 2.5 景点介绍 """
    pk_url_kwarg = None
    slug_url_kwarg = 'pk'
    # URL中的pk对应到ORM中的字段名
    slug_field = 'sight__pk'

    def get_queryset(self):
        return Info.objects.all()

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['object']
        if page_obj is not None:
            data = serializers.SightInfoSerializer(page_obj).to_dict()
            return http.JsonResponse(data=data)
        return NotFoundJsonResponse()


class TicketDetailView(DetailView):
    """ 2.6 门票详情 """
    def get_queryset(self):
        return Ticket.objects.filter(is_valid=True)

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['object']
        if page_obj is not None:
            data = serializers.TicketDetailSerializer(page_obj).to_dict()
            return http.JsonResponse(data=data)
        return NotFoundJsonResponse()