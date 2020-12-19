from rest_framework import serializers

from curriculo.models import *
from lattes_service.settings import PRAZO_DO_CACHE
from datetime import timedelta


class MembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membro
        exclude = ('id', 'id_membro',)


class ExtracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extracao
        fields = ['data_hora']


class ProducaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producao
        fields = '__all__'


####
#### Producoes Bibliograficas
####
class ApresentacaoDeTrabalhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApresentacaoDeTrabalho
        exclude = ('id', 'membros')


class ArtigoAceitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtigoAceito
        exclude = ('id', 'membros')


class ArtigoEmPeriodicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtigoEmPeriodico
        exclude = ('id', 'membros')


class CapituloDeLivroPublicadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapituloDeLivroPublicado
        exclude = ('id', 'membros')


class LivroPublicadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LivroPublicado
        exclude = ('id', 'membros')


class OutroTipoDeProducaoBibliograficaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutroTipoDeProducaoBibliografica
        exclude = ('id', 'membros')


class ResumoEmCongressoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumoEmCongresso
        exclude = ('id', 'membros')


class ResumoExpandidoEmCongressoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumoExpandidoEmCongresso
        exclude = ('id', 'membros')


class TextoEmJornalDeNoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextoEmJornalDeNoticia
        exclude = ('id', 'membros')


class TrabalhoCompletoEmCongressoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrabalhoCompletoEmCongresso
        exclude = ('id', 'membros')


#####
##### Producao Tecnica
#####
class OutroTipoDeProducaoTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutroTipoDeProducaoTecnica
        exclude = ('id', 'membros')


class ProcessoOuTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessoOuTecnica
        exclude = ('id', 'membros')


class ProdutoTecnologicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoTecnologico
        exclude = ('id', 'membros')


class SoftwareComPatenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareComPatente
        exclude = ('id', 'membros')


class SoftwareSemPatenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareSemPatente
        exclude = ('id', 'membros')


class TrabalhoTecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrabalhoTecnico
        exclude = ('id', 'membros')


#####
##### Producao Artistica
#####
class ProducaoArtisticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProducaoArtistica
        exclude = ('id', 'membros')


#####
##### Patentes e Registros
#####
class DesenhoIndustrialSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesenhoIndustrial
        exclude = ('id', 'membros')


class PatenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patente
        exclude = ('id', 'membros')


class ProgramaComputadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaComputador
        exclude = ('id', 'membros')


