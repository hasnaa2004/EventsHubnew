from django.urls import path
from .views import (
    products_list_view,
    product_detail_view,
)

urlpatterns = [

    path(
        '',
        products_list_view,
        name='products_list'
    ),

    path(
        '<int:product_id>/',
        product_detail_view,
        name='product_detail'
    ),

]