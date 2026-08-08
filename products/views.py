from django.shortcuts import render, get_object_or_404
from .models import Product


def products_list_view(request):
    products = Product.objects.all().order_by('-created_at')

    return render(
        request,
        'products/products_list.html',
        {
            'products': products
        }
    )


def product_detail_view(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product
        }
    )