from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from products.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductDetailView(View):
    ...


class AddToCartView(View):
    ...


class RemoveToCartView(View):
    ...


class CartView(View):
    ...


class FinaliseView(View):
    ...
