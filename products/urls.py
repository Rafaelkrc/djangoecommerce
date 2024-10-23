from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('product/list/addtocart/',
         views.AddToCartView.as_view(), name='addtocart'),
    path('product/removetocart/',
         views.RemoveToCartView.as_view(), name='removetocart'),
    path('product/cart/', views.CartView.as_view(), name='cart'),
    path('product/purchasesummary/', views.PurchaseSummaryView.as_view(),
         name='purchasesummary'),
    path('product/list/', views.ProductListView.as_view(), name='list'),
    path('product/list/<slug>/',
         views.ProductDetailView.as_view(), name='detail'),
]
