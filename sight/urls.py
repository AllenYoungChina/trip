from django.urls import path

from .views import SightListView, SightDetailView, SightCommentListView, SightTicketListView, \
    SightInfoDetailView, TicketDetailView, SightListCacheView

urlpatterns = [
    # 2.1 景点列表接口
    path('sight/list/', SightListView.as_view(), name='sight_list'),
    path('sight/list/cache/', SightListCacheView.as_view(), name='sight_list_cache'),
    # 2.2 景点详情接口
    path('sight/detail/<int:pk>/', SightDetailView.as_view(), name='sight_detail'),
    # 2.3 景点评论列表接口
    path('comment/list/<int:pk>/', SightCommentListView.as_view(), name='sight_comment_list'),
    # 2.4 景点门票列表接口
    path('ticket/list/<int:pk>/', SightTicketListView.as_view(), name='sight_ticket_list'),
    # 2.5 景点介绍接口
    path('sight/info/<int:pk>/', SightInfoDetailView.as_view(), name='sight_info'),
    # 2.6 门票详情接口
    path('ticket/detail/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
]