class ProducaoPorMembroSerializer(serializers.ModelSerializer):
    extracao = serializers.SerializerMethodField()
    proxima_extracao = serializers.SerializerMethodField()
    apresentacoes_de_trabalhos = serializers.SerializerMethodField()
    artigos_aceitos = serializers.SerializerMethodField()
    artigos_em_periodicos  = serializers.SerializerMethodField()
    capitulos_de_livros_publicados = serializers.SerializerMethodField()
    livros_publicados = serializers.SerializerMethodField()
    outros_tipos_de_producao_bibliografica = serializers.SerializerMethodField()
    resumos_em_congresso = serializers.SerializerMethodField()
    resumos_expandidos_em_congresso = serializers.SerializerMethodField()
    textos_em_jornal_de_noticia = serializers.SerializerMethodField()
    trabalhos_completos_em_congresso = serializers.SerializerMethodField()
    outros_tipos_de_producao_tecnica = serializers.SerializerMethodField()
    processos_ou_tecnicas = serializers.SerializerMethodField()
    produtos_tecnologicos = serializers.SerializerMethodField()
    softwares_com_patente = serializers.SerializerMethodField()
    softwares_sem_patente = serializers.SerializerMethodField()
    trabalhos_tecnicos = serializers.SerializerMethodField()
    producoes_artisticas = serializers.SerializerMethodField()
    desenhos_industriais = serializers.SerializerMethodField()
    patentes = serializers.SerializerMethodField()
    programas_computador = serializers.SerializerMethodField()

    def get_extracao(self, obj):
        qs = Extracao.objects.order_by('-data_hora').first()
        serializer = ExtracaoSerializer(instance=qs)
        return serializer.data['data_hora']

    def get_proxima_extracao(self, obj):
        extracao = Extracao.objects.values('data_hora').order_by('-data_hora').first()
        proxima_extracao = extracao['data_hora'] + timedelta(days=PRAZO_DO_CACHE);
        return proxima_extracao.strftime('%d/%m/%Y')

    def get_apresentacoes_de_trabalhos(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = ApresentacaoDeTrabalho.objects.filter(membros=obj, ano__gte=ano)
        serializer = ApresentacaoDeTrabalhoSerializer(instance=qs, many=True)
        return serializer.data

    def get_artigos_aceitos(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = ArtigoAceito.objects.filter(membros=obj, ano__gte=ano)
        serializer = ArtigoAceitoSerializer(instance=qs, many=True)
        return serializer.data

    def get_artigos_em_periodicos(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = ArtigoEmPeriodico.objects.filter(membros=obj, ano__gte=ano)
        serializer = ArtigoEmPeriodicoSerializer(instance=qs, many=True)
        return serializer.data

    def get_capitulos_de_livros_publicados(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = CapituloDeLivroPublicado.objects.filter(membros=obj, ano__gte=ano)
        serializer = CapituloDeLivroPublicadoSerializer(instance=qs, many=True)
        return serializer.data

    def get_livros_publicados(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = LivroPublicado.objects.filter(membros=obj, ano__gte=ano)
        serializer = LivroPublicadoSerializer(instance=qs, many=True)
        return serializer.data

    def get_outros_tipos_de_producao_bibliografica(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = OutroTipoDeProducaoBibliografica.objects.filter(membros=obj, ano__gte=ano)
        serializer = OutroTipoDeProducaoBibliograficaSerializer(instance=qs, many=True)
        return serializer.data

    def get_resumos_em_congresso(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = ResumoEmCongresso.objects.filter(membros=obj, ano__gte=ano)
        serializer = ResumoEmCongressoSerializer(instance=qs, many=True)
        return serializer.data

    def get_resumos_expandidos_em_congresso(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = ResumoExpandidoEmCongresso.objects.filter(membros=obj, ano__gte=ano)
        serializer = ResumoExpandidoEmCongressoSerializer(instance=qs, many=True)
        return serializer.data

    def get_textos_em_jornal_de_noticia(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = TextoEmJornalDeNoticia.objects.filter(membros=obj, ano__gte=ano)
        serializer = TextoEmJornalDeNoticiaSerializer(instance=qs, many=True)
        return serializer.data

    def get_trabalhos_completos_em_congresso(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = TrabalhoCompletoEmCongresso.objects.filter(membros=obj, ano__gte=ano)
        serializer = TrabalhoCompletoEmCongressoSerializer(instance=qs, many=True)
        return serializer.data

    def get_outros_tipos_de_producao_tecnica(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = OutroTipoDeProducaoTecnica.objects.filter(membros=obj, ano__gte=ano)
        serializer = OutroTipoDeProducaoTecnicaSerializer(instance=qs, many=True)
        return serializer.data

    def get_processos_ou_tecnicas(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = ProcessoOuTecnica.objects.filter(membros=obj, ano__gte=ano)
        serializer = ProcessoOuTecnicaSerializer(instance=qs, many=True)
        return serializer.data

    def get_produtos_tecnologicos(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = ProdutoTecnologico.objects.filter(membros=obj, ano__gte=ano)
        serializer = ProdutoTecnologicoSerializer(instance=qs, many=True)
        return serializer.data

    def get_softwares_com_patente(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = SoftwareComPatente.objects.filter(membros=obj, ano__gte=ano)
        serializer = SoftwareComPatenteSerializer(instance=qs, many=True)
        return serializer.data

    def get_softwares_sem_patente(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = SoftwareSemPatente.objects.filter(membros=obj, ano__gte=ano)
        serializer = SoftwareSemPatenteSerializer(instance=qs, many=True)
        return serializer.data

    def get_trabalhos_tecnicos(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = TrabalhoTecnico.objects.filter(membros=obj, ano__gte=ano)
        serializer = TrabalhoTecnicoSerializer(instance=qs, many=True)
        return serializer.data

    def get_producoes_artisticas(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = ProducaoArtistica.objects.filter(membros=obj, ano__gte=ano)
        serializer = ProducaoArtisticaSerializer(instance=qs, many=True)
        return serializer.data

    def get_desenhos_industriais(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = DesenhoIndustrial.objects.filter(membros=obj, ano__gte=ano)
        serializer = DesenhoIndustrialSerializer(instance=qs, many=True)
        return serializer.data

    def get_patentes(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = Patente.objects.filter(membros=obj, ano__gte=ano)
        serializer = PatenteSerializer(instance=qs, many=True)
        return serializer.data

    def get_programas_computador(self, obj):
        ano = self.context.get('ano', None) or 0
        qs = ProgramaComputador.objects.filter(membros=obj, ano__gte=ano)
        serializer = ProgramaComputadorSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Membro
        fields = ('id_lattes',
                  'nome_inicial',
                  'nome_lattes',
                  'extracao',
                  'proxima_extracao',
                  'apresentacoes_de_trabalhos',
                  'artigos_aceitos',
                  'artigos_em_periodicos',
                  'capitulos_de_livros_publicados',
                  'livros_publicados',
                  'outros_tipos_de_producao_bibliografica',
                  'resumos_em_congresso',
                  'resumos_expandidos_em_congresso',
                  'textos_em_jornal_de_noticia',
                  'trabalhos_completos_em_congresso',
                  'outros_tipos_de_producao_tecnica',
                  'processos_ou_tecnicas',
                  'produtos_tecnologicos',
                  'softwares_com_patente',
                  'softwares_sem_patente',
                  'trabalhos_tecnicos',
                  'producoes_artisticas',
                  'desenhos_industriais',
                  'patentes',
                  'programas_computador'
        )
        # Seria mais pratico utilizar o exclude, mas isso faria com que os dados do orientador
        # aparecessem somente no final do JSON, o que atrapalharia a visualizacao.
        #exclude = ('id','id_membro')
