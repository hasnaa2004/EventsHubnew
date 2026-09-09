from django.shortcuts import render
from .models import Category
from django.contrib import messages
def categories_list_view(request):

    categories = Category.objects.all()

    return render(
        request,
        'categories/categories_list.html',
        {
            'categories': categories
        }
    )