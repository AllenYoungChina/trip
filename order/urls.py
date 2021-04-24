from django.urls import path

from order import views

urlpatterns = [
    # 3.1 订单提交接口
    path('ticket/submit/', views.TicketOrderSubmitView.as_view(), name='ticket_submit'),
    # 3.2 订单详情接口（查询get、支付post、取消put、删除delete）
    path('order/detail/<int:sn>/', views.OrderDetail.as_view(), name='order_detail'),
    # 3.3 我的订单列表接口
    path('order/list/', views.OrderListView.as_view(), name='order_list'),
]