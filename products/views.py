from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from products.models import Product
from django.http import HttpResponse


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddToCartView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Adicionar carrinho')


class RemoveToCartView(View):
    ...


class CartView(View):
    ...


class FinaliseView(View):
    ...
