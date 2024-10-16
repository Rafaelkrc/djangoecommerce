from django.shortcuts import render
from django.views.generic import ListView
from django.views import View


class ProductListView(ListView):
    ...


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
