from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path('', views.PayView.as_view(), name='pay'),
    path('save_order/', views.SaveOrderView.as_view(), name='save_order'),
    path('detail_order/', views.DetailOrderView.as_view(), name='detail_order'),
]
