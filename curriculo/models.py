# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Extracao(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True)


class Membro(models.Model):
    id_membro = models.IntegerField()  #Id sequencial gerado pelo ScriptLattes.
    id_lattes = models.TextField() #Id que identifica o currículo na Plataforma Lattes
    nome_inicial = models.TextField()  #Nome importado do arquivo .txt com a lista de pesquisadores
    nome_lattes = models.TextField() #Nome importado da Plataforma Lattes

    class Meta:
        verbose_name_plural = "Membros"


class Producao(models.Model):
    ano = models.IntegerField(null=True, blank=True)
    autores = models.TextField(null=True, blank=True)
    titulo = models.TextField(null=True, blank=True)
    membros = models.ManyToManyField(Membro, through='ProducaoMembro', through_fields=('producao','membro'))

    class Meta:
        verbose_name_plural = "Producoes"
        ordering = ['-ano','titulo']

# Foi utilizado este Model intermediário na criação da relação m2m para
# que o ID da tabela intermediária possa ser zerado
# por meio da connection.ops.sequence_reset_sql, que requer o Model como parâmetro
# Além disso, é possível definir a exclusão dos registros em cascata, facilitando
# zerar o banco antes da nova importação
class ProducaoMembro(models.Model):
    producao = models.ForeignKey(Producao, on_delete=models.CASCADE)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "ProducoesMembros"
        auto_created = True
        db_table = 'curriculo_producao_membros'

#####
##### Producao Bibliografica
#####

class ApresentacaoDeTrabalho(Producao):
    natureza = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Apresentacoes de Trabalhos"


class ArtigoAceito(Producao):
    revista = models.TextField(null=True, blank=True)
    volume = models.TextField(null=True, blank=True)
    numero = models.TextField(null=True, blank=True)
    paginas = models.TextField(null=True, blank=True)
    doi = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Artigos Aceitos"


class ArtigoEmPeriodico(Producao):
    revista = models.TextField(null=True, blank=True)
    issn = models.TextField(null=True, blank=True)
    volume = models.TextField(null=True, blank=True)
    numero = models.TextField(null=True, blank=True)
    paginas = models.TextField(null=True, blank=True)
    doi = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Artigos em Periodicos"


class CapituloDeLivroPublicado(Producao):
    livro = models.TextField(null=True, blank=True)
    edicao = models.TextField(null=True, blank=True)
    editora = models.TextField(null=True, blank=True)
    volume = models.TextField(null=True, blank=True)
    paginas = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Capitulos de Livro Publicados"


class LivroPublicado(Producao):
    edicao = models.TextField(null=True, blank=True)
    editora = models.TextField(null=True, blank=True)
    volume = models.TextField(null=True, blank=True)
    paginas = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Livros Publicados"


class OutroTipoDeProducaoBibliografica(Producao):
    natureza = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Outros Tipos de Producao Bibliografica"


class ResumoEmCongresso(Producao):
    nomeDoEvento = models.TextField(null=True, blank=True)
    volume = models.TextField(null=True, blank=True)
    numero = models.TextField(null=True, blank=True)
    paginas = models.TextField(null=True, blank=True)
    doi = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Resumos em Congresso"


class ResumoExpandidoEmCongresso(Producao):
    nomeDoEvento = models.TextField(null=True, blank=True)
    volume = models.TextField(null=True, blank=True)
    paginas = models.TextField(null=True, blank=True)
    doi = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Resumos Expandidos em Congresso"


class TextoEmJornalDeNoticia(Producao):
    nomeJornal = models.TextField(null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    volume = models.TextField(null=True, blank=True)
    paginas = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Textos em Jornais de Noticia"


class TrabalhoCompletoEmCongresso(Producao):
    nomeDoEvento = models.TextField(null=True, blank=True)
    volume = models.TextField(null=True, blank=True)
    paginas = models.TextField(null=True, blank=True)
    doi = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Trabalhos Completos em Congresso"


#####
##### Producao Tecnica
#####
class OutroTipoDeProducaoTecnica(Producao):
    natureza = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Outros Tipos de Producao Tecnica"


class ProcessoOuTecnica(Producao):
    natureza = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Processos ou Tecnicas"


class ProdutoTecnologico(Producao):
    pass

    class Meta:
        verbose_name_plural = "Produtos Tecnologicos"


class SoftwareComPatente(Producao):
    pass

    class Meta:
        verbose_name_plural = "Softwares com Patente"


class SoftwareSemPatente(Producao):
    pass

    class Meta:
        verbose_name_plural = "Softwares sem Patente"


class TrabalhoTecnico(Producao):
    pass

    class Meta:
        verbose_name_plural = "Trabalhos Tecnicos"


#####
##### Producao Artistica
#####
class ProducaoArtistica(Producao):
    pass

    class Meta:
        verbose_name_plural = "Producoes Artisticas"


#####
##### Patentes e Registros
#####
class DesenhoIndustrial(Producao):
    pais = models.TextField(null=True, blank=True)
    tipo_patente = models.TextField(null=True, blank=True)
    numero_registro = models.TextField(null=True, blank=True)
    data_deposito = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Desenhos Industriais"


class Patente(Producao):
    pais = models.TextField(null=True, blank=True)
    tipo_patente = models.TextField(null=True, blank=True)
    numero_registro = models.TextField(null=True, blank=True)
    data_deposito = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Patentes"


class ProgramaComputador(Producao):
    pais = models.TextField(null=True, blank=True)
    tipo_patente = models.TextField(null=True, blank=True)
    numero_registro = models.TextField(null=True, blank=True)
    data_deposito = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Programas de Computador"
