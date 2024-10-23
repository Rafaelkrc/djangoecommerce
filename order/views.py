from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse


class PayView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagamento')


class SaveOrderView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Salvar Pedido')


class DetailOrderView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhe do pedido')
