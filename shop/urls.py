from django.conf.urls import url
from .views import My_shop_view

urlpatterns = [
    url(r'^list_customer/$', My_shop_view.list_customer, name = "list_customer"),
    url(r'^sale_order/(?P<slug>[\w-]+)/$', My_shop_view.update_sale_order, name='sale'),
    url(r'^delete_sale_order/$', My_shop_view.delete_sale_order, name='delete'),
    url(r'^confirmed/$', My_shop_view.confirmed, name='confirmed'),
    
]