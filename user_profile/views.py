from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import models
from . import forms
import copy


class BaseProfile(View):
    template_name = 'user_profile/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        self.profile = None

        if self.request.user.is_authenticated:
            self.profile = models.UserProfile.objects.filter(
                user_profile=self.request.user).first()
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None, user_profile=self.request.user, instance=self.request.user),
                'profileform': forms.ProfileForm(data=self.request.POST or None, instance=self.profile)
            }

        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None)
            }

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']

        if self.request.user.is_authenticated:
            self.template_name = 'user_profile/update.html'

        self.renderized = render(
            self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.renderized


class CreateView(BaseProfile):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.profileform.is_valid():
            messages.error(
                self.request, 'Existe erros nos dados informados, por favor verique!')
            return self.renderized

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        # usuário logado
        if self.request.user.is_authenticated:
            user_up = get_object_or_404(
                User, username=self.request.user.username)  # type: ignore
            user_up.username = username

            if password:
                user_up.set_password(password)

            user_up.email = email
            user_up.first_name = first_name
            user_up.last_name = last_name
            user_up.save()

            if not self.profile:
                self.profileform.cleaned_data['user_profile'] = user_up
                print(self.profileform.cleaned_data)
                profile = models.UserProfile(**self.profileform.cleaned_data)
                profile.save()
            else:
                profile = self.profileform.save(commit=False)
                profile.user_profile = user_up
                profile.save()

        else:
            user_up = self.userform.save(commit=False)
            user_up.set_password(password)
            user_up.save()

            new_profile = self.profileform.save(commit=False)
            new_profile.user_profile = user_up
            new_profile.save()

        if password:
            authentic = authenticate(
                self.request, username=username, password=password)

            if authentic:
                login(self.request, user=user_up)

        self.request.session['cart'] = self.cart
        self.request.session.save()

        messages.success(
            self.request, 'Seu cadastro foir criado ou atualizado com sucesso!')

        messages.success(
            self.request, 'Você fez login e pode concluir sua compra.')

        if self.request.session['cart']:
            return redirect('product:cart')

        return redirect('product:list')
        return self.renderized


class UpdateView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')


class LoginView(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request, 'Usuário ou senha inválido.')
            return redirect('user_profile:create')

        user_autentic = authenticate(
            self.request, username=username, password=password)

        if not user_autentic:
            messages.error(
                self.request, 'Usuário ou senha inválido.')
            return redirect('user_profile:create')

        login(self.request, user=user_autentic)
        messages.success(
            self.request, 'Você fez login no sistema.')
        return redirect('product:cart')


class LogoutView(View):
    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart'))
        logout(self.request)
        self.request.session['cart'] = cart
        self.request.session.save()
        return redirect('product:list')
