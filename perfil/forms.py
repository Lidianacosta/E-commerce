from django import forms
from .models import PerfilUsuario
from django.contrib.auth.models import User


class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        exclude = ("user",)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='confirmação senha'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password', 'password2'
        )

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data

        username = cleaned_data.get('username')
        email_data = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        usuario_db = User.objects.filter(username__exact=username).first()
        usuario_email_db = User.objects.filter(email__exact=email_data).first()

        if self.usuario:
            if usuario_db and not self.usuario.is_authenticated:
                self.add_error('username', 'Username já existe')

            if password:
                if password != password2:
                    self.add_error('password', 'As duas senhas não confere')
                    self.add_error('password2', 'As duas senhas não confere')

                if len(password) < 6:
                    self.add_error(
                        'password',
                        'Sua senha precisa pelo menos 6 caracteres'
                    )

            if usuario_email_db != self.usuario:
                self.add_error('email', 'Email já existe')

        else:
            if usuario_db:
                self.add_error('username', 'Username já existe')

            if not password:
                self.add_error('password', 'Este campo é obrigatório')
            if not password2:
                self.add_error('password2', 'Este campo é obrigatório')

            if password:
                if password != password2:
                    self.add_error(
                        'password', 'As duas senhas não confere')
                    self.add_error(
                        'password2', 'As duas senhas não confere')

                if len(password) < 6:
                    self.add_error(
                        'password',
                        'Sua senha precisa pelo menos 6 caracteres'
                    )

            if usuario_email_db:
                self.add_error('email', 'Email já existe')

        return cleaned_data
