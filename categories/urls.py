from django.urls import path
from .views import categories_list_view

urlpatterns = [
    path('', categories_list_view, name='categories_list'),
]