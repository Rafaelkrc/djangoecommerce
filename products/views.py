from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from products.models import Product, Variation
from django.contrib import messages
from django.db.models import Q
from user_profile.models import UserProfile


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['-id']


class SearchView(ProductListView):
    def get_queryset(self, *args, **kwargs):
        term = self.request.GET.get('term') or self.request.session['term']
        queryset = super().get_queryset(*args, **kwargs)

        if not term:
            return queryset

        self.request.session['term'] = term

        queryset = queryset.filter(
            Q(name__icontains=term) |
            Q(short_description__icontains=term) |
            Q(long_description__icontains=term)
        )

        self.request.session.save()
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_field = 'slug'


class AddToCartView(View):

    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER', resolve_url('product:list'))

        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(self.request, 'Produto não existe!')
            return redirect(http_referer)

        variation = get_object_or_404(Variation, id=variation_id)

        variation_stock = variation.stock
        product = variation.product

        product_id = product.id  # type: ignore
        product_name = product.name
        variation_name = variation.name or ''
        unit_price = variation.price
        unit_promotional_price = variation.promotional_price
        quantity = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        else:
            image = ''

        if variation.stock < 1:
            messages.error(
                self.request, 'Estoque insuficiente!'
            )
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            cart_quantity = cart[variation_id]['quantity']
            cart_quantity += 1

            if variation_stock < cart_quantity:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {
                        cart_quantity}x no produto "{product_name}".'
                    f'Adicionamos {variation_stock}x no seu carrinho.'
                )
                cart_quantity = variation_stock

            cart[variation_id]['quantity'] = cart_quantity
            cart[variation_id]['quantitative_price'] = unit_price * cart_quantity
            cart[variation_id]['quantitative_promotional_price'] = unit_promotional_price * cart_quantity
        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'unit_price': unit_price,
                'unit_promotional_price': unit_promotional_price,
                'quantitative_price': unit_price,
                'quantitative_promotional_price': unit_promotional_price,
                'quantity': quantity,
                'slug': slug,
                'image': image,
            }

        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {product.name} {
                variation_name} adicionado ao seu carrinho,'
            f' total de {cart[variation_id]['quantity']} unidades!'
        )
        return redirect(http_referer)


class RemoveToCartView(View):

    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER', resolve_url('product:list'))
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            return redirect(http_referer)

        if variation_id not in self.request.session['cart']:
            return redirect(http_referer)

        cart = self.request.session['cart'][variation_id]

        messages.warning(
            self.request,
            f'Produto {cart["product_name"]} {cart['variation_name']} '
            f'removido com sucesso do seu pedido!'
        )

        del self.request.session['cart'][variation_id]
        self.request.session.save()
        return redirect(http_referer)


class CartView(View):

    def get(self, *args, **kwargs):
        context = {'cart': self.request.session.get('cart', {})}
        return render(self.request, 'products/cart.html', context)


class PurchaseSummaryView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user_profile:create')

        profile = UserProfile.objects.filter(
            user_profile=self.request.user).exists()

        if not profile:
            messages.error(self.request, 'Usuário sem perfil')
            return redirect('user_profile:create')

        if not self.request.session.get('cart'):
            messages.error(self.request, 'Carrinho vazio!')
            return redirect('product:list')

        context = {
            'user': self.request.user,
            'cart': self.request.session['cart'],
        }
        return render(self.request, 'products/purchasesummary.html', context)
