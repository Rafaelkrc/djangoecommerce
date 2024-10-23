from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from . import models
from . import forms


class BaseProfile(View):
    template_name = 'user_profile/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        if self.request.user.is_authenticated:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None, user=self.request.user, instance=self.request.user),
                'profileform': forms.ProfileForm(data=self.request.POST or None)
            }

        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None)
            }
            self.renderized = render(
                self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.renderized


class CreateView(BaseProfile):
    def post(self, *args, **kwargs):
        return self.renderized


class UpdateView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')


class LoginView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class LogoutView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')
