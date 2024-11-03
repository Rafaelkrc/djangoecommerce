from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from products.models import Variation
from utils import utils
from .models import Order, OrderItem


class DispatchLoginRequired(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user_profile:create')
        return super().dispatch(*args, **kwargs)


class PayView(DispatchLoginRequired, DetailView):
    template_name = 'order/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)
        return queryset


class SaveOrderView(View):
    template_name = 'order/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Você precisa fazer Login!')
            return redirect('user_profile:create')

        if not self.request.session.get('cart'):
            messages.error(self.request, 'Carrinho vazio!')
            return redirect('product:list')

        cart = self.request.session.get('cart')
        variation_cart_ids = [v for v in cart]
        variation_db = list(Variation.objects.select_related('product').filter(
            id__in=variation_cart_ids))

        for variation in variation_db:
            vid = str(variation.id)
            stock = variation.stock
            qtd_cart = cart[vid]['quantity']
            unit_price = cart[vid]['unit_price']
            promotional_price = cart[vid]['unit_promotional_price']

            error_msg_stock = ''

            if stock < qtd_cart:
                cart[vid]['quantity'] = stock
                cart[vid]['quantitative_price'] = stock * unit_price
                cart[vid]['quantitative_promotional_price'] = stock * \
                    promotional_price

                error_msg_stock = 'Estoque insuficiente para alguns produtos do seu carrinho, a quantidade deles foi reduzida. Verifique os produtos a seguir.'
                messages.error(
                    self.request, error_msg_stock)

                self.request.session.save()
                return redirect('product:cart')

        total_cart_quantity = utils.total_cart_quantity(cart)
        cart_total = utils.total_cart(cart)

        order = Order(
            user=self.request.user,
            total=cart_total,
            total_quantity=total_cart_quantity,
            status='C',
        )

        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=v['product_name'],
                    product_id=v['product_id'],
                    variation=v['variation_name'],
                    variation_id=v['variation_id'],
                    price=v['quantitative_price'],
                    promotional_price=v['quantitative_promotional_price'],
                    quantity=v['quantity'],
                    image=v['image'],
                ) for v in cart.values()
            ]
        )
        del self.request.session['cart']
        # return render(self.request, self.template_name, context)
        return redirect(reverse('order:pay', kwargs={'pk': order.pk}))


class DetailOrderView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhe do pedido')


class ListOrderView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Listar')
