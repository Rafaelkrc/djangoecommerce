from django import forms
from django.contrib.auth.models import User
from . import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = ('user_profile',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False, widget=forms.PasswordInput, label='Senha')

    password2 = forms.CharField(
        required=False, widget=forms.PasswordInput, label='Confirmação da senha')

    def __init__(self, user_profile=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_profile = user_profile

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password', 'password2', 'email')

    def clean(self, *args, **kwargs):
        cleaned = self.cleaned_data
        validation_error_messages = {}

        user_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')

        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'Email já existe'
        error_msg_password_short = 'Senha precisa de 6 digitos'
        error_msg_password_match = 'As duas senha precisam ser iguais'
        error_msg_required_field = 'Senha obrigatória'

        # usuário logados:update
        if self.user_profile:
            if user_db:
                if user_data != user_db.username:
                    validation_error_messages['username'] = error_msg_user_exists

            if email_db:
                if email_data != email_db.email:
                    validation_error_messages['email'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_messages['password'] = error_msg_password_match
                    validation_error_messages['password2'] = error_msg_password_match

                if len(password_data) < 6:
                    validation_error_messages['password'] = error_msg_password_short

        else:
            if user_db:
                validation_error_messages['username'] = error_msg_user_exists

            if email_db:
                validation_error_messages['email'] = error_msg_email_exists

            if not password_data:
                validation_error_messages['password'] = error_msg_required_field

            if not password2_data:
                validation_error_messages['password2'] = error_msg_required_field

            if password_data != password2_data:
                validation_error_messages['password'] = error_msg_password_match
                validation_error_messages['password2'] = error_msg_password_match

            if len(password_data) < 6:  # type: ignore
                validation_error_messages['password'] = error_msg_password_short

        if validation_error_messages:
            raise (forms.ValidationError(validation_error_messages))
