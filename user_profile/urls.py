from django.urls import path
from . import views


app_name = 'user_profile'

urlpatterns = [
    path('user_profile/create/', views.CreateView.as_view(), name='create'),
    path('user_profile/update/', views.UpdateView.as_view(), name='update'),
    path('user_profile/login/', views.LoginView.as_view(), name='login'),
    path('user_profile/logout/', views.LogoutView.as_view(), name='logout'),
]
