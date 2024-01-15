import copy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserForm, PerfilForm
from .models import PerfilUsuario
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
        messages.success(
            self.request,
            'Seu cadastro foi criado ou atualizado com sucesso'
        )
        messages.success(
            self.request,
            'Você fez login e pode concluir sua compra'
        )
        return redirect('perfil:criar')


class LoginView(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        if not username or not password:
            messages.error(
                self.request,
                'Usuário ou senha inválidos'
            )
            return redirect('perfil:criar')

        authenticate = auth.authenticate(
            self.request, username=username, password=password
        )

        if authenticate:
            usuario = User.objects.filter(username__exact=username).first()
            auth.login(self.request, user=usuario)
            messages.success(
                self.request,
                'Você fez login no sistema e pode concluir sua comprar'
            )
            return redirect('produto:carrinho')

        messages.error(
            self.request,
            'Usuário ou senha inválidos'
        )
        return redirect('perfil:criar')


class LogoutView(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        auth.logout(self.request)
        self.request.session['carrinho'] = carrinho
        self.request.session.save()
        return redirect('produto:lista')
