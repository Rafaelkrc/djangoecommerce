from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path('order/pay/<int:pk>', views.PayView.as_view(), name='pay'),
    path('order/save_order/', views.SaveOrderView.as_view(), name='save_order'),
    path('order/list/', views.ListOrderView.as_view(), name='list_order'),
    path('order/detail_order/<int:pk>',
         views.DetailOrderView.as_view(), name='detail_order'),
]
