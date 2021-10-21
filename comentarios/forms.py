from django.forms import ModelForm
from .models import Comentario


class FormComentario(ModelForm):
    #fazendo as validações de erros referente aos comentários
    def clean(self):
        data = self.cleaned_data
        nome = data.get('nome_comentario')
        email = data.get('email_comentario')
        comentario = data.get('comentario')

        if len(nome) < 5:
            self.add_error(
                'nome_comentario',
                'ERROR: O nome deve conter mais que 5 caracteres!'
            )

    class Meta:
        model = Comentario
        fields = ('nome_comentario', 'email_comentario', 'comentario')

