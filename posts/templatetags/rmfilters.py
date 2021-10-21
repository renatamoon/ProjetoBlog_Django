from django import template

#decorar uma funcao
register = template.Library()

#mostra a quantidade de comentários dentro da página.
@register.filter(name='plural_comentarios')
def plural_comentarios(num_comentarios):
    try:
        num_comentarios = int(num_comentarios)

        if num_comentarios == 0:
            return f'Nenhum comentário postado'
        elif num_comentarios == 1:
            return f'{num_comentarios} comentário'
        else:
            return f'{num_comentarios} comentários'
    except:
        return f'{num_comentarios} comentário(s)'