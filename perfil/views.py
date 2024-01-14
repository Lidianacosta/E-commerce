from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .forms import UserForm, PerfilForm
from .models import PerfilUsuario
from django.contrib import auth
from django.contrib.auth.models import User
import copy
# Create your views here.


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        usuario = self.request.user
        self.perfil = None

        if self.request.user.is_authenticated:
            self.perfil = PerfilUsuario.objects.filter(user=usuario).first()
            self.context = {
                'user_form': UserForm(
                    data=self.request.POST or None,
                    usuario=usuario,
                    instance=usuario,
                ),
                'perfil_form': PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil,
                ),
            }
        else:
            self.context = {
                'user_form': UserForm(data=self.request.POST or None),
                'perfil_form': PerfilForm(data=self.request.POST or None),
            }

        self.user_form = self.context['user_form']
        self.perfil_form = self.context['perfil_form']

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        self.renderizar = render(
            self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.renderizar


class CriarView(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.user_form.is_valid() or not self.perfil_form.is_valid():
            return self.renderizar

        username = self.user_form.cleaned_data.get('username')
        password = self.user_form.cleaned_data.get('password')
        email = self.user_form.cleaned_data.get('email')
        first_name = self.user_form.cleaned_data.get('first_name')
        last_name = self.user_form.cleaned_data.get('last_name')

        if self.request.user.is_authenticated:
            usuario = get_object_or_404(
                User,
                username__exact=self.request.user.username
            )
            usuario.username = username
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            if password:
                usuario.set_password(password)
            usuario.save()

            if not self.perfil:
                perfil = PerfilUsuario(
                    **self.perfil_form.cleaned_data, user=usuario
                )
                perfil.save()
            else:
                perfil = self.perfil_form.save(commit=False)
                perfil.user = usuario
                perfil.save()
        else:
            usuario = self.user_form.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfil_form.save(commit=False)
            perfil.user = usuario
            perfil.save()

        if password:
            authenticate = auth.authenticate(
                self.request, username=username, password=password
            )

            if authenticate:
                auth.login(self.request, usuario)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        return self.renderizar


class UpdateView(View):
    pass


class LoginView(View):
    pass


class LogoutView(View):
    pass
