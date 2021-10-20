from django.db import models
from categorias.models import Categoria
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    titulo_post = models.CharField(max_length=255, verbose_name='TÍTULO')
    autor_post = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='AUTOR')
    data_post = models.DateTimeField(default=timezone.now, verbose_name='DATA')
    conteudo_post = models.TextField(verbose_name='CONTEÚDO')
    excerto_post = models.TextField(verbose_name='EXCERTO')
    categoria_post = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, blank=True,
                                       null=True, verbose_name='CATEGORIA')
    imagem_post = models.ImageField(upload_to='post_img/%Y/%m/%d', blank=True, null=True,
                                    verbose_name='IMAGEM')
    publicado_post = models.BooleanField(default=False, verbose_name='PUBLICADO')


    def __str__(self):
        return self.titulo_post
