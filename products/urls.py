from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('<slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('addtocart/', views.AddToCartView.as_view(), name='addtocart'),
    path('removetocart/', views.RemoveToCartView.as_view(), name='removetocart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('finalise/', views.FinaliseView.as_view(), name='finalise'),
]
