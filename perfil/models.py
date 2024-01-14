import re
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from utils.valida_cpf import valida_cpf

# Create your models here.


class PerfilUsuario(models.Model):
    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfil dos Usuários"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idade = models.PositiveIntegerField()
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    endereco = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=20)
    bairro = models.CharField(max_length=30)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        max_length=2,
        default='RN',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self) -> str:
        return f'{self.user.get_full_name()}' if self.user.get_full_name() else f'{self.user}'

    def clean(self) -> None:
        error_messages = {}

        if not valida_cpf(self.cpf):
            error_messages.update({
                'cpf': 'CPF inválido',
            })

        if not re.search(r'^[0-9]{0,}$', self.cep):
            error_messages.update({
                'cep': 'CEP inválido, digite os 8 digitos do CEP',
            })

        if error_messages:
            raise ValidationError({
                **error_messages
            })

        return super().clean()
