# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import coreapi
import coreschema
from datetime import datetime, timedelta
from rest_framework import viewsets, mixins, status, schemas
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import UltimaRequisicao
from .serializers import *
from curriculo.models import *
from lattes_service.settings import FORCAR_CACHE_NO_CLIENTE, PRAZO_DO_CACHE


class VerificarHistoricoDeRequisicoes():

    @staticmethod
    def tem_requisicao(request):

        full_path = str(request.get_full_path())
        ip = request.META['REMOTE_ADDR']
        host = request.META['HTTP_HOST']
        extracao = Extracao.objects.order_by('-data_hora').first()
        ultima_requisicao = UltimaRequisicao.objects.filter(full_path=full_path, ip=ip, http_host=host)

        if ultima_requisicao:
            nao_tem_atualizacao = ultima_requisicao.filter(data__gte=extracao.data_hora)
            if nao_tem_atualizacao:
                ultima_requisicao.delete()
                UltimaRequisicao.objects.create(full_path=full_path, ip=ip, http_host=host)
                return True
            ultima_requisicao.delete()

        UltimaRequisicao.objects.create(full_path=full_path, ip=ip, http_host=host)

        return False

class ProducaoPorMembroViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    Disponibiliza toda a produção científica do orientador.
    '''
    serializer_class = ProducaoPorMembroSerializer
    queryset = Membro.objects.all()
    lookup_field = 'id_lattes'
    lookup_value_regex = '[0-9]{16}'

    schema = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(
                name='a_partir_de',
                location='query',
                schema=coreschema.String(
                    description='Este parâmetro permite filtrar a produção a partir do ano determinado.'),
                required=False,
                example='a_partir_de=2015'
            ),
            coreapi.Field(
                name='id_lattes',
                location='path',
                schema=coreschema.String(
                    description='Id Lattes do orientador com 16 dígitos.'),
                required=True,
            ),
        ],
    )

    # Devido a estrutura dos dados serializados (há vários nós com o campo ano)
    # essa foi a saíde encontrada para filtrar a produção. Por isso, a Query Parameter
    # não foi documentada automaticamente pelo DRF.
    # Outra saída possível seria filtrar com os dados a partir de parâmetro recebido
    # via url pattern. Assim o DRF documentaria em Path Parameter. Porém, sairia do padrão
    # e complicaria a implementação do client.
    def get_serializer_context(self):
        return {'ano': self.request.query_params.get('a_partir_de', None)}

    def retrieve(self, request, id_lattes):
        '''
        Obtém a produção científica do orientador. \n
        '''

        if self.request.query_params:
            for key,value in self.request.query_params.items():
                if key not in ('format','a_partir_de'):
                    return Response(None, status=status.HTTP_400_BAD_REQUEST)
                if key == 'a_partir_de':
                    if int(value) < 1970 or int(value) > datetime.now().year:
                        return Response(None, status=status.HTTP_400_BAD_REQUEST)
                if key == 'format' and value != 'json':
                    return Response(None, status=status.HTTP_400_BAD_REQUEST)

        if FORCAR_CACHE_NO_CLIENTE:
            if VerificarHistoricoDeRequisicoes.tem_requisicao(request):
                return Response(None, status=status.HTTP_204_NO_CONTENT)

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class ProducaoFilter(filters.FilterSet):
    # Filtros a serem utilizados na ViewSet que exibirá a produção por tipo.
    a_partir_de = filters.NumberFilter(name='ano', lookup_expr='gte', label='Filtrar a partir do ano determinado')
    class Meta:
        model = Producao
        fields = ('a_partir_de', )


class ProducaoPorTipoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    Disponibiliza as produções conforme o tipo.
    '''
    tipos = {'apresentacoes_de_trabalhos': [ApresentacaoDeTrabalhoSerializer, ApresentacaoDeTrabalho],
             'artigos_aceitos': [ArtigoAceitoSerializer, ArtigoAceito],
             'artigos_em_periodicos': [ArtigoEmPeriodicoSerializer, ArtigoEmPeriodico],
             'capitulos_de_livros_publicados': [CapituloDeLivroPublicadoSerializer, CapituloDeLivroPublicado],
             'livros_publicados': [LivroPublicadoSerializer, LivroPublicado],
             'outros_tipos_de_producao_bibliografica': [OutroTipoDeProducaoBibliograficaSerializer, OutroTipoDeProducaoBibliografica],
             'resumos_em_congresso': [ResumoEmCongressoSerializer, ResumoEmCongresso],
             'resumos_expandidos_em_congresso': [ResumoExpandidoEmCongressoSerializer, ResumoExpandidoEmCongresso],
             'textos_em_jornal_de_noticia': [TextoEmJornalDeNoticiaSerializer, TextoEmJornalDeNoticia],
             'trabalhos_completos_em_congresso': [TrabalhoCompletoEmCongressoSerializer, TrabalhoCompletoEmCongresso],
             'outros_tipos_de_producao_tecnica': [OutroTipoDeProducaoTecnicaSerializer, OutroTipoDeProducaoTecnica],
             'processos_ou_tecnicas': [ProcessoOuTecnicaSerializer, ProcessoOuTecnica],
             'produtos_tecnologicos': [ProdutoTecnologicoSerializer, ProdutoTecnologico],
             'softwares_com_patente': [SoftwareComPatenteSerializer, SoftwareComPatente],
             'softwares_sem_patente': [SoftwareSemPatenteSerializer, SoftwareSemPatente],
             'trabalhos_tecnicos': [TrabalhoTecnicoSerializer, TrabalhoTecnico],
             'producoes_artisticas': [ProducaoArtisticaSerializer, ProducaoArtistica],
             'desenhos_industriais': [DesenhoIndustrialSerializer, DesenhoIndustrial],
             'patentes': [PatenteSerializer, Patente],
             'programas_computador': [ProgramaComputadorSerializer, ProgramaComputador],}

    serializer_class = ProducaSerializer
    queryset = Producao.objects
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = ProducaoFilter
    pagination_class = None  # Comente esta linha caso queira incluir paginação dos resultados

    schema = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(
                name='tipo',
                location='path',
                schema=coreschema.String(
                    description='Tipo da produção científica que deseja consumir. Tipos possíveis: ' + ', '.join(tipos.keys()) ),
                required=True,
            ),
            coreapi.Field(
                name='id_lattes',
                location='path',
                schema=coreschema.String(
                    description='Id Lattes do orientador com 16 dígitos.'),
                required=True,
            ),
            coreapi.Field(
                name='a_partir_de',
                location='query',
                schema=coreschema.String(
                    description='Este parâmetro permite filtrar a produção a partir do ano determinado.'),
                required=False,
            ),


        ],
    )

    def list(self, request, tipo, id_lattes):
        if tipo not in self.tipos:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        if self.request.query_params:
            for key,value in self.request.query_params.items():
                if key not in ('format','a_partir_de'):
                    return Response(None, status=status.HTTP_400_BAD_REQUEST)
                if key == 'a_partir_de':
                    if int(value) < 1970 or int(value) > datetime.now().year:
                        return Response(None, status=status.HTTP_400_BAD_REQUEST)
                if key == 'format' and value != 'json':
                    return Response(None, status=status.HTTP_400_BAD_REQUEST)

        if FORCAR_CACHE_NO_CLIENTE:
            if VerificarHistoricoDeRequisicoes.tem_requisicao(request):
                return Response(None, status=status.HTTP_204_NO_CONTENT)

        self.queryset = self.tipos[tipo][1].objects.filter(membros__id_lattes=id_lattes)
        self.serializer_class = self.tipos[tipo][0]

        producao = super(self.__class__, self).list(request, tipo, id_lattes)

        membro = Membro.objects.filter(id_lattes=id_lattes).first()
        membro_serializer = MembroSerializer(membro)

        extracao = Extracao.objects.values('data_hora').order_by('-data_hora').first()
        extracao_serializer = ExtracaoSerializer(extracao)

        proxima_extracao = extracao['data_hora'] + timedelta(days=PRAZO_DO_CACHE);

        dados = {
            'id_lattes': membro_serializer.data.get('id_lattes'),
            'nome_inicial': membro_serializer.data.get('nome_inicial'),
            'nome_lattes': membro_serializer.data.get('nome_lattes'),
            'extracao': extracao_serializer.data.get('data_hora'),
            'proxima_extracao': proxima_extracao.strftime('%d/%m/%Y'),
            tipo: producao.data
        }

        return Response(dados)
