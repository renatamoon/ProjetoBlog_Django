from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComentario
from comentarios.models import Comentario
from django.contrib import messages

class PostIndex(ListView):
    model = Post #subscrevendo o atributo Model
    template_name = 'posts/index.html'
    paginate_by = 3
    context_object_name = 'posts'

    #sobrescrevendo o método get_query set
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('categoria_post')
        qs = qs.order_by('-id').filter(publicado_post=True) #somente mostra na pagina o
        #campos que estão publicados, os que noa estão nem aparecem
        #pedindo que façamos a ordem dos ids de forma ordenada
        qs = qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(comentario__publicado_comentario=True, then=1)
                )
                #ajusta o numero de comentarios para o numero de comentarios na sessao da pagina inicial
            )
        )
        return qs

class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')

        if not termo:
            return qs

        #filtrando ainda mais a consulta
        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo)
        )

        return qs

class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return qs #se nao existir nenhuma categoria, retorna o index da pagina mesmo

        #levantando um filtro para a consulta
        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)
        #fazendo isso falamos para filtrar os posts de cada categoria de acordo com a sua categoria

        return qs


class PostDetalhes(UpdateView):
    template_name = 'posts/post_detalhes.html'
    model = Post
    form_class = FormComentario
    context_object_name = 'post'
#somente conseguimos sobrescrever as funções de cada classe, pois estamos herdando
#da classe master POSTINDEX;
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object() #aqui pegaremos o post que estamos no momento
        comentarios = Comentario.objects.filter(publicado_comentario=True,
                                              post_comentario=post.id)
        contexto['comentarios'] = comentarios
        #aqui injeta o novo comentario dentro da sessão de comentarios
        return contexto

    def form_valid(self, form):
        post = self.get_object()
        comentario = Comentario(**form.cleaned_data)
        comentario.post_comentario = post
        #caso o usuario queira fazer um comentario, ele pede para logar com o usuario
        if self.request.user.is_authenticated:
            comentario.usuario_comentario = self.request.user

            comentario.save()
            messages.success(self.request, 'COMENTÁRIO ENVIADO COM SUCESSO!')
            return redirect('post_detalhes', pk=post.id)




