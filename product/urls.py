from django.conf.urls import url
from .views import My_product_view

urlpatterns = [
    url(r'^list_product/$', My_product_view.list_product, name = "list_product"), 
    url(r'^delete_product/$', My_product_view.delete_product, name='delete'),
    url(r'^update_product/$', My_product_view.update_product, name='update'),    
]